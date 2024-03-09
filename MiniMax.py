from typing import Tuple, Callable, Any

from Graph import Graph
from Problem import Problem
from name_tuppels import Point


class MiniMax:

    def __init__(self, problem: Problem, cutoff):
        self.problem = problem
        self.cutoff = cutoff

    def get_algo(self, utility):
        if utility == "cooperative":
            return self.coo_max_decision
        elif utility == "semi":
            return self.semiminimax_decision
        elif utility == "adversarial":
            return self.maxi_max_decision

    def maxi_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action = self.minimax(graph, aigent_id, 0, True)
        return action

    def coo_max_decision(self, graph: Graph, aigent_id) -> Point:
        _, action, _ = self.coominimax(graph, aigent_id, 0)
        return action

    def semiminimax_decision(self, graph: Graph, aigent_id) -> Point:
        _, action, _ = self.semiminimax(graph, aigent_id, 0)
        return action

    def minimax(self, graph: Graph, agent_id: int, deep: int, maximizing: bool, alpha: float = float("-inf"),
                beta: float = float("inf")) -> Tuple[int, Point]:

        if graph.game_over() or deep == self.cutoff:
            # Base case: return heuristic value
            IS1, IS2 = graph.calc_heuristic(agent_id)
            TS1 = graph.utility(IS1, IS2)
            TS2 = graph.utility(IS2, IS1)
            print(f"aigent {agent_id} IS: {IS1}, aigent {1-agent_id} IS: {IS2}. aigent {agent_id} TS: {TS1}, aigent {1-agent_id} TS: {TS2}")
            return TS1 if maximizing else TS2, None

        best_value = float("-inf") if maximizing else float("inf")
        best_move = None

        for action, successor_state in self.problem.find_successors(graph).items():
            # Explore successors recursively with alpha-beta pruning
            heuristic, _ = self.minimax(successor_state, 1 - agent_id, deep + 1, not maximizing, alpha, beta)

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
        # print(f"aigent = {agent_id}, best move: {best_move}, best value: {best_value}, deep: {deep}")
        return best_value, best_move

    def coominimax(self, graph: Graph, agent_id: int, deep: int) -> Tuple[int, Point, int]:

        if graph.game_over() or deep == self.cutoff:
            # Base case: return heuristic value
            IS1, IS2 = graph.calc_heuristic(agent_id)
            TS1 = graph.utility(IS1, IS2)
            TS2 = graph.utility(IS2, IS1)
            print(
                f"aigent {agent_id} IS: {IS1}, aigent {1 - agent_id} IS: {IS2}. aigent {agent_id} TS: {TS1}, aigent {1 - agent_id} TS: {TS2}")
            return TS2, None, TS1

        best_value = float("-inf")
        best_move = None
        best_other_heuristic = float("-inf")
        for action, successor_state in self.problem.find_successors(graph).items():
            # Explore successors recursively with alpha-beta pruning
            heuristic, _, other_heuristic = self.coominimax(successor_state, 1 - agent_id, deep + 1)

            # Update best value and move based on maximizing/minimizing player
            if heuristic > best_value:
                best_value = heuristic
                best_move = action
                best_other_heuristic = other_heuristic

        return best_value, best_move, best_other_heuristic

    def semiminimax(self, graph: Graph, agent_id: int, deep: int) -> Tuple[int, Any, int]:

        if graph.game_over() or deep == self.cutoff:
            IS = graph.calc_heuristic_semi()
            print(f"{deep=}, IS-{agent_id}={IS[agent_id]}. IS-{1- agent_id}={IS[1-agent_id]}")
            return IS[agent_id], None, IS[1 - agent_id]

        best_value = float("-inf")
        best_move = None
        best_other_heuristic = float("-inf")
        for action, successor_state in self.problem.find_successors(graph).items():
            other_heuristic, _, heuristic = self.semiminimax(successor_state, 1 - agent_id, deep + 1)

            if heuristic > best_value:
                best_value = heuristic
                best_move = action
                best_other_heuristic = other_heuristic
            elif heuristic == best_value and other_heuristic > best_other_heuristic:
                best_move = action
                best_other_heuristic = other_heuristic

        return best_value, best_move, best_other_heuristic
