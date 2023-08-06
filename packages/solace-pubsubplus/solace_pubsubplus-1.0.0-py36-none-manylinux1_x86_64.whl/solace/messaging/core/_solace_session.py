# pubsubplus-python-client
#
# Copyright 2021 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Module contains classes to interact with underlying c api

# pylint: disable=missing-module-docstring,too-many-statements,no-else-raise,inconsistent-return-statements
# pylint:disable=too-many-public-methods,too-many-branches,broad-except,missing-function-docstring
# pylint: disable=missing-class-docstring,too-many-instance-attributes

import ctypes
import datetime
import enum
import logging
import os
import platform
import threading
import weakref
from ctypes import Structure, pointer, byref, sizeof, POINTER, util
from ctypes import cdll, py_object, c_void_p, c_char_p, c_int
from itertools import chain
from os.path import dirname
from queue import Queue
from struct import calcsize

import solace
from solace.messaging import _SolaceServiceAdapter
from solace.messaging._solace_logging._core_api_log import last_error_info
from solace.messaging.config._ccsmp_property_mapping import CCSMP_SESSION_PROP_MAPPING
from solace.messaging.config._default_session_props import default_props
from solace.messaging.config._sol_constants import SOLCLIENT_CALLBACK_OK, SOLCLIENT_LOG_DEFAULT_FILTER, \
    SOLCLIENT_OK, SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE, \
    SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE, SOLCLIENT_SESSION_EVENT_CAN_SEND, SOLCLIENT_SESSION_EVENT_DOWN_ERROR, \
    SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR, SOLCLIENT_SESSION_EVENT_UP_NOTICE, \
    SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT, SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR
from solace.messaging.config._solace_message_constants import CCSMP_SUB_CODE, UNABLE_TO_LOAD_SOLCLIENT_LIBRARY, \
    CCSMP_SUB_CODE_OK, SESSION_FORCE_DISCONNECT, \
    ESTABLISH_SESSION_ON_HOST, CCSMP_SUB_CODE_LOGIN_FAILURE, CCSMP_SUB_CODE_FAILED_TO_LOAD_TRUST_STORE, \
    FAILED_TO_LOAD_TRUST_STORE, CCSMP_SUB_CODE_UNRESOLVED_HOST, UNRESOLVED_SESSION, \
    FAILED_TO_LOADING_CERTIFICATE_AND_KEY, CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY, \
    BAD_CREDENTIALS, CCSMP_SUBCODE_UNTRUSTED_CERTIFICATE, UNTRUSTED_CERTIFICATE_MESSAGE, CCSMP_INFO_SUB_CODE, \
    UNABLE_TO_FORCE_DISCONNECT, UNABLE_TO_DESTROY_SESSION, FAILURE_CODE
from solace.messaging.config.solace_properties import transport_layer_security_properties, transport_layer_properties
from solace.messaging.config.sub_code import SolClientSubCode
from solace.messaging.core._core_api_utility import context_destroy, session_disconnect, session_force_failure, \
    session_destroy, session_connect, session_create, prepare_array
from solace.messaging.core._publish import _SolacePublisherEvent, _SolacePublisherEventEmitter, \
    _SolacePublisherAcknowledgementEmitter
from solace.messaging.core._solace_transport import _SolaceTransportState
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, ServiceUnreachableError, \
    AuthenticationError, MessageRejectedByBrokerError, \
    MessageDestinationDoesNotExistError, PubSubPlusCoreClientError
from solace.messaging.messaging_service import _ServiceEvent
from solace.messaging.publisher._impl._publisher_utilities import _PublisherUtilities
from solace.messaging.utils._solace_utilities import get_last_error_info, read_key_from_config

logger = logging.getLogger('solace.messaging.core')


