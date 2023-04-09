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

import random
from search_algorithms.and_or_graph_search import and_or_graph_search
from utils import *


def get_broken_action(joint_action, action_library):
    broken_action = []
    for i, action in enumerate(joint_action):
        if action == action_library[i][1]:
            broken_action.append(action_library[i][3])
        elif action == action_library[i][2]:
            broken_action.append(action_library[i][4])
        elif action == action_library[i][3]:
            broken_action.append(action_library[i][2])
        elif action == action_library[i][4]:
            broken_action.append(action_library[i][1])
        else:
            broken_action.append(action)
    return broken_action

def broken_results(state, action, action_library):
    # Building the Results() function containing the indeterminism
    # If performing two of the same actions is possible from the state,
    # this result is added as a possible outcome..

    standard_case = state.result(action)
    
    # return possible_states
    broken_action = get_broken_action(action, action_library)
    if state.is_applicable(broken_action):
        broken_case = state.result(broken_action)
        return [standard_case, broken_case]
    return [standard_case]

CHANCE_OF_BROKEN_ACTION = 0.5

def non_deterministic_advanced_agent_type(level, initial_state, action_library, goal_description):
    # Create an action set for the agents without pull actions
    action_set = [action_library[:17]] * level.num_agents

    # Call AND-OR-GRAPH-SEARCH to compute a conditional plan
    plan = and_or_graph_search(initial_state, action_set, goal_description, broken_results)

    if plan is None:
        print("Failed to find strong plan!", file=sys.stderr)
        return

    print("Found plan", file=sys.stderr)

    current_state = initial_state

    while True:
        # If we have reached the goal, then we are done
        if goal_description.is_goal(current_state):
            break

        if current_state not in plan:
            # The agent reached a state not covered by the plan; AND-OR-GRAPH-SEARCH failed.
            print(f"Reached state not covered by plan!\n{current_state}", file=sys.stderr)
            break

        # Otherwise, read the correct action to execute
        joint_action = plan[current_state]

        # Broken executor non-determinism: After performing action, roll dice to check whether
        # action will be no-op instead
        is_broken = random.random() < CHANCE_OF_BROKEN_ACTION
        broken_action = get_broken_action(joint_action, action_set)
        if is_broken and current_state.is_applicable(broken_action):
            print(f"Ups! Wrong direction!", flush=True, file=sys.stderr)
            print(joint_action_to_string(broken_action), flush=True, file=sys.stderr)
            print(joint_action_to_string(broken_action), flush=True)
            _ = parse_response(read_line())
            current_state = current_state.result(broken_action)
        else:
            # Send the joint action to the server (also print it for help)
            print(joint_action_to_string(joint_action), flush=True, file=sys.stderr)
            print(joint_action_to_string(joint_action), flush=True)
            _ = parse_response(read_line())
            current_state = current_state.result(joint_action)