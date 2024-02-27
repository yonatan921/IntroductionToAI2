from typing import Tuple

from Graph import Graph
from Problem import Problem
from name_tuppels import Point


class MiniMax:

    def __init__(self, problem: Problem, cutoff_deep):
        self.problem = problem
        self.cutoff_deep = cutoff_deep

    def mini_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action, _, _ = self.max_value(graph, float("-inf"), float("inf"), 0, aigent_id)
        return action

    def max_value(self, graph: Graph, a, b, deep, aigent_id) -> Tuple[int, Point, int, int]:
        aigent = graph.find_aigent_by_id(aigent_id)
        IS1, IS2 = graph.calc_heuristic(aigent_id)
        TS1 = graph.utility(IS1, IS2)
        if graph.game_over() or deep == self.cutoff_deep:
            if deep == self.cutoff_deep:
                # print(f"MAX- {aigent_id=}, {IS1=}, {IS2=}, {TS1=}, {deep=}")

                pass
                # print(f"Cutoff!!! {aigent.point},{aigent_id} ")
            return TS1, aigent.point, IS1, IS2

        v = float("-inf")
        IS2_max = IS2
        best_action = None
        for action, state in self.problem.find_successors(graph, aigent, False).items():  # The smart aigent move
            x, min_action, new_IS1, new_IS2 = self.min_value(state, a, b, deep + 1, 1 - aigent_id)
            if x > v:
                v = x
                best_action = action
                IS2_max = new_IS2
            elif x == v:
                # new_p1, new_p2 = state.calc_heuristic(aigent_id)
                if new_IS2 > IS2_max:
                    IS2_max = new_IS2
                    v = x
                    best_action = action
            if v >= b:
                return v, action, IS1, IS2_max
            a = max(a, v)
        return v, best_action, IS1, IS2_max

    def min_value(self, graph: Graph, a, b, deep, aigent_id) -> Tuple[int, Point, int, int]:
        aigent = graph.find_aigent_by_id(aigent_id)
        IS1, IS2 = graph.calc_heuristic(aigent_id)
        TS2 = graph.utility(IS1, IS2)

        if graph.game_over() or deep == self.cutoff_deep:
            if deep == self.cutoff_deep:
                # print(f"MIN- {aigent_id=}, {IS1=}, {IS2=}, {TS2=}, {deep=}")
                pass
                # print(f"Cutoff!!! {aigent.point}")
            return TS2, aigent.point, IS1, IS2

        v = float("inf")
        IS2_max = IS2
        best_point = None
        for action, state in self.problem.find_successors(graph, aigent, True).items():  # The dummy aigent move
            x, max_action, new_IS1, newIS2 = self.max_value(state, a, b, deep + 1, 1- aigent_id )
            if x < v:
                v = x
                best_point = max_action
                IS2_max = newIS2
            elif x == v:
                # new_p1, new_p2 = state.calc_heuristic(aigent_id)
                if newIS2 < IS2_max:
                    IS2_max = newIS2
                    v = x
                    best_point = action
            # v = min(v, self.max_value(state, a, b))
            if v <= a:
                return v, action, IS1, IS2_max
            b = min(b, v)
        return v, best_point, IS1, IS2_max
