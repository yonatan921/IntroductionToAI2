from typing import Callable

from Graph import Graph


class Problem:
    def __init__(self, init_state: Graph, goal_state: Callable[[Graph], bool]):
        self.init_state = init_state
        self.goal_state = goal_state
