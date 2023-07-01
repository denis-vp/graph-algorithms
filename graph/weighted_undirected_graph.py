from graph.directed_graph import GraphError
from graph.undirected_graph import UndirectedGraph
from graph.vertex import Vertex


class WeightedUndirectedGraph(UndirectedGraph):

    """
    A weighted undirected graph is an undirected graph where each edge has a cost.
    It is represented by two dictionaries:
        - _neighbors: maps each vertex to a list of its neighbors
        - _weights: maps each edge to its cost
    """

    def __init__(self):
        """
        Initializes the graph.
        """

        super().__init__()
        self._weights = {}

    # ----------------------- #

    def get_edge_cost(self, vertex_1: Vertex, vertex_2: Vertex) -> int:
        """
        Returns the cost of the edge between vertex_1 and vertex_2.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge

        :return: int, the cost of the edge

        :raises GraphError: if vertex_1 or vertex_2 are not in the graph or if the edge does not exist
        """

        if vertex_1 not in self._neighbors or vertex_2 not in self._neighbors:
            raise GraphError("Invalid vertex!")

        if vertex_2 not in self._neighbors[vertex_1]:
            raise GraphError("Invalid edge!")

        return self._weights[{vertex_1, vertex_2}]

    def set_edge_cost(self, vertex_1: Vertex, vertex_2: Vertex, cost: int):
        """
        Sets the cost of the edge between vertex_1 and vertex_2.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge
        :param cost: int, the cost of the edge

        :raises GraphError: if vertex_1 or vertex_2 are not in the graph or if the edge does not exist
        """

        if vertex_1 not in self._neighbors or vertex_2 not in self._neighbors:
            raise GraphError("Invalid vertex!")

        if vertex_2 not in self._neighbors[vertex_1]:
            raise GraphError("Invalid edge!")

        self._weights[{vertex_1, vertex_2}] = cost

    # ----------------------- #

    def remove_vertex(self, vertex: Vertex):
        """
        Removes a vertex from the graph.
        :param vertex: Vertex, the vertex to be removed

        :raises GraphError: if vertex is not in the graph
        """

        if vertex not in self._neighbors:
            raise GraphError("Invalid vertex!")

        for neighbor in self._neighbors[vertex]:
            self._neighbors[neighbor].remove(vertex)
            self._weights.pop({vertex, neighbor})

        del self._neighbors[vertex]

    def add_edge(self, vertex_1: Vertex, vertex_2: Vertex, cost: int = 0):
        """
        Adds an edge between vertex_1 and vertex_2.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge
        :param cost: int, the cost of the edge

        :raises GraphError: if vertex_1 or vertex_2 are not in the graph or if the edge already exists
        """

        super().add_edge(vertex_1, vertex_2)
        self._weights[{vertex_1, vertex_2}] = cost

    def remove_edge(self, vertex_1: Vertex, vertex_2: Vertex):
        """
        Removes an edge between vertex_1 and vertex_2.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge

        :raises GraphError: if vertex_1 or vertex_2 are not in the graph or if the edge does not exist
        """

        super().remove_edge(vertex_1, vertex_2)
        self._weights.pop({vertex_1, vertex_2})

    # ----------------------- #

    def read_from_file_big(self, file_path: str):
        """
        Reads a graph from a file in big format.
        First line contains the number of vertices and the number of edges.
        The vertices are numbered from 0 to n - 1.
        The next lines contain the edges. Ex: 1 2 means that there is an edge from 1 to 2.

        :param file_path: str, the path to the file
        """

        with open(file_path, "r") as file:
            for index, line in enumerate(file):
                if index == 0:
                    number_of_vertices = int(line.split()[0])
                    for vertex in range(number_of_vertices):
                        self.add_vertex(Vertex(vertex))
                    continue

                line = line.split()
                vertex_1, vertex_2, cost = Vertex(int(line[0])), Vertex(int(line[1])), int(line[2])

                self.add_edge(vertex_1, vertex_2, cost)

    def read_from_file(self, file_path: str):
        """
        Reads a graph from a file.
        The file contains the edges of the graph and the isolated vertices.
        An edge is represented by two vertices. Ex: 1 2 means that there is an edge from 1 to 2.
        An isolated vertex is represented by its number and -1. Ex: 1 -1 means that there is an isolated vertex with the number 1.

        :param file_path: str, the path to the file
        """

        with open(file_path, "r") as file:
            for line in file:
                line = line.split()

                if line[1] == "-1":
                    self.add_vertex(Vertex(int(line[0])))
                    continue

                vertex_1, vertex_2, cost = Vertex(int(line[0])), Vertex(int(line[1])), int(line[2])

                for vertex in [vertex_1, vertex_2]:
                    if vertex not in self._neighbors:
                        self.add_vertex(vertex)

                self.add_edge(vertex_1, vertex_2, cost)

    def write_to_file(self, file_path: str):
        """
        Writes the graph to a file.

        :param file_path: str, the path to the file
        """

        with open(file_path, "w") as file:
            seen_edges = []
            for vertex in self._neighbors:
                if not self._neighbors[vertex]:
                    file.write(f"{vertex} -1")
                    if vertex != list(self._neighbors.keys())[-1]:
                        file.write("\n")
                    continue

                for neighbor in self._neighbors[vertex]:
                    if (seen_edge := {vertex, neighbor}) not in seen_edges:
                        seen_edges.append(seen_edge)
                        file.write(f"{vertex} {neighbor} {self._weights[{vertex, neighbor}]}")
                        if vertex != list(self._neighbors.keys())[-1] or neighbor != self._neighbors[vertex][-1]:
                            file.write("\n")

    # ----------------------- #

    def __str__(self) -> str:
        """
        Returns a string representation of the graph.

        :return: str, the string representation of the graph
        """

        string = f"{self.number_of_vertices} {self.number_of_edges}"

        for vertex in self._neighbors:
            if not self._neighbors[vertex]:
                string += f"\n{vertex} -1"
                continue

            for neighbor in self._neighbors[vertex]:
                string += f"\n{vertex} -- {neighbor} : {self._weights[{vertex, neighbor}]}"

        return string

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.

        :return: str, the string representation of the graph
        """

        return f"WeightedUndirectedGraph({self.number_of_vertices}, {self.number_of_edges})"
