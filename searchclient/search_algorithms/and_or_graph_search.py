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
import time
import memory
from copy import deepcopy
import domains.hospital.actions as actions
import domains.hospital.state as state
import domains.hospital.goal_description as goal_description
import strategies.dfs as dfs


def and_or_graph_search(initial_state: state.HospitalState, action_set: list[list[actions.AnyAction]],
                        goal_description: goal_description.HospitalGoalDescription, frontier: dfs.FrontierDFS, results) -> tuple[bool, list[list[actions.AnyAction]]]:
    global start_time

    # Set start time
    start_time = time.time()
    iterations = 0
    frontier.prepare(goal_description)

    # Clear the parent pointer and cost in order make sure that the initial state is a root node
    initial_state.parent = None
    initial_state.path_cost = 0

    # first initializes the frontier with the initial state,
    frontier.add(initial_state)

    # creates two sets to keep track of the expanded and visited states
    # Keep track of  expanded and visited states
    expanded = set()
    visited = set()
    # The expanded set contains the states that have already been explored,
    # and the visited set contains the states that are in the frontier or have already been explored

    while frontier:
        # Next state from frontier
        current_state = frontier.pop()

        # Check if goal state
        if goal_description.is_goal(current_state):
            # Printing generated states:
            # print(f"Generated states is contained here: {print_search_status(expanded, frontier)}")
            return True, []

        if current_state in expanded:
            return False, []

        # If the state is not a goal state, the function adds it to the expanded set
        # Add to expanded set
        expanded.add(current_state)
        # and generates the applicable actions for the state.

        applicable_actions = current_state.get_applicable_actions(action_set)

        # Get successor states for each applicable action
        for action in applicable_actions:
            next_state = current_state.result(action)

            # Check if next state has been visited
            if next_state in visited:
                continue

            # Add the next state to the frontier and visited sets
            frontier.add(next_state)
            visited.add(next_state)



    # Here you should implement AND-OR-GRAPH-SEARCH. We are going to use a policy format, mapping from states to actions.
    # The algorithm should return a pair (worst_case_length, or_plan)
    # where the or_plan is a dictionary with states as keys and actions as values
    raise NotImplementedError()


def or_search(state, path, goal_description, action_set, results):
    # Check if goal state
    if goal_description.is_goal(state):
        # Printing generated states:
        # print(f"Generated states is contained here: {print_search_status(expanded, frontier)}")
        return True, []
    if state in path:
        return False, []

    applicable_actions = state.get_applicable_actions(action_set)
    for action in applicable_actions:
        plan = and_search(results[state, action], [state, path], goal_description, action_set, results)
        if plan != False:
            return action, plan


def and_search(states, path, goal_description, action_set, results):
    plan = []
    for i, state in enumerate(states):
        plan.append(or_search(state, path, goal_description, action_set, results))
        if plan[0] == False:
            return False, []
    return plan


# A global variable used to keep track of the start time of the current search
start_time = 0


def print_search_status(expanded, frontier):
    global start_time
    if len(expanded) == 0:
        start_time = time.time()
    memory_usage_bytes = memory.get_usage()
    # Replacing the generated comma thousands separators with dots is neither pretty nor locale aware but none of
    # Pythons four different formatting facilities seems to handle this correctly!
    num_expanded = f"{len(expanded):8,d}".replace(',', '.')
    num_frontier = f"{frontier.size():8,d}".replace(',', '.')
    num_generated = f"{len(expanded) + frontier.size():8,d}".replace(',', '.')
    elapsed_time = f"{time.time() - start_time:3.3f}".replace('.', ',')
    memory_usage_mb = f"{memory_usage_bytes / (1024*1024):3.2f}".replace('.', ',')
    status_text = f"#Expanded: {num_expanded}, #Frontier: {num_frontier}, #Generated: {num_generated}," \
                  f" Time: {elapsed_time} s, Memory: {memory_usage_mb} MB"
    print(status_text, file=sys.stderr)