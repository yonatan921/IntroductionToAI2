from Graph import Graph
from Problem import Problem
from SearchALgo import GreedySearch, AStar, RealTimeAStar


class GameMaster:
    def __init__(self, graph: Graph, packages, algo_string):
        string_to_algo = {"Astar": AStar(), "Gready": GreedySearch(), "RealTime": RealTimeAStar(50)}
        self.graph = graph
        self.turn_index = 0
        self.all_packages = packages
        self.update_packages()
        self.graph.agents[0].problem = Problem(self.graph, lambda g: g.game_over())
        self.graph.agents[0].algo = string_to_algo[algo_string]
        self.graph.agents[0].run_algo()

    def start_game(self):
        while not self.game_over():
            print(self)
            self.graph.timer += 1
            self.turn_index += 1
            self.update_packages()
            self.graph.agents[self.turn_index % len(self.graph.agents)].make_move(self.graph)

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
