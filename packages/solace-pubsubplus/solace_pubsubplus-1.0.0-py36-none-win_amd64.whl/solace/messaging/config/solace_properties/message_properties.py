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

""" This module contains ``Message`` properties."""

# pylint: disable=trailing-whitespace, pointless-string-statement

APPLICATION_MESSAGE_TYPE = "solace.messaging.message.application-message-type"
""" Property-key to specify application message type. This value is used by applications only,
 and is passed through the API untouched. 
 This can be set using
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_application_message_type()`."""

ELIDING_ELIGIBLE = "solace.messaging.message.eliding-eligible"
"""Property-key to specify whether the message is eligible for eliding."""

PRIORITY = "solace.messaging.message.priority"
"""Property-key to specify optional message priority.
 The valid priority value range is 0-255 (0 is the lowest priority and 255 is the
 highest priority). A value of -1 indicates the priority is not set and a default priority value is used instead.
 This can be set using
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_priority()`."""

HTTP_CONTENT_TYPE = "solace.messaging.message.http-content"
"""Property-key to specify HTTP content type header value for interaction with an HTTP client 
 The accepted values are defined in RFC 7231, section-3.1.2.2.
 This can be set using 
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_http_content_header()`."""

HTTP_CONTENT_ENCODING = "solace.messaging.message.http-encoding"
"""Property-key to specify HTTP content-type encoding value for interaction with an HTTP client.
 The accepted values are defined in RFC 2616, section-14.11l.
 This can be set using
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_http_content_header()`.
"""

CORRELATION_ID = "solace.messaging.message.correlationId"
"""Property-key to specify correlation ID. The correlation ID is used for correlating a request
to a reply and should be as random as possible.
This variable is being also used for the Request-Reply API, this is why it is suggested
not to use this property on a message builder instance but only on a publisher interface
where available."""

PERSISTENT_TIME_TO_LIVE = "solace.messaging.message.persistent.time-to-live"
"""Property-key to specify number of milliseconds before the message is discarded or moved to a
Dead Message Queue.
The value of 0 means the message never expires. The default value is 0.
This property is only valid for persistent messages."""

PERSISTENT_EXPIRATION = "solace.messaging.message.persistent.expiration"
"""Property-key to specify The UTC time (Epoch time in milliseconds)
 when the message is supposed to expire. Setting this property has no effect if the TimeToLive 
 is set in the same message. It is carried to clients that receive the message, unmodified and 
 does not effect the life cycle of the message.This property is only valid for persistent messages.
 This can be set using 
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_expiration()`."""

PERSISTENT_DMQ_ELIGIBLE = "solace.messaging.message.persistent.dmq-eligible"
"""Property-key to specify if message is eligible to be moved to a Dead Message Queue.
 The default value is ``True``.
 This property is only valid for persistent messages."""

PERSISTENT_ACK_IMMEDIATELY = "solace.messaging.message.persistent.ack-immediately"
"""Property-key to specify if broker should ACK this message immediately upon receipt.
 The default value is ``False``.
 This property is only valid for persistent messages."""

SEQUENCE_NUMBER = "solace.messaging.message.sequence-number"
"""Property-key to specify the message sequence number. If not set no sequence number is set on the message.
 The default value is not set.
 This can be set using
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_sequence_number()`."""

APPLICATION_MESSAGE_ID = "solace.messaging.message.application-message-id"
"""Property-key to specify the message application id. If not set no application message id is set on the message.
 The default value is not set.
 This can be set using
 :py:meth:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_application_message_id()`."""
