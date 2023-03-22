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



"""
def helper_agent_type(level, initial_state, action_library, goal_description, frontier):

    # Initialize variables
    actor = 0
    helpers = list(range(1, level.num_agents))
    subgoals = goal_description.get_sub_goal(actor)


    #print(f" subgoal:     {subgoals}")
    #print("")
    subgoals_complete = [False] * goal_description.num_sub_goals()

    print(f"numb_sub_goals:    {goal_description.num_sub_goals()}")
    print("")
    

    # Loop through subgoals
    while not all(subgoals_complete):

        # Pick a subgoal to work on
        subgoal_idx = subgoals_complete.index(False)
        print(f" subgoal:     {subgoals}")
        print("")
        subgoal = subgoals.box_goals[0][0]
        print(f" subgoal0:     {subgoal}")
        print("")

        # Plan and execute to achieve subgoal
        planning_success, plan = graph_search(initial_state, action_library, subgoal, frontier)



        if not planning_success:
            print("Unable to solve level.", file=sys.stderr)
            return
        for action in plan:
            joint_action = [action] + [None] * (level.num_agents - 1)
            print(joint_action_to_string(joint_action), flush=True)
            action_success = parse_response(read_line())
            if not all(action_success):
                blocking_helper = action_success.index(False) + 1
                helper_subgoal = get_blocking_helper_subgoal(plan, blocking_helper, helpers, initial_state, level)
                planning_success, helper_plan = graph_search(initial_state, action_library, helper_subgoal, frontier)
                if not planning_success:
                    print("Unable to solve level.", file=sys.stderr)
                    return
                for helper_action in helper_plan:
                    joint_action = [None] * actor + [helper_action] + [None] * (level.num_agents - 1 - actor)
                    print(joint_action_to_string(joint_action), flush=True)
                    action_success = parse_response(read_line())
                    if not all(action_success):
                        print("Unable to execute joint action.", file=sys.stderr)
                        return
            initial_state = update_state(initial_state, action)

        subgoals_complete[subgoal_idx] = True

    print("All subgoals achieved!", file=sys.stderr)
"""
def create_negative_subgoals(excluded_positions, agent_index, agent_color, level):
    negative_subgoals = []

    for pos in excluded_positions:
        negative_subgoals.append(('agent', agent_index, agent_color, pos, False))
        for box_char, box_color in level.colors.items():
            if box_color != agent_color:
                negative_subgoals.append(('box', box_char, box_color, pos, False))

    return negative_subgoals

def helper_agent_type(level, initial_state, action_library, goal_description, frontier):
   
   
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
    #   which takes a list of subgoals
   
    num_agents = level.num_agents
    current_state = initial_state

    # Create an action set where all agents can perform all actions
    # action_set = [action_library] * level.num_agents
    action_set = [action_library]

    # Implement the HELPER-AGENT algorithm.
    

    actor_index = 0

    # Monochrome goal description
    #Create monochrome problem
    agent_character = level.initial_agent_positions[actor_index][1]
    agent_color = level.colors[agent_character]
    monochrome_problem = initial_state.color_filter(agent_color)
    monochrome_goal_description = goal_description.color_filter(agent_color)




    # Extract subgoals from goal_description
    subgoals_number = monochrome_goal_description.num_sub_goals()
    subgoals = goal_description.get_sub_goal(actor_index)
    # Search for the actor's individual plan and goal description)
    result, actor_plan = graph_search(monochrome_problem, action_set, subgoals, frontier)
    print(f" actor_plan        :   {actor_plan}")
    
    pi = []
    # Loop through subgoals
    for subgoal in actor_plan:
        subgoal_goal_description = HospitalGoalDescription([subgoal], goals=monochrome_goal_description.goals)
        planning_success, subplan = graph_search(current_state.color_filter(agent_color), action_set, subgoal_goal_description, frontier)
        print(f" subplan? :    {subplan}")
        pi += [subplan[j][0] for j in range(len(subplan))]

        if not planning_success:
            print("Planning failed for subgoal:", subgoal)
            return
        
        while pi:
            action = pi[0]
            joint_action = [action] + [GenericNoOp()] * (num_agents - 1)
            joint_action_string = joint_action_to_string(joint_action)
            print(f"joint_action_string   :  {joint_action_string}")
            print("")
            print("")

            # Execute the joint action
            print(joint_action_string, flush=True)
            action_success = parse_response(read_line())[0]
            print(f"action_success   :   {action_success}")
            print("")
            print()

            if action_success:
                joint_action = [action] + [GenericNoOp()] * (num_agents - 1)
                joint_action_string = joint_action_to_string(joint_action)
                current_state = current_state.result(joint_action)
                pi = pi[1:]
            else:
                print(f"subplan nu:   {pi}")
                print("")
                print("")
                conflict_positions, _ = current_state.agent_positions[actor_index]
                print(f"conflict_positions:   {conflict_positions}")
                print("")
                print("")
                excluded_positions = set(conflict_positions)

                #excluded_positions = set(conflict_positions + [pos for a in pi[1:] for pos in a.get_positions(current_state)])

                helper_requests = []
                for i in range(1, num_agents):
                    helper_color = level.colors[level.initial_agent_positions[i][1]]
                    negative_subgoals = create_negative_subgoals(excluded_positions, i, helper_color, level)
                    helper_goal_description = goal_description.create_new_goal_description_of_same_type(negative_subgoals)
                    helper_requests.append((i, helper_goal_description))

                for helper_index, helper_goal_description in helper_requests:
                    helper_action_set = [[GenericNoOp()]] * num_agents
                    helper_action_set[helper_index] = action_library

                    planning_success, helper_pi = graph_search(current_state, helper_action_set, helper_goal_description, frontier)
                    helper_pi = [helper_pi[j][0] for j in range(len(helper_pi))]
                    if not planning_success:
                        print(f"Planning failed for helper {helper_index}")
                        return

                    while helper_pi:
                        joint_action = helper_pi[0]
                        joint_action_string = joint_action_to_string(joint_action)

                        # Execute the joint action
                        print(joint_action_string, flush=True)
                        helper_action_success = parse_response(read_line())[helper_index]

                        if helper_action_success:
                            current_state, _ = current_state.result(joint_action)
                            helper_pi = helper_pi[1:]
                        else:
                            print(f"Helper {helper_index} action failed")
                            return