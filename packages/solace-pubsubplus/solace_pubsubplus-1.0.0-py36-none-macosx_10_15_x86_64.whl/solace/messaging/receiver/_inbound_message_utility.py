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


# This module contains the class and functions which actually make the call to ccsmp
# this is an internal utility module, used by implementors of the API.

# pylint: disable=missing-function-docstring,missing-module-docstring,no-else-return

import ctypes
import logging
from ctypes import c_char_p, sizeof, byref

import solace
from solace.messaging.config._sol_constants import SOLCLIENT_OK, \
    SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM, SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM, SOLCLIENT_NOT_FOUND
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusCoreClientError
from solace.messaging.utils._solace_utilities import get_last_error_info

logger = logging.getLogger('solace.messaging.core.api')


class SolClientDestination(ctypes.Structure):  # pylint: disable=too-few-public-methods
    """ Conforms to solClient_destination_t """
    _fields_ = [
        ("dest_type", ctypes.c_int),
        ("dest", ctypes.c_char_p)
    ]


def topic_subscribe_with_dispatch(session_p, subscription, func_info_p):
    #   Adds a Topic subscription to a Session like SolClient_session_topicSubscribeExt(),
    #   but this function also allows a different message receive callback and dispatchUser_p to be specified.
    #   Specifying a NULL func_info_p or if func_info_p references a NULL  dispatchCallback_p and
    # a NULL dispatchUser_p makes this function
    #   act the same as SolClient_session_topicSubscribeExt(). Used in this manner, an application
    # can set the correlationTag, which appears in asynchronouus confirmations
    # (SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_OK). Setting correlationTag is not available when using
    #   SolClient_session_topicSubscribeExt().
    #
    #   Usually this API is used to provide a separate callback and user pointer for messages received
    # on the given topic.
    #   The Session property SOLCLIENT_SESSION_PROP_TOPIC_DISPATCH must be enabled for a non-NULL callback to be
    #   specified. When func_info_p is non-NULL and a dispatchCallback_p is specified, the callback
    # pointer and dispatchUser_p are stored
    #   in an internal callback table. func_info_p is <b>not</b> saved by the API.
    # Args:
    #     session_p: The opaque Session returned when Session was created.
    #     flags:  subscribeflags "Flags" to control the operation. Valid flags for this operation are:
    #     SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM
    #     SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
    #    SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY
    #     subscription:The Topic subscription string (a NULL-terminated UTF-8 string)
    #     func_info_p:   The message receive callback information. See
    #     struct SolClientReceiverCreateRxMsgDispatchFuncInfo

    #     correlation_tag :    A correlationTag pointer that is returned as is in the confirm or fail
    #     sessionEvent for the subscription. This is only used if SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM is set and
    #                             SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM is not set
    # Returns:
    #   SOLCLIENT_OK, SOLCLIENT_NOT_READY, SOLCLIENT_FAIL, SOLCLIENT_WOULD_BLOCK, SOLCLIENT_IN_PROGRESS
    #      A successful call has a return code of SOLCLIENT_OK, except when
    #     using SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM without
    #   SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM. In that case, the return code will
    # be SOLCLIENT_IN_PROGRESS because the call returns without
    #   waiting for the operation to complete.
    return solace.CORE_LIB.solClient_session_topicSubscribeWithDispatch(
        session_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
        c_char_p(subscription.encode()), byref(func_info_p), sizeof(func_info_p))


