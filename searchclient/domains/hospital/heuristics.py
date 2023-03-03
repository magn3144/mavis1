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
from __future__ import annotations
import sys
import itertools
from utils import pos_add, pos_sub, APPROX_INFINITY

import domains.hospital.state as h_state
import domains.hospital.goal_description as h_goal_description
import domains.hospital.level as h_level

class HospitalGoalCountHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        count = 0
        for (position, char, is_positive) in goal_description.agent_goals:
            if not state.agent_at(position):
                count += 1
        return count


class HospitalAdvancedHeuristics:

    def __init__(self):
        pass

    def preprocess(self, level: h_level.HospitalLevel):
        # This function will be called a single time prior to the search allowing us to preprocess the level such as
        # pre-computing lookup tables or other acceleration structures
        pass

    '''
    function improve_heuristic(state, goal_description) returns an integer
      count <-- 0
      agentDistances <-- 0
      boxDistances <-- 0
        
      for position in box_goals: 
        if not position in state.boxes: 
          count += 1
      
      for i <-- 0 to length(box_goals): 
        (x1, y1) <-- box_goals[i]
        (x2, y2) <-- agent_positions
        distance <-- abs(x2- x1) + abs(y2 - y1) 
        agentDistances <-- distance
        
      for box_goal in goal_description: 
        for box_position, box_char in state.box_positions: 
          min_distance <-- inf
          boxMatchesGoal = False
          if box_char is goal_char: 
            (x1, y1) <-- box_position
            (x2, y2) <-- box_goal
            distance <-- abs(x2 - x1) + abs(y2 - y1)
            if distance < min_distance: 
              min_distance <-- distance
              boxMatchesGoal <-- True
            if boxMatchesGoal is True: 
              boxDistances += min_distance
      
      return agentDistances + boxDistances + count
    '''

    def h(self, state: h_state.HospitalState, goal_description: h_goal_description.HospitalGoalDescription) -> int:
        # Your heuristic goes here...
        count = 0
        # for (position, char, is_positive) in goal_description.agent_goals:
        #     if not state.agent_at(position):
        #         count += 1

        for (position, char, is_positive) in goal_description.box_goals:
            if state.box_at(position)[0] != -1:
                count += 1

        agentDistances = 0
        boxDistances = 0

        for i in range(0, len(goal_description.box_goals)):
            (x1, y1), _, _ = goal_description.box_goals[i]
            ((x2, y2), _) = state.agent_positions[0]
            distance = abs(x2 - x1) + abs(y2 - y1)
            agentDistances += distance
        
        for box_goal in goal_description.box_goals:
            goal_char = box_goal[1]
            for box_position, box_char in state.box_positions:
                min_distance = 10000
                boxMatchesGoal = False
                if box_char == goal_char:
                    (x2, y2), _, _ = box_goal
                    x1, y1 = box_position
                    distance = abs(x2 - x1) + abs(y2 - y1)
                    if distance < min_distance:
                        min_distance = distance
                        boxMatchesGoal = True
                if boxMatchesGoal:
                    boxDistances += min_distance

        # print((agentDistances, boxDistances, count), file=sys.stderr)
        # return agentDistances + boxDistances + count
        return agentDistances*(1/5) + boxDistances*10 + (count)
