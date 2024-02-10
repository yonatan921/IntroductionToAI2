import copy
from typing import Callable

from Graph import Graph


class Problem:
    def __init__(self, init_state: Graph, goal_state: Callable[[Graph], bool]):
        self.init_state = init_state
        self.goal_state = goal_state

    @staticmethod
    def find_successors(graph, aigent, update_timer):
        successors = {}
        for available_point in graph.available_moves(aigent.point):
            new_graph = copy.deepcopy(graph)
            new_graph.update_packages()
            if update_timer:
                new_graph.timer += 1
                new_graph.agents[1].move_agent(new_graph, available_point)
            else:
                new_graph.agents[0].move_agent(new_graph, available_point)
            # aigent.move_agent(new_graph, available_point)
            successors[available_point] = new_graph

        return successors
