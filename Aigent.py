import abc
from Tile import Tile
from name_tuppels import Point


class Aigent(abc.ABC, Tile):
    def __init__(self, starting_point: Point, _id):
        super().__init__(starting_point)
        self.id = _id
        self.score = 0
        self.pakages = set()

    @abc.abstractmethod
    def make_move(self, graph):
        """
        Consider fragile.
        Consider update packages.


        :return:
        """
        pass

    def update_packages(self, timer):
        self.pakages = {package for package in self.pakages if package.from_time <= timer <= package.dead_line}

    def game_over(self):
        return len(self.pakages) == 0

    def no_op(self):
        pass

    def move_agent(self, graph, new_location):
        current_point = self.point
        edge_crossed = frozenset({current_point, new_location})
        if edge_crossed in graph.fragile:
            graph.remove_edge(edge_crossed)
            graph.remove_fragile_edge(edge_crossed)
        # pick package from new location
        taken_packages = set()
        for package in graph.relevant_packages:
            if package.point == new_location:
                taken_packages.add(package)
                self.pakages.add(package)
                package.picked_up = True
                graph.remove_tile(package.point)
        graph.relevant_packages -= taken_packages
        graph.all_packages -= taken_packages
        # deliver package
        if len(self.pakages) > 0:
            deliver_packages = set()
            for package in self.pakages:
                if package.point_dst == new_location:
                    deliver_packages.add(package)
                    graph.remove_tile(package.point_dst)
                    self.score += 1
            self.pakages -= deliver_packages

        # move the agent
        if self.point != new_location:
            self.point = new_location
            graph.move_agent(current_point, new_location)

    def move_agent_without_packages(self, graph, new_location):
        edge_crossed = {self.point, new_location}
        if edge_crossed in graph.fragile:
            graph.remove_edge(edge_crossed)
            graph.remove_fragile_edge(edge_crossed)
        # move the agent
        graph.move_agent(self.point, new_location)
        self.point = new_location

    def __key(self):
        return self.point, self.symbol, tuple(self.pakages), self.score

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Aigent):
            return False

        return self.__key() == other.__key()

    def string_state(self):
        return f"{self.symbol}: packages:{[pakage.to_string() for pakage in self.pakages]}, score: {self.score}"


class AiAigent(Aigent):
    def __init__(self, starting_point: Point, _id):
        super().__init__(starting_point, _id)
        self.symbol = f"AI{_id} "
        self.moves = []
        self.problem = None
        self.algo = None

    def make_move(self, graph):
        pass

