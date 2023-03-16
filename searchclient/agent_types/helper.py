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

from domains.hospital import HospitalGoalDescription
from search_algorithms.graph_search import graph_search
from utils import *




def helper_agent_type(level, initial_state, action_library, goal_description, frontier):


    num_agents = level.num_agents

    action_set = [action_library] * num_agents


    agent_postion, agent_char = initial_state.agent_positions[0]
    agent_color = level.colors[agent_char]
    actor_action_set = goal_description.color_filter(agent_color)
    helper_action_set = action_library

    print(f"actor_action_set    :   {actor_action_set}")


    # Here you should implement the HELPER algorithm.
    # You can use the 'classic' agent type as a starting point for how to communicate with the server, i.e.
    # use 'print(joint_action_to_string(joint_action), flush=True)' to send a joint_action to the server and
    # use 'parse_response(read_line())' to read back an array of booleans indicating whether each individual action
    #   in the joint action succeeded.
    # Compute a plan for each agent

    planning_success, plan = graph_search(initial_state, actor_action_set, goal_description, frontier)

    #print(plan)
    if not planning_success:
        print("Unable to solve level.", file=sys.stderr)
        return

    num_helpers = num_agents - 1
    print(f"num_heplers    :    {num_heplers}")
    while len(plan) > 0:
        action = plan[0]
        joint_action = [action] + ["NoOp"] * num_helpers
        print(joint_action_to_string(joint_action), flush=True)
        # Uncomment the below line to print the executed actions to the command line for debugging purposes
        #print(joint_action_to_string(joint_action), file=sys.stderr, flush=True)

        # Read back whether the agents succeeded in performing the joint action
        execution_successes = parse_response(read_line())
        if False in execution_successes:
            initial_state.apply(action)
            plan.pop(0)
        else:
            helper_color = level.colors[initial_state.get_position_of_box(action.args[0])[1]]
            helper_action_set = action_library.color_filter(helper_color)
            helper_plan = graph_search(initial_state, helper_action_set, goal_description, frontier, use_custom_heuristic=False)
            if not helper_plan:
                print("Unable to solve help goal.", file=sys.stderr)
                return
            helper_goal = create_helper_goal(level, initial_state, action)
            helper_joint_action = [helper_plan[0]] + [NoOp] * (num_helpers - 1)
            #print(joint_action, file=sys.stderr)
            print(joint_action_to_string(helper_joint_action), flush=True)
            # Uncomment the below line to print the executed actions to the command line for debugging purposes
            #print(joint_action_to_string(joint_action), file=sys.stderr, flush=True)

            # Read back whether the agents succeeded in performing the joint action
            execution_successes = parse_response(read_line())
            if False in execution_successes:
                print("Execution failed! Stopping...", file=sys.stderr)
                # One of the agents failed to execute their action.
                # This should not occur in classical planning and we therefore just abort immediately
                return

def create_helper_goal(level, state, blocked_action):
    actor_position = state.agent_positions[0][0]
    actor_color = level.colors[state.agent_positions[0][1]]
    blocked_position = state.get_position_of_box(blocked_action.args[0])
    free_cells = get_free_cells_in_path(level, state, actor_position, blocked_position, actor_color)
    goal_literals = [f"agent goals({pos[0]},{pos[1]},{actor_color},{False})" for pos in free_cells]
    return " ^ ".join(goal_literals)

def get_free_cells_in_path(level, state, start, end, color):
    path = level.get_shortest_path(start, end)
    free_cells = []
    for pos in path:
        if state.is_free(pos) and (not state.has_box(pos) or state.get_color_at(pos) == color):
            free_cells.append(pos)
    return free_cells


    