class _SolaceApiLibrary:
    # Singleton class to load dll
    _core_lib = None  # it is a protected member, and is used for holding the C Library
    _instance = None  # it is a protected member, and it holds the instance of the _SolaceApiLibrary super class
    _global_config = None

    def __new__(cls, *args, **kwargs):
        """
        return: instance of Solace Library
        """
        if cls._instance is None:
            cls._instance = super(_SolaceApiLibrary, cls).__new__(cls, *args, **kwargs)
            cls._core_lib = cls.__load_core_library()
            cls.__init_api()
        return cls._instance

    @staticmethod
    def _get_shared_lib_default_path(platform_os: str) -> str:
        # used to find shared_lib_config_default path based on platform
        # returns the default native library path or None if no matching
        # platform is found
        void_pointer_struct_char = 'P'
        is32bit = (calcsize(void_pointer_struct_char) * 8) == 32
        # get relative path of package installed library
        path_default_base = os.path.join(dirname(dirname(__file__)), "lib")
        lib_arch_32bit = {"Windows": "32"}
        lib_arch_64bit = {"Linux": "-x86_64", "Darwin": "-x86_64", "Windows": "-amd64"}
        lib_platform_name = {"Linux": "linux", "Darwin": "macosx", "Windows": "win"}
        lib_arch = lib_arch_32bit if is32bit else lib_arch_64bit
        arch = lib_arch.get(platform_os, None)
        platform_name = lib_platform_name.get(platform_os, None)
        if arch is not None and platform_name is not None:
            return os.path.join(path_default_base, "%s%s" % (platform_name, arch))

        return None  # pragma: no cover # Due to core error scenario

    @staticmethod
    def __load_core_library():
        # method to load dll based on OS
        #     Raises:
        #         PubSubPlusClientError: if library is missing
        # shared_lib_config_optional holds the key:value pairs for the the names
        # of shared libraries that can be used for accessing shared libraries in
        # user-customized locations. shared_lib_config_optional is different
        # from shared_lib_config_default because of different methods are used
        # to find the shared library in each case. util.find_library is required
        # to find custom installations of a shared library since it uses the
        # PATH on Windows or the LD_LIBRARY_PATH on Linux to find the custom
        # installation, and in Linux the shared library name passed to the
        # find_library() function must not have the 'lib' prefix or '.so'
        # suffix. In contrast, the default installation of the shared library
        # is within this package so it is always in the same place. Therefore,
        # the relative path from this file to the location of the default
        # installation of the shared library can be used to find it and load
        # it.

        shared_lib_config_optional = {"Linux": 'solclient', "Windows": 'libsolclient.dll',
                                      "Darwin": 'libsolclient.dylib'}

        # get the shared library name for this platform
        shared_lib_name_optional = shared_lib_config_optional.get(platform.system(), None)
        if shared_lib_name_optional:
            # search the PATH variable on Windows and the LD_LIBRARY_PATH on
            # Linux for a custom installation of a Solace CCSMP shared library
            shared_lib_path_optional = util.find_library(shared_lib_name_optional)
            if shared_lib_path_optional is not None:
                # if the custom shared library was found, load and return it
                try:
                    return cdll.LoadLibrary(shared_lib_path_optional)  # pragma: no cover
                except Exception as exception:  # pragma: no cover # Due to core error scenario
                    logger.info('%s from custom location [%s]. Exception: %s', UNABLE_TO_LOAD_SOLCLIENT_LIBRARY,
                                shared_lib_path_optional, str(exception))
                # if a custom installation of a CCSMP shared library was not
                # found, assume that the default shared library included in the
                # distribution should be loaded
            shared_lib_config_default = {"Linux": 'libsolclient.so', "Windows": 'libsolclient.dll',
                                         "Darwin": 'libsolclient.dylib'}
            # get the shared library name for this platform
            shared_lib_name_default = shared_lib_config_default.get(platform.system(), None)
            if shared_lib_name_default:  # pragma: no cover
                # join the relative path from this file to the shared
                # library file
                # prepend the current directory path to the relative path
                # from the this file to the shared library file
                shared_lib_path_default = _SolaceApiLibrary._get_shared_lib_default_path(platform.system())
                if shared_lib_path_default is not None:
                    shared_lib_path_default = os.path.join(
                        _SolaceApiLibrary._get_shared_lib_default_path(platform.system()),
                        shared_lib_name_default)
                    if shared_lib_path_default is not None:
                        try:
                            # if the default installation was found, load and return it
                            return cdll.LoadLibrary(shared_lib_path_default)
                        except Exception as exception:  # pragma: no cover # Due to core error scenario
                            logger.error('%s from [%s]. Exception: %s', UNABLE_TO_LOAD_SOLCLIENT_LIBRARY,
                                         shared_lib_path_default, str(exception))
                            raise PubSubPlusClientError(message=f'{UNABLE_TO_LOAD_SOLCLIENT_LIBRARY} '
                                                                f'from [{shared_lib_path_default}]. '
                                                                f'Exception: {exception}') from exception
        # if neither the custom nor default location of the shared library
        # contain the required shared library, throw the relevant error and
        logger.error(UNABLE_TO_LOAD_SOLCLIENT_LIBRARY)  # pragma: no cover # Due to core error scenario
        raise PubSubPlusClientError(
            message=UNABLE_TO_LOAD_SOLCLIENT_LIBRARY)  # pragma: no cover # Due to core error scenario

    @classmethod
    def __init_api(cls):
        # ssl & crypt config begins
        # log setup begins
        cls._core_lib.solClient_log_setFile(ctypes.c_char_p(None))
        cls._core_lib.solClient_initialize(SOLCLIENT_LOG_DEFAULT_FILTER, cls._global_config)
        cls.__set_version(cls._core_lib)
        cls._core_lib.solClient_log_setFilterLevel(0, 1)

    @property
    def solclient_core_library(self):
        # property to return the dll
        # return: Returns loaded dll
        return self._core_lib

    @staticmethod
    def __set_version(core_lib):  # pylint: disable=too-many-locals
        # Get and Set version using Core lib """

        class SolClientVersionInfo(Structure):  # pylint: disable=too-few-public-methods
            # Conforms to SolClient_version_info
            _fields_ = [
                ("version_p", c_char_p),
                ("dateTime_p", c_char_p),
                ("variant_p", c_char_p)
            ]

        version_pointer = pointer(SolClientVersionInfo())
        get_result = core_lib.solClient_version_get(byref(version_pointer))
        if get_result == SOLCLIENT_OK:
            app_name = read_key_from_config('solace_props', 'solace.messaging.client.app')
            core_api_name = 'C API'

            core_api_version = version_pointer.contents.version_p.decode("utf-8")
            core_api_date = version_pointer.contents.dateTime_p.decode("utf-8")
            core_api_variant = version_pointer.contents.variant_p.decode("utf-8")

            time_stamp = datetime.date.today().strftime("%b %d %Y %H:%M:%S")

            new_version = f'{app_name} / {core_api_name} {core_api_version}'
            new_date = f'{app_name} {time_stamp} / {core_api_name} {core_api_date}'
            new_variant = f'{app_name} / {core_api_variant}'

            updated_details = SolClientVersionInfo(c_char_p(new_version.encode('utf-8')),
                                                   c_char_p(new_date.encode('utf-8')),
                                                   c_char_p(new_variant.encode('utf-8')))

            return_code = core_lib._solClient_version_set(byref(updated_details))  # pylint: disable=protected-access
            if return_code != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenario
                exception: PubSubPlusCoreClientError = \
                    get_last_error_info(return_code=return_code,
                                        caller_description='SolaceApiLibrary->set_version',
                                        exception_message='Unable to set version')
                logger.warning(str(exception))
        else:  # pragma: no cover # Due to core error scenario
            logger.warning('Unable to set version')


