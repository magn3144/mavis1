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
# from goal_recognition import goal_recognition_agent_type
import time


def robot_agent_type(level, initial_state, action_library, goal_description, frontier, robot_ip):
  rb = robot_controller(robot_ip, initial_state, action_library, goal_description, frontier)

  numberOfGoals = len(goal_description.goals)
  if numberOfGoals > 1:
    rb.say("There are {} goals, which goal should I persue first.".format(numberOfGoals))
    goalNotRecognized = True
    goalIndex = None
    while goalNotRecognized:
      goal = rb.listen()
      goalNotRecognized = False
      if goal == "one":
        goalIndex = 0
      elif goal == "two":
        goalIndex = 1
      elif goal == "three":
        goalIndex = 2
      elif goal == "four":
        goalIndex = 3
      else:
        goalNotRecognized = True
        rb.say("I did not hear that can you say it again?")
    if goalIndex is not None:
      subGoal = goal_description.get_sub_goal(goalIndex)
      solvable, plan = graph_search(initial_state, [action_library], subGoal, frontier)
      if not solvable:
        rb.say("The level you have given me is not solvable.")
        return
      rb.say("I found a solution.")

      rb.execute_plan(plan)

      rb.say("The plan is executed.")


  '''
  solvable, plan = graph_search(initial_state, [action_library], goal_description, frontier)
  if not solvable:
    rb.say("The level you have given me is not solvable.")
    return
  rb.say("I found a solution.")

  rb.execute_plan(plan)

  rb.say("The plan is executed.")
  '''

  # close the connection
  rb.shutdown()