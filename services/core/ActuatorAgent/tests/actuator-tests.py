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

import unittest
import subprocess
import time
from datetime import datetime, timedelta
import volttron.platform.messaging.topics
from volttron.platform.agent import utils, matching
from volttron.platform.agent import PublishMixin, BaseAgent
from volttron.tests import base
 
"""
Test 
"""
 
AGENT_DIR = "Agents/ActuatorAgent"
CONFIG_FILE = "Agents/ActuatorAgent/actuator-deploy.service"

class ActuatorTests(base.BasePlatformTest):

    def setUp(self):
        super(ActuatorTests, self).setUp()
        self.startup_platform("base-platform-test.json")
        
    def tearDown(self):
        super(ActuatorTests, self).tearDown()
    
#     def test_direct_build_and_install(self):
#         self.direct_buid_install_agent(AGENT_DIR)
# 
#     def test_direct_install_and_start(self):
#         self.direct_build_install_run_agent(AGENT_DIR)

    def test_direct_install_and_start(self):
        self.direct_build_install_run_agent(AGENT_DIR, CONFIG_FILE)

         
#     def test_schedule(self):
#         print "test something"
# #         self.publish_schedule()
         
    def publish_schedule(self):
     
        headers = {
                    'AgentID': self._agent_id,
                    'type': 'NEW_SCHEDULE',
                    'requesterID': self._agent_id, #The name of the requesting agent.
                    'taskID': self._agent_id + "-TASK", #The desired task ID for this task. It must be unique among all other scheduled tasks.
                    'priority': 'LOW', #The desired task priority, must be 'HIGH', 'LOW', or 'LOW_PREEMPT'
                } 
         
        now = datetime.now()
        start =  now.strftime("%Y-%m-%d %H:%M:00")
        end = (now + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:00")
        msg = [
                ["campus/building/device1", #First time slot.
                 start,     #Start of time slot.
                 end],     #End of time slot.
                #etc...
            ]
         
        self.subagent.subscribe(self, prefix='',callback=self.on_match)
        self.publish_json(topics.ACTUATOR_SCHEDULE_REQUEST, headers, msg)
        time.sleep(20)
         
    def on_match(self, topic, headers, message, match):
        print "**********************************Match"
  