def context_cleanup(context_pointer):
    # Function for cleaning up the context
    try:
        if context_pointer and context_pointer.value is not None:
            context_destroy(context_pointer)
    except PubSubPlusClientError as exception:  # pragma: no cover # Due to core error scenario
        logger.error(exception)


class _SolaceApiContext:
    # Class to create context

    def __init__(self):
        # return: instance of Solace context
        self.__context_p = c_void_p(None)  # it is a protected member, which holds the context pointer of
        # type (ctypes)
        return_code = self._create_context()
        self._finalizer = weakref.finalize(self, context_cleanup, self.__context_p)
        self._id_info = f"SolaceApiContext Id: {str(hex(id(self)))}"
        self.adapter = _SolaceServiceAdapter(logger, {'id_info': self._id_info})
        if return_code != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenario
            exception: PubSubPlusCoreClientError = \
                get_last_error_info(return_code=return_code,
                                    caller_description='SolaceApiContext->init',
                                    exception_message='Failed to create solace context')
            self.adapter.warning(str(exception))
            raise exception

    def _create_context(self):
        # Method to create context

        class SolClientContextCreateRegisterFdFuncInfo \
                    (Structure):  # pylint: disable=too-few-public-methods,trailing-whitespace
            # Conforms to solClient_context_createRegisterFdFuncInfo_t
            #  .. _class solClient_context_createRegisterFdFuncInfo:
            #
            #  Function is set on a per-Context basis. Providing these functions is optional. If provided, both
            #  function information for file descriptor registration and file descriptor un-registration functions.
            #  Tht be non-NULL, and if not provided, both must be NULL.
            #
            # These functions are used when the application wants to own event generation, and they supply file
            # descriptor events to the API. Such applications typically want to poll several different devices,
            # of which the API is only one. When these functions are provided, the API does not manage its own
            # devices. Instead, when a device is created, the provided 'register' function is called to register the
            # device file descriptor for read and/or write events. It is the responsibility of the application to
            # call back into API when the appropriate event occurs on the device file descriptor. The API callback is
            # provided to the register function (see SolClient_context_registerFdFunc_t). If this interface is
            # chosen, the application <b>must</b> also call solClient_context_timerTick() at regular intervals.
            #
            #  Normally these are not used, and the API owns event registrations. If an internal Context thread is used
            #  by enabling SOLCLIENT_CONTEXT_PROP_CREATE_THREAD
            #  (see also SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD),
            #  the API takes care of all devices and timers and no action is required by the application.
            #  If the internal thread is
            #  not enabled, the application must call solClient_context_processEvents() to provide scheduling time to
            #   the API.
            #
            # When the API owns event registrations, it also provides file descriptor register/unregister service to
            # the application. solClient_context_registerForFdEvents() and solClient_context_unregisterForFdEvents()
            # can be used by applications to pass file descriptors to the API for managing, keeping event generation
            # localized to the internal thread or the thread that calls solClient_context_processEvents(). """
            _fields_ = [
                ("reg_fd_func_p", c_void_p),
                ("unreg_fd_func_p", c_void_p),
                ("user_p", c_void_p)
            ]

        class SolClientContextCreateFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # Conforms to solClient_context_createFuncInfo_t
            _fields_ = [
                ("reg_fd_info", SolClientContextCreateRegisterFdFuncInfo)
            ]

        # create native context
        context_props = pointer(c_char_p.in_dll(self.solclient_core_library,
                                                "_solClient_contextPropsDefaultWithCreateThread"))
        context_func_info = SolClientContextCreateFuncInfo()
        context_func_info.reg_fd_info = \
            SolClientContextCreateRegisterFdFuncInfo(None, None, None)  # pylint: disable=attribute-defined-outside-init
        return_code = self.solclient_core_library.solClient_context_create(context_props, byref(self.__context_p),
                                                                           byref(context_func_info),
                                                                           sizeof(context_func_info))
        return return_code

    @property
    def context_p(self):
        #     Get underlying c api pointer
        #     return:Returns contexts pointer
        return self.__context_p

    @property
    def solclient_core_library(self):
        # property to return the dll
        # return: Returns loaded dll
        return _SolaceApiLibrary().solclient_core_library


class SolClientServiceEventCallbackInfo(Structure):  # pylint: disable=too-few-public-methods
    # Conforms to solClient_session_eventCallbackInfo_t
    # this is a C structure incorporated using c-types module for providing the session event callback info
    _fields_ = [
        ("session_event", ctypes.c_int32),
        ("response_code", ctypes.c_uint32),
        ("info_p", c_char_p),
        ("correlation_p", c_void_p)
    ]


