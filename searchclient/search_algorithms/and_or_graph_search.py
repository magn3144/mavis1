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


def and_or_graph_search(initial_state, action_set, goal_description, results):

    def or_search(state, path):
        if goal_description.is_goal(state):
            return {}
        if state in path:
            return "failure"

        #policy = {}
        #applicable_actions = state.get_applicable_actions(action_set)
        #print(f"action_s   :   {applicable_actions}")
        print("")
        applicable_a = []
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
            plan = and_search(results(next_state, [action]), path + [next_state])
            print("")
            print("")
            #print(f"plan :  {plan}")
            if plan != "failure":
                print(plan)
                return {next_state: action, **plan}
        return "failure"

    def and_search(states, path):
        plans = []
        for state in states:
            print("")
            #print(f"path2 :  {path}")
            plan = or_search(state, path)
            #print(f"plan   :   {plan}")
            print("")
            if plan == "failure":
                return "failure"

            if plan != "failure":
                plans.append(plan)
        

    return or_search(initial_state, [])
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