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
import sys

from search_algorithms.graph_search import graph_search
from utils import *


def decentralised_agent_type(level, initial_state, action_library, goal_description, frontier):
    # Create an action set where all agents can perform all actions
    action_set = [action_library] * level.num_agents

    # Here you should implement the DECENTRALISED-AGENTS algorithm.
    # You can use the 'classic' agent type as a starting point for how to communicate with the server, i.e.
    # use 'print(joint_action_to_string(joint_action), flush=True)' to send a joint_action to the server and
    # use 'parse_response(read_line())' to read back an array of booleans indicating whether each individual action
    #   in the joint action succeeded.

    # planning_success, plan = graph_search(initial_state, action_set, goal_description, frontier)

    # if not planning_success:
    #     print("Unable to solve level.", file=sys.stderr)
    #     return

    # print(f"Found solution of length {len(plan)}", file=sys.stderr)

    num_agents = level.num_agents

    # Compute a plan for each agent
    pi = []
    for i in range(num_agents):
        agent_postion, agent_char = initial_state.agent_positions[i]
        agent_color = level.colors[agent_char]
        monochrome_problem = initial_state.color_filter(agent_color)
        planning_success, pi_i = graph_search(monochrome_problem, action_set, goal_description, frontier)
        pi.append(pi_i)


    while len(pi)!=0:

        actions = [""]*num_agents
        for i in range(num_agents):
            if len(pi[i])==0:
                actions[i] = "NoOp"
            else:
                actions[i] = pi[0]

        __return = False

        for i in range(len(actions)):
            for joint_action in actions[i]:
                #print("joint_action: ", file=sys.stderr)

                # Send the joint action to the server
                #print(joint_action, file=sys.stderr)
                print(joint_action_to_string(joint_action), flush=True)
                # Uncomment the below line to print the executed actions to the command line for debugging purposes
                #print(joint_action_to_string(joint_action), file=sys.stderr, flush=True)

                # Read back whether the agents succeeded in performing the joint action
                execution_successes = parse_response(read_line())
                #print("execution_successes: ", file=sys.stderr)
                #print(execution_successes, file=sys.stderr)
                if execution_successes[i] and pi[i]:
                    pi[i] = pi[i][1:]
                if False in execution_successes:
                    # print("Number of actions that fail: {}".format(sum(execution_successes)))
                    print("Execution failed! Stopping...", file=sys.stderr)
                    # One of the agents failed to execute their action.
                    # This should not occur in classical planning and we therefore just abort immediately
                    __return = True
                    return

            if __return:
                return

