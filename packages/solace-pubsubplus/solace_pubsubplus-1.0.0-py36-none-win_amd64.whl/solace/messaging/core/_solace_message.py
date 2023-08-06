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


# module containing the class and methods/functions which represent a C-API opaqueMsg

# pylint:disable=missing-module-docstring, missing-function-docstring, too-many-public-methods,R1710
# pylint: disable=too-many-arguments,no-else-raise,no-else-return

import ctypes
import logging
import weakref
from ctypes import c_uint32, sizeof, c_int64, c_int32, c_uint64, byref

import solace
from solace.messaging.config._sol_constants import SOLCLIENT_OK, SOLCLIENT_MSGDUMP_FULL, DEFAULT_BUFFER_SIZE, \
    DEFAULT_BUFFER_MULTIPLIER, SOLCLIENT_NOT_FOUND, SOLCLIENT_FAIL
from solace.messaging.config._solace_message_constants import FAILED_TO_GET_DUPLICATE_MESSAGE
from solace.messaging.config.solace_properties.message_properties import APPLICATION_MESSAGE_TYPE, PRIORITY, \
    HTTP_CONTENT_TYPE, ELIDING_ELIGIBLE, PERSISTENT_TIME_TO_LIVE, PERSISTENT_DMQ_ELIGIBLE, HTTP_CONTENT_ENCODING, \
    CORRELATION_ID, PERSISTENT_EXPIRATION, PERSISTENT_ACK_IMMEDIATELY, APPLICATION_MESSAGE_ID, SEQUENCE_NUMBER
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, PubSubPlusCoreClientError
from solace.messaging.utils._solace_utilities import get_last_error_info

logger = logging.getLogger('solace.messaging.core.api')


def message_cleanup(msg_p, caller):
    #  Free a solClient Msg previously allocated by solClient_msg_alloc().
    #   Applications are responsible for releasing all message buffers they allocate by
    #   solClient_msg_alloc() or solClient_msg_dup(). Message buffers received by callback
    #   are owned by the API and <b>must not</b> be released. However the application may
    #   take ownership of these message buffers as well by returning
    #   SOLCLIENT_CALLBACK_TAKE_MSG on return from the receive message callback function.
    #   If the application returns SOLCLIENT_CALLBACK_TAKE_MSG, it <b>must</b> release
    #   the message by calling solClient_msg_free() when it is finished with the message
    #   buffer.
    #  Args:
    #    msg_p :   A pointer to the msg_p previously allocated. On return
    #                        this reference is NULL and the memory previously referenced by
    #                        it is no longer valid.
    #  Returns:
    #     SOLCLIENT_OK on success. SOLCLIENT_FAIL when msg_p does
    #                        not point to a valid msg"""
    try:
        if msg_p is None:  # pylint: disable=no-else-return
            return
        elif isinstance(msg_p, ctypes.c_int):
            msg_p = ctypes.c_void_p(int(msg_p))
            solace.CORE_LIB.solClient_msg_free(byref(msg_p))
        elif isinstance(msg_p, ctypes.c_void_p):
            solace.CORE_LIB.solClient_msg_free(byref(msg_p))
        else:
            logger.error("%s msg_p not a valid type", caller)
    except PubSubPlusClientError as exception:  # pragma: no cover # Ignored due to log level
        logger.error(exception)


