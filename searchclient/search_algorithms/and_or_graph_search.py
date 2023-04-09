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
from collections import ChainMap


def and_or_graph_search(initial_state, action_set, goal_description, results):
    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a policy format, mapping from states to actions.
    # The algorithm should return a pair (worst_case_length, or_plan)
    # where the or_plan is a dictionary with states as keys and actions as values
    
    action_set = action_set * initial_state.level.num_agents
    max_depth = 15
    for i in range(2, max_depth):
        policy, cyclic = or_search(initial_state, [], goal_description, action_set, results, {}, i)
        if policy is not None and not cyclic:
            return policy
    return None

def or_search(state, path, goal_description, action_set, results, policy, depth):
    if goal_description.is_goal(state):
        return {}, False
    if state in path:
        return policy, True
    if depth == 0:
        return None, False
    applicable_actions = state.get_applicable_actions(action_set)
    all_actions_cyclic = True
    for i, action in enumerate(applicable_actions):
        new_states = results(state, action, action_set)
        policy, cyclic = and_search(new_states, [state] + path, goal_description, action_set, results, {}, depth - 1)
        all_actions_cyclic = all_actions_cyclic and cyclic
        if (policy is not None and not cyclic) or (all_actions_cyclic and i == len(applicable_actions) - 1):
            policy[state] = action
            return policy, cyclic
    return None, False

def and_search(states, path, goal_description, action_set, results, policy, depth):
    policies = [None] * len(states)
    cyclic = [False] * len(states)
    for i, s_i in enumerate(states):
        policies[i], cyclic[i] = or_search(s_i, path, goal_description, action_set, results, policy, depth)
        if policies[i] == None:
            return None, False
    policies = dict(ChainMap(*policies))
    return policies, all(cyclic)