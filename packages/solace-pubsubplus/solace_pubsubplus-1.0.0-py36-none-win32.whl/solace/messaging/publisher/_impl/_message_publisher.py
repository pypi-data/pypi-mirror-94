# pubsubplus-python-client
#
# Copyright 2021 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Module contains the implementation class and methods for the MessagePublisher
# pylint: disable=missing-module-docstring, too-many-branches,no-else-break,too-many-boolean-expressions
# pylint: disable=missing-function-docstring,protected-access,no-else-raise,no-else-return,useless-super-delegation

import concurrent
import enum
import logging
import queue
import threading
import typing
import weakref
from abc import abstractmethod, ABC
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union

from solace.messaging import _SolaceServiceAdapter
from solace.messaging.config._sol_constants import SOLCLIENT_WOULD_BLOCK, SOLCLIENT_OK
from solace.messaging.config._solace_message_constants import UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_STARTED, \
    PUBLISHER_TERMINATED, WOULD_BLOCK_EXCEPTION_MESSAGE, PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED, \
    PUBLISHER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED, QUEUE_FULL_EXCEPTION_MESSAGE, \
    UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER, UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATING, \
    UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_READY, GRACE_PERIOD_DEFAULT_MS, \
    UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATED, PUBLISHER_ALREADY_TERMINATED, \
    PUBLISHER_TERMINATED_UNABLE_TO_START, PUBLISHER_UNAVAILABLE_FOR_TERMINATE, UNPUBLISHED_MESSAGE_COUNT
from solace.messaging.builder._impl._message_publisher_builder import PublisherBackPressure
from solace.messaging.core._publish import _SolacePublisherEvent
from solace.messaging.errors.pubsubplus_client_error import IllegalStateError, PublisherOverflowError, \
    InvalidDataTypeError, PubSubPlusClientError, IncompleteMessageDeliveryError
from solace.messaging.publisher._impl._outbound_message import _OutboundMessageBuilder
from solace.messaging.publisher._impl._publisher_utilities import validate_topic_type, _PublisherUtilities
from solace.messaging.publisher._outbound_message_utility import add_message_properties, set_correlation_tag_ptr
from solace.messaging.publisher._publishable import Publishable
from solace.messaging.publisher.message_publisher import MessagePublisher
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.publisher_health_check import PublisherReadinessListener
from solace.messaging.resources.topic import Topic
from solace.messaging.utils._solace_utilities import is_type_matches, validate_grace_period, convert_ms_to_seconds, \
    _ThreadingUtil, _PubSubPlusQueue, executor_shutdown, COMPLETED_FUTURE

logger = logging.getLogger('solace.messaging.publisher')


class _MessagePublisherState(enum.Enum):  # pylint: disable=too-few-public-methods,missing-class-docstring
    # Enum class for defining the message publisher state
    NOT_STARTED = 0
    STARTING = 1
    STARTED = 2
    TERMINATING = 3
    TERMINATED = 4


class _MessagePublisherActiveSubState(enum.Enum):  # pylint: disable=too-few-public-methods,missing-class-docstring
    # Enum class for defining the message publisher active sub state
    READY = 0
    FLOW_CONTROLLED = 1
    DOWN = 2


class _SendTask(ABC):
    @abstractmethod
    def on_publishable_sent(self):
        """ Remove item from buffer """

    @abstractmethod
    def get_publishable_for_send(self) -> 'TopicPublishable':
        """ peek first item can, return None """

    @abstractmethod
    def on_publishable_send_error(self, error: Exception = None):
        """ Error occurred on sending that can not be recovered remove poison message from buffer """


class _PublisherSendTask(_SendTask, ABC):
    def __init__(self, publisher: '_MessagePublisher'):
        self._publisher = publisher

    @property
    def publisher(self):
        return self._publisher


