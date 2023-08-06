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


# module contains the class and functions which actually make the call to ccsmp #pylint:disable=missing-module-docstring
# this is an internal utility module, used by implementors of the API. #pylint:disable=missing-function-docstring
import ctypes
from ctypes import byref

import solace


def get_transmitted_statistics(session_p, tx_stats_p):
    # Returns an array of Session transmit statistics.
    #   If the array is smaller than the number of defined transmit statistics, only the first N
    #   defined statistics are returned.
    #   If the array is larger than the number of defined transmit statistics, only the defined
    #   entries are filled in. The other entries are not touched
    # Args:
    #     session_p: An opaque Session returned when the Session was created.
    #     tx_stats_p: A pointer to an array of statistic values
    #    array_size : The number of entries in the array passed in (NOT the number of bytes).
    # Returns:
    #    SOLCLIENT_OK, SOLCLIENT_FAIL
    return solace.CORE_LIB.solClient_session_getTxStats(session_p, tx_stats_p, ctypes.c_uint32(len(tx_stats_p)))


def get_received_statistics(session_p, rx_stats_p):
    # Returns an array of Session receive statistics.
    #   If the array is smaller than the number of defined receive statistics, only the first N
    #   defined statistics are returned.
    #   If the array is larger than the number of defined receive statistics, only the defined
    #   entries are filled in. The other entries are not touched.
    # Args:
    #     session_p: An opaque Session returned when the Session was created.
    #     rx_stats_p: A pointer to an array of statistic values
    #    array_size : The number of entries in the array passed in (NOT the number of bytes).
    # Returns:
    #    SOLCLIENT_OK, SOLCLIENT_FAIL
    return solace.CORE_LIB.solClient_session_getRxStats(session_p, rx_stats_p, ctypes.c_uint32(len(rx_stats_p)))


def get_transmitted_statistic(session_p, tx_stat_type):
    # Returns an individual transmit statistic.
    #   If multiple transmit statistics are needed, it is more efficient to use
    #   solClient_session_getTxStats rather than to call this routine multiple times for
    #   different statistics.
    #     Args:
    #         session_p: An opaque Session returned when Session was created.
    #         tx_stat_type: The type of transmit statistic to return.
    # Returns:
    #    SOLCLIENT_OK, SOLCLIENT_FAIL
    tx_stat_p = ctypes.c_uint64()  # A pointer to a variable to hold the returned statistic.
    solace.CORE_LIB.solClient_session_getTxStat(session_p, tx_stat_type, byref(tx_stat_p))
    return tx_stat_p.value


def get_received_statistic(session_p, rx_stat_type):
    # Returns an individual receive statistic.
    #   If multiple receive statistics are needed, it is more efficient to use
    #   solClient_session_getRxStats rather than to call this routine multiple times for
    #   different statistics.
    #     Args:
    #         session_p: An opaque Session returned when Session was created.
    #         rx_stat_type: TThe type of receive statistic to return.
    # Returns:
    #    SOLCLIENT_OK, SOLCLIENT_FAIL
    rx_stat_p = ctypes.c_uint64()  # A pointer to a variable to hold the returned statistic.
    solace.CORE_LIB.solClient_session_getRxStat(session_p, rx_stat_type, byref(rx_stat_p))
    return rx_stat_p.value


def reset_statistics(session_p):
    # Clears all of the receive and transmit statistics for the specified Session. All previous
    #   Session statistics are lost when this is called.
    # Args:
    #   session_p: An opaque Session returned when Session was created.
    # Returns:
    #    SOLCLIENT_OK, SOLCLIENT_FAIL
    return solace.CORE_LIB.solClient_session_clearStats(session_p)
