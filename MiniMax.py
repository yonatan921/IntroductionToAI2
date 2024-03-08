from typing import Tuple, Callable

from Graph import Graph
from Problem import Problem
from name_tuppels import Point


class MiniMax:

    def __init__(self, problem: Problem, cutoff_deep):
        self.problem = problem
        self.cutoff_deep = cutoff_deep

    def mini_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action, _, _ = self.max_value(graph, float("-inf"), float("inf"), 0, aigent_id, self.min_value)
        return action

    def maxi_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action = self.minimax(graph, aigent_id, True)
        return action

    def coo_max_decision(self, graph: Graph, aigent_id) -> Point:
        _, action, _ = self.coominimax(graph, aigent_id)
        return action

    def max_value(self, caller_aigent, graph: Graph, a, b, deep, aigent_id, min_max: Callable) -> Tuple[
        int, Point, int, int]:
        aigent = graph.find_aigent_by_id(aigent_id)
        ts = (IS1, IS2) = graph.calc_heuristic(aigent_id)
        # TS1 = graph.utility(IS1, IS2)
        if graph.game_over() or deep == self.cutoff_deep:
            if deep == self.cutoff_deep:
                # print(f"MAX- {aigent_id=}, {IS1=}, {IS2=}, {TS1=}, {deep=}")

                pass
                # print(f"Cutoff!!! {aigent.point},{aigent_id} ")
            return ts[caller_aigent], aigent.point, IS1, IS2

        v = float("-inf")
        IS2_max = IS2
        best_action = None
        for action, state in self.problem.find_successors(graph).items():  # The smart aigent move
            x, min_action, new_IS1, new_IS2 = min_max(caller_aigent, state, float("-inf"), float("inf"), deep + 1,
                                                      1 - aigent_id, self.max_value)
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
        return v, best_action, IS1, IS2

    def min_value(self, graph: Graph, a, b, deep, aigent_id, min_max: Callable) -> Tuple[int, Point, int, int]:
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
        for action, state in self.problem.find_successors(graph).items():  # The dummy aigent move
            x, max_action, new_IS1, newIS2 = min_max(state, a, b, deep + 1, 1 - aigent_id, self.min_value)
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

    def new_maxi_max(self, graph: Graph, deep, aigent_id, maxing: bool) -> Tuple[int, Point]:
        aigent = graph.find_aigent_by_id(aigent_id)
        IS1, IS2 = graph.calc_heuristic(aigent_id)
        TS1 = graph.utility(IS1, IS2)
        TS2 = graph.utility(IS2, IS1)
        if graph.game_over():
            return TS2 if graph.turn % 2 == 0 else TS1, aigent.point

        best_h = float("-inf")
        best_move = None
        for action, state in self.problem.find_successors(graph).items():
            current_h, _ = self.new_maxi_max(state, deep + 1, 1 - aigent_id, not maxing)
            if current_h > best_h:
                best_h = current_h
                best_move = action
        return best_h, best_move

    def minimax(self, graph: Graph, agent_id: int, maximizing: bool, alpha: float = float("-inf"),
                beta: float = float("inf")) -> Tuple[int, Point]:
        """
        Implements the minimax algorithm with alpha-beta pruning.

        Args:
            graph: The current game state representation.
            agent_id: The ID of the current player.
            maximizing: Whether the current level is for maximizing or minimizing player.
            alpha: The lower bound of potential scores for maximizing player.
            beta: The upper bound of potential scores for minimizing player.

        Returns:
            A tuple containing the best heuristic value found and the corresponding action (move).
        """

        if graph.game_over():
            # Base case: return heuristic value
            IS1, IS2 = graph.calc_heuristic(agent_id)
            TS1 = graph.utility(IS1, IS2)
            TS2 = graph.utility(IS2, IS1)
            return TS1 if maximizing else TS2, None

        best_value = float("-inf") if maximizing else float("inf")
        best_move = None

        for action, successor_state in self.problem.find_successors(graph).items():
            # Explore successors recursively with alpha-beta pruning
            heuristic, _ = self.minimax(successor_state, 1 - agent_id, not maximizing, alpha, beta)

            # Update best value and move based on maximizing/minimizing player
            if maximizing:
                if heuristic > best_value:
                    best_value = heuristic
                    best_move = action
                alpha = max(alpha, best_value)  # Pruning for maximizing player
                if beta <= alpha:  # Pruning condition
                    break
            else:
                if heuristic < best_value:
                    best_value = heuristic
                    best_move = action
                beta = min(beta, best_value)  # Pruning for minimizing player
                if beta <= alpha:  # Pruning condition
                    break

        return best_value, best_move

    def coominimax(self, graph: Graph, agent_id: int) -> Tuple[int, Point, int]:
        """
        Implements the minimax algorithm with alpha-beta pruning.

        Args:
            graph: The current game state representation.
            agent_id: The ID of the current player.
            maximizing: Whether the current level is for maximizing or minimizing player.
            alpha: The lower bound of potential scores for maximizing player.
            beta: The upper bound of potential scores for minimizing player.

        Returns:
            A tuple containing the best heuristic value found and the corresponding action (move).
        """

        if graph.game_over():
            # Base case: return heuristic value
            IS1, IS2 = graph.calc_heuristic(agent_id)
            TS1 = graph.utility(IS1, IS2)
            TS2 = graph.utility(IS2, IS1)
            return TS1, None, TS2

        best_value = float("-inf")
        best_move = None
        best_other_heuristic = float("-inf")
        for action, successor_state in self.problem.find_successors(graph).items():
            # Explore successors recursively with alpha-beta pruning
            heuristic, _, other_heuristic = self.coominimax(successor_state, 1 - agent_id)

            # Update best value and move based on maximizing/minimizing player
            if heuristic > best_value:
                best_value = heuristic
                best_move = action
                best_other_heuristic = other_heuristic
            elif heuristic == best_value and other_heuristic > best_other_heuristic:
                best_move = action
                best_other_heuristic = heuristic

        return best_value, best_move, best_other_heuristic
