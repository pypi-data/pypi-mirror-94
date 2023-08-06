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

"""Module contains the implementation class and methods for the PersistentMessagePublisher"""

# pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-ancestors,protected-access
# pylint: disable=missing-function-docstring, unused-variable,no-else-break,no-else-return,no-else-continue
# pylint: disable=no-else-raise,broad-except

import itertools
import logging
import queue
import threading
import time
import weakref
from typing import Union, Any, Dict

from solace.messaging.config._sol_constants import SOLCLIENT_DELIVERY_MODE_PERSISTENT, SOLCLIENT_DELIVERY_MODE_DIRECT
from solace.messaging.config._solace_message_constants import VALUE_CANNOT_BE_NEGATIVE, \
    UNABLE_TO_SET_LISTENER, PUBLISH_TIME_OUT, UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER, \
    INVALID_ADDITIONAL_PROPS, UNPUBLISHED_MESSAGE_COUNT, UNPUBLISHED_PUBLISH_RECEIPT_COUNT
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, PubSubTimeoutError, \
    IllegalArgumentError, IncompleteMessageDeliveryError, IllegalStateError
from solace.messaging.publisher._impl._message_publisher import _MessagePublisher, _MessagePublisherState, \
    _CommonSendTask
from solace.messaging.publisher._impl._publisher_utilities import validate_topic_type, _PublisherUtilities
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.persistent_message_publisher import PersistentMessagePublisher \
    , MessagePublishReceiptListener, PublishReceipt
from solace.messaging.resources.topic import Topic
from solace.messaging.utils._solace_utilities import is_type_matches, is_none_or_empty_exists, convert_ms_to_seconds, \
    _PubSubPlusQueue, _ThreadingUtil, executor_shutdown

logger = logging.getLogger('solace.messaging.publisher')


class _DeliveryDispatcher:
    def __init__(self, upper_bound: int = 3):
        self._upper_bound = upper_bound
        self._executor = None
        self._submit_count = 0

    def start(self):
        if self._executor is None:
            logger.debug('Starting delivery dispatcher')
            self._executor = _ThreadingUtil.create_serialized_executor('DeliveryDispatcher')

    def dispatch_delivery(self, handler, context=None):
        self._submit_count += 1
        # logger.warning('Delivery dispatcher dispatch_delivery with submit count[%s]', self._submit_count)
        executor = self._executor
        if executor and self._submit_count <= self._upper_bound:
            def _dispatch_handler():
                try:
                    handler(context)
                except Exception as error:
                    logger.error('Error on Delivery dispatcher dispatch_delivery with submit count[%s], error: [%s]',
                                 self._submit_count,
                                 str(error))
                    raise
                finally:
                    self._submit_count -= 1
            try:
                return executor.submit(_dispatch_handler)
            except Exception as ex_error:
                # on rare occurences of unexpected shutdown executor can be shutdown
                # without the publisher unregistering for events
                # only occurs when the application receives an unexpected error
                # and all api object are being cleaned up with finalizers and GC
                # log any failure at debug
                logger.debug('Error on executor submit: [%s]', str(ex_error))
                # correct submit count to prevent mulitple errors from blocking
                # new submit tasks
                self._submit_count -= 1
                # leave to default return of None

        else:
            self._submit_count -= 1
        return None

    def shutdown(self, wait: bool = True):
        executor = self._executor

        if executor:
            self._executor = None
            executor.shutdown(wait=wait)


class _PersistentSendTask(_CommonSendTask):
    def get_publishable_for_send(self) -> 'TopicPublishable':
        element: tuple = self._publisher.publishable_buffer.peek()
        publishable = None if element is None else element[0]
        correlation_tag = None if element is None else element[1]
        if correlation_tag and publishable:
            self._publisher.add_correlation(publishable, correlation_tag)
        return publishable


def publisher_cleanup(delivery_dispatcher, executor):
    executor_shutdown(executor)
    if delivery_dispatcher:
        delivery_dispatcher.shutdown(wait=False)


