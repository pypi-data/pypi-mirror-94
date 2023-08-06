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
This module contains the abstract classes used to define the ``MessagePublisher`` and ``MessageReceiver`` life cycle.

An object in the PubSub+ API for Python that contains these interfaces may be:

- started

- terminated

- ``MessagePublisher`` and ``MessageReceiver`` state
"""
import concurrent
from abc import ABC, abstractmethod

from solace.messaging.config._solace_message_constants import GRACE_PERIOD_DEFAULT_MS


class LifecycleControl(ABC):
    """ A class that abstracts the control service lifecycle operations such as start and terminate."""

    @abstractmethod
    def start(self):
        """
        Enables service regular duties. Before this method is called, service is considered off duty.
        In order to operate normally this method needs to be called on a service instance. If the service
        is already started, or starting, this operation has no effect.

        Raises:
            PubSubPlusClientError: When service start failed for some internal reason.
            IllegalStateError: If method has been invoked at an illegal or inappropriate time for some another reason.
        """

    @abstractmethod
    def terminate(self, grace_period: int = GRACE_PERIOD_DEFAULT_MS):
        """
        Disables regular duties of a service. If this service is already terminated or terminating, this
        operation has no effect.  All attempts to use a service after termination is requested will be
        refused with an exception.

        Args:
            grace_period(int): The positive integer grace period to use. The default is 600000ms.

        Raises:
            PubSubPlusClientError: When service termination failed for some internal reason.
            IllegalStateError: If method has been invoked at an illegal or inappropriate time for some another reason.
            IllegalArgumentError: If the grace_period is invalid.
        """

    @abstractmethod
    def is_running(self) -> bool:
        """
        Checks if the process was successfully started and not stopped yet.

        Returns:
            bool: False if process was not started or already stopped, True otherwise.
        """

    @abstractmethod
    def is_terminated(self) -> bool:
        """
        Checks if message delivery process is terminated.

        Returns:
            bool: True if message delivery process is terminated, False otherwise.
        """

    @abstractmethod
    def is_terminating(self) -> bool:
        """
        Checks if message delivery process termination is on-going.

        Returns:
            bool: True if message delivery process being terminated, but termination is not finished, False otherwise.
        """


class AsyncLifecycleControl(ABC):
    """
    A class that abstracts asynchronous control service lifecycle operations such as start_async
    and terminate_async.
    """

    @abstractmethod
    def start_async(self) -> concurrent.futures.Future:
        """
        Enables service regular duties. Before this method is called, service is considered off duty.
        In order to operate normally, this method needs to be called on a service instance. If the service
        is already started, or starting, this operation has no effect.

        Returns:
            concurrent.futures.Future:  An object that the application can use to determine when
            the service start has completed.
        
        Raises:
            IllegalStateError: If method has been invoked at an illegal or inappropriate time for some another reason.

        """

    @abstractmethod
    def terminate_async(self, grace_period: int = GRACE_PERIOD_DEFAULT_MS) -> concurrent.futures.Future:
        """
        Disables regular duties of a service. If this service is already terminated or terminating, this
        operation has no effect. All attempts to use a service after termination is requested will be
        refused with an exception.

        Args:
            grace_period(int): The positive integer grace period to use. The default is 600000ms.

        Returns:
            concurrent.futures.Future: An future object which the application can use to determine terminate completion.

        Raises:
            IllegalArgumentError: If the grace_period is invalid.
        """
