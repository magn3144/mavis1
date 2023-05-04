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

import random
from search_algorithms.all_optimal_plans import all_optimal_plans, visualize_solution_graph
from search_algorithms.and_or_graph_search import and_or_graph_search
from utils import *
from collections import ChainMap
import copy
import sys


actor_AGENT = 0
HELPER_AGENT = 1


class DisjunctiveGoalDescription:
    """
    DisjunctiveGoalDescription is a wrapper class which allow for the representation of multiple possible
    goal descriptions. It has the same 'is_goal' method as a GoalDescription object and can therefore be
    used in the same places, but in contrast to the regular GoalDescription object, it returns True when
    one of its give goals are satisfied, thus allowing for a logical 'OR' to be expressed.
    """

    def __init__(self, possible_goal_descriptions):
        # possible_goal_descriptions should be a list of goals
        self.possible_goals = possible_goal_descriptions

    def is_goal(self, belief_node):
        for possible_goal in self.possible_goals:
            if possible_goal.is_goal(belief_node.state):
                return True
        return False


class GoalRecognitionNode:
    """
    GoalRecognitionNode is a wrapper class which can be used for implementing AND-OR based graph search.
    It allow a hospital state object and a solution graph object to be integrated into a single object, which
    the methods 'get_applicable_actions' and 'result' as required by the AND-OR graph search.
    Note that the usage of this class is completely optional and you are free to implement your goal recognition
    in a different manner, if you so desire.

    """

    def __init__(self, state, solution_graph):
        self.state = state
        self.solution_graph = solution_graph

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.state == other.state and self.solution_graph == other.solution_graph
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.state, self.solution_graph))
    
    def __repr__(self):
        return str(self.state)

    # def get_applicable_actions(self, action_set):
    #     # Here we are only interested in the actions of the helper, but state.get_applicable_actions will return a list
    #     # of joint actions, where the actor action is always GenericNoOp().
    #     applicable_joint_actions = self.state.get_applicable_actions(action_set)
    #     applicable_actions = [joint_action[HELPER_AGENT] for joint_action in applicable_joint_actions]
    #     return applicable_actions

    def applicable_helper_actions(self, action_set):
        # Returns a list of all possible helper actions, i.e., all possible OR-branches.
        applicable_actions = []
        for action in action_set:
            if action.is_applicable(HELPER_AGENT, self.state):
                applicable_actions.append(action)
        return applicable_actions

    def results(self, helper_action):
        # The result method should return a new GoalRecognitionNode which contains the resulting state and the
        # solution graph obtained from executing the joint_action in the current state.

        next_goal_recognition_nodes = set()
        for action in self.solution_graph.optimal_actions_and_results.keys():
            next_node = self.solution_graph.optimal_actions_and_results[action]
            if self.state.is_applicable([action, helper_action]) and not self.state.is_conflicting([action, helper_action]):
                next_state = self.state.result([action, helper_action])
                next_goal_recognition_nodes.add(GoalRecognitionNode(next_state, next_node))
            elif self.state.is_applicable([GenericNoOp(), helper_action]):
                next_state = self.state.result([GenericNoOp(), helper_action])
                next_goal_recognition_nodes.add(GoalRecognitionNode(next_state, self.solution_graph))
        return next_goal_recognition_nodes


# def solution_graph_results(goalRecognitionNode, helper_action):
#     # This results method can be used as the 'results' function for the AND-OR graph-search.
#     # It takes a GoalRecognitionNode (or something else if you choose to not use the GoalRecognitionNode class) and
#     # the action taken by the helper, i.e., the chosen OR-branch.
#     # This function should then return all of the possible outcomes, i.e., the possible AND-nodes. 
#     next_nodes = set()
#     next_states = set()
#     for action in node.optimal_actions_and_results.keys():
#         next_node = node.optimal_actions_and_results[action]
#         if state.is_applicable([action, helper_action]) and not state.is_conflicting([action, helper_action]):
#             next_state = state.result([action, helper_action])
#             next_nodes.add(next_node)
#             next_states.add(next_state)
#         # elif state.is_applicable([action, GenericNoOp()]):
#         #     next_state = state.result([action, GenericNoOp()])
#         #     next_nodes.add(next_node)
#         #     next_states.add(next_state)
#         elif state.is_applicable([GenericNoOp(), helper_action]) and helper_action.name != "NoOp":
#             next_state = state.result([GenericNoOp(), helper_action])
#             next_nodes.add(node)
#             next_states.add(next_state)
#     return next_nodes, next_states

def and_or_graph_search_goal_recognition(initial_node, initial_state, action_set, goal_description):
    # Returns a solution tree using the all_optimal_plans algorithm and the AND-OR graph search.
    # The solution tree should be a GoalRecognitionNode object, where the helper action in each node is the chosen OR-branch.
    action_set = [action_set] * initial_state.level.num_agents
    max_depth = 25
    for i in range(1, max_depth):
        goal_recognition_node = GoalRecognitionNode(copy.deepcopy(initial_state), copy.deepcopy(initial_node))
        policy_found = or_search(goal_recognition_node, [], goal_description, action_set, i)
        if policy_found:
            return goal_recognition_node.solution_graph
    return None

def or_search(g_node, path, goal_description, action_set, depth):
    #print(g_node.solution_graph.id)
    if g_node.solution_graph.is_goal_state:
        return True
    if g_node.state in path:
        return False
    if depth == 0:
        return False
    applicable_actions = g_node.applicable_helper_actions(action_set[HELPER_AGENT])
    for action in applicable_actions:
        # print("State:\n" + str(g_node.state))
        # print("Action: " + str(action))
        and_goal_recognition_nodes = g_node.results(action)
        if len(and_goal_recognition_nodes) == 0:
            continue
        policy = and_search(and_goal_recognition_nodes, [g_node.state] + path, goal_description, action_set, depth - 1)
        if policy:
            g_node.solution_graph.helper_actions.append(action)
            return True
    return False

def and_search(goal_recognition_nodes, path, goal_description, action_set, depth):
    for g_node in goal_recognition_nodes:
        # if len(g_node.solution_graph.consistent_goals) == 0:
        #     continue
        policy = or_search(g_node, path, goal_description, action_set, depth)
        if not policy:
            return False
    return True

def goal_recognition_agent_type(level, initial_state, action_library, goal_description, frontier):
    # You should implement your goal recognition agent type here. You can take inspiration on how to structure the code
    # from your previous helper and non deterministic agent types.
    # Note: Similarly to the non deterministic agent type, this is not a fast algorithm and you should therefore start
    # by testing on very small levels, such as those found in the assignment.
    possible_goals = []
    for i in range(goal_description.num_sub_goals()):
        possible_goals.append(goal_description.get_sub_goal(i))
    actor_color = initial_state.level.colors[str(actor_AGENT)]
    monocrome_initial_state = initial_state.color_filter(actor_color)
    solutions_found, solution_graph = all_optimal_plans(monocrome_initial_state, action_library, possible_goals, frontier)
    if not solutions_found:
        print("no actor policy found")
        return None
    # visualize_solution_graph(solution_graph)
    solution_graph = and_or_graph_search_goal_recognition(solution_graph, initial_state, action_library, goal_description)
    if solution_graph:
        print("success")
        # visualize_solution_graph(solution_graph)
        return solution_graph
    else:
        print("no helper policy found")
        return None