class _CommonSendTask(_PublisherSendTask):
    def __init__(self, publisher: '_MessagePublisher'):
        super().__init__(publisher)

    def on_publishable_sent(self):
        # remove item from buffer
        try:
            self._publisher.publishable_buffer.get_nowait() if self._publisher._is_active else (None, None)
        except queue.Empty:
            # rare cases on transport failure this can be emptied
            pass
        finally:
            self._publisher.on_sent()

    def on_publishable_send_error(self, error: Exception = None):
        # error occurred on sending that can not be recovered
        # remove poison message from buffer
        publishable = None
        tag = None
        try:
            publishable, tag = self._publisher.publishable_buffer.get_nowait() if self._publisher._is_active else (
                None, None)
        except queue.Empty:
            # rare cases on transport failure this can be emptied
            pass
        finally:
            self._publisher.on_sent()
            self._publisher.notify_publish_error(error, publishable, tag)

    def get_publishable_for_send(self) -> 'TopicPublishable':
        # peek first item can, return None
        element: tuple = self._publisher.publishable_buffer.peek()
        return None if element is None else element[0]


class _MessagePublisher(MessagePublisher) \
        :  # pylint: disable=R0904, missing-function-docstring, too-many-instance-attributes, missing-class-docstring
    # implementation class for message publisher for common publishing

    def __init__(self, builder: Union['_DirectMessagePublisherBuilder', '_PersistentMessagePublisherBuilder']):
        self._messaging_service: '_BasicMessagingService' = builder.messaging_service
        self._id_info = f"{self._messaging_service.logger_id_info} - " \
                        f"[PUBLISHER: {str(hex(id(self)))}]"
        self.adapter = _SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized', type(self).__name__)

        self._publisher_back_pressure_type = builder.publisher_back_pressure_type
        self._publishable_buffer_queue = None
        self._readiness_event_executor = None
        self.__init_back_pressure(builder)
        self._readiness_listener = None
        self._state = _MessagePublisherState.NOT_STARTED
        # _active_sub_state only has application meaning or value in the _state is active
        # which would only be in the message publisher states STARTED or TERMINATING
        self._active_sub_state = None
        self._solace_publisher_handlers = dict()
        self._solace_publisher_emitter = self._solace_publisher.emitter
        self._outbound_message_builder = _OutboundMessageBuilder()
        self._publishable = None
        self._start_future = None
        self._terminate_future = None
        self._start_lock = threading.Lock()
        self._start_async_lock = threading.Lock()
        self._terminate_lock = threading.Lock()
        self._terminate_async_lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix=type(self).__name__)
        self._finalizer = weakref.finalize(self, executor_shutdown, self._executor)

    def is_ready(self) -> bool:
        return self._state == _MessagePublisherState.STARTED and \
               self._active_sub_state == _MessagePublisherActiveSubState.READY

    def set_publisher_readiness_listener(self, listener: PublisherReadinessListener) -> 'MessagePublisher':
        # Sets a publisher state listener
        # Args:
        #     listener: listener to observe publisher state
        # Returns:
        is_type_matches(listener, PublisherReadinessListener)
        self._readiness_listener = listener
        return self

    def notify_when_ready(self):
        #
        # Non-blocking request to notify PublisherReadinessListener.
        # This method helps to overcome race condition between completion of the exception
        # processing on publishing of 'ready' aka can send event
        # Returns:
        #     None : returns none
        #
        if self._readiness_listener is None:
            self.adapter.warning("%s is not set", PublisherReadinessListener)
            raise PubSubPlusClientError(message=f"{PublisherReadinessListener} is not set")
        self._send_ready_notification()

    def _check_start_state(self):
        if self._state in [_MessagePublisherState.TERMINATING, _MessagePublisherState.TERMINATED]:
            self.adapter.warning("%s", PUBLISHER_TERMINATED_UNABLE_TO_START)
            raise IllegalStateError(PUBLISHER_TERMINATED_UNABLE_TO_START)

    def start(self):
        self._check_start_state()
        if self._state == _MessagePublisherState.STARTED:
            return self

        with self._start_lock:
            # Even after acquiring lock still we have to check the state to avoid re-doing the work
            if self._state == _MessagePublisherState.STARTED:
                return self

            if self._state == _MessagePublisherState.NOT_STARTED:
                self._is_message_service_connected()
                self._active_sub_state = _MessagePublisherActiveSubState.READY
                self._state = _MessagePublisherState.STARTED
                # register for solace publisher events
                self._register_publisher_events()
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug('[%s] is %s. Publisher back-pressure Type: %s', type(self).__name__,
                                       _MessagePublisherState.STARTED.name, self._publisher_back_pressure_type)
            return self

    def start_async(self) -> concurrent.futures.Future:
        # Start the Publisher asynchronously (non-blocking)
        if self.__is_in_startable_state():
            return self._start_future
        with self._start_async_lock:
            self._check_start_state()
            # Even after acquiring lock still we have to check the state to avoid spinning up the executor
            if self.__is_in_startable_state():
                return self._start_future
            self._start_future = self._executor.submit(self.start)
            return self._start_future

    def is_running(self) -> bool:
        # Method to validate publisher state is running
        # Returns:
        #     bool: True, if message publisher state is running else False
        is_running = self._state == _MessagePublisherState.STARTED
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] is running?: %s', type(self).__name__, is_running)
        return is_running

    def is_terminated(self) -> bool:
        # Method to validate publisher state is terminated
        # Returns:
        #     bool: True, if message publisher state is terminated else False
        is_terminated = self._state == _MessagePublisherState.TERMINATED
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] is terminated?: %s', type(self).__name__, is_terminated)
        return is_terminated

    def is_terminating(self) -> bool:
        # Method to validate publisher state is terminating
        # Returns:
        #     bool: True, if message publisher state is terminating else False
        is_terminating = self._state == _MessagePublisherState.TERMINATING
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] is terminating?: %s', type(self).__name__, is_terminating)
        return is_terminating

    def terminate_async(self, grace_period: int = GRACE_PERIOD_DEFAULT_MS) -> concurrent.futures.Future:
        # Terminate the PersistentMessageReceiver asynchronously (non-blocking).
        validate_grace_period(grace_period=grace_period, logger=logger)
        if self.__is_in_terminal_state():
            self._is_publisher_available_for_terminate()
            return self._terminate_future

        with self._terminate_async_lock:
            if self.__is_in_terminal_state():
                self._is_publisher_available_for_terminate()
                return self._terminate_future
            self._terminate_future = self._executor.submit(self.terminate, grace_period)
            return self._terminate_future

    def terminate(self, grace_period: int = GRACE_PERIOD_DEFAULT_MS):
        validate_grace_period(grace_period=grace_period, logger=logger)
        if not self._is_publisher_available_for_terminate():
            return

        with self._terminate_lock:
            # Even after acquiring lock still we have to check the state, since state can be modified by other threads
            if not self._is_publisher_available_for_terminate():
                return

            self._state = _MessagePublisherState.TERMINATING
            grace_period_in_seconds = convert_ms_to_seconds(grace_period)
            self._wait_pending_tasks(grace_period_in_seconds)
            self._cleanup()
            self._check_unpublished_state()

    def _wait_pending_tasks(self, timeout: float) -> float:
        remaining = timeout
        # wait for publishable queue if publisher is using one
        if self._publishable_buffer_queue:
            remaining = self._publishable_buffer_queue.wait_for_empty(remaining)
        return remaining if remaining > 0 else 0

    def __is_in_terminal_state(self):
        return self._terminate_future and \
               self._state in [_MessagePublisherState.TERMINATING, _MessagePublisherState.TERMINATED]

    def __is_in_startable_state(self):
        return self._start_future and \
               self._state in [_MessagePublisherState.STARTING, _MessagePublisherState.STARTED]

    def _resource_cleanup(self):
        # based publisher resource cleanup for shutdown
        # this can be overriden by specific publishers implementation

        # shutdown readiness executor
        if self._readiness_event_executor is not None:
            self._readiness_event_executor.shutdown(wait=True)
            self._readiness_event_executor = None
        # set async tasks to completed before shutdown
        with self._start_async_lock:
            if self._start_future is None:
                self._start_future = COMPLETED_FUTURE
        with self._terminate_async_lock:
            if self._terminate_future is None:
                self._terminate_future = COMPLETED_FUTURE
        # shutdown async executor
        self._executor.shutdown(wait=False)

    def _cleanup(self):
        # update state to shutdown pending task execution
        self._state = _MessagePublisherState.TERMINATED
        # prevent any new task from queueing
        self._unregister_publisher_events()
        self._resource_cleanup()
        self.adapter.info("%s", PUBLISHER_TERMINATED)

    def _is_publisher_available_for_terminate(self):
        if self._state == _MessagePublisherState.NOT_STARTED:
            self.adapter.debug('%s %s', PUBLISHER_UNAVAILABLE_FOR_TERMINATE,
                               self._state.name)
            return False
        elif self._is_already_terminated():
            return False
        return True

    def _is_already_terminated(self):
        # Return True if it is already TERMINATED
        if self._state == _MessagePublisherState.TERMINATED:
            self.adapter.debug(PUBLISHER_ALREADY_TERMINATED)
            return True
        return False

    def _check_unpublished_state(self):
        if self._publishable_buffer_queue is not None and self._publishable_buffer_queue.qsize() != 0:
            message = f'{UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER}. ' \
                      f'{UNPUBLISHED_MESSAGE_COUNT} [{self._publishable_buffer_queue.qsize()}]'
            self.adapter.warning(message)
            self._publishable_buffer_queue = None
            raise IncompleteMessageDeliveryError(message)

    def _message_publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                         additional_message_properties: typing.Dict[str, Union[str, int, bytearray]] = None,
                         correlation_tag=None):
        #     Sends message to the given destination(Topic) without checking arguments
        #       Note safely validating given is asummed before calling this method
        #           See _check_message_publish for validation of publisher state and args
        # Args:
        #         destination: Topic endpoint
        #         message: message payload
        #         additional_message_properties :
        #         correlation_tag

        # convert bytearray & string type messages to OutboundMessage
        if not isinstance(message, OutboundMessage):
            publish_message = self._outbound_message_builder.build(message)
        else:
            publish_message = message

        publishable = Publishable.of(publish_message.solace_message, destination)
        publishable.get_message().set_delivery_mode(self._delivery_mode)
        if correlation_tag:
            set_correlation_tag_ptr(publishable.get_message().msg_p, correlation_tag)
        # only add additional properties to publishable message self._message should not be modified
        if additional_message_properties:
            add_message_properties(additional_message_properties, publishable.get_message())
        if _PublisherUtilities.is_correlation_type(correlation_tag, _PublisherUtilities.AWAIT_TYPE):
            # inform  the broker to send ack ASAP
            # when its comes to  messages published via publish await acknowledgement method
            publishable.get_message().set_ack_immediately(True)
        if self._publisher_back_pressure_type != PublisherBackPressure.No:
            self._handle_back_pressure(publishable, correlation_tag)
        else:
            self.do_publish(publishable, correlation_tag)

    def _check_message_publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic):
        validate_topic_type(destination=destination, logger=logger)
        # validate a publisher to send a message
        # Raises:
        #     IllegalStateError: When publisher is NOT_STARTED/TERMINATED/NOT_READY
        #     PublisherOverflowError: When buffer queue is full
        #     SolaceWouldBlockException: When publisher receive WOULD_BLOCK
        #     PubSubPlusClientError: When unable to send message
        if not self.is_ready():
            if self._state == _MessagePublisherState.NOT_STARTED or \
                    self._state == _MessagePublisherState.STARTING:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_STARTED)
                raise IllegalStateError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_STARTED)
            elif self._state == _MessagePublisherState.TERMINATED:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATED)
                raise IllegalStateError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATED)
            elif self._state == _MessagePublisherState.TERMINATING:
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATING)
                raise IllegalStateError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_TERMINATING)
            elif self._state == _MessagePublisherState.STARTED and \
                    self._active_sub_state == _MessagePublisherActiveSubState.DOWN:
                self.adapter.warning(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED)
                raise IllegalStateError(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED)
            else:  # state should be STARTED and active sub-state should be FLOW_CONTROLLED
                self.adapter.warning(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_READY)
                raise PublisherOverflowError(UNABLE_TO_PUBLISH_MESSAGE_PUBLISHER_NOT_READY)

        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] enabled', self._publisher_back_pressure_type)
        if not isinstance(message, (OutboundMessage, str, bytearray)):
            raise InvalidDataTypeError(f"{type(message)} is unsupported at the "
                                       f"moment to publish a message")

    def message_publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                        additional_message_properties: typing.Dict[str, Union[str, int, bytearray]] = None,
                        correlation_tag=None):  # pylint: disable=too-many-branches
        #     Sends message to the given destination(Topic)
        # Args:
        #         destination: Topic endpoint
        #         message: message payload
        #         additional_message_properties :
        #         correlation_tag
        # Raises:
        #     IllegalStateError: When publisher is NOT_STARTED/TERMINATED/NOT_READY
        #     PublisherOverflowError: When buffer queue is full
        #     SolaceWouldBlockException: When publisher receive WOULD_BLOCK
        #     PubSubPlusClientError: When unable to send message
        # check if publisher can publish
        self._check_message_publish(message, destination)
        # publish message
        self._message_publish(message, destination, additional_message_properties, correlation_tag)

    def do_publish_async(self, send_task: '_PublisherSendTask'):  # pylint: disable=missing-function-docstring
        # Method to call underlying CORE publish method from publisher thread
        # Args:
        #     send_task (_PublisherSendTask): _PublisherSendTask instance to publish a message
        # Returns:
        #     void

        if not self._can_publish:
            # bail out early as the publisher is down permanently
            # this is the behaviour for a cancelled send task
            return
        publishable = None
        try:
            # get message
            publishable = send_task.get_publishable_for_send()
            # publishable can be None if the message buffer was emptied
            if publishable:
                # assume blocking
                publish_status = SOLCLIENT_WOULD_BLOCK
                while publish_status != SOLCLIENT_OK and self._can_publish:
                    # publish publishable on internal solace publisher
                    publish_status = self._solace_publisher.send(publishable)
                    # should internal publisher be blocked on send channel wait for send channel availability
                    if publish_status is SOLCLIENT_WOULD_BLOCK:
                        # wait for internal publisher to be able to send again
                        self._solace_publisher.wait_for_writable()
                # message was sent handle publisher state
                send_task.on_publishable_sent()
        except PubSubPlusClientError as exception:
            if publishable:
                # TODO add on_publishable_error for now treat like its sent to move on
                send_task.on_publishable_send_error(exception)
            else:
                # notify application of error asynchronously
                self.notify_publish_error(exception, publishable)
        except Exception as exception:
            # Something very bad happened log error
            self.adapter.error("Error on publisher send thread: [%s]", str(exception))
            raise PubSubPlusClientError("Error on publisher send thread") from exception

    def do_publish(self, publishable: 'TopicPublishable',
                   correlation_tag: bytes = None):  # pylint: disable=missing-function-docstring
        # Method to call underlying CORE publish method from application thread
        # Args:
        #     publishable (TopicPublishable): TopicPublishable instance contains OutboundMessage & Topic
        # Returns:
        #     publish status code
        try:
            if correlation_tag:
                # add correlation before send to ensure correlation on response
                self.add_correlation(publishable, correlation_tag)
            publish_status = self._solace_publisher.send(publishable)
            if publish_status == SOLCLIENT_WOULD_BLOCK:
                raise PublisherOverflowError(WOULD_BLOCK_EXCEPTION_MESSAGE)
            return publish_status
        except (PubSubPlusClientError, PublisherOverflowError) as exception:
            if correlation_tag:
                # remove correlation on error path as message was not sent
                self.remove_correlation(correlation_tag)
            if not self._messaging_service.is_connected:
                self.adapter.warning(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED)
                raise IllegalStateError(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED) from exception
            if isinstance(exception, PublisherOverflowError):
                self.adapter.info(exception)  # pragma: no cover
            else:
                self.adapter.warning(exception)  # pragma: no cover
            raise exception  # pragma: no cover

    def _handle_back_pressure(self, publishable: 'TopicPublishable',
                              correlation_tag: bytes = None):  # pylint: disable=missing-function-docstring
        # Method for handling the back pressure
        # Args:
        #   publishable(TopicPublishable) : publishable object
        # Raises:
        #     SolaceWouldBlockException: if WOULD-BLOCK received
        #     PublisherOverflowError: if buffer FULL
        try:
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug("%s", "Enqueue message to buffer/queue")
            if self._publisher_back_pressure_type == PublisherBackPressure.Reject:
                self.publishable_buffer.put((publishable, correlation_tag), block=False)
            else:
                self.publishable_buffer.put((publishable, correlation_tag))

            # async send closure
            def _serialized_send(send_task):
                send_task.publisher.do_publish_async(send_task)

            self._solace_publisher.submit(_serialized_send, self._send_task)
        except queue.Full:
            # under rare multi-threaded cases where a single publisher calling publish
            # from multiple threads can get a queue.full on back pressure reject
            # otherwise publisher active sub state is updated using the registered call
            # back on the publishable buffer, see __init_back_pressure
            self._handle_buffer_full()

    def _handle_buffer_full(self):  # this method will raise an exception if the queue is full
        current_size = self.publishable_buffer.qsize()
        raise PublisherOverflowError(f'{QUEUE_FULL_EXCEPTION_MESSAGE} Size: {current_size}')

    def on_sent(self):
        pass  # reserved this for future

    def _create_send_task(self):
        return _CommonSendTask(self)

    def _is_message_service_connected(self):
        # Method to check message_service connected or not
        # Returns:
        #     True if connected
        # Raises:
        #     IllegalStateError: if message_service not connected
        if not self._messaging_service.is_connected:
            self.adapter.warning(PUBLISHER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED)
            raise IllegalStateError(PUBLISHER_CANNOT_BE_STARTED_MSG_SERVICE_NOT_CONNECTED)
        return True

    @property
    def _is_active(self):
        return self._state in [_MessagePublisherState.STARTED, _MessagePublisherState.TERMINATING]

    @property
    def _can_publish(self):
        return self._is_active and self._active_sub_state != _MessagePublisherActiveSubState.DOWN

    def _register_publisher_event(self, event: '_SolacePublisherEvent', handler):
        handler_id = self._solace_publisher_emitter.register_publisher_event_handler(event, handler)
        self._solace_publisher_handlers[event] = handler_id

    def _send_ready_notification(self):
        if self._readiness_listener and self._readiness_event_executor:
            def on_ready_event():
                if self._readiness_listener is not None:
                    self._readiness_listener.ready()

            self._readiness_event_executor.submit(on_ready_event)

    def _on_publisher_down(self):
        if self._is_active:
            self._active_sub_state = _MessagePublisherActiveSubState.DOWN

    def _register_publisher_events(self):
        # registers live solace protocol publisher event handlers

        def on_publisher_down():
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                self.adapter.debug("%s", "Publisher DOWN event")
            self._on_publisher_down()

        # register underlying publisher trasnport failure handler this is for publisher types
        self._register_publisher_event(_SolacePublisherEvent.PUBLISHER_DOWN, on_publisher_down)
        if self._publisher_back_pressure_type == PublisherBackPressure.No:
            # for reject no buffer publisher register ready events
            # with the underlying solace publisher writeable event (aka CAN_SEND event)
            def on_publisher_writable():
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    self.adapter.debug("%s", "Publisher CAN_SEND event")
                if self._state is _MessagePublisherState.STARTED and \
                        self._active_sub_state is not _MessagePublisherActiveSubState.DOWN:
                    # self._active_sub_state = _MessagePublisherActiveSubState.READY
                    self._send_ready_notification()

            self._register_publisher_event(_SolacePublisherEvent.PUBLISHER_CAN_SEND, on_publisher_writable)

    def _unregister_publisher_events(self):
        # unregisters live solace protocol publisher event handlers
        for handler_id in self._solace_publisher_handlers.values():
            self._solace_publisher_emitter.unregister_publisher_event_handler(handler_id)
        self._solace_publisher_handlers.clear()

    def __init_back_pressure(self, builder):
        # initializes back pressure resources based on type
        # create underlying solace protocol publisher
        self._solace_publisher = self._messaging_service.create_publisher(self._publisher_back_pressure_type)
        # create back pressure buffer if required
        if self._publisher_back_pressure_type != PublisherBackPressure.No:
            # note the builder.buffer_capacity is assumed to validated before assignment
            self._publishable_buffer_queue = _PubSubPlusQueue(maxsize=builder.buffer_capacity)
            self._send_task = self._create_send_task()
        else:
            # back pressure reject with no buffer does not need a buffer
            self._publishable_buffer_queue = None

        # create readiness executor for ready events
        if self._publisher_back_pressure_type != PublisherBackPressure.Elastic:
            self._readiness_event_executor = _ThreadingUtil.create_serialized_executor(
                f"Publisher-{str(hex(id(self)))}-readiness-thread")
        else:
            # back pressure elastic never emits ready events
            self._readiness_event_executor = None

        if self._publisher_back_pressure_type == PublisherBackPressure.Reject:
            # reject with buffer publisher have ready state reflect the internal publishable
            # buffer capacity threshold where if the publisher is not ready when the
            # buffer capacity is reached and ready when there is capacity
            #
            # note other back pressure type publisher may register event on the underlying
            # solace protocol publisher see _register_publisher_events.
            def on_buffer_full():
                # when the buffer has reached it capacity limit update state
                # note do not update state when underlying native publisher is DOWN
                if self._is_active and self._active_sub_state != _MessagePublisherActiveSubState.DOWN:
                    self._active_sub_state = _MessagePublisherActiveSubState.FLOW_CONTROLLED

            def on_buffer_available():
                # when the buffer has available capacity update pulbisher sub state and notify application
                # note do not update state or send ready events when underlying native publisher is DOWN
                if self._is_active and self._active_sub_state != _MessagePublisherActiveSubState.DOWN:
                    self._active_sub_state = _MessagePublisherActiveSubState.READY
                    self._send_ready_notification()

            # register events with the buffer
            self._publishable_buffer_queue.register_on_event(_PubSubPlusQueue.ON_FULL_EVENT, on_buffer_full)
            self._publishable_buffer_queue.register_on_event(_PubSubPlusQueue.ON_AVAILABLE_EVENT, on_buffer_available)

    def add_correlation(self, publishable: 'TopicPublishable', tag: bytes):
        pass

    def remove_correlation(self, tag: bytes):
        pass

    @abstractmethod
    def notify_publish_error(self, exception: 'Exception', publishable: 'TopicPublishable', tag: bytes = None):
        """ Notify error on publish """

    @property
    @abstractmethod
    def _delivery_mode(self) -> str:
        """ Delivery mode """

    @property
    def publishable_buffer(self):
        return self._publishable_buffer_queue