class _PersistentMessagePublisher(_MessagePublisher, PersistentMessagePublisher) \
        :  # pylint: disable=too-many-instance-attributes, too-many-ancestors

    # implementation class for persistent message publisher
    def __init__(self, builder):
        super().__init__(builder)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('[%s] initialized', type(self).__name__)
        # create unique puack id for publisher
        self._pub_id = _PublisherUtilities.create_publisher_id(self)
        # id(self).to_bytes(8, byteorder='big')
        # init messaging gen, note this is only unique to the publisher
        # this uses a implementation detail of cpython and Pypy for thread safety
        # this should be revisited if other python implementation must be supported
        self._pub_msg_id_gen = itertools.count()

        self._persistent_ack_queue = _PubSubPlusQueue()

        self._persistent_await_ack_queue = _PubSubPlusQueue()

        self._publish_receipt_listener: 'MessagePublishReceiptListener' = None

        self._delivery_dispatcher = _DeliveryDispatcher()
        self._correlation = dict()
        self._publish_await_mutex = threading.Lock()
        self._finalizer = weakref.finalize(self, publisher_cleanup, self._delivery_dispatcher, self._executor)

    def _next_msg_id(self) -> int:
        # used built-in GIL lock for thread safe increment and return
        return next(self._pub_msg_id_gen)

    def set_message_publish_receipt_listener(self, listener: 'MessagePublishReceiptListener'):
        # Method for setting the message publish listener"""
        is_type_matches(listener, MessagePublishReceiptListener, logger=logger)
        if self._state in [_MessagePublisherState.STARTED]:
            self._publish_receipt_listener = listener
            self._delivery_dispatcher.start()
            if self._persistent_ack_queue.qsize() > 0:
                self._delivery_dispatcher.dispatch_delivery(self._on_delivery_task)
            return self
        else:
            error_message = f'{UNABLE_TO_SET_LISTENER}. Message Publisher is NOT started/ready'
            self.adapter.warning(error_message)
            raise IllegalStateError(error_message)

    def publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic, user_context: Any = None,
                additional_message_properties: Dict[str, Union[str, int, bytearray]] = None):
        # Sends message to the given destination
        validate_topic_type(destination=destination, logger=logger)
        if additional_message_properties:
            is_none_or_empty_exists(additional_message_properties,
                                    error_message=INVALID_ADDITIONAL_PROPS, logger=logger)
        # verify publisher can publish
        self._check_message_publish(message, destination)
        # create correlation state iff there is a receipt listener
        # persistent messages pulbished without can not receive publish receipts
        if self._publish_receipt_listener is not None:
            # uniquely identify this message for publish
            msg_id = self._next_msg_id()
            # create correlation tag to map ack events bad to this publisher for a specific message
            correlation_tag = _PublisherUtilities.create_message_correlation_tag(self._pub_id, msg_id=msg_id)
            # add user_context to correlation mapping
            self._correlation[correlation_tag] = (None, user_context)
        else:
            # prevent correlation mapping on acknowledgement handler events
            correlation_tag = None
        # publish message on internal solace publisher
        self._message_publish(message, destination, additional_message_properties, correlation_tag=correlation_tag)

    def publish_await_acknowledgement(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                                      time_out: int = None,
                                      additional_message_properties: Dict[str, Union[str, int, bytearray]] = None):
        # Sends OutboundMessage to the given destination, blocking until delivery acknowledgement is received or timeout
        # occurs
        #
        # :py:class:`~solace.messaging.builder.direct_message_publisher_builder.DirectMessagePublisherBuilder`
        #  can be used to create the OutboundMessage instance.  Alternatively, a bytearray or string payload may be
        #  passed to publish() and the API will create a py:class:`~solace.messaging.core.message.Message` to send.
        #
        # Args:
        #     message ():   py:class:`~solace.messaging.core.message.Message` or payload to publish
        #     destination (): Destination to add to the message
        #     time_out (:obj:`int`, optional):  max time in ms to wait for the message acknowledgement
        #     additional_message_properties (Dict[str, Union[str, int, bytearray]]):additional properties,
        #     to customize a particular message, each key can be customer provided, or it can be a key from a
        #     :py:mod:`~solace.messaging.config.solace_properties.message_properties`, The value can be either a string
        #      or an integer or a bytearray
        #
        # Returns:
        #
        # Raises:
        # PubSubTimeoutError:  is thrown after specified timeout when no response received
        # MessageRejectedByBrokerError: when message was rejected from a broker for some reason
        # PublisherOverflowError: when publisher publishes too fast, application may attempt to
        # republish the message.
        # MessageDestinationDoesNotExistError: given message destination does not exist
        # IllegalArgumentError: if the value of timeout is negative or invalid
        validate_topic_type(destination=destination, logger=logger)
        if time_out is not None and time_out < 0:
            raise IllegalArgumentError(VALUE_CANNOT_BE_NEGATIVE)
        # protect with mutex for thread safe access to target correlation tag
        with self._publish_await_mutex:
            # create await correlation tag
            msg_id = self._next_msg_id()
            correlation_tag = \
                _PublisherUtilities.create_message_correlation_tag(self._pub_id, \
                                                                   pub_type=_PublisherUtilities.AWAIT_TYPE,
                                                                   msg_id=msg_id)
            # publish message with correlation tag
            self.message_publish(message, destination, additional_message_properties, correlation_tag=correlation_tag)
            # wait for acknowledgement
            try:
                timeout_in_seconds = convert_ms_to_seconds(time_out) if time_out is not None else None
                start = time.time()
                # get first item for ack await queue
                tag, event, exception = self._persistent_await_ack_queue.get(True, timeout=timeout_in_seconds)
                # since this can be an ack from a previous publish drain await queue
                # until published tag is received from ack
                if timeout_in_seconds is not None:
                    # handle remaining timeout if any left
                    remaining = timeout_in_seconds - (time.time() - start)
                    while tag != correlation_tag and self._is_active and remaining > 0.0:
                        tag, event, exception = self._persistent_await_ack_queue.get(True, timeout=remaining)
                        remaining = timeout_in_seconds - (time.time() - start)
                    if tag != correlation_tag and not remaining > 0.0:
                        exception = PubSubTimeoutError(PUBLISH_TIME_OUT)
                else:
                    # block until ack is received
                    while tag != correlation_tag and self._is_active:
                        tag, event, exception = self._persistent_await_ack_queue.get(True, timeout=None)
                if exception:
                    raise exception
                elif tag != correlation_tag:
                    raise PubSubPlusClientError('Failed to confirm message was published')
            except queue.Empty as exception:
                raise PubSubTimeoutError(PUBLISH_TIME_OUT) from exception

    def notify_publish_error(self, exception: 'Exception', publishable: 'TopicPublishable', tag: bytes = None):
        def _handle_publishable_exception(pub: 'TopicPublishable'):
            if tag:
                # enqueue publish receipt event
                user_context = None
                if tag in self._correlation.keys():
                    _, user_context = self._correlation[tag]
                # ensure correlation map is complete
                self._correlation[tag] = (pub, user_context)
                # put error event on ack queue
                self._persistent_ack_queue.put_nowait((tag, -1, exception))
                if self._publish_receipt_listener:
                    # submit error event dispatch task for enqueue error event
                    self._delivery_dispatcher.dispatch_delivery(self._on_delivery_task)

            else:
                self.adapter.error("Received asynchronous persistent publisher failure without identifiable tag,"
                                   "message destination='%s' exception='%s'",
                                   str(pub.get_destination()), str(exception))

        if not _PublisherUtilities.is_correlation_type(tag, _PublisherUtilities.ASYNC_TYPE):
            # log synchronous failures at info as exceptions shodl be raised instead of passed to notify
            self.adapter.info(
                "Received synchronous publisher failure, tag='%s' exception='%s'",
                str(tag) if tag else 'None',
                str(exception))
            # exit early
            return
        if publishable:
            _handle_publishable_exception(publishable)
        else:
            # check if there is a publishable in the correlation map
            pub = None
            if tag and tag in self._correlation.keys():
                pub, _ = self._correlation[tag]
                if pub:
                    _handle_publishable_exception(pub)
                else:
                    self.adapter.error(
                        "Received asynchronous publisher failure without publishable message, tag='%s' exception='%s'",
                        str(tag), str(exception))
            else:
                self.adapter.error(
                    "Received asynchronous publisher failure without publishable message, tag='%s' exception='%s'",
                    str(tag), str(exception))

    def add_correlation(self, publishable: 'TopicPublishable', tag: bytes):
        if _PublisherUtilities.is_correlation_type(tag, _PublisherUtilities.ASYNC_TYPE) and \
                self._correlation and tag in self._correlation.keys():
            _, user_context = self._correlation[tag]
            self._correlation[tag] = (publishable, user_context)

    def remove_correlation(self, tag: bytes):
        if _PublisherUtilities.is_correlation_type(tag, _PublisherUtilities.ASYNC_TYPE) and \
                self._correlation and tag in self._correlation.keys():
            self._correlation.pop(tag)

    def _create_send_task(self):
        return _PersistentSendTask(self)

    def _check_unpublished_state(self):
        # receipt_count = self._persistent_await_ack_queue.qsize() + self._persistent_ack_queue.qsize()
        receipt_count = len(self._correlation)
        unpublished_count = 0 if self._publishable_buffer_queue is None else self._publishable_buffer_queue.qsize()
        if unpublished_count != 0 or receipt_count != 0:
            error_message = f"{UNCLEANED_TERMINATION_EXCEPTION_MESSAGE_PUBLISHER}. " \
                            f"{UNPUBLISHED_MESSAGE_COUNT} [{unpublished_count}]. "
            if receipt_count != 0:
                error_message += f"{UNPUBLISHED_PUBLISH_RECEIPT_COUNT} [{receipt_count}]"
            self.adapter.warning(error_message)
            self._publishable_buffer_queue = None
            self._persistent_await_ack_queue = None
            self._persistent_ack_queue = None
            self._correlation.clear()
            raise IncompleteMessageDeliveryError(error_message)

    def _wait_pending_tasks(self, timeout: float) -> float:
        # waiting for all pending sends
        remaining = super()._wait_pending_tasks(timeout)

        # wait for all pending acks
        # use correlation map to count pending publishable acknowledgement
        def are_pending_publish_receipts() -> bool:
            return len(self._correlation) != 0

        # The _persistent_ack_queue is only the currently received acknowledgement from the network protocol
        # must add the condition that the correlation map must be empty for all published messages.
        # Additions to the correlation map occur for every publish requested by the application.
        if self._publish_receipt_listener:
            remaining = self._persistent_ack_queue.wait_for_empty(remaining,
                                                                  are_pending_publish_receipts) if remaining > 0 else 0
        return remaining

    def _resource_cleanup(self):
        super()._resource_cleanup()
        # TODO cleanup remaining
        self._delivery_dispatcher.shutdown(wait=True)

    def _register_publisher_events(self):
        super()._register_publisher_events()

        def _on_ack_closure(tag, event, error):
            self._on_ack(tag, event, error)

        self._solace_publisher.ack_emitter.register_acknowledgement_handler(_on_ack_closure, self._pub_id)

    def _unregister_publisher_events(self):
        self._solace_publisher.ack_emitter.unregister_acknowledgement_handler(self._pub_id)
        super()._unregister_publisher_events()

    def _on_publisher_down(self):
        # call parent to update state
        super()._on_publisher_down()
        # created publish receipts for all pending sends for clearing the buffer
        if self._publishable_buffer_queue:
            # enqueue error notification on dispatch thread instead of event thread
            self._delivery_dispatcher.dispatch_delivery(self._on_cancel_pending_publishables_task)

    def _on_cancel_pending_publishables_task(self, context=None):
        # drain all pending publishable task
        publishable, tag = self._publishable_buffer_queue.peek()
        # TODO use context to pass more informative error information or maybe use get last error?
        error = PubSubPlusClientError('Publisher Down can not publish')
        while publishable and tag:
            # enqueue error notification for each publishable
            self.notify_publish_error(error, publishable, tag)
            self._publishable_buffer_queue.get_nowait()
            publishable, tag = self._publishable_buffer_queue.peek()

    def _on_ack(self, correlation_tag: bytes, event, error: Exception = None):
        if self._is_active:
            if _PublisherUtilities.is_correlation_type(correlation_tag, _PublisherUtilities.ASYNC_TYPE):
                self._persistent_ack_queue.put_nowait((correlation_tag, event, error))
                if self._publish_receipt_listener:
                    self._delivery_dispatcher.dispatch_delivery(self._on_delivery_task)
            else:
                self._persistent_await_ack_queue.put_nowait((correlation_tag, event, error))

    def _on_delivery_task(self, context=None):
        # TODO use context to pass more informative error information or maybe use get last error?
        # verify everything for a delivery is available
        # tag, _, exception = self._persistent_ack_queue.unsafe_peek()
        element: tuple = self._persistent_ack_queue.unsafe_peek()
        tag = None if element is None else element[0]
        # peek exception as well
        exception = None if element is None else element[2]
        listener = self._publish_receipt_listener
        # to dispatch a delivery task:
        # the publisher must be active
        # the publisher must have a listener
        # the delivery task must have a tag
        while self._is_active and tag and listener:
            # prepare publish receipt components
            outbound_message, persisted, timestamp, user_context = \
                self._prepare_publish_receipt(tag)
            if not any([outbound_message, persisted, timestamp, user_context]):
                # tag, _, exception = self._persistent_ack_queue.unsafe_peek()
                # advance queue
                tag, _, exception = self._persistent_ack_queue.get_nowait()
                # TODO log warning droping publish receipt?
                # peek next element
                element: tuple = self._persistent_ack_queue.unsafe_peek()
                tag = None if element is None else element[0]
                exception = None if element is None else element[2]
                listener = self._publish_receipt_listener
                continue
            else:
                publish_receipt = PublishReceipt(outbound_message, exception, timestamp, persisted, user_context)
                try:
                    listener.on_publish_receipt(publish_receipt)
                except Exception as error:
                    self.adapter.warning("Failed to dispatch. Message handler type: [%s]. "
                                         "Exception: %s",
                                         type(listener),
                                         str(exception))

            # advance queue as delivery is complete (error or not)
            tag, _, exception = self._persistent_ack_queue.get_nowait()
            # peek the next delivery and keep pushing out deliveries if available
            # tag, _, exception = self._persistent_ack_queue.unsafe_peek()
            element: tuple = self._persistent_ack_queue.unsafe_peek()
            tag = None if element is None else element[0]
            exception = None if element is None else element[2]
            listener = self._publish_receipt_listener

    def _prepare_publish_receipt(self, correlation_tag: bytes):
        if self._correlation and correlation_tag in self._correlation.keys():
            publishable, user_context = self._correlation.pop(correlation_tag)
            outbound_message = publishable.get_message()
            delivery_mode = outbound_message.get_delivery_mode()
            is_persisted = delivery_mode != SOLCLIENT_DELIVERY_MODE_DIRECT
            return outbound_message, is_persisted, time.time(), user_context
        else:
            return None, None, None, None

    @property
    def _delivery_mode(self):
        return SOLCLIENT_DELIVERY_MODE_PERSISTENT
