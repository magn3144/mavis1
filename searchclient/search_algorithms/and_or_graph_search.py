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


    def or_search(state, path):

        if goal_description.is_goal(state):
                   return 0, {}

        #print(f"state :  {state}")
        #print("")
        #print(f"path   :   {path}")
        if state in path:
            return None, False

        
        best_worst_case_length = None
        best_plan = False
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
        #print(f"applicable_a : {applicable_a}")

        #print(applicable_a)
        for action in applicable_a:
            action = [action]
            result_states = results(state, action)
            worst_case_length, plan = and_search(result_states, [state] + path)
            if plan != False:
                if best_worst_case_length is None or worst_case_length < best_worst_case_length:
                    best_worst_case_length = worst_case_length
                #print(f"min_depth :   {min_depth}")
                #print("")
                    best_plan = {state: action, **plan}
                    return best_worst_case_length, best_plan

        return 0, False


    def and_search(states, path):   

        total_worst_case_length = 0
        combined_plan = {}
        for state in states:
            worst_case_length, plan = or_search(state, path)
            #print(plan)
            #print(f"plan1 : {plan[1]}")
            #print("")
            #print(f"plan : {plan}")
            #print("")
            if plan == False:
                return None, False
            max_depth = max(total_worst_case_length, worst_case_length)
            combined_plan.update(plan)
        #print("")
        #print(f"combined_plan    :   {combined_plan.values()}")
        return max_depth, combined_plan

    return or_search(initial_state, [])

