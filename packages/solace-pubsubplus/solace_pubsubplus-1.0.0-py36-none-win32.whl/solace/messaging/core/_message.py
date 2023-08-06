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
# pylint: disable=no-else-break,missing-module-docstring,missing-function-docstring,inconsistent-return-statements
# pylint: disable=missing-class-docstring

import ctypes
import logging
from enum import Enum
from typing import Union

from solace.messaging._impl._interoperability_support import _RestInteroperabilitySupport
from solace.messaging.config._sol_constants import SOLCLIENT_NOT_FOUND, SOLCLIENT_OK, SOLCLIENT_EOS, \
    SOLCLIENT_FAIL, SOLCLIENT_NOT_SET_PRIORITY_VALUE
from solace.messaging.config._solace_message_constants import FAILED_TO_RETRIEVE
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, PubSubPlusCoreClientError
from solace.messaging.message import Message
from solace.messaging.publisher._outbound_message_utility import get_next_field
from solace.messaging.utils._solace_utilities import get_last_error_info, is_type_matches

logger = logging.getLogger('solace.messaging.core')


class _SolClientDestination(ctypes.Structure):  # pylint: disable=too-few-public-methods,missing-class-docstring
    #   Conforms to solClient_destination . A data structure to represent the message destination. A publisher can
    #   send messages to topics or queues and solClient_destination specifies
    #   the details.
    _fields_ = [
        ("destType", ctypes.c_int),  # The type of destination
        ("dest", ctypes.c_char_p)  # The name of the destination (as a NULL-terminated UTF-8 string)
    ]


class _SolClientFieldType(Enum):  # pylint: disable=too-few-public-methods
    #  Conforms to solClient_fieldType . Data types that can be transmitted by the machine-independent read and write
    #   functions.
    SOLCLIENT_BOOL = 0  # Boolean.
    SOLCLIENT_UINT8 = 1  # 8-bit unsigned integer.
    SOLCLIENT_INT8 = 2  # 8-bit signed integer.
    SOLCLIENT_UINT16 = 3  # 16-bit unsigned integer.
    SOLCLIENT_INT16 = 4  # 16-bit signed integer.
    SOLCLIENT_UINT32 = 5  # 32-bit unsigned integer.
    SOLCLIENT_INT32 = 6  # 32-bit signed integer.
    SOLCLIENT_UINT64 = 7  # 64-bit unsigned integer.
    SOLCLIENT_INT64 = 8  # 64-bit signed integer.
    SOLCLIENT_WCHAR = 9  # 16-bit unicode character.
    SOLCLIENT_STRING = 10  # Null terminated string (ASCII or UTF-8).
    SOLCLIENT_BYTEARRAY = 11  # Byte array.
    SOLCLIENT_FLOAT = 12  # 32-bit floating point number.
    SOLCLIENT_DOUBLE = 13  # 64-bit floating point number.
    SOLCLIENT_MAP = 14  # Solace Map (container class).
    SOLCLIENT_STREAM = 15  # Solace Stream (container class).
    SOLCLIENT_NULL = 16  # NULL field.
    SOLCLIENT_DESTINATION = 17  # Destination field.
    SOLCLIENT_SMF = 18  # A complete Solace Message Format (SMF) message is encapsulated in the container.
    SOLCLIENT_UNKNOWN = -1  # A validly formatted but unrecognized data type was received.


class _SolClientValue(ctypes.Union):  # pylint: disable=too-few-public-methods
    # this class is relevant to c union for creating solclient values
    _fields_ = [('boolean', ctypes.c_bool),
                ('uint8', ctypes.c_uint8),
                ('int8', ctypes.c_int8),
                ('uint16', ctypes.c_uint16),
                ('int16', ctypes.c_int16),
                ('uint32', ctypes.c_uint32),
                ('int32', ctypes.c_int32),
                ('uint64', ctypes.c_uint64),
                ('int64', ctypes.c_int64),
                ('wchar', ctypes.c_wchar),
                ('float32', ctypes.c_float),
                ('float64', ctypes.c_double),
                ('string', ctypes.c_char_p),
                ('bytearray', ctypes.c_char_p),
                ('map', ctypes.c_uint64),
                ('stream', ctypes.c_uint64),
                ('dest', _SolClientDestination),
                ('smf', ctypes.POINTER(ctypes.c_ubyte)),
                ('unknownField', ctypes.POINTER(ctypes.c_ubyte))

                ]