def topic_unsubscribe_with_dispatch(session_p, subscription, func_info_p):
    # Removes a Topic subscription from a Session like SolClient_session_topicUnsubscribeExt(),
    #   but this function also allows a message receive callback and dispatchUser_p to be specified.
    #   Specifying a NULL func_info_p or if func_info_p references a NULL  dispatchCallback_p
    # and a NULL dispatchUser_p makes this function
    #   act the same as SolClient_session_topicUnsubscribeExt(). Used in this manner,
    # an application can set the correlationTag which appears in asynchronouus confirmations
    # (SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK). Setting correlationTag is not available when using
    #   SolClient_session_topicUnsubscribeExt().
    #   Usually this API is used to provide a separate callback and user pointer for messages received
    # on the given topic.
    #   The Session property SOLCLIENT_SESSION_PROP_TOPIC_DISPATCH must be enabled for a non-NULL callback to be
    #   specified. When func_info_p is non-NULL and a dispatchCallback_p is specified, the callback
    # pointer and dispatchUser_p are removed
    #   from an internal callback table. func_info_p does not have to match the func_info_p used in
    # SolClient_session_topicSubscribeWithDispatch(). However,
    #   the contents referenced in func_info_p must match an entry found in the callback table.
    # Args:
    #     session_p: The opaque Session returned when Session was created.
    #     flags:  subscribeflags "Flags" to control the operation. Valid flags for this operation are:
    #     SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM
    #     SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
    #    SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY
    #     subscription:The Topic subscription string (a NULL-terminated UTF-8 string)
    #     func_info_p:  The message receive callback information. See
    #     struct SolClientReceiverCreateRxMsgDispatchFuncInfo.
    #     correlation_tag :    A correlationTag pointer that is returned as is in the confirm or fail
    #     sessionEvent for the subscription. This is only used if SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM is set and
    #                             SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM is not set
    # Returns:
    #  SOLCLIENT_OK, SOLCLIENT_NOT_READY, SOLCLIENT_FAIL, SOLCLIENT_WOULD_BLOCK, SOLCLIENT_IN_PROGRESS
    return solace.CORE_LIB.solClient_session_topicUnsubscribeWithDispatch(
        session_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM), c_char_p(subscription.encode()),
        byref(func_info_p), ctypes.sizeof(func_info_p))


def get_message_id(msg_p):
    #  Given a msg_p, return the Guaranteed message Id
    # Args:
    #   msg_p : message pointer that is returned from a previous call
    #                   to solClient_msg_alloc() or received in a receive
    #                   message callback.
    # Returns:
    #   SOLCLIENT_OK on success, SOLCLIENT_FAIL if
    #                   msg_p is invalid, SOLCLIENT_NOT_FOUND if msg_p does not contain an
    #                   assured delivery message.
    msg_id = ctypes.c_uint64()  # will be passed a pointer to memory to store the returned msg_id.
    return_code = solace.CORE_LIB.solClient_msg_getMsgId(msg_p, byref(msg_id))
    if return_code == SOLCLIENT_OK:
        return msg_id
    elif return_code == SOLCLIENT_NOT_FOUND:
        return None
    exception: PubSubPlusCoreClientError = get_last_error_info(return_code=return_code,
                                                               caller_description='_InboundMessage->get_message_id',
                                                               exception_message='Unable to get message id')
    logger.warning(str(exception))
    raise exception


def acknowledge_message(flow_p, msg_id):
    #   Sends an acknowledgment on the specified Flow. This instructs the API to consider
    #   the specified msg_id acknowledged at the application layer. The library
    #   does not send acknowledgments immediately. It stores the state for
    #      acknowledged messages internally and acknowledges messages, in bulk, when a
    #  threshold or timer is reached.
    #
    #  Applications must only acknowledge a message on the Flow on which
    #  it is received. Using the msg_id received on one Flow when acknowledging
    #  on another may result in no message being removed from the message-spool or the wrong
    #  message being removed from the message-spool.
    #
    #  The exact behavior of solClient_flow_sendAck() is controlled by Flow property
    #  SOLCLIENT_FLOW_PROP_ACKMODE:
    #  1. SOLCLIENT_FLOW_PROP_ACKMODE_AUTO - messages are acknowledged automatically by C API
    #  and calling this function has no effect.
    #  2.  SOLCLIENT_FLOW_PROP_ACKMODE_CLIENT - every message received must be acknowledged by the
    #  application through individual calls to solClient_flow_sendAck().
    #  WARNING: If SOLCLIENT_FLOW_PROP_ACKMODE is set to SOLCLIENT_FLOW_PROP_ACKMODE_AUTO
    #  (the default behavior), the function returns SOLCLIENT_OK, but with a warning that
    #  solClient_flow_sendAck is ignored as the flow is in auto-ack mode.
    # Args:
    #   flow_p : The opaque Flow that is returned when the Flow was created.
    #   msg_id  : The 64-bit messageId for the acknowledged message.
    # Returns:
    #   SOLCLIENT_OK, SOLCLIENT_FAIL
    return solace.CORE_LIB.solClient_flow_sendAck(flow_p, msg_id)


