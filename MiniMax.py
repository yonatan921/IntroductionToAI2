from typing import Tuple

from Graph import Graph
from Problem import Problem
from name_tuppels import Point


class MiniMax:

    def __init__(self, problem: Problem, cutoff_deep):
        self.problem = problem
        self.cutoff_deep = cutoff_deep

    def mini_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action = self.max_value(graph, float("-inf"), float("inf"), 0, aigent_id)
        return action

    def max_value(self, graph: Graph, a, b, deep, aigent_id) -> Tuple[int, Point]:
        aigent = graph.find_aigent_by_id(aigent_id)
        p1, p2 = graph.calc_heuristic()
        utility_value = graph.utility(p1, p2)
        if graph.game_over() or deep == self.cutoff_deep:
            return utility_value, aigent.point

        v = float("-inf")
        p2_max = p2
        best_action = None
        for action, state in self.problem.find_successors(graph, aigent, False).items():  # The smart aigent move
            x, min_action = self.min_value(state, a, b, deep + 1, 1 - aigent_id)
            if x > v:
                v = x
                best_action = action
            elif x == v:
                new_p1, new_p2 = state.calc_heuristic()
                if new_p2 > p2_max:
                    p2_max = new_p2
                    v = x
                    best_action = action
            if v >= b:
                return v, action
            a = max(a, v)
        return v, best_action

    def min_value(self, graph: Graph, a, b, deep, aigent_id) -> Tuple[int, Point]:
        aigent = graph.find_aigent_by_id(aigent_id)
        p1, p2 = graph.calc_heuristic()
        utility_value = graph.utility(p1, p2)
        if graph.game_over() or deep == self.cutoff_deep:
            return utility_value, aigent.point

        v = float("inf")
        p2_max = p2
        best_point = None
        for action, state in self.problem.find_successors(graph, aigent, True).items():  # The dummy aigent move
            x, max_action = self.max_value(state, a, b, deep + 1, 1- aigent_id )
            if x < v:
                v = x
                best_point = max_action
            elif x == v:
                new_p1, new_p2 = state.calc_heuristic()
                if new_p2 > p2_max:
                    p2_max = new_p2
                    v = x
                    best_point = action
            # v = min(v, self.max_value(state, a, b))
            if v <= a:
                return v, action
            b = min(b, v)
        return v, best_point
