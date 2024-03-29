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


# def add_negative_subgoals(agent_pos, agent_characters, box_characters, goal_description, plan):
#     for action in plan:
#         agent_pos += action.agent_delta
#         for agent_character in agent_characters:
#             goal_description.goals.append((agent_pos, agent_character, False))
#             goal_description.agent_goals.append((agent_pos, agent_character, False))
#         for box_character in box_characters:
#             goal_description.goals.append((agent_pos, box_character, False))
#             goal_description.box_goals.append((agent_pos, box_character, False))

def helper_agent_type(level, initial_state, action_library, goal_description, frontier, debug=False):
    # Here you should implement the HELPER-AGENT algorithm.
    # Some tips are:
    # - From goal_description, you should look into color_filter and get_sub_goal to create monochrome and subgoal problems.
    # - You should handle communication with the server yourself and check successes of joint actions.
    #   Look into classic.py to see how this is done.
    # - You can create an action set where only a specific agent is allowed to move as follows:
    #   action_set = [[GenericNoOp()]] * level.num_agents
    #   action_set[agent_index] = action_library
    # - You probably want to create a helper function for creating the set of negative obstacle subgoals.
    #   You can then create a new goal description using 'goal_description.create_new_goal_description_of_same_type'
    #   which takes a list of subgoals.
    # raise NotImplementedError()

    # Create the action set where only agent-0 is allowed to move
    agent_index = 0
    action_set = [[GenericNoOp()]] * level.num_agents
    action_set[agent_index] = action_library

    # Create the monochrome problem and goal description
    agent_character = level.initial_agent_positions[agent_index][1]
    agent_color = level.colors[agent_character]
    monochrome_problem = initial_state.color_filter(agent_color)
    monochrome_goal_description = goal_description.color_filter(agent_color)

    # Create a plan for the agent to solve the monochrome problem
    planning_success, plan = graph_search(monochrome_problem, action_set, monochrome_goal_description, frontier)

    # Add NoOps to the plan to make it a valid joint action plan
    for i in range(len(plan)):
        plan[i].extend([GenericNoOp() for _ in range(level.num_agents - 1)])

    # agent_pos = level.initial_agent_positions[0]
    helper_characters = [agent_position[1] for agent_position in level.initial_agent_positions][1:]
    # box_characters = [box_position[1] for box_position in level.initial_box_positions][1:]
    # add_negative_subgoals(agent_pos, agent_characters, box_characters, goal_description, plan)

    if not planning_success:
        print("Unable to solve level.", file=sys.stderr)
        return
    print(f"Found solution of length {len(plan)}", file=sys.stderr)

    current_state = initial_state
    i = 0
    while i < len(plan):
        # Get the next joint action
        joint_action = plan[i]

        # Execute joint action if applicable
        if joint_action[0].is_applicable(0, current_state):
            current_state = current_state.result(joint_action)
            print(current_state, file=sys.stderr)
            if not debug:
                # Execute the joint action and get wether each individual action succeeded
                joint_action_string = joint_action_to_string(joint_action)
                print(joint_action_string, flush=True)
                action_success = parse_response(read_line())
            i += 1
        else: # If something is blocking its path, then request a helper to remove the obstacle
            # Create a new goal description where the box or agent blocking agent-0's path should be removed
            obstacle_position = pos_add(current_state.agent_positions[0][0], joint_action[0].agent_delta)
            obstacle_char = current_state.object_at(obstacle_position)
            negative_goal = (obstacle_position, obstacle_char, False)
            helper_goal_description = goal_description.create_new_goal_description_of_same_type([negative_goal])
            # Run the appropriate helper agent with the new goal description
            # If the obstacle is an agent, then just get the agent index for that char
            # If the obstacle is a box, then get the index of an agent with that color
            if obstacle_char == '':
                print("Error: No obstacle found at position", obstacle_position, file=sys.stderr)
                return
            if obstacle_char in helper_characters:
                helper_agent_index = helper_characters.index(obstacle_char)
            else:
                helper_agent_index = helper_characters.index(list(level.colors.keys())[list(level.colors.values()).index(level.colors[obstacle_char])]) + 1
            action_set = [[GenericNoOp()]] * level.num_agents
            action_set[helper_agent_index] = action_library
            planning_success, plan_helper = graph_search(current_state, action_set, helper_goal_description, frontier)
            current_state = current_state.result_of_plan(plan_helper)
            print(current_state, file=sys.stderr)

            if not debug:
                # Execute the joint action and get wether each individual action succeeded
                for joint_action in plan_helper:
                    joint_action_string = joint_action_to_string(joint_action)
                    print(joint_action_string, flush=True)
                    action_success = parse_response(read_line())