def pause(flow_p):
    # """"
    #  Closes the receiver on the specified Flow. This method will close the Flow
    #  window to the appliance so further messages will not be received until
    #  solClient_flow_start() is called. Messages in transit when this method is
    #  called will still be delivered to the application. So the application must
    #  expect that the receive message callback can be called even after calling
    #  solClient_flow_stop(). The maximum number of messages that may be
    #  in transit at any one time is controlled by SOLCLIENT_FLOW_PROP_WINDOWSIZE
    #  and SOLCLIENT_FLOW_PROP_MAX_UNACKED_MESSAGES (see solClient_flow_setMaxUnAcked()).
    #
    #  A Flow can be created with the window closed by setting the Flow property SOLCLIENT_FLOW_PROP_START_STATE
    #  to SOLCLIENT_PROP_DISABLE_VAL. When a Flow is created in this way, messages will not be received
    #  on the Flow until after SolClient_flow_start() is called.
    # Args:
    #     flow_p : The opaque Flow that is returned when the Flow was created.
    #
    # Returns:
    #   SOLCLIENT_OK, SOLCLIENT_FAIL
    return solace.CORE_LIB.solClient_flow_stop(flow_p)


def resume(flow_p):
    #     Opens the receiver on the specified Flow. This method opens the Flow window
    #     to the appliance so further messages can be received. For browser flows (SOLCLIENT_FLOW_PROP_BROWSER),
    #     applications have to call the function to get more messages.
    #
    #     A Flow may be created with the window closed by setting the Flow property SOLCLIENT_FLOW_PROP_START_STATE
    #     to SOLCLIENT_PROP_DISABLE_VAL. When a Flow is created in this way, messages will not be received
    #     on the Flow until after SolClient_flow_start() is called.
    # Args:
    #     flow_p : The opaque Flow that is returned when the Flow was created.
    #
    # Returns:
    #   SOLCLIENT_OK, SOLCLIENT_FAIL
    return solace.CORE_LIB.solClient_flow_start(flow_p)


def flow_topic_subscribe_with_dispatch(flow_p, subscription, func_info_p):
    # Allows topics to be dispatched to different message receive callbacks and with different
    #  dispatchUser_p for received messages on an endpoint Flow. If the endpoint supports adding topics
    #  (Queue endpoints), then this function will also add the Topic subscription to the endpoint unless
    #  SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY is set. SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY is
    #  implied for all other endpoints.
    #
    #  If the dispatch function info (func_info_p) is NULL, the Topic subscription is only added to the endpoint and
    #  no local dispatch entry is created. This operation is then i
    # dentical to solClient_session_endpointTopicSubscribe().
    #
    #  SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY can only be set when func_info_p
    #  is not NULL. Consequently func_info_p may not be NULL for non-Queue endpoints.
    #
    #  The Session property SOLCLIENT_SESSION_PROP_TOPIC_DISPATCH must be enabled for a non-NULL func_info_p
    #  to be specified.
    #
    #  When func_info_p is not NULL, the received messages on the Topic Endpoint Flow are further
    # demultiplexed based on the received
    #  topic.
    # Args:
    #     flow_p: The opaque Flow that is returned when the Flow was created.
    #     flags : "Flags" to control the operation. Valid flags for this operation are:
    #       SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM
    #       SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
    #       SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY
    #     subscription:  The Topic subscription string (a NULL-terminated UTF-8 string).
    #     func_info_p:  The message receive callback information. See structure SolClientFlowCreateRxCallbackFuncInfo
    #     correlation_tag : A correlationTag pointer that is returned in the confirm or fail sessionEvent for the
    #                      subscription. This is only used if SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
    # is set and SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM is not set.
    # Returns:
    #  SOLCLIENT_OK, SOLCLIENT_NOT_READY, SOLCLIENT_FAIL, SOLCLIENT_WOULD_BLOCK, SOLCLIENT_IN_PROGRESS
    return solace.CORE_LIB.solClient_flow_topicSubscribeWithDispatch(
        flow_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
        c_char_p(subscription.encode()), byref(func_info_p), sizeof(func_info_p))


