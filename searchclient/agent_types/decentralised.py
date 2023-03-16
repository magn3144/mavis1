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

from search_algorithms.graph_search import graph_search
from utils import *


def decentralised_agent_type(level, initial_state, action_library, goal_description, frontier, debug=False):
    current_state = initial_state

    # Create an action set where all agents can perform all actions
    action_set = [action_library] * level.num_agents

    # Here you should implement the DECENTRALISED-AGENTS algorithm.
    # You can use the 'classic' agent type as a starting point for how to communicate with the server, i.e.
    # use 'print(joint_action_to_string(joint_action), flush=True)' to send a joint_action to the server and
    # use 'parse_response(read_line())' to read back an array of booleans indicating whether each individual action
    #   in the joint action succeeded.
    num_agents = level.num_agents
    pi = [None] * num_agents
    for i in range(num_agents):
        agent_character = level.initial_agent_positions[i][1]
        agent_color = level.colors[agent_character]
        monochrome_problem = initial_state.color_filter(agent_color)
        print(f"monochrome problem for {agent_color} agent:", file=sys.stderr)
        print(monochrome_problem, file=sys.stderr)
        monochrome_goal_description = goal_description.color_filter(agent_color)
        print("goal description:", file=sys.stderr)
        print(goal_description, file=sys.stderr)
        print(f"monochrome goal description for {agent_color} agent:", file=sys.stderr)
        print(monochrome_goal_description, file=sys.stderr)
        planning_success, pi[i] = graph_search(monochrome_problem, action_set, monochrome_goal_description, frontier)
        pi[i] = [pi[i][j][0] for j in range(len(pi[i]))]

    print("----------------------------------------", file=sys.stderr)
    print(current_state, file=sys.stderr)
    while any(pi):
        actions = [None] * num_agents
        for i in range(num_agents):
            if len(pi[i]) == 0:
                actions[i] = action_library[0]
            else:
                actions[i] = pi[i][0]

        # Convert the joint action to a string
        joint_action_string = joint_action_to_string(actions)
        print("joint_action_string: " + joint_action_string, file=sys.stderr)
        if debug:
            current_state, action_success = current_state.result(actions, debug=True)
            print(current_state, file=sys.stderr)
        else:
            # Execute the joint action and get wether each individual action succeeded
            print(joint_action_string, flush=True)
            action_success = parse_response(read_line())

        print(f"All actions succeeded!" * all(action_success) + f"Some action(s) failed: {action_success}" * (not all(action_success)), file=sys.stderr)

        # Update the plan for each agent
        for i in range(num_agents):
            if action_success[i] and len(pi[i]) > 0:
                pi[i] = pi[i][1:]