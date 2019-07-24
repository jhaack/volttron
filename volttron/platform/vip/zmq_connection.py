# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2017, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}


import zmq
import gevent
import logging
import green as vip

from volttron.platform.vip.rmq_connection import BaseConnection
from volttron.platform.vip.socket import Message


class ZMQConnection(BaseConnection):
    """
    Maintains ZMQ socket connection
    """
    def __init__(self, url, identity, instance_name, context):
        super(ZMQConnection, self).__init__(url, instance_name, identity)

        self.socket = None
        self.context = context
        self._logger = logging.getLogger(__name__)
        self._logger.debug("ZMQ connection {}".format(identity))

    def open_connection(self, type):
        if type == zmq.DEALER:
            self.socket = vip.Socket(self.context)
            if self._identity:
                self.socket.identity = self._identity
        else:
            self.socket = zmq.Socket()

    def set_properties(self,flags):
        hwm = flags.get('hwm', 6000)
        self.socket.set_hwm(hwm)
        reconnect_interval = flags.get('reconnect_interval', None)
        if reconnect_interval:
            self.socket.setsockopt(zmq.RECONNECT_IVL, reconnect_interval)

    def connect(self, callback=None):
        self.socket.connect(self._url)
        if callback:
            callback(True)

    def bind(self):
        pass

    def register(self, handler):
        self._vip_handler = handler

    def send_vip_object(self, message):
        self.socket.send_vip_object(message)

    def recv_vip_object(self):
        return self.socket.recv_vip_object()

    def disconnect(self):
        self.socket.disconnect(self._url)

    def close_connection(self, linger=1):
        """This method closes ZeroMQ socket"""
        self.socket.close(linger)