def flow_topic_unsubscribe_with_dispatch(flow_p, subscription, func_info_p):
    # Removes a topic dispatch from an endpoint Flow. When the Flow is connected to a Queue endpoint,
    # this function also removes the Topic
    #  subscription from the Queue unless SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY is set
    # Args:
    #     flow_p: The opaque Flow returned when the Flow was create
    #     subscription: topic subscription
    #     func_info_p: The message receive callback information. See structure SolClientFlowCreateRxCallbackFuncInfo
    #     correlation_tag : A correlationTag pointer that is returned as is in the confirm or
    #                         fail sessionEvent for the subscription. This is only used if
    #                         SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM is set and
    #                         * SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM is not set.
    #     topic_subscription_p : The Topic subscription string (a NULL-terminated UTF-8 string).
    #      #     flags : "Flags" to control the operation. Valid flags for this operation are:
    #     #       SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM
    #     #       SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
    #     #       SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY
    # Returns:
    #    SOLCLIENT_OK, SOLCLIENT_NOT_READY, SOLCLIENT_FAIL, SOLCLIENT_WOULD_BLOCK, SOLCLIENT_IN_PROGRESS
    return solace.CORE_LIB.solClient_flow_topicUnsubscribeWithDispatch(
        flow_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
        c_char_p(subscription.encode()), byref(func_info_p), sizeof(func_info_p))


def end_point_provision(props, session_p):
    # Provision, on the appliance, a durable Queue or Topic Endpoint using the specified Session.
    #  SOLCLIENT_ENDPOINT_PROP_ID must be set to either SOLCLIENT_ENDPOINT_PROP_QUEUE or
    # SOLCLIENT_ENDPOINT_PROP_TE
    #  in this interface. Only durable (SOLCLIENT_ENDPOINT_PROP_DURABLE is enabled) endpoints
    # may be provisioned. A non-durable
    #  endpoint is created when a Flow is bound to it with solClient_session_createFlow().
    #  Endpoint creation can be carried out in a blocking or non-blocking mode, depending upon the provisionflag.
    #  If SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM is set in provisionFlags,
    #  the calling thread is blocked until the endpoint creation attempt either
    #  succeeds or is determined to have failed. If the endpoint is created, SOLCLIENT_OK is
    #  returned.
    #  When SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM is not set, SOLCLIENT_IN_PROGRESS is returned when the endpoint
    #  provision request is successfully sent, and the creation attempt proceeds in the background.
    #  An endpoint creation timer, controlled by the property
    #  SOLCLIENT_SESSION_PROP_PROVISION_TIMEOUT_MS, controls the maximum amount of
    #  time a creation attempt lasts for. Upon expiry of this time,
    #  a SOLCLIENT_SESSION_EVENT_PROVISION_ERROR event is issued for the Session.
    #     * If there is an error when solClient_session_endpointProvision() is invoked, then SOLCLIENT_FAIL
    #  is returned, and a provision event will not be subsequently issued. Thus, the caller must
    #  check for a return code of SOLCLIENT_FAIL if it has logic that depends upon a subsequent
    #  provision event to be issued.
    #  For a non-blocking endpoint provision, if the creation attempt eventually
    #  fails, the error information that indicates the reason for the failure cannot be
    #  determined by the calling thread, rather it must be discovered through the Session event
    #  callback (and solClient_getLastErrorInfo() can be called in the Session event callback
    #                                                                                 * to get further information).
    #  For a blocking endpoint creation invocation, if the creation attempt does not
    #  return SOLCLIENT_OK, then the calling thread can determine the failure reason by immediately
    #  calling solClient_getLastErrorInfo. For a blocking endpoint creation, SOLCLIENT_NOT_READY is returned
    #  if the create failed due to the timeout expiring
    # Args:
    #  props : The provision  endpointProps "properties" used to define the endpoint.
    #  session_p : The Session which is used to create the endpoint.
    # provision_flags : "Flags" to control provision operation.
    # correlation_tag : # A correlation tag returned in the resulting Session event.
    # queue_network_name : This parameter is deprecated but still supported for backwards compatibility.
    #                          It is recommended to pass NULL for this parameter.  When a non-null pointer is passed,
    #                          it is used as a pointer to the location in which the network name of the created Queue
    #                          Network Name is returned. This can be used to set the destination for published
    #                              messages. An empty string is returned when the created endpoint is a Topic Endpoint.
    #                          For publishing to a queue, the current recommended practice is to use
    #                          solClient_destination_t where the destType is set to SOLCLIENT_QUEUE_DESTINATION and
    #                          dest is set to the queue name.
    #  qnn_size : As with queue_network_name, this is a deprecated paramter.  When passing NULL as the
    #                          queue_network_name, pass 0 as qnn_size.  When queue_network_name is not null,
    # qnn_size is the maximum length of the Queue Network Name string that can be returned.
    #
    # Returns:
    #  SOLCLIENT_OK, SOLCLIENT_FAIL, SOLCLIENT_NOT_READY, SOLCLIENT_IN_PROGRESS, SOLCLIENT_WOULD_BLOCK
    #

    return solace.CORE_LIB.solClient_session_endpointProvision(ctypes.cast(props, ctypes.POINTER(c_char_p)),
                                                               session_p,
                                                               ctypes.c_int(SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM),
                                                               ctypes.c_char_p(None), c_char_p(),
                                                               ctypes.c_int(0))


