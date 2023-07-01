from graph.directed_graph import GraphError
from graph.vertex import Vertex


class UndirectedGraph:

    """
    An undirected graph is a graph where each edge is bidirectional.
    It is represented by a dictionary:
        - _neighbors: maps each vertex to a list of its neighbors
    """

    def __init__(self):
        """
        Initializes the graph.
        """

        self._neighbors = {}

    @property
    def number_of_vertices(self) -> int:
        """
        Returns the number of vertices in the graph.

        :return: int, the number of vertices
        """

        return len(self._neighbors)

    @property
    def vertices(self):
        """
        Returns an iterator over the vertices in the graph.

        :return: generator, the vertices
        """

        for vertex in self._neighbors:
            yield vertex

    @property
    def number_of_edges(self) -> int:
        """
        Returns the number of edges in the graph.

        :return: int, the number of edges
        """

        return len(list(self.edges))

    @property
    def edges(self):
        """
        Returns a generator of the edges in the graph.

        :return: generator, the edges
        """

        seen_edges = []
        for vertex in self._neighbors:
            for neighbor in self._neighbors[vertex]:
                if (seen_edge := {vertex, neighbor}) not in seen_edges:
                    seen_edges.append(seen_edge)
                    yield vertex, neighbor

    # ----------------------- #

    def is_vertex(self, vertex: Vertex) -> bool:
        """
        Checks if a vertex is in the graph.

        :param vertex: Vertex, the vertex to check

        :return: True if the vertex is in the graph, False otherwise
        """

        return vertex in self._neighbors

    def is_edge(self, vertex_1: Vertex, vertex_2: Vertex) -> bool:
        """
        Checks if an edge is in the graph.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge

        :return: True if the edge is in the graph, False otherwise

        :raises GraphError: if one of the vertices is not in the graph
        """

        if vertex_1 not in self._neighbors or vertex_2 not in self._neighbors:
            raise GraphError("Invalid vertex!")

        return vertex_2 in self._neighbors[vertex_1]

    # ----------------------- #

    def get_degree(self, vertex: Vertex) -> int:
        """
        Returns the degree of a vertex.

        :param vertex: Vertex, the vertex

        :return: int, the degree of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._neighbors:
            raise GraphError("Invalid vertex!")

        return len(self._neighbors[vertex])

    def get_neighboring_edges(self, vertex: Vertex):
        """
        Returns a generator of the edges that have the given vertex as a neighbor.

        :param vertex: Vertex, the vertex

        :return: generator, the neighboring edges

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._neighbors:
            raise GraphError("Invalid vertex!")

        for neighbor in self._neighbors[vertex]:
            yield vertex, neighbor

    def get_neighbors(self, vertex: Vertex):
        """
        Returns a generator of the neighbors of a vertex.

        :param vertex: Vertex, the vertex

        :return: generator, the neighbors

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._neighbors:
            raise GraphError("Invalid vertex!")

        for neighbor in self._neighbors[vertex]:
            yield neighbor

    # ----------------------- #

    def add_vertex(self, vertex: Vertex):
        """
        Adds a vertex to the graph.

        :param vertex: Vertex, the vertex to add

        :raises GraphError: if the vertex already exists
        """

        if vertex in self._neighbors:
            raise GraphError("Vertex already exists!")

        self._neighbors[vertex] = []

    def remove_vertex(self, vertex: Vertex):
        """
        Removes a vertex from the graph.

        :param vertex: Vertex, the vertex to remove

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._neighbors:
            raise GraphError("Invalid vertex!")

        for neighbor in self._neighbors[vertex]:
            self._neighbors[neighbor].remove(vertex)

        del self._neighbors[vertex]

    def add_edge(self, vertex_1: Vertex, vertex_2: Vertex, cost: int = None):
        """
        Adds an edge to the graph.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge
        :param cost: int, the cost of the edge (used in weighted graph) UNUSED IN THIS CLASS

        :raises GraphError: if one of the vertices is not in the graph or if the edge already exists
        """

        if vertex_1 not in self._neighbors or vertex_2 not in self._neighbors:
            raise GraphError("Invalid vertex!")

        if vertex_2 in self._neighbors[vertex_1]:
            raise GraphError("Edge already exists!")

        self._neighbors[vertex_1].append(vertex_2)
        self._neighbors[vertex_2].append(vertex_1)

    def remove_edge(self, vertex_1: Vertex, vertex_2: Vertex):
        """
        Removes an edge from the graph.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge

        :raises GraphError: if one of the vertices is not in the graph or if the edge does not exist
        """

        if vertex_1 not in self._neighbors or vertex_2 not in self._neighbors:
            raise GraphError("Invalid vertex!")

        if vertex_2 not in self._neighbors[vertex_1]:
            raise GraphError("Edge does not exist!")

        self._neighbors[vertex_1].remove(vertex_2)
        self._neighbors[vertex_2].remove(vertex_1)

    # ----------------------- #

    def read_from_file_big(self, file_path: str):
        """
        Reads a graph from a file.
        The file contains the edges of the graph and the isolated vertices.
        An edge is represented by two vertices. Ex: 1 2 means that there is an edge from 1 to 2.
        An isolated vertex is represented by its number and -1. Ex: 1 -1 means that there is an isolated vertex with the number 1.

        :param file_path: str, the path to the file
        """

        with open(file_path, "r") as file:
            for index, line in enumerate(file):
                if index == 0:
                    number_of_vertices = int(line.split()[0])
                    for vertex in range(number_of_vertices):
                        self.add_vertex(Vertex(vertex))
                    continue

                line = line.strip().split()
                vertex_1, vertex_2 = Vertex(int(line[0])), Vertex(int(line[1]))

                self.add_edge(vertex_1, vertex_2)

    def read_from_file_big_with_costs(self, file_path: str):
        """
        Reads a graph from a file in big format that also contains the costs of the edges.
        The costs will be ignored.

        :param file_path: str, the path to the file
        """

        with open(file_path, "r") as file:
            for index, line in enumerate(file):
                if index == 0:
                    number_of_vertices = int(line.split()[0])
                    for vertex in range(number_of_vertices):
                        self.add_vertex(Vertex(vertex))
                    continue

                line = line.strip().split()
                vertex_1, vertex_2, cost = Vertex(int(line[0])), Vertex(int(line[1])), int(line[2])

                if not self.is_edge(vertex_1, vertex_2):
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

                vertex_1, vertex_2 = Vertex(int(line[0])), Vertex(int(line[1]))

                for vertex in [vertex_1, vertex_2]:
                    if vertex not in self._neighbors:
                        self.add_vertex(vertex)

                self.add_edge(vertex_1, vertex_2)

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
                        file.write(f"{vertex} {neighbor}")

                        if vertex != list(self._neighbors.keys())[-1] or neighbor != self._neighbors[vertex][-1]:
                            file.write("\n")

    # ----------------------- #

    def __str__(self) -> str:
        """
        Returns a string representation of the graph.

        :return: str, the string representation of the graph
        """

        string = f"{self.number_of_vertices} {self.number_of_edges}"

        seen_edges = []
        for vertex in self._neighbors:
            if not self._neighbors[vertex]:
                string += f"\n{vertex} -1"
                continue

            for neighbor in self._neighbors[vertex]:
                seen_edge = {vertex, neighbor}
                if (seen_edge := {vertex, neighbor}) not in seen_edges:
                    seen_edges.append(seen_edge)
                    string += f"\n{vertex} -- {neighbor}"

        return string

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.

        :return: str, the string representation of the graph
        """

        return f"UndirectedGraph({self.number_of_vertices}, {self.number_of_edges})"