class _MessagingServiceState(enum.Enum):  # pylint: disable=too-few-public-methods
    NOT_CONNECTED = -1
    CONNECTING = 0
    CONNECTED = 1
    RECONNECTING = 2
    RECONNECTED = 3
    DISCONNECTING = 4
    DISCONNECTED = 5
    # TODO work out Down state as its a part of the underlying transport and can be transtioned from
    DOWN = 6


def _session_cleanup(adapter, session_pointer):
    try:
        if session_pointer:
            session_destroy(session_pointer)
    except PubSubPlusClientError as exception:  # pragma: no cover # Due to core error scenario
        adapter.error(exception)


class _SolaceApi(_SolacePublisherEventEmitter, _SolacePublisherAcknowledgementEmitter):
    # class to interact with underlying C core functionality
    _event_callback = None  # this is an protected member, and is used for event callback
    _msg_callback = None  # this is an protected member, and is used for message callback
    # _log_callback = None
    #  solclient_session_event_callback_info_pt ia an public member which is used for holding
    #  the pointer object of SolClientServiceEventCallbackInfo
    solclient_session_event_callback_info_pt = POINTER(SolClientServiceEventCallbackInfo)
    # protected member, holds c-type event callback function type
    _event_callback_func_type = ctypes.CFUNCTYPE(ctypes.c_int, c_void_p,
                                                 solclient_session_event_callback_info_pt,
                                                 py_object)
    _msg_callback_func_type = ctypes.CFUNCTYPE(ctypes.c_int, c_void_p, c_void_p, py_object)

    # it is a protected member, holds the message callback function type of c-types

    def __init__(self, messaging_service: '_BasicMessagingService'):
        # This method is used to initialize _SolaceApiContext() for creating context
        self._messaging_service = messaging_service
        self._id_info = self._messaging_service.logger_id_info
        self.adapter = _SolaceServiceAdapter(logger, {'id_info': self._id_info})
        self._core_lib = solace.CORE_LIB
        self._core_lib.solClient_returnCodeToString.restype = c_char_p
        self._core_lib.solClient_returnCodeToString.argtypes = [c_int]
        self._session_func_info = None
        self._context = _SolaceApiContext()
        self._context_p = self._context.context_p
        self._attempt_listeners = set()
        self._reconnection_listeners = set()
        self._service_interruption_listeners = set()
        self._connection_can_listen = threading.Event()  # common for event 12,13,1
        self._listener_queue = None  # common for event 12,13,1
        self._host = None  # it holds the host value
        self._can_send_received = threading.Event()  # this sets the threading event based on the can send received
        self._messaging_service_state = _MessagingServiceState.NOT_CONNECTED  # defines the msg service state
        self._transport_state = None
        self._can_listen = threading.Event()
        # this is a private member & is used for holding session pointer which is of c-types
        self.__session_p = c_void_p(None)
        self._finalizer = weakref.finalize(self, _session_cleanup, self.adapter, self.__session_p)
        self._pub_handler_id_gen = 0
        self._pub_event_handlers = dict()
        self._pub_ack_handlers = dict()
        for pub_event in _SolacePublisherEvent:
            self._pub_event_handlers[pub_event] = dict()
        self._can_receive = list()  # will have receiver's id to set can_receive_event
        self._state_change = list()  # will have receiver's id to set state_change_event
        self._receiver_queues = list()  # maintains the list of attributes
        # used to unblock direct/persistent receiver queue during blocking receive_message call

    def emit_publisher_event(self, event: '_SolacePublisherEvent'):
        for handler in self._pub_event_handlers[event].values():
            handler()

    def register_publisher_event_handler(self, event: '_SolacePublisherEvent', handler) -> int:
        handler_id = self._pub_handler_id_gen
        self._pub_handler_id_gen += 1
        event_dict = self._pub_event_handlers[event]
        event_dict[handler_id] = handler
        return handler_id

    def unregister_publisher_event_handler(self, handler_id: int):
        for event_handlers in self._pub_event_handlers.values():
            if event_handlers.get(handler_id) is not None:
                event_handlers.pop(handler_id)
                break

    def register_acknowledgement_handler(self, handler, publisher_correlation_id: bytes):
        self._pub_ack_handlers[publisher_correlation_id] = handler

    def unregister_acknowledgement_handler(self, publisher_correlation_id: bytes):
        if self._pub_ack_handlers.get(publisher_correlation_id) is not None:
            self._pub_ack_handlers.pop(publisher_correlation_id)

    @property
    def receiver_queues(self):
        return self._receiver_queues

    @property
    def can_receive(self):
        return self._can_receive

    @property
    def state_change(self):
        return self._state_change

    @property
    def service_interruption_listeners(self):
        return self._service_interruption_listeners

    @property
    def attempt_listeners(self):
        return self._attempt_listeners

    @property
    def reconnection_listeners(self):
        return self._reconnection_listeners

    @property
    def listener_queue(self):
        return self._listener_queue

    @listener_queue.setter
    def listener_queue(self, val: Queue):
        self._listener_queue = val

    @property
    def connection_can_listen(self):
        return self._connection_can_listen

    @property
    def can_send_received(self):
        return self._can_send_received

    @property
    def can_listen(self):
        return self._can_listen

    def _session_connect(self) -> int:
        # connects to broker in  blocking mode
        # Returns:
        #     int :  returns   the return code from do_connect() i.e (-1 to 8)
        self._messaging_service_state = _MessagingServiceState.CONNECTING
        return self.__do_connect()

    def session_disconnect(self) -> int:
        #  Disconnects the specified Session by the help of the C API solClient_session_disconnect,
        #  if the session is disconnected then the return code will be SOLCLIENT_OK else this method
        #  will raise exception.
        # Returns:
        #     int :  returns  0 or -1
        #  Raises:
        #         PubSubPlusClientError: if we didn't receive 0 as return code
        self._core_lib.solClient_session_disconnect.argtypes = [c_void_p]

        return_code = session_disconnect(self.__session_p)
        if return_code != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenario
            exception: PubSubPlusCoreClientError = \
                get_last_error_info(return_code=return_code,
                                    caller_description='SolaceApi->session_disconnect',
                                    exception_message='Unable to disconnect session')
            self.adapter.warning("%s", str(exception))
            raise exception

        # NOTE: Once after successful session disconnect, we're clearing __session_p object since we don't have
        # business of reconnecting the session again, but if we introduce re-connection mechanism inside
        # (actually RetryStrategy are wrapped inside C api) wrapper api then we can't assign None to __session_p
        self._messaging_service_state = _MessagingServiceState.DISCONNECTED
        return return_code

    def session_force_disconnect(self) -> int:
        # function to disconnect with event broker. HIGH RISK: We should use this only for testing.
        # In ideal scenario, we won't FORCE DISCONNECT SESSION
        # Returns:
        #     int :  returns  0 or -1
        #  Raises:
        #         PubSubPlusClientError: if we didn't receive 1 as return code
        self._messaging_service_state = _MessagingServiceState.DISCONNECTING
        self._core_lib.solClient_session_disconnect.argtypes = [c_void_p]
        return_code = session_force_failure(self.__session_p)
        if return_code != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenario
            failure_message = f'{UNABLE_TO_FORCE_DISCONNECT}{return_code}'
            exception: PubSubPlusCoreClientError = \
                get_last_error_info(return_code=return_code,
                                    caller_description='SolaceApi->session_force_disconnect',
                                    exception_message=failure_message)
            self.adapter.warning(str(exception))
            raise exception
        self._messaging_service_state = _MessagingServiceState.DISCONNECTED
        self.adapter.warning(SESSION_FORCE_DISCONNECT)
        return return_code

    def service_cleanup(self):
        self._messaging_service_state = _MessagingServiceState.DISCONNECTING
        self._transport_state = _SolaceTransportState.DOWN
        self.session_destroy()
        context_cleanup(self._context_p)
        self._can_send_received.set()
        # emit publisher DOWN event for any lingering publishers
        self.emit_publisher_event(_SolacePublisherEvent.PUBLISHER_DOWN)
        self._messaging_service_state = _MessagingServiceState.DISCONNECTED

    def session_destroy(self) -> int:  # pragma: no cover
        # Destroys the specified session. On return, the opaque Context pointer
        # is set to NULL. This operation must not be performed in a Context callback
        # for the Context being destroyed. This includes all Sessions on the Context,
        # timers on the Context, and application-supplied register file descriptor
        # functions.
        # Returns:
        #      int :  returns  0 or -1
        # Raises:
        #      PubSubPlusClientError: if we didn't receive 0 as return code
        if self.__session_p:
            self._core_lib.solClient_session_destroy.argtypes = [c_void_p]
            return_code_on_destroy = session_destroy(self.__session_p)
            if return_code_on_destroy != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenario
                error_message = f"{UNABLE_TO_DESTROY_SESSION} {FAILURE_CODE}{return_code_on_destroy}"
                exception: PubSubPlusCoreClientError = \
                    get_last_error_info(return_code=return_code_on_destroy,
                                        caller_description='SolaceApi->session_destroy',
                                        exception_message=error_message)
                self.adapter.warning("%s", str(exception))
                raise exception
            return return_code_on_destroy
        return None

    def create_session(self, config: dict) -> int:
        # When creating the Context, specify that the Context thread be
        # created automatically instead of having the application create its own
        # Context thread.
        # Args:
        #     config (dict):Configuration has been sent in the form of key value pairs.
        # Returns:
        #     int : returns return code from solClient_session_create and value will be '0' for success
        # Raises:
        #         PubSubPlusClientError: if we didn't receive 1 as return code
        arr = self.__prepare_session_props(config)
        self._session_func_info = self.__create_session_func_info()
        return_code = session_create(arr, self._context_p, self.__session_p,
                                     self._session_func_info)
        if transport_layer_properties.HOST in config:
            self.adapter.info('%s [%s]. [%s]', ESTABLISH_SESSION_ON_HOST,
                              config[transport_layer_properties.HOST],
                              "Connected" if return_code == SOLCLIENT_OK else "Not connected")
        if return_code != SOLCLIENT_OK:
            core_exception_msg = last_error_info(status_code=return_code, caller_desc="Session Creation")
            info_sub_code = core_exception_msg[CCSMP_INFO_SUB_CODE]
            exception_message = core_exception_msg[CCSMP_SUB_CODE]
            if f"unspecified property '" \
               f"{CCSMP_SESSION_PROP_MAPPING[transport_layer_security_properties.TRUST_STORE_PATH]}'" \
                    in core_exception_msg:
                self.adapter.warning("HOST: %s is secured, %s param is expected to establish SESSION",
                                     config[transport_layer_properties.HOST],
                                     transport_layer_security_properties.TRUST_STORE_PATH)
                raise PubSubPlusCoreClientError(message=f"HOST: {config[transport_layer_properties.HOST]} is secured, "
                                                        f"{transport_layer_security_properties.TRUST_STORE_PATH} "
                                                        f"param is expected to establish SESSION",
                                                sub_code=info_sub_code)
            self.adapter.error(core_exception_msg[CCSMP_SUB_CODE])
            if exception_message == CCSMP_SUB_CODE_FAILED_TO_LOAD_TRUST_STORE:
                self.adapter.error(FAILED_TO_LOAD_TRUST_STORE)
                raise PubSubPlusCoreClientError(message=FAILED_TO_LOAD_TRUST_STORE, sub_code=info_sub_code)
            elif exception_message == CCSMP_SUB_CODE_UNRESOLVED_HOST:
                self.adapter.error(UNRESOLVED_SESSION)
                raise ServiceUnreachableError(UNRESOLVED_SESSION)
            elif exception_message == CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY:  # pragma: no cover
                # Due to core error scenario
                self.adapter.error(FAILED_TO_LOADING_CERTIFICATE_AND_KEY)
                raise PubSubPlusCoreClientError(message=FAILED_TO_LOADING_CERTIFICATE_AND_KEY, sub_code=info_sub_code)
            else:
                raise PubSubPlusCoreClientError(message=core_exception_msg, sub_code=info_sub_code)
        return return_code

    def send_message(self, msg_p) -> int:
        # Sends a message on the specified Session. The message is composed of a number of optional
        #  components that are specified by the msg_p. The application should first
        #  allocate a solClient_msg, then use the methods defined in solClientMsg.h to
        #  build the message to send.
        #  solClient_session_sendMsg() returns SOLCLIENT_OK when the message has been successfully
        #  copied to the transmit buffer or underlying transport, this does not guarantee successful
        #  delivery to the Solace messaging appliance. When sending Guaranteed messages (persistent or non-persistent),
        #  the application will receive a subsequent SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT event for all
        #  messages successfully delivered to the Solace messaging appliance.
        # For Guaranteed messages, notifications of
        #  quota, permission, or other delivery problems will be indicated in a
        # SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR
        #  event.
        #  <b>Special Buffering of Guaranteed Messages</b>\n
        #  Guaranteed messages (SOLCLIENT_DELIVERY_MODE_PERSISTENT or SOLCLIENT_DELIVERY_MODE_NONPERSISTENT) are
        #  assured by the protocol between the client and the Solace message router. To make developers' task easier,
        #  guaranteed messages are queued for delivery in many instances:
        #  1. While transport (TCP) flow controlled.
        #  2. While message router flow controlled.
        #  3. While sessions are connecting or reconnecting.
        #  4. While sessions are disconnected or down.
        #  The C-SDK will buffer up to a publishers window size
        # of guaranteed messages before
        #  solClient_session_sendMsg() will either block (when SOLCLIENT_SESSION_PROP_SEND_BLOCKING is enabled)
        # or return SOLCLIENT_WOULD_BLOCK
        #  (on active sessions) or return SOLCLIENT_NOT_READY (on disconnected or reconnecting sessions).
        #  For the most part this is desired behavior. Transient sessions failures do not require special handling
        # in applications. When
        #  SOLCLIENT_SESSION_PROP_RECONNECT_RETRIES is non-zero, the underlying transport will automatically
        # reconnect and the publishing
        #  application does not need to concern itself with special handling for the transient reconnecting state.
        # Args:
        #    session_pointer :  The opaque Session returned when the Session was created.
        #     msg_p:  The opaque message created by solClient_msg_alloc.
        # Returns:
        #     SOLCLIENT_OK, SOLCLIENT_NOT_READY, SOLCLIENT_FAIL, SOLCLIENT_WOULD_BLOCK
        return self._core_lib.solClient_session_sendMsg(self.session_pointer, msg_p)

    @property
    def is_session_connected(self) -> bool:
        # property to know whether we are connected to session or not
        # Returns :
        # bool : True if service is connected else False
        if self._messaging_service_state in [_MessagingServiceState.CONNECTED, _MessagingServiceState.RECONNECTED]:
            return True
        return False

    @property
    def transport_state(self) -> _SolaceTransportState:
        return self._transport_state

    @property
    def message_service_state(self) -> _MessagingServiceState:
        # property to know the state of messaging service
        # Returns :
        # MessagingServiceState
        return self._messaging_service_state

    @property
    def session_pointer(self):
        # This method will return the underlying  C-api session pointer
        return self.__session_p

    def __do_connect(self) -> int:
        # this method establishes the connection to the service, if the connection is established
        # the return code will be zero stating SOLCLIENT_OK, if the connection is not established properly
        # then the return_code will be anything other than zero, in order to handle exception the return code
        # is sent to the __handle_exception_message() along with the caller description.
        # Returns:
        #     int: returns the return code ranging from (-1 to 8)
        return_code = session_connect(self.__session_p)
        if return_code == SOLCLIENT_OK:
            return return_code
        self.__handle_exception_message(return_code=return_code, caller_desc='do_connect')

    def __handle_exception_message(self, return_code, caller_desc='SessionConnect'):  # pylint: disable=no-self-use
        core_exception_msg = last_error_info(status_code=return_code, caller_desc=caller_desc)
        core_sub_code = core_exception_msg[CCSMP_SUB_CODE]
        info_sub_code = core_exception_msg[CCSMP_INFO_SUB_CODE]

        if core_sub_code == CCSMP_SUBCODE_UNTRUSTED_CERTIFICATE:
            self.adapter.warning(' %s %s', UNTRUSTED_CERTIFICATE_MESSAGE, core_exception_msg)
            raise PubSubPlusCoreClientError(message=f'{UNTRUSTED_CERTIFICATE_MESSAGE} {core_exception_msg}',
                                            sub_code=info_sub_code)
        elif core_sub_code == CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY:
            self.adapter.warning(' %s %s', FAILED_TO_LOADING_CERTIFICATE_AND_KEY, core_exception_msg)
            raise PubSubPlusCoreClientError(message=f'{FAILED_TO_LOADING_CERTIFICATE_AND_KEY} {core_exception_msg}',
                                            sub_code=info_sub_code)
        elif core_sub_code == CCSMP_SUB_CODE_LOGIN_FAILURE:
            self.adapter.warning('%s %s', BAD_CREDENTIALS, core_exception_msg)
            raise AuthenticationError(message=f'{BAD_CREDENTIALS} {core_exception_msg}')
        self.adapter.warning('%s', core_exception_msg)
        raise PubSubPlusCoreClientError(message=core_exception_msg, sub_code=info_sub_code)

    def __create_session_func_info(self):
        # Create session function information needed for session creation.

        class SolClientServiceCreateRxCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # Conforms to solClient_session_createRxMsgCallbackFuncInfo_t
            # Applications should use solClient_session_createRxMsgCallbackFuncInfo.
            # Callback information for Session message receive callback. This is set on a per-Session basis.
            _fields_ = [
                ("callback_p", c_void_p),
                ("user_p", c_void_p)
            ]

        class SolClientServiceCreateEventCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # Conforms to solClient_session_createEventCallbackFuncInfo_t.
            # Callback information for Session event callback. This is set on a per-Session basis.
            _fields_ = [
                ("callback_p", self._event_callback_func_type),
                ("user_p", py_object)
            ]

        class SolClientServiceCreateRxMsgCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # Conforms to solClient_session_createRxMsgCallbackFuncInfo_t
            # Applications should use solClient_session_createRxMsgCallbackFuncInfo.
            # Callback information for Session message receive callback. This is set on a per-Session basis
            _fields_ = [
                ("callback_p", self._msg_callback_func_type),
                ("user_p", py_object)
            ]

        class SolClientServiceCreateFuncInfo(Structure):  # pylint: disable=too-few-public-methods

            # Conforms to solClient_session_createFuncInfo_t and
            #   Function information for Session creation. This is set on a per-Session basis.
            #   The application must set the eventInfo callback information. All Sessions must have an
            # event callback registered.
            #   The application must set one, and only one, message callback information.
            # The <i>rxInfo</i> message callback interface is
            #  <b>deprecated</b> and should be set to NULL. All applications should prefer to use
            # the <i>rxMsgInfo</i> callback interface.
            #  The application has available to it a SolClient_opaqueMsg_pt, which can be kept for
            # later processing and provides a
            #  structured interface for accessing elements of the received message. The application
            # callback routine then has the signature
            #  (see SolClient_session_rxMsgCallbackFunc_t) :

            _fields_ = [
                ("rx_info", SolClientServiceCreateRxCallbackFuncInfo),  # deprecated
                ("event_info", SolClientServiceCreateEventCallbackFuncInfo),
                ("rx_msg_info", SolClientServiceCreateRxMsgCallbackFuncInfo)
            ]

        if not self._event_callback and not self._msg_callback:
            self._event_callback = self._event_callback_func_type(self.__service_event_callback_routine)

            self._msg_callback = self._msg_callback_func_type(self.__service_msg_rx_callback_routine)

        session_func_info = SolClientServiceCreateFuncInfo(
            (c_void_p(None), c_void_p(None)),
            (self._event_callback, py_object),
            (self._msg_callback, py_object))
        return session_func_info

    def __service_event_callback_routine \
                    (self, _opaque_session_p,
                     event_info_p, _pyobject) \
            :  # pylint: disable=too-many-branches  # pragma: no cover # Due to invocation in callbacks
        # conforms to eventCallback
        #     The event callback function is mandatory for session creation.
        # Args:
        #     _opaque_session_p: The Session event that has occurred
        #     event_info_p: A pointer to a NULL-terminated string providing further information about the event,
        #      when available.
        #     _pyobject: Application-supplied correlation pointer where applicable
        # Returns: int
        info = event_info_p
        correlation_tag = b''
        if info.contents.correlation_p:
            correlation_tag = _PublisherUtilities.decode(info.contents.correlation_p)
        event = info.contents.session_event

        if event != SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT:
            message = info.contents.info_p.decode()
        else:
            message = ""
        response_code = info.contents.response_code
        error_info = last_error_info(status_code=response_code,
                                     caller_desc="From service event callback")
        exception = None
        if error_info[CCSMP_SUB_CODE] != CCSMP_SUB_CODE_OK:
            self.adapter.warning("%s", error_info)
            exception = PubSubPlusClientError(message=error_info)
            if error_info[CCSMP_INFO_SUB_CODE] == SolClientSubCode.SOLCLIENT_SUBCODE_PUBLISH_ACL_DENIED.value:
                exception = MessageRejectedByBrokerError(message=error_info)
            elif error_info[CCSMP_INFO_SUB_CODE] == SolClientSubCode.SOLCLIENT_SUBCODE_NO_SUBSCRIPTION_MATCH.value:
                exception = MessageDestinationDoesNotExistError(message=error_info)

        if event == SOLCLIENT_SESSION_EVENT_UP_NOTICE:
            self._transport_state = _SolaceTransportState.LIVE
            self._messaging_service_state = _MessagingServiceState.CONNECTED

        elif event == SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE:
            self._messaging_service_state = _MessagingServiceState.RECONNECTING
            if self.listener_queue and self.attempt_listeners:
                self.connection_can_listen.set()

            for listener in self.attempt_listeners:
                self.__put_service_event(listener, self.listener_queue, message, exception)
            self.connection_can_listen.clear()

        elif event == SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE:
            self._messaging_service_state = _MessagingServiceState.RECONNECTED
            if self.reconnection_listeners and self.listener_queue:
                self.connection_can_listen.set()

            for listener in self.reconnection_listeners:
                self.__put_service_event(listener, self.listener_queue, message, exception)
            self.connection_can_listen.clear()

        elif event == SOLCLIENT_SESSION_EVENT_CAN_SEND:
            self.emit_publisher_event(_SolacePublisherEvent.PUBLISHER_CAN_SEND)
            self.can_send_received.set()

        elif event == SOLCLIENT_SESSION_EVENT_DOWN_ERROR:
            self._transport_state = _SolaceTransportState.DOWN
            self._messaging_service_state = _MessagingServiceState.DOWN
            self.emit_publisher_event(_SolacePublisherEvent.PUBLISHER_DOWN)
            self.can_send_received.set()  # wake up blocked publisher listener or worker threads
            # get the receiver's can_receive event,  set it to wake up the thread
            # get the receiver's state_change event, set it to wake up the thread
            # get the publisher's can_peek event, set it to wake up the thread
            for event_down_error in chain(self._can_receive, self._state_change):
                if hasattr(self, event_down_error):
                    getattr(self, event_down_error).set()
            for queue in self._receiver_queues:  # unblock direct/persistent receiver's queues
                queue.put(None)

            if self.service_interruption_listeners and self.listener_queue:
                self.connection_can_listen.set()

            for listener in self.service_interruption_listeners:
                self.__put_service_event(listener, self.listener_queue, message, exception)
            self.connection_can_listen.clear()

        elif event == SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR:
            self._transport_state = _SolaceTransportState.DOWN
            self._messaging_service_state = _MessagingServiceState.DISCONNECTED
        # TODO handle SOLCLIENT_SESSION_EVENT_RX_MSG_TOO_BIG_ERROR
        elif event in [SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT, SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR]:
            # Based on the correlation tag ack is sent to respective publisher's queue
            # self.adapter.warning('Received message acknowledgement with [%s] len [%s] from internal publisher',
            #    correlation_tag, len(correlation_tag))
            pub_id = _PublisherUtilities.get_publisher_id(correlation_tag)
            if pub_id:
                ack_handler = self._pub_ack_handlers.get(pub_id)
                if ack_handler:
                    ack_handler(correlation_tag, event, exception)
                else:
                    # no matching publisher
                    self.adapter.info('Received message acknowledgement with [%s] without a publisher',
                                      correlation_tag)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            self.adapter.debug('Session Event: [%d]', event)
        return SOLCLIENT_CALLBACK_OK

    def __service_msg_rx_callback_routine(self, _opaque_session_p, _msg_p, _pyobject) \
            :  # pylint: disable=no-self-use  # pragma: no cover # Due to invocation in callbacks
        # conforms to messageReceiveCallback
        #  The message receive callback function is mandatory for session creation
        # Args:
        #     _opaque_sess ion_p:The Session event that has occurred
        #     _msg_p : pointer to message
        #     _pyobject : Application-supplied correlation pointer where applicable
        # Returns:
        #     int : return value 0
        return SOLCLIENT_CALLBACK_OK

    def __put_service_event(self, listener, listener_queue, message, exception):
        # Method for adding service event"""

        obj = _ServiceEvent(self._host, exception, message, datetime.datetime.now().timestamp())
        listener_queue.put((listener, obj))

    def __prepare_session_props(self, config: dict) -> ctypes.Array:
        #     Prepares the session props by comparing their instances and type casting the property value
        #     and finally adding the key value pairs to the dictionary
        #     Args:
        #     config: has key prop_value pairs of session property
        #     Returns:Array of config needed for session creation which got from config argument
        if transport_layer_properties.HOST in config:
            self._host = config[transport_layer_properties.HOST]
        tmp_dict = dict()
        for key, value in config.items():
            if key in CCSMP_SESSION_PROP_MAPPING:
                tmp_dict[CCSMP_SESSION_PROP_MAPPING[key]] = str(int(value)) if isinstance(value, bool) else str(value)
        tmp_dict = {**default_props, **tmp_dict}  # merge the config with default props
        return prepare_array(tmp_dict)

    @property
    def messaging_service_state(self):
        return self._messaging_service_state