class _SolClientField(ctypes.Structure):  # pylint: disable=too-few-public-methods
    # Conforms to solClient_field. The general solClient_field structure is returned by generic accessors to
    # the container. The application must first check the fieldType to determine
    # which member of the union to use.
    _fields_ = [
        ("type", ctypes.c_int),
        ("length", ctypes.c_uint32),
        ("value", _SolClientValue)
    ]


class _Message(Message):
    # implementation class for Message

    def __init__(self, solace_message: _SolaceMessage):
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug('[%s] initialized', type(self).__name__)
        self._solace_message: _SolaceMessage = solace_message
        self._user_properties = dict()
        self._get_http_content_type = None
        self._get_http_content_encoding = None
        self.__process_rest_interoperability(self.solace_message)
        self.__rest_interoperability_support = _RestInteroperabilitySupport(self._get_http_content_type,
                                                                            self._get_http_content_encoding)

    def get_rest_interoperability_support(self) -> '_RestInteroperabilitySupport':
        # Get RestInteroperabilitySupport object to invoke it's method
        return self.__rest_interoperability_support

    def __process_rest_interoperability(self, msg_p: _SolaceMessage):
        content_type_p = ctypes.c_char_p()
        encoding_p = ctypes.c_char_p()
        content_type_return_code = msg_p.get_message_http_content_type(content_type_p)
        content_encoding_return_type = msg_p.get_message_http_content_encoding(encoding_p)
        self._get_http_content_type = self.__process_rest_data(content_type_return_code, content_type_p)
        self._get_http_content_encoding = self.__process_rest_data(content_encoding_return_type, encoding_p)

    @staticmethod
    def __process_rest_data(return_code, ptr_value):
        if return_code == SOLCLIENT_OK:
            return ptr_value.value.decode()
        if return_code == SOLCLIENT_NOT_FOUND:
            return None
        exception: PubSubPlusCoreClientError = \
            get_last_error_info(return_code=return_code,
                                caller_description='Message->process_rest_data',
                                exception_message=FAILED_TO_RETRIEVE)
        logger.warning(str(exception))
        raise exception

    @property
    def solace_message(self):
        #  Property holds and returns a PubSub+ message.
        return self._solace_message

    def get_properties(self) -> dict:
        # Return the properties attached to the message
        map_p = ctypes.c_void_p(None)
        return_code = self._solace_message.message_get_user_property_map(map_p)
        if return_code == SOLCLIENT_NOT_FOUND:
            return {}
        if return_code == SOLCLIENT_FAIL:
            exception: PubSubPlusCoreClientError = \
                get_last_error_info(return_code=return_code,
                                    caller_description='Message->get_properties',
                                    exception_message='Unable to get payload user properties')
            logger.warning(str(exception))
            return {}
        sol_client_field_t = _SolClientField()
        key_p = ctypes.c_char_p()
        while True:
            return_code = get_next_field(map_p, sol_client_field_t, key_p)
            if return_code == SOLCLIENT_FAIL:  # pragma: no cover # Ignored due to core error scenarios
                exception: PubSubPlusCoreClientError = \
                    get_last_error_info(return_code=return_code,
                                        caller_description='Message->get_next_field',
                                        exception_message='Unable to get message next field')
                logger.warning(str(exception))
                break
            elif return_code == SOLCLIENT_EOS:
                break
            elif return_code == SOLCLIENT_OK:
                # Rest of the data types will be handled in future
                if sol_client_field_t.type == _SolClientFieldType.SOLCLIENT_STRING.value:
                    self._user_properties[key_p.value.decode()] = sol_client_field_t.value.string.decode()
                elif sol_client_field_t.type == _SolClientFieldType.SOLCLIENT_INT64.value:
                    self._user_properties[key_p.value.decode()] = sol_client_field_t.value.int64
                elif sol_client_field_t.type == _SolClientFieldType.SOLCLIENT_BYTEARRAY.value:
                    self._user_properties[key_p.value.decode()] = sol_client_field_t.value.bytearray
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug("[%s] get Props: [%s]", Message.__name__, self._user_properties)
        return self._user_properties

    def has_property(self, name: str) -> bool:
        # checks if message has a specific property attached.
        # :param name:
        # :return: boolean value
        is_type_matches(name, str, logger=logger)
        if not self._user_properties:
            self.get_properties()
        has_prop = name in self._user_properties
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug("Is property: [%s] exists? %s", name, has_prop)
        return has_prop

    def get_property(self, name: str) -> Union[str, int, bytearray, None]:
        # Get the value of a specific property.
        # :param: name the name of the property
        # :return: the value of the property or None if the property was not defined
        is_type_matches(name, str, logger=logger)
        if not self._user_properties:
            self.get_properties()
        user_prop = self._user_properties.get(name, None)
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug("Get Prop:[%s] Values: [%s]", name, user_prop)
        return user_prop

    def get_payload_as_bytes(self) -> Union[bytearray, None]:
        # Get the raw payload of the message
        # Returns:
        #     bytearray : The byte [] with the message payload.
        #     None : There is no payload
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug("Get [%s] payload as bytes", Message.__name__)
        buffer_p = ctypes.c_void_p(None)
        buffer_size = ctypes.c_uint32(0)
        xml_buffer_p = ctypes.c_void_p(None)
        xml_buffer_size = ctypes.c_uint32(0)
        return_code = self._solace_message.message_get_binary_attachment_ptr(buffer_p, buffer_size)
        xml_return_code = self._solace_message.get_xml_ptr(xml_buffer_p, xml_buffer_size)
        return _SolaceMessage.process_payload(return_code, buffer_p, buffer_size, xml_return_code,
                                              xml_buffer_p, xml_buffer_size, is_str=False)

    def get_binary_attachment(self):
        # This method is used to get the binary attachment from the receiver side
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug("Get [%s] binary attachment", Message.__name__)
        buffer_size, buffer_p = self._solace_message.get_payload_details()
        if buffer_size in [None, 0]:
            return None
        return _SolaceMessage.get_payload_from_memory(buffer_size, buffer_p)

    def get_payload_as_string(self) -> Union[str, None]:
        # Get especially to String decoded payload
        # Returns:
        #     payload (str) : the String representation of a payload
        if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
            logger.debug("Get [%s] payload as string", Message.__name__)
        binary_p = ctypes.c_char_p()
        xml_buffer_p = ctypes.c_void_p(None)
        xml_buffer_size = ctypes.c_uint32(0)
        str_return_code = self._solace_message.message_get_binary_attachment_string(binary_p)
        xml_return_code = self._solace_message.get_xml_ptr(xml_buffer_p, xml_buffer_size)
        return _SolaceMessage.process_payload(str_return_code, binary_p, None, xml_return_code,
                                              xml_buffer_p, xml_buffer_size, is_str=True)

    def get_correlation_id(self) -> Union[str, None]:
        # Get correlation id passed from a message producer
        # Returns:
        #     str or None : the unique identifier for the message set by the producer or None
        return_code = SOLCLIENT_FAIL
        try:
            correlation_p = ctypes.c_char_p()
            return_code = self._solace_message.message_get_correlation_id(correlation_p)
            if return_code == SOLCLIENT_OK:
                correlation_id = correlation_p.value.decode()
                if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                    logger.debug("Get [%s] correlation id: [%d]", Message.__name__, correlation_id)
                return correlation_id
            if return_code == SOLCLIENT_NOT_FOUND:
                return None
            logger.warning("Unable to get correlation id. Status code: %d", return_code)  # pragma: no cover
            # Ignored due to core error scenarios
            raise PubSubPlusClientError(f"Unable to get correlation id. Status code: {return_code}")  # pragma: no cover
            # Ignored due to core error scenarios
        except PubSubPlusClientError as exception:
            logger.warning("Unable to get correlation id. Status code: %d", return_code)  # pragma: no cover
            # Ignored due to core error scenarios
            raise PubSubPlusClientError(
                f"Unable to get correlation id. Status code: {return_code}") from exception  # pragma: no cover
            # Ignored due to core error scenarios

    def get_expiration(self) -> int:
        # The UTC time (in ms, from midnight, January 1, 1970 UTC) when the message is supposed
        # to expire.A value of 0 means the message never expires. The default value is 0.
        # Returns:
        #     int: The UTC time when the message is discarded or moved to a Dead Message Queue
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Get [%s] expiration", Message.__name__)
        timestamp_p = ctypes.c_uint64(0)
        return_code = self._solace_message.get_message_expiration(timestamp_p)
        if return_code == SOLCLIENT_OK:
            expiration_timestamp = timestamp_p.value
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug("Get [%s] expiration: [%s]", Message.__name__, expiration_timestamp)
            return expiration_timestamp
        if return_code == SOLCLIENT_NOT_FOUND:  # pragma: no cover # Ignored due to core error scenarios
            return None
        logger.warning("Unable to get expiration time. Status code: %d", return_code)  # pragma: no cover
        # Ignored due to core error scenarios
        raise PubSubPlusClientError(f"Unable to get expiration time. Status code:{return_code}")  # pragma: no cover
        # Ignored due to core error scenarios

    def get_sequence_number(self) -> Union[int, None]:
        # Gets the sequence number
        # Returns:
        #     int : The positive sequence number or -1 if it was not set.
        seq_num_p = ctypes.c_uint64(0)
        return_code = self._solace_message.get_message_sequence_number(seq_num_p)
        if return_code == SOLCLIENT_OK:
            sequence_number = seq_num_p.value
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug("Get [%s] sequence number: [%d]", Message.__name__, sequence_number)
            return sequence_number
        if return_code == SOLCLIENT_NOT_FOUND:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug("[%s] sequence number NOT FOUND", Message.__name__)
            return None
        logger.warning("Unable to get sequence number. Status code: %d", return_code)  # pragma: no cover
        # Ignored due to core error scenarios
        raise PubSubPlusClientError(f"Unable to get sequence number. Status code: {return_code}")  # pragma: no cover
        # Ignored due to core error scenarios

    def get_priority(self) -> Union[int, None]:
        # Gets priority value in the range of 0–255, or -1 if it is not set
        #
        # Returns:
        #     int: priority value in the range of 0–255, or -1 if it is not set
        priority_p = ctypes.c_uint32(0)
        return_code = self._solace_message.get_message_priority(priority_p)

        if return_code == SOLCLIENT_OK:
            if priority_p.value == SOLCLIENT_NOT_SET_PRIORITY_VALUE:
                priority = None
            else:
                priority = priority_p.value
            if logger.isEnabledFor(logging.DEBUG):  # pragma: no cover # Ignored due to log level
                logger.debug("Get %s priority: %d", Message.__name__, priority)
            return priority
        if return_code == SOLCLIENT_NOT_FOUND:  # pragma: no cover # Ignored due to core error scenarios
            return None
        logger.warning("Unable to get priority. Status code: %d", return_code)  # pragma: no cover
        # Ignored due to core error scenarios
        raise PubSubPlusClientError(f"Unable to get priority. Status code: {return_code}")  # pragma: no cover
        # Ignored due to core error scenarios
