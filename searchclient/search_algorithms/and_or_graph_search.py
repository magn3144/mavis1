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
    # def is_goal(state):
    #    return goal_description.is_goal(initial_state)

    # def actions(state):
    #    for action in action_set:
    #        return [a for a in action if a.is_applicable(0, state)]

    def or_search(state, path, depth):

        if goal_description.is_goal(state):
            return depth, {}

        # print(f"state :  {state}")
        # print("")
        # print(f"path   :   {path}")
        if state in path:
            return float("inf"), "failure"

        min_depth = float('inf')
        best_plan = "failure"

        applicable_a = []
        for action in action_set:
            # print(f" action_is_applicable: {state.is_applicable(action)}")
            for a in action:

                if a.is_applicable(0, state):
                    applicable_a.append(a)

        for action in applicable_a:
            action = [action]
            result_states = results(state, action)
            new_depth, plan = and_search(result_states, [state] + path, depth + 1)
            if plan != "failure" and new_depth < min_depth:
                min_depth = new_depth
                # print(f"min_depth :   {min_depth}")
                # print("")
                best_plan = {state: action, **plan}
                # print(f"best_plan  :   {best_plan}")

        return min_depth, best_plan

    def and_search(states, path, depth):

        max_depth = depth
        combined_plan = {}
        for state in states:
            state_depth, plan = or_search(state, path, depth)
            # print(plan)
            # print(f"plan1 : {plan[1]}")
            # print("")
            # print(f"plan : {plan}")
            # print("")
            if plan == "failure":
                return float("inf"), "failure"
            max_depth = max(max_depth, state_depth)
            combined_plan.update(plan)
        print("")
        print(f"combined_plan    :   {combined_plan.values()}")
        return max_depth, combined_plan

    return or_search(initial_state, [], 0)