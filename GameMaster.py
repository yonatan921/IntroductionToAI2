import copy

from Graph import Graph
from MiniMax import MiniMax
from Problem import Problem
from SearchALgo import GreedySearch, AStar, RealTimeAStar


class GameMaster:
    def __init__(self, graph: Graph, packages):
        # string_to_algo = {"Astar": AStar(), "Gready": GreedySearch(), "RealTime": RealTimeAStar(50)}
        self.graph = graph
        self.turn_index = 0
        self.all_packages = packages
        self.update_packages()
        self.graph.agents[0].problem = Problem(self.graph, lambda g: g.game_over())
        self.mini_max_algo = MiniMax(self.graph.agents[0].problem, 4)
        # self.graph.agents[0].algo = mini_max_algo
        # self.graph.agents[0].run_algo()

    def start_game(self):
        while not self.game_over():
            print(self)
            self.graph.timer += 1
            for aigent in self.graph.agents:
                self.update_packages()
                action = self.mini_max_algo.mini_max_decision(self.graph, aigent.id)
                aigent.move_agent(self.graph, action)
        print(self)

    def game_over(self):
        return self.graph.game_over()

    def update_packages(self):
        self.update_graph_packages()
        self.update_aigent_packages()

    def update_aigent_packages(self):
        for aigent in self.graph.agents:
            aigent.update_packages(self.graph.timer)

    def update_graph_packages(self):
        self.graph.update_packages()

    def __str__(self):
        return str(self.graph)


