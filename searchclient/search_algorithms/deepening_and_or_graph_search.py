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
from copy import deepcopy
import domains.hospital.actions as actions
import domains.hospital.state as state


def and_or_graph_search(initial_state, action_set, goal_description, results):


#def is_goal(state):
#    return goal_description.is_goal(initial_state)

#def actions(state):
#    for action in action_set:
#        return [a for a in action if a.is_applicable(0, state)]


    def or_search(state, path, depth):
        
        if goal_description.is_goal(state):
            return depth, {}

        #print(f"state :  {state}")
        #print("")
        #print(f"path   :   {path}")
        if state in path or depth == 0:
            return 0, False

        
        best_worst_case_length = float('inf')
        best_plan = 0, False
        """
        applicabble_a = []
        for action in action_set:
            applicabble_a.append([a for a in action if a.is_applicable(0, state)])
        """
        applicable_a = []
        for action in action_set:
            #print(f" action_is_applicable: {state.is_applicable(action)}")
            for a in action:

                if a.is_applicable(0, state):
                    applicable_a.append(a)

        #print(applicable_a)
        for action in applicable_a:
            action = [action]
            result_states = results(state, action)
            worst_case_length, plan = and_search(result_states, [state] + path, depth - 1)
            if plan != False and worst_case_length < best_worst_case_length:
                best_worst_case_length = worst_case_length
                #print(f"min_depth :   {min_depth}")
                #print("")
                best_plan = {state: action, **plan}
                return best_worst_case_length, best_plan
        
        return 0, False


    def and_search(states, path, depth):   
        
        total_worst_case_length  = 0
        combined_plan = {}

        for state in states:
            worst_case_length, plan = or_search(state, path, depth)
            #print(plan)
            #print(f"plan1 : {plan[1]}")
            #print("")
            #print(f"plan : {plan}")
            #print("")
            if plan == False:
                return None, False
            total_worst_case_length += worst_case_length
            combined_plan.update(plan)
        #print("")
        #print(f"combined_plan    :   {combined_plan.values()}")
        return total_worst_case_length, combined_plan

    depth = 0
    while True:
        worst_case_length, plan = or_search(initial_state, [], depth)
        if plan != False:
            return worst_case_length, plan
        depth += 1
    #return or_search(initial_state, [], depth)
        



"""

    print (goal_description.is_goal(initial_state))
    return goal_description.is_goal(initial_state)

def or_search(state, path, depth):
    if goal_description.is_goal(state):
        return {}
    if state in path or depth == 0:
        return None

    #policy = {}
    #applicable_actions = state.get_applicable_actions(action_set)
    #print(f"action_s   :   {applicable_actions}")
    print("")
    applicable_a = []
    policy = {}
    for action in action_set:
        #print(f" action_is_applicable: {state.is_applicable(action)}")
        for a in action:

            if a.is_applicable(0, state):
                applicable_a.append(a)
    #print(f"applicable_a : {applicable_a}")
    for action in applicable_a:
        next_state = state.result([action])
        #print(f" action   :  {[i for i in action]}")
        print("")
        #print(f" state, action   :  {[next_state for next_state in results(state, action)]}")
        #print(f"path1 :  {path}")
        plan = and_search(results(next_state, [action]), path + [next_state], depth - 1)
        print("")
        print("")
        #print(f"plan :  {plan}")
        if plan is not None:
            #print(**plan)
            policy.update( {next_state: action, **plan} )
            print(f"ahahahha hah :  {policy}")
    return None

def and_search(states, path, depth):
    policy = {}
    for state in states:
        print("")
        #print(f"path2 :  {path}")
        plan = or_search(state, path, depth - 1)    
        #print(f"plan   :   {plan}")
        print("")
        if plan is None:
            return None

        policy.update(plan)
        print(f"kafkafoafok :  {policy}")
        return policy
    max_depth = 5

    for depth in range(max_depth + 1):
        policy = or_search(initial_state, [], depth)
        if policy is not None:
            return {state: action, **plan}
    return None
"""      

"""
    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a policy format, mapping from states to actions.
    # The algorithm should return a pair (worst_case_length, or_plan)
    # where the or_plan is a dictionary with states as keys and actions as values
    return or_search(goal_description.initial_state, [], problem)

def or_search(state, path, level):
    # Check if we have reached a goal state
    if level.is_goal(state):
        return {}

    # Check for loops in the path
    if state in path:
        return "failure"

    # Try each applicable action in the state
    for action in level.actions(state):
        results = level.results(state, action)
        plan = and_search(results, [state] + path, level)
        if plan != "failure":
            return {state: action, **plan}

    # No action led to a solution
    return "failure"

def and_search(states, path, level):
    # Recursively search for a plan for each outcome state
    plans = []
    for state in states:
        plan = or_search(state, path, level)
        if plan == "failure":
            return "failure"
        plans.append(plan)

    # Combine the plans into a single conditional plan
    conditionals = {}
    for plan in plans:
        for state, action in plan.items():
            if state not in conditionals:
                conditionals[state] = action
    return conditionals
"""