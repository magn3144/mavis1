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






from utils import *
from robot_interface import *
from domains.hospital.actions import ROBOT_ACTION_LIBRARY
from search_algorithms.graph_search import graph_search
import time

def robot_agent_type(level, initial_state, action_library, goal_description, frontier, robot_ip):
  rb = robot_controller(robot_ip, initial_state, action_library, goal_description, frontier)

  # Keep running until the program is manually stopped.
  while True:

    # Ask the human for the action they are performing.
    rb.say("Please tell me the action you are performing.")
    action_description = rb.listen()

    # Update the state based on the human's action.
    # This would require parsing `action_description` into the actual action and its arguments, 
    # and then applying this action to the `initial_state`. I'm leaving this as a placeholder 
    # since the specifics would depend on your application.
    initial_state = update_state_based_on_action(initial_state, action_description)

    # Perform goal recognition based on the updated state and the action library.
    # Again, the specifics of `recognize_goal` would depend on your application.
    goal_description = recognize_goal(initial_state, action_library)

    # Check if a goal was recognized.
    if goal_description is not None:
      rb.say("I think your goal is: {}".format(goal_description))
      # Plan and execute actions to help achieve the recognized goal.
      solvable, plan = graph_search(initial_state, [action_library], goal_description, frontier)
      if not solvable:
        rb.say("I'm unable to help achieve this goal.")
        continue
      rb.say("I found a solution and will execute it now.")
      rb.execute_plan(plan)
      rb.say("Plan executed.")
    else:
      rb.say("I'm not sure what your goal is. Please continue with your actions.")
  
  # close the connection
  rb.shutdown()

def update_state_based_on_action(state, action_description):
  action_parts = action_description.split()

  # Let's assume that the actions are in the form of 'move to X' or 'pick up Y'
  if action_parts[0] == 'move':
    state['actor_location'] = action_parts[1]

  elif action_parts[0] == 'push':
    item = action_parts[1]
    if item in state[state['actor_location']]:
      state['actor_items'].append(state[state['actor_location']].pop(state[state['actor_location']].index(item)))
    else:
      print('Error: Tried to push an item not in current location.')

  return state

def recognize_goal(state, action_library):
  # For this example, let's assume that if the actor moves to the location of an item, 
  # their goal is to pick up that item.

  actor_location = state['actor_location']
  items_at_location = state[actor_location]

  if len(items_at_location) > 0:
    # If there's at least one item at the actor's location, 
    # we'll say that the goal is to pick up the first item.
    return "pick up {}".format(items_at_location[0])

  else:
    # If there are no items at the actor's location, we'll say that no goal was recognized.
    return None



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