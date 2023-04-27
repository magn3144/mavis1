# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Using the robot agent type differs from previous agent types.
  - Firstly, install additional package 'msgpack'.
    Use pip for installation, like this: 
        'python -m pip install numpy msgpack'. 
    Exact steps may vary based on your platform and Python 
    installation. 
  - Secondly, you don't need the Java server for the robot. So, the command
    to start the search client in the terminal is different, for example:
        'python searchclient/searchclient.py -robot -ip 192.168.0.102 -level levels/SAsoko1_04.lvl'
    runs the searchclient with the 'robot' agent type on the robot at IP 192.168.0.102. See a
    list of robot IPs at the github page for the course.
  - To connect to the robots, connect to the Pepper hotspot. To reduce
    the load on the hotspot, please disconnect between your sessions.
    
  - A good starting point is using something similar to the 'classic' agent type and then
    replacing it with calls to the 'robot' interface.
"""
from utils import *
from robot_interface import *
from domains.hospital.actions import ROBOT_ACTION_LIBRARY
from search_algorithms.graph_search import graph_search
import time


def robot_agent_type(level, initial_state, action_library, goal_description, frontier, robot_ip):
    print(robot_ip)
    robot = RobotClient(robot_ip)
    robot.stand()
    time.sleep(3)
    robot.say("I am listening now")
    time.sleep(1)


    #### Very experimental implementation of whisper
    action = "Move(N)"
    robot.listen(4, playback=True)
    time.sleep(4)
    robot.say("Hi")
    time.sleep(3)
    print(cmd_input)
    if cmd_input=="move left":
        action = "Move(W)"
    elif cmd_input=="move right":
        action = "Move(E)"

    angle = robot.direction_mapping[action] / 360 * 2 * math.pi
    robot.declare_direction(action)
    time.sleep(3)
    robot.forward(distance=0.5, block=False)
    time.sleep(3)
    robot.turn(angle, block=False)
    time.sleep(3)
    robot.forward(distance=0.5, block=False)
    time.sleep(3)

    robot.say("Im done moving")
    time.sleep(3)

    # close the connection
    robot.close()