def topic_endpoint_subscribe(props, session_p, subscription):
    #     """/**
    #  * Add a Topic subscription to the endpoint defined by the endpoint properties if the operation is supported
    #  * on the endpoint. Topic subscriptionscan be added to Queue endpoints (::SOLCLIENT_ENDPOINT_PROP_QUEUE) and
    #  * to the special endpoint for each Session on appliances running SolOS-TR(::SOLCLIENT_ENDPOINT_PROP_CLIENT_NAME).
    #  *
    #  * <b>Adding subscriptions to Queues</b>
    #  *
    #  * Guaranteed messages are published to a Queue when it is set as the destination of the message. However,
    #  * you can also add one or more Topic subscriptions to a durable or temporary Queue so that
    #  * Guaranteed messages published to those topics are also delivered to the Queue.
    #  * @li Only a Queue (::SOLCLIENT_ENDPOINT_PROP_QUEUE) Endpoint can be used.
    #  * @li Only a Topic subscription can be used.
    #  * @li Must have modify-topic permission on the Endpoint.
    #  *
    #  * <b>Adding subscriptions to remote clients</b>
    #  *
    #  * A subscription manager client can add subscriptions on behalf of other clients. These Topic
    #  * subscriptions are not retained in the subscription cache and are not be reapplied upon reconnection.
    #  * @li Only supported in SolOS-TR mode.
    #  * @li Only a ClientName (::SOLCLIENT_ENDPOINT_PROP_CLIENT_NAME) Endpoint can be used.
    #  * @li Only a Topic subscription can be used.
    #  * @li Must have subscription-manager permissions on the client username.
    #  *
    #  * It is an error to add subscriptions to a Topic Endpoint (::SOLCLIENT_ENDPOINT_PROP_TE)  with this interface.
    #  * A subscription can only be added to a Topic Endpoint when a Flow is bound to it.
    #  The subscription is part of the Flow properties.
    # * @param endpointProps   The \ref endpointProps "provision properties" used to identify the endpoint.
    # * @param opaqueSession_p The Session which is used to perform the subscription request.
    #                           If the Session also supports ::SOLCLIENT_SESSION_PROP_REAPPLY_SUBSCRIPTIONS,
    #                           then the subscriptions are be remembered and automatically reapplied should
    #                           the Session fail and reconnect automatically.
    # * @param flags           \ref subscribeflags "Flags" to control the operation. Valid flags for this operation are:
    # * @li ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM
    # * @li ::SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
    # * @param topicSubscription_p Topic Subscription to apply as a NULL-terminated UTF-8 string.
    # * @param correlationTag  Correlation tag returned in the resulting Session event.
    # * @return ::SOLCLIENT_OK, ::SOLCLIENT_FAIL, ::SOLCLIENT_NOT_READY, ::SOLCLIENT_IN_PROGRESS
    # * @subcodes
    # * @li ::SOLCLIENT_SUBCODE_TIMEOUT - The operation timed out trying to provision
    #                   (only for blocking provision operations; refer to ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM).
    # * @li ::SOLCLIENT_SUBCODE_COMMUNICATION_ERROR - The underlying connection failed.
    # * @li ::SOLCLIENT_SUBCODE_UNKNOWN_QUEUE_NAME
    # * @li ::SOLCLIENT_SUBCODE_UNKNOWN_CLIENT_NAME
    # * @li ::SOLCLIENT_SUBCODE_SUBSCRIPTION_ACL_DENIED
    # * @see ::solClient_subCode for a description of all subcodes."""
    return solace.CORE_LIB.solClient_session_endpointTopicSubscribe(ctypes.cast(props, ctypes.POINTER(c_char_p)),
                                                                    session_p,
                                                                    ctypes.c_int(
                                                                        SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
                                                                    c_char_p(subscription.encode()),
                                                                    ctypes.c_char_p(None))


def topic_endpoint_unsubscribe(props, session_p, subscription):
    """
    Remove a Topic subscription from the endpoint defined by the endpoint properties if the operation is supported
    on the endpoint. Used to remove subscriptions added by solClient_session_endpointTopicSubscribe() .
    Refer to that function's documentation for operational parameters. This method cannot remove subscriptions added
    through the CLI.

    Args:
        @param endpointProps   The \ref endpointProps "provision properties" used to identify the endpoint.
        @param opaqueSession_p The Session which is used to perform the remove subscription request.
        @param flags           \ref subscribeflags "Flags" to control the operation. Valid flags for this operation are:
        @li ::SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM
        @li ::SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM
        @param topicSubscription_p Topic Subscription to remove as a NULL-terminated UTF-8 string.
        @param correlationTag  Correlation tag returned in the resulting Session event.

    Returns:
        @return ::SOLCLIENT_OK, ::SOLCLIENT_FAIL, ::SOLCLIENT_NOT_READY, ::SOLCLIENT_IN_PROGRESS
        @subcodes
        @li ::SOLCLIENT_SUBCODE_TIMEOUT - The operation timed out trying to provision
        (only for blocking provision operations; refer to ::SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM).
        @li ::SOLCLIENT_SUBCODE_COMMUNICATION_ERROR - The underlying connection failed.
        @li ::SOLCLIENT_SUBCODE_UNKNOWN_QUEUE_NAME
        @li ::SOLCLIENT_SUBCODE_UNKNOWN_CLIENT_NAME
        @see ::solClient_subCode for a description of all subcodes.
    """
    return solace.CORE_LIB.solClient_session_endpointTopicUnsubscribe(ctypes.cast(props, ctypes.POINTER(c_char_p)),
                                                                      session_p,
                                                                      ctypes.c_int(
                                                                          SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
                                                                      c_char_p(subscription.encode()),
                                                                      ctypes.c_char_p(None))


def flow_destination(flow_p, dest_p):
    #    """
    #    /**
    # * Retrieve the destination for the Flow. The destination returned can
    # * be used to set the ReplyTo field in a message, or otherwise communicated
    # * to partners that need to send messages to this Flow. This is especially useful
    # * for temporary endpoints (Queues and Topic Endpoints), as the destination
    # * is unknown before the endpoint is created.
    # * @param opaqueFlow_p The opaque Flow returned when the Flow was created.
    # * @param dest_p       A pointer to a solClient_destination_t.
    # * @param destSize     The size of (solClient_destination_t).
    #       This parameter is used for backwards binary compatibility if solClient_destination_t changes in the future.
    # * @return ::SOLCLIENT_OK, ::SOLCLIENT_FAIL
    # * @subcodes
    # * @see ::solClient_subCode for a description of all subcodes.
    # */
    #    """
    return solace.CORE_LIB.solClient_flow_getDestination(flow_p, ctypes.byref(dest_p),
                                                         ctypes.sizeof(dest_p))