class _SolaceMessage:
    # The class handles PubSub+ messaging.
    def __init__(self, msg_p=None):
        self._msg_p = ctypes.c_void_p(None)
        self._message_properties_mapping = {APPLICATION_MESSAGE_TYPE: self.set_message_application_message_type,
                                            ELIDING_ELIGIBLE: self.set_eliding_eligible,
                                            PRIORITY: self.set_message_priority,
                                            HTTP_CONTENT_TYPE: self.set_message_http_content_type,
                                            HTTP_CONTENT_ENCODING: self.set_message_http_content_encoding,
                                            CORRELATION_ID: self.message_set_correlation_id,
                                            PERSISTENT_TIME_TO_LIVE: self.set_ttl,
                                            PERSISTENT_EXPIRATION: self.set_message_expiration,
                                            PERSISTENT_DMQ_ELIGIBLE: self.set_persistent_dmq_eligible,
                                            PERSISTENT_ACK_IMMEDIATELY: self.set_ack_immediately,
                                            SEQUENCE_NUMBER: self.set_message_sequence_number,
                                            APPLICATION_MESSAGE_ID: self.set_message_application_message_id}

        if msg_p is None:
            #   Allocate a solClient Msg that can be used for storing and sending
            #   messages to and from the Solace Messaging Appliance.
            #   Applications are responsible for releasing all message buffers they allocate
            #   by solClient_msg_alloc()
            # returnsSOLCLIENT_OK on success. SOLCLIENT_FAIL on failure.
            #   msg_p is only valid after a SOLCLIENT_OK return.
            return_code = solace.CORE_LIB.solClient_msg_alloc(ctypes.byref(self._msg_p))
            if return_code != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenario
                exception: PubSubPlusCoreClientError = \
                    get_last_error_info(return_code=return_code,
                                        caller_description='SolaceMessage->msg_alloc',
                                        exception_message='Unable to allocate SolaceMessage.')
                logger.warning(str(exception))
                raise exception
        else:
            self._msg_p = msg_p
        self._finalizer = weakref.finalize(self, message_cleanup, self._msg_p, "Solace message cleanup")

    @property
    def msg_p(self):
        return self._msg_p

    @property
    def message_properties_mapping(self):
        return self._message_properties_mapping

    def handle_message_properties(self, message_properties: dict):
        if message_properties:
            for key, value in message_properties.items():
                if key in self._message_properties_mapping:
                    return_code = self._message_properties_mapping[key](value)  # call the respective property setter
                    if return_code != SOLCLIENT_OK:  # pragma: no cover # Due to core error scenarios
                        exception: PubSubPlusCoreClientError = \
                            get_last_error_info(return_code=return_code,
                                                caller_description='SolaceMessage->handle_message_properties')
                        logger.warning(str(exception))

    def set_persistent_dmq_eligible(self, dmqe):
        # Given a msg_p, set the Dead Message Queue (DMQ) eligible property on a message. When this
        #   option is set, messages that expire in the network, are saved on a appliance dead message
        #   queue. Otherwise expired messages are discarded.
        # Args:
        #     msg_p (): solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback
        #     dmqe ():0 - clear, 1 - set
        #
        # Returns:
        #    SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid

        return solace.CORE_LIB.solClient_msg_setDMQEligible(self._msg_p, ctypes.c_int(int(dmqe)))

    def set_ttl(self, ttl):
        #  Given a msg_p, set the Time To Live (TTL) for a message. Setting the Time To Live to
        #  zero disables TTL for the message   This property is only valid for Guaranteed messages
        #  (Persistent and Non-Persistent).
        #   It has no effect when used in conjunction with other message types unless the message
        #   is promoted by the appliance to a Guaranteed message..
        # Args:
        #     msg_p (): solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback
        #     ttl (int): 64-bit value in ms to use for message time to live.
        #
        # Returns:
        #    SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid
        return solace.CORE_LIB.solClient_msg_setTimeToLive(self._msg_p, ctypes.c_int64(ttl))

    def set_dmq_eligible(self, dmqe):
        # Given a msg_p, set the Dead Message Queue (DMQ) eligible property on a message. When this
        #   option is set, messages that expire in the network, are saved on a appliance dead message
        #   queue. Otherwise expired messages are discarded.
        # Args:
        #     dmqe ():0 - clear, 1 - set
        #
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if
        #                         msg_p is invalid

        return solace.CORE_LIB.solClient_msg_setDMQEligible(self._msg_p, ctypes.c_int(int(dmqe)))

    def set_eliding_eligible(self, elide):
        #  Given a msg_p, set the ElidingEligible property on a message. Setting this property
        #  to true indicates that this message should be eligible for eliding. Message eliding
        #  enables filtering of data to avoid transmitting every single update to a subscribing
        #  client. It can be used to overcome slow consumers or any situation where a slower
        #  message rate is desired.
        #
        #  Time-based eliding (supported in SolOS-TR) ensures that subscriber applications
        #  always receive only the most current update of a published topic at a rate that
        #  they can manage. By limiting the incoming message rate, a subscriber application
        #  is able to avoid a message backlog filled with outdated messages.
        #
        #  This property does not indicate whether the message was elided or even provide
        #  information about the subscriber's configuration (with regards to Message Eliding)
        # Args:
        #     elide :A Boolean that indicates whether to set or reset the Eliding Eligible
        #                   attribute
        #
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid.
        return solace.CORE_LIB.solClient_msg_setElidingEligible(self._msg_p, ctypes.c_int(int(elide)))

    def set_ack_immediately(self, val):
        #  Given a msg_p, set the optional ACK Immediately message property.
        #  When the ACK Immediately property is set to true on an outgoing Guaranteed Delivery message,
        #  it indicates that the appliance should ACK this message immediately upon receipt.
        #  By default the property is set to false on newly created messages.
        #
        #  This property, when set by a publisher, may or may not be removed by the appliance prior to delivery
        #  to a consumer, so message consumers must not expect the property value indicates how the message was
        #  originally published. Therefore if a received message
        #  is forwarded by the application, the ACK immediately property should be explicitly set to the desired
        #  value (true or false).
        #
        #  Setting this property on an outgoing direct message has no effect
        # Args:
        #     val (): A Boolean that indicates whether to set or clear the ACK Immediately message property.
        #
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg is invalid.

        return solace.CORE_LIB.solClient_msg_setAckImmediately(self._msg_p, ctypes.c_int(int(val)))

    def message_duplicate(self):
        #  Duplicate a message buffer and allocate a new msg which references all the
        #       same data. For any data blocks, the reference count is incremented to
        #       indicate that two message buffers have pointers to the data.
        #       Applications are responsible for releasing all message buffers they allocate by
        #       solClient_msg_dup()
        #
        # Args:
        #     msg_p:  A pointer to a Msg.
        #      new_msg_p:  A pointer to return a pointer to new msg.
        #   Returns:
        # SOLCLIENT_OK or SOLCLIENT_FAIL.
        new_msg_p = ctypes.c_void_p(None)
        return_code = solace.CORE_LIB.solClient_msg_dup(self._msg_p, byref(new_msg_p))
        if return_code == SOLCLIENT_OK:
            return _SolaceMessage(new_msg_p)
        if return_code == SOLCLIENT_NOT_FOUND:  # pragma: no cover # Due to core error scenarios
            return None
        exception: PubSubPlusCoreClientError = \
            get_last_error_info(return_code=return_code,
                                caller_description='SolaceMessage->message_duplicate',
                                exception_message=FAILED_TO_GET_DUPLICATE_MESSAGE)  # pragma: no cover
        # Due to core error scenarios
        logger.warning(str(exception))  # pragma: no cover # Due to core error scenarios
        raise exception  # pragma: no cover # Due to core error scenarios

    def message_set_destination(self, destination):
        #  Given a msg_p, set the Destination field (queue or topic).
        #   A destination can be removed from a message
        #   by setting the SolClient_destination_t structure to
        #   {SOLCLIENT_NULL_DESTINATION, NULL}
        # Args:
        #    msg_p        solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive
        #                  message callback.
        #     destination: A pointer to destination information.
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if
        #                         msg_p is invalid
        return solace.CORE_LIB.solClient_msg_setDestination(self._msg_p,
                                                            byref(destination), sizeof(destination))

    def set_message_expiration(self, timestamp_ms):
        #  Given a msg_p, set the expiration time field. The expiration time is the UTC time
        #   (that is, the number of milliseconds from midnight January 1, 1970 UTC) when the
        #   message is to expire. The expiration time is carried in the message when set to
        #   a non-zero value. Expiration time is not included when this value is set to zero.
        #
        #   The message expiration time is carried to clients that receive the message
        #   unmodified and does not effect the life cycle of the message. Use
        #   solClient_msg_setTimeToLive() to enforce message expiry in the network.
        #   In fact when solClient_msg_setTimeToLive() is used, setting this property has no effect.
        #   When solClient_msg_setTimeToLive() is called, the expiration time is never carried
        #   in the message, however it may be calculated and retrieved by the sender if the session property
        #   SOLCLIENT_SESSION_PROP_CALCULATE_MESSAGE_EXPIRATION is enabled. Thus if
        #   SolClient_msg_getExpiration() is called after the message is sent, a calculated
        #   expiration time is returned based on the time-to-live.
        #
        #   <b>Note:</b> When solClient_msg_setTimeToLive() is set on a message, the receiving
        #   client may also calculate the expiration time if it has enabled the session
        #   property SOLCLIENT_SESSION_PROP_CALCULATE_MESSAGE_EXPIRATION."""
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive
        #                  message callback.
        #    timestamp_ms:  The sender timestamp value to set. The value is in milliseconds.
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if
        #                         msg_p is invalid
        #
        return solace.CORE_LIB.solClient_msg_setExpiration(self._msg_p, c_int64(timestamp_ms))

    def set_message_priority(self, priority):
        # method to set the message priority
        # Args:
        #    msg_p : A pointer to the message
        #    priority:  Priority value. The valid value range is 0-255 with 0 as the lowest priority and
        #    255 as the highest, or -1 to delete priority.
        # Returns:
        # SOLCLIENT_OK or SOLCLIENT_FAIL
        #
        return solace.CORE_LIB.solClient_msg_setPriority(self._msg_p, c_int32(priority))

    def set_message_sequence_number(self, sequence_number):
        #  Given a msg_p, set the Sequence Number field.
        #   This overrides the SOLCLIENT_SESSION_PROP_GENERATE_SEQUENCE_NUMBER
        #   session property and forces the specified Sequence Number
        #   into the binary message header. This does <b>not</b> change the
        #   internal sequence numbering and the next generated sequence number will
        #   still be one more than the last generated sequence number.
        #
        #   A sequence number is automatically included (if not already present) in
        #   the Solace-defined fields for each message sent if the session property
        #   SOLCLIENT_SESSION_PROP_GENERATE_SEQUENCE_NUMBER is enabled.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive
        #                  message callback.
        #    sequence_number :  The 64-bit Sequence Number.
        #
        #  # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if
        #                         msg_p is invalid
        return solace.CORE_LIB.solClient_msg_setSequenceNumber(self._msg_p, c_uint64(sequence_number))

    def set_message_http_content_type(self, content_type):
        #  Given a msg_p, set or delete (if content_type == NULL) its HTTP Content Type
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive
        #                  message callback.
        #    content_type :  A pointer to a null terminated HTTP Content Type .
        # Returns:
        #    SOLCLIENT_OK or SOLCLIENT_FAIL
        return solace.CORE_LIB.solClient_msg_setHttpContentType(self._msg_p, ctypes.c_char_p(content_type.encode()))

    def set_message_http_content_encoding(self, content_encoding):
        #  Given a msg_p, set or delete (if content_encoding == NULL) its HTTP Content Encoding
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive
        #                  message callback.
        #    content_type :  A pointer to a null terminated HTTP Content Encoding .
        # Returns:
        #    SOLCLIENT_OK or SOLCLIENT_FAIL
        return solace.CORE_LIB.solClient_msg_setHttpContentEncoding(self._msg_p,
                                                                    ctypes.c_char_p(content_encoding.encode()))

    def message_create_user_property_map(self, map_p, size=0):
        #  Create a User Property map in the binary metadata header.
        #   The map is a multimap in which more than one value may be associated
        #   with a given field name. A call to SolClient_container_addXyz() does not
        #   overwrite an existing one, but adds a new one instead. To overwrite an existing
        #   field, the field has to been deleted and then added with a new value. To get all
        #   values associated with a given field name, a linear search is required.
        #   Any existing data is overwritten with the map that is created by subsequent
        #   primitive data functions.
        #   It returns an opaque container reference that must be used for subsequent
        #   add functions.
        #   The returned map should later be closed by a call to
        #   SolClient_container_closeMapStream(). However, if it is not, the stream
        #   is automatically closed when the associated message is freed through a call to
        #   SolClient_msg_free(). If the stream is closed automatically, the
        #   application may not continue to use the stream. Attempting to use a closed stream
        #   returns an invalid pointer error (SOLCLIENT_SUBCODE_PARAM_NULL_PTR)
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive
        #                  message callback.
        #    map_p :  A pointer location to receive the container pointer.
        #    size  :        A hint to the size (in bytes) of the map to be created. This
        #                        is used to determine what size of data block to allocate.
        #                        Datablocks are available in fixed sizes from
        #                        SOLCLIENT_GLOBAL_PROP_DBQUANTASIZE_0
        #                        to SOLCLIENT_GLOBAL_PROP_DBQUANTASIZE_4.
        #                        If it is too small for the subsequently created map, a
        #                        larger data block is allocated when necessary, and
        #                        existing structured data is copied into place. This
        #                        reallocation can negatively affect performance.
        # Returns:
        #    SOLCLIENT_OK or SOLCLIENT_FAIL
        return solace.CORE_LIB.solClient_msg_createUserPropertyMap(self._msg_p, ctypes.byref(map_p), size)

    def message_set_binary_attachment(self, msg, msg_length=None):
        #   Given a msg_p, set the contents of the binary attachment part by copying in from
        #   the given pointer and size. This causes memory to be allocated from
        #   API internal or heap storage. If any binary attachment previously existed it will
        #   be first removed before the new data is copied in.
        #
        #   Passing in a buf_p of NULL and a size of zero results in
        #   a binary attachment not being present in the message.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #     msg: A pointer to buffer.
        #     msg_length:  The maximum number of bytes in buffer.
        # Returns:
        #     SOLCLIENT_OK or SOLCLIENT_FAIL if msg_p is invalid  or memory not available.
        if msg_length is None:
            msg_length = len(msg)
        return solace.CORE_LIB.solClient_msg_setBinaryAttachment(self._msg_p, msg, c_uint32(msg_length))

    def message_get_binary_attachment_ptr(self, buf_ptr_p, binary_len):
        # Given a msg_p, retrieve the contents of a binary attachment part and
        #  return the pointer and length.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   buf_ptr_p :  A pointer to the application pointer to fill in with the
        #                         message data pointer on return. The programmer may cast
        #                         the returned void pointer to any reference suitable for
        #                         the application.
        #  size_p : A pointer to memory that contains data size on
        #                         return.
        # Returns:
        #  SOLCLIENT_OK or SOLCLIENT_FAIL or SOLCLIENT_NOT_FOUND

        return solace.CORE_LIB.solClient_msg_getBinaryAttachmentPtr(self._msg_p, ctypes.byref(buf_ptr_p),
                                                                    ctypes.byref(binary_len))

    def message_set_binary_attachment_string(self, buf_p):
        #  Given a msg_p, set the contents of the binary attachment part to a UTF-8 or ASCII string
        #   by copying in from the given pointer until null-terminated. The message
        #   will be TLV-encoded suitable for reading by any other Solace Corporation Messaging APIs.
        #   If any binary attachment previously existed it is first
        #   removed before the new data is copied in.
        #
        #   Passing in a buf_p of NULL results in
        #   a binary attachment not being present in the message.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #    buf_p:          A pointer to a buffer containing a UTF-8 or ASCII string.
        # Returns:
        #       SOLCLIENT_OK or SOLCLIENT_FAIL if msg_p is invalid
        #                         or memory is not available.
        return solace.CORE_LIB.solClient_msg_setBinaryAttachmentString(self._msg_p,
                                                                       buf_p.encode())

    def get_xml_ptr(self, buf_ptr_p, size_p):
        # Given a msg_p, retrieve the contents of a XML part of the message.
        #
        #  msg_p  :  solClient_opaqueMsg_pt that is returned from a previous call
        #                 to solClient_msg_alloc() or received in a receive
        #                 message callback.
        #  buf_ptr_p :      A pointer to the application pointer to fill in with the
        #                       message XML data pointer on return. The programmer may cast
        #                       the returned void pointer to any reference suitable for
        #                       the application.
        #  size_p :        A pointer to memory that contains data size on
        #                       return.
        # Returns:
        #      SOLCLIENT_OK or  SOLCLIENT_FAIL or SOLCLIENT_NOT_FOUND
        return solace.CORE_LIB.solClient_msg_getXmlPtr(self._msg_p, ctypes.byref(buf_ptr_p),
                                                       ctypes.byref(size_p))

    def set_message_application_message_id(self, application_message_id):
        # Given a msg_p, set the Application MessageID field.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #    application_message_id :        pointer to string containing messageId.
        # Returns:
        #       SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid.
        return solace.CORE_LIB.solClient_msg_setApplicationMessageId(self._msg_p,
                                                                     ctypes.c_char_p(application_message_id.encode()))

    def set_message_application_message_type(self, application_message_type):
        # Given a msg_p, set the MsgType field.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #    application_message_type:         A pointer to string with msgType.
        # Returns:
        #      SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg or length is invalid.
        return solace.CORE_LIB.solClient_msg_setApplicationMsgType(self._msg_p,
                                                                   ctypes.c_char_p(application_message_type.encode()))

    def delete_message_application_message_type(self):
        # Given a msg_p, delete the MsgType field.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        # Returns:
        #      SOLCLIENT_OK, SOLCLIENT_FAIL, SOLCLIENT_NOT_FOUND
        return solace.CORE_LIB.solClient_msg_deleteApplicationMsgType(self._msg_p)

    @staticmethod
    def get_payload_from_memory(buffer_size, buffer_p):
        payload = bytearray(buffer_size)
        char_array = ctypes.c_char * buffer_size
        ctypes.memmove(char_array.from_buffer(payload), buffer_p, buffer_size)
        return payload

    def delete_message_application_message_id(self):
        # Given a msg_p, delete the Application MessageId  field.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        # Returns:
        #      SOLCLIENT_OK, SOLCLIENT_FAIL, SOLCLIENT_NOT_FOUND
        return solace.CORE_LIB.solClient_msg_deleteApplicationMessageId(self._msg_p)

    @staticmethod
    def process_payload(str_return_code, str_buffer_p, str_buffer_size, xml_return_code,
                        xml_buffer_p, xml_buffer_size, is_str=False):
        #
        # first makes sure neither returnCode is FAIL
        for code in [str_return_code, xml_return_code]:
            if code == SOLCLIENT_FAIL:  # pragma: no cover # Due to core error scenario
                exception: PubSubPlusCoreClientError = \
                    get_last_error_info(return_code=code,
                                        caller_description='SolaceMessage->process_payload',
                                        exception_message='Unable to get payload for the message.')
                logger.warning(str(exception))
                # if there is no payload, then size is zero
                raise exception
        if str_return_code == xml_return_code == SOLCLIENT_OK:  # both shouldn't return data
            logger.warning("Internal Error str/bytearray return code:  %d and xml return code: %d ", str_return_code,
                           xml_return_code)
            raise PubSubPlusClientError("Message Decode Error: multiple payloads")
        elif str_return_code == xml_return_code == SOLCLIENT_NOT_FOUND:
            return None
        elif str_return_code == SOLCLIENT_OK:
            if not is_str:
                return _SolaceMessage.get_payload_from_memory(str_buffer_size.value, str_buffer_p.value)
            else:
                try:
                    payload_str = str_buffer_p.value.decode()
                    return payload_str
                except UnicodeDecodeError \
                        as exception:  # pylint: disable=broad-except  # pragma: no cover # Due to core error scenario
                    logger.info("get_binary_attachment_string returned invalid (non-utf-8) string: ignoring: %s"
                                , str(exception))
        else:
            return _SolaceMessage.get_payload_from_memory(xml_buffer_size.value, xml_buffer_p.value)

    def get_payload_details(self):
        buffer_p = ctypes.c_void_p(None)
        buffer_size = ctypes.c_uint32(0)
        return_code = self.message_get_binary_attachment_ptr(buffer_p, buffer_size)
        if return_code == SOLCLIENT_OK:
            return buffer_size.value, buffer_p.value
        if return_code == SOLCLIENT_NOT_FOUND:  # pragma: no cover # Due to core not found scenario
            return 0, None
        exception: PubSubPlusCoreClientError = \
            get_last_error_info(return_code=return_code,
                                caller_description='SolaceMessage->get_payload_details',
                                exception_message='Unable to get payload for the message.')  # pragma: no cover
        # Due to core error
        logger.warning(str(exception))
        # if there is no payload, then size is zero
        return 0, None

    def get_message_dump(self):
        # first determine how large the payload is, we need 3 byte of string for each
        # byte of payload.  Then add 1000 for the rest of the message headers.
        buffer_size, _ = self.get_payload_details()

        buffer = ctypes.create_string_buffer(DEFAULT_BUFFER_SIZE + buffer_size * DEFAULT_BUFFER_MULTIPLIER)
        return_code = solace.CORE_LIB.solClient_msg_dumpExt(self._msg_p, ctypes.byref(buffer),
                                                            DEFAULT_BUFFER_SIZE +
                                                            (DEFAULT_BUFFER_MULTIPLIER * buffer_size),
                                                            SOLCLIENT_MSGDUMP_FULL)
        if return_code == SOLCLIENT_OK:
            return buffer.value.decode()
        if return_code == SOLCLIENT_NOT_FOUND:  # pragma: no cover # Due to core not found scenario
            return None
        exception: PubSubPlusCoreClientError = \
            get_last_error_info(return_code=return_code,
                                caller_description='SolaceMessage->get_message_dump',
                                exception_message='Failed to retrieve the message dump')  # pragma: no cover
        logger.warning(str(exception))
        raise exception

    def get_message_expiration(self, timestamp_p):
        #  Given a msg_p, copy the Message Expiration timestamp into the given buffer. If
        #   message expiration time is not set in the message and the session property
        #   SOLCLIENT_SESSION_PROP_CALCULATE_MESSAGE_EXPIRATION is enabled, the expiration time
        #   is calculated based on the message Time To Live. When enabled, the expiration time
        #   for sent messages will be the UTC time when the message is sent plus the Time To Live. The
        #   expiration time for received messages is the UTC time when the message was received
        #   plus the Time To Live in the message at the time it was received.
        #
        #   If the expiration time is not set in the message, and it cannot be calculated, the
        #   timestamp is set to zero.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   timestamp_p :   A pointer to a 64-bit field to receive the value. The value is in milliseconds.
        #
        # Returns:             SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid.
        return solace.CORE_LIB.solClient_msg_getExpiration(self._msg_p, ctypes.byref(timestamp_p))

    def get_message_priority(self, priority_p: int):
        # Get message priority.
        # Args:
        #    msg_p :       A pointer to the message
        #   priority_p :   A pointer to memory that contains priority on return, or -1 if it is not set.
        # Returns:
        #    SOLCLIENT_OK or SOLCLIENT_FAIL
        return solace.CORE_LIB.solClient_msg_getPriority(self._msg_p, ctypes.byref(priority_p))

    def get_message_sequence_number(self, sequence_number):
        #  Given a msg_p, copy the Sequence Number into the given buffer.
        #   A sequence number is automatically included (if not already present) in
        #   the Solace-defined fields for each message sent if the session property
        #   SOLCLIENT_SESSION_PROP_GENERATE_SEQUENCE_NUMBER is enabled.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   sequence_number :    A pointer to 64-bit field to receive the value.
        #
        # Returns:
        #       SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid, SOLCLIENT_NOT_FOUND if not found.
        #
        return solace.CORE_LIB.solClient_msg_getSequenceNumber(self._msg_p, ctypes.byref(sequence_number))

    def get_destination(self, dest_p):
        #  Given a msg_p, get the Destination field (queue or topic), which is the
        #   destination this message was published to. On successful
        #   return dest_p->dest points to message memory and is only valid as
        #   long as msg_p is valid.
        # Args:
        #    msg_p : solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive  message callback.
        #   dest_p : A pointer to destination information.
        #   dest_size : The size of destination_t structure.
        # Returns:
        #    SOLCLIENT_OK, SOLCLIENT_FAIL, SOLCLIENT_NOT_FOUND
        return solace.CORE_LIB.solClient_msg_getDestination(self._msg_p, ctypes.byref(dest_p),
                                                            ctypes.sizeof(dest_p))

    def get_message_timestamp(self, timestamp_p):
        # Given a msg_p, copy the Receive Timestamp into the given buffer.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   timestamp_p :   A pointer to a 64-bit field to receive the value. The value is in milliseconds.
        # Returns:
        #   SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid, SOLCLIENT_NOT_FOUND if not found.
        return solace.CORE_LIB.solClient_msg_getRcvTimestamp(self._msg_p, ctypes.byref(timestamp_p))

    def get_message_sender_timestamp(self, timestamp_p):
        # Given a msg_p, copy the SenderTimestamp into the given buffer.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   timestamp_p :   A pointer to a 64-bit field to receive the value. The value is in milliseconds.
        # Returns:
        #  SOLCLIENT_OK on success, SOLCLIENT_FAIL if  msg_p is invalid, SOLCLIENT_NOT_FOUND for none found.
        return solace.CORE_LIB.solClient_msg_getSenderTimestamp(self._msg_p, ctypes.byref(timestamp_p))

    def get_message_http_content_type(self, type_p):
        # Method to get the http content type
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   type_p :   On return, it points to message memory containing HTTP Content Type.
        # Returns:
        # SOLCLIENT_OK on success, SOLCLIENT_NOT_FOUND if the field is  not present and SOLCLIENT_FAIL if
        # msg_p is invalid
        return solace.CORE_LIB.solClient_msg_getHttpContentType(self._msg_p, ctypes.byref(type_p))

    def get_message_http_content_encoding(self, encoding_p):
        #  Given a msg_p, retrieve the HTTP Encoding Type. On return type_p points to
        #   message memory and is only valid as long as msg_p is valid.
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   encoding_p :   On return, it points to message memory containing HTTP Encoding Type.
        # Returns:
        # SOLCLIENT_OK on success, SOLCLIENT_NOT_FOUND if the field is  not present and SOLCLIENT_FAIL if
        # msg_p is invalid
        return solace.CORE_LIB.solClient_msg_getHttpContentEncoding(self._msg_p, ctypes.byref(encoding_p))

    def message_get_user_property_map(self, map_p):
        #  Given a msg_p, retrieve the user property Map from binary metadata.
        #   The returned map is a multimap, in which more than one value may be associated
        #   with a given field name. A call to SolClient_container_addXyz() does not
        #   overwrite an existing one, instead it adds a new field. To overwrite an existing
        #   field, the field has to been deleted and then added with a new value. To get all
        #   values associated with a given field name, a linear search is required.
        #   The returned map should later be closed by a call to
        #   SolClient_container_closeMapStream(). However, if it is not, the map
        #   is automatically closed when the associated message is freed through a call to
        #   SolClient_msg_free(). If the map is closed automatically, the
        #   application cannot continue to use the map. Attempting to use a closed map
        #   returns an invalid pointer error (SOLCLIENT_SUBCODE_PARAM_NULL_PTR).
        # Args:
        #    msg_p :       solClient_opaqueMsg_pt that is returned from a previous call
        #                           to solClient_msg_alloc() or received in a receive
        #                          message callback.
        #   map_p :   A pointer to memory that contains a map pointer on return.
        # Returns:
        # SOLCLIENT_OK, SOLCLIENT_FAIL, or SOLCLIENT_NOT_FOUND
        return solace.CORE_LIB.solClient_msg_getUserPropertyMap(self._msg_p, ctypes.byref(map_p))

    def message_get_correlation_id(self, correlation_p):
        # Given a msg_p, copy the Correlation Id into the given buffer.
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #     correlation_p:  A pointer to string pointer to receive correlation
        #                         Id pointer.
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_NOT_FOUND if the field is
        #                         not present and SOLCLIENT_FAIL if  msg_p is invalid
        return solace.CORE_LIB.solClient_msg_getCorrelationId(self._msg_p, ctypes.byref(correlation_p))

    def message_set_correlation_id(self, correlation_id):
        #  Given a msg_p, set the Correlation Id field. The message Correlation Id
        #   is carried in the Solace message headers unmodified by the appliance and may
        #   be used for peer-to-peer message synchronization.
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #     correlation_p:  A pointer to string to copy into correlationId.
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if  msg_p is invalid.
        return solace.CORE_LIB.solClient_msg_setCorrelationId(self._msg_p, ctypes.c_char_p(correlation_id.encode()))

    def message_get_binary_attachment_string(self, buf_ptr_p):
        # Given a msg_p, retrieve the contents of a binary attachment part if it is
        #   a JMS string and return a pointer to the string (NULL-terminated string).
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #     buf_ptr_p: A pointer to memory that contains the string pointer on return.
        # Returns:
        #     SOLCLIENT_OK or SOLCLIENT_FAIL or SOLCLIENT_NOT_FOUND
        return solace.CORE_LIB.solClient_msg_getBinaryAttachmentString(self._msg_p, ctypes.byref(buf_ptr_p))

    def get_application_message_id(self, msg_id):
        # Given a msg_p, copy the Application MessageId pointer into the given buffer.
        # Args:
        #     msg_p: solClient_opaqueMsg_pt that is returned from a previous call
        #                  to solClient_msg_alloc() or received in a receive message callback.
        #     msg_id: A pointer to string pointer to receive MessageId pointer.
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid, SOLCLIENT_NOT_FOUND for none found
        return solace.CORE_LIB.solClient_msg_getApplicationMessageId(self._msg_p, ctypes.byref(msg_id))

    def get_application_msg_type(self, app_msg_type):
        # Given a msg_p, copy the msgType topic pointer into the given pointer.
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #     app_msg_type: A pointer to string pointer to receive msgType pointer.
        # Returns:
        #     SOLCLIENT_OK on success,  SOLCLIENT_FAIL if msg is invalid, SOLCLIENT_NOT_FOUND if it
        #     contains no msgType field.
        return solace.CORE_LIB.solClient_msg_getApplicationMsgType(self._msg_p, ctypes.byref(app_msg_type))

    def get_message_id(self, msg_id):
        # Given a msg_p, return the Guaranteed message Id.
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #     msg_id:  pointer to memory to store the returned msgId.
        # Returns:
        #     SOLCLIENT_OK on success, SOLCLIENT_FAIL if
        #                   msg_p is invalid, SOLCLIENT_NOT_FOUND if msg_p does not contain an
        #                   assured delivery message.
        return solace.CORE_LIB.solClient_msg_getMsgId(self._msg_p, ctypes.byref(msg_id))

    def has_discard_indication(self):
        #  Given a msg_p, test the discard indication status.
        #   Returns true if one or more messages have been discarded prior to the current
        #   message, otherwise it returns false.
        #   This indicates congestion discards only, and is not affected by message eliding.
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        # Returns:
        #    True, if the message had the discard indication set.
        return solace.CORE_LIB.solClient_msg_isDiscardIndication(self._msg_p)

    def get_delivery_mode(self):
        # Given a msg_p, return the delivery mode
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #    mode :  A place to store the returned delivery mode, one of
        #                        SOLCLIENT_DELIVERY_MODE_DIRECT
        #                        SOLCLIENT_DELIVERY_MODE_PERSISTENT
        #                        SOLCLIENT_DELIVERY_MODE_NONPERSISTENT
        # Returns:
        #   SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid.
        mode = ctypes.c_uint32()
        solace.CORE_LIB.solClient_msg_getDeliveryMode(self._msg_p, ctypes.byref(mode))
        return mode.value

    def set_delivery_mode(self, mode):
        # Given a msg_p, set the delivery mode
        # Args:
        #     msg_p:  solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback.
        #    mode :  The delivery mode to use for this message. It can be one of the following:
        #                        SOLCLIENT_DELIVERY_MODE_DIRECT
        #                        SOLCLIENT_DELIVERY_MODE_PERSISTENT
        #                        SOLCLIENT_DELIVERY_MODE_NONPERSISTENT
        # Returns:
        #   SOLCLIENT_OK on success, SOLCLIENT_FAIL if msg_p is invalid.
        return solace.CORE_LIB.solClient_msg_setDeliveryMode(self._msg_p, c_uint32(mode))
