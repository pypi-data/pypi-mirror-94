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


"""
This module abstracts message receiving behavior; it is a base class for all receivers.
"""
from abc import ABC, abstractmethod
from typing import Union

from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.utils.life_cycle_control import LifecycleControl, AsyncLifecycleControl


class MessageReceiver(LifecycleControl, AsyncLifecycleControl):
    """An abstract class that provides the message receiver implementation. """

    @abstractmethod
    def receive_async(self, message_handler: 'MessageHandler'):
        """
        Register an asynchronous message receiver on the
        :py:class:`solace.messaging.receiver.persistent_message_receiver.PersistentMessageReceiver` instance.

        Args:
            message_handler(MessageHandler): The object that receives all inbound messages (InboundMessage)
                in its onMessage() callback. If the provided value is None, then asynchronous receiver is removed &
                receive_message()
                (:py:class:`solace.messaging.receiver.persistent_message_receiver.PersistentMessageReceiver`) is used.
        """

    @abstractmethod
    def receive_message(self, timeout: int = None) -> Union[InboundMessage, None]:
        """
        Blocking request to receive the next message. You acknowledge the message using the
        :py:func:`solace.messaging.receiver.acknowledgement_support.AcknowledgementSupport.ack()` function
        for (:py:class:`solace.messaging.receiver.persistent_message_receiver.PersistentMessageReceiver`).

        This method is usually used in loop an its use is mutually exclusive when
        used asynchronously.

        Args:
            timeout(int): The time, in milliseconds, to wait for a message to arrive.

        Returns:
            InboundMessage: An object that represents an inbound message. Returns None on timeout, or upon
             service or receiver shutdown.

        Raises:
            PubSubPlusClientError: If error occurred while receiving or processing the message.
    """


class MessageHandler(ABC):
    """
    An abstract base class that defines the interface for a  message handler for inbound messages.
    """

    @abstractmethod
    def on_message(self, message: InboundMessage):
        """
        Definition for a message processing function.

        Args:
            message(InboundMessage): The inbound message.
        """
