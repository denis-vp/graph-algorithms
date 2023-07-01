from graph.vertex import Vertex


class GraphError(Exception):
    pass


class DirectedGraph:

    """
    A directed graph is a graph where each edge has a direction.
    It is represented by two dictionaries:
        - _predecessors: maps each vertex to a list of its predecessors
        - _successors: maps each vertex to a list of its successors
    """

    def __init__(self):
        """
        Initializes the graph.
        """

        self._predecessors = {}
        self._successors = {}

    @property
    def number_of_vertices(self) -> int:
        """
        Returns the number of vertices in the graph.

        :return: int, the number of vertices
        """

        return len(self._predecessors)

    @property
    def vertices(self):
        """
        Returns a generator of the vertices in the graph.

        :return: generator, the vertices
        """

        return self._predecessors.keys()

    @property
    def number_of_edges(self) -> int:
        """
        Returns the number of edges in the graph.

        :return: int, the number of edges
        """

        return sum([len(self._predecessors[vertex]) for vertex in self._predecessors])

    @property
    def edges(self):
        """
        Returns a generator of the edges in the graph.

        :return: generator, the edges
        """

        for vertex in self._predecessors:
            for predecessor in self._predecessors[vertex]:
                yield predecessor, vertex

    # ----------------------- #

    def is_vertex(self, vertex: Vertex) -> bool:
        """
        Checks if a vertex is in the graph.

        :param vertex: Vertex, the vertex to check

        :return: True if the vertex is in the graph, False otherwise
        """

        return vertex in self._predecessors

    def is_edge(self, vertex_1: Vertex, vertex_2: Vertex) -> bool:
        """
        Checks if an edge is in the graph.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge

        :return: True if the edge is in the graph, False otherwise

        :raises GraphError: if one of the vertices is not in the graph
        """

        if vertex_1 not in self._predecessors or vertex_2 not in self._predecessors:
            raise GraphError("Invalid vertex!")

        return vertex_2 in self._successors[vertex_1]

    # ----------------------- #

    def get_in_degree(self, vertex: Vertex) -> int:
        """
        Returns the in-degree of a vertex.

        :param vertex: Vertex, the vertex

        :return: int, the in-degree of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        return len(self._predecessors[vertex])

    def get_inbound_edges(self, vertex: Vertex):
        """
        Returns a generator of the inbound edges of a vertex.

        :param vertex: Vertex, the vertex

        :return: generator, the inbound edges of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        for predecessor in self._predecessors[vertex]:
            yield predecessor, vertex

    def get_inbound_vertices(self, vertex: Vertex):
        """
        Returns a generator of the inbound vertices of a vertex.

        :param vertex: Vertex, the vertex

        :return: generator, the inbound vertices of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        for predecessor in self._predecessors[vertex]:
            yield predecessor

    def get_out_degree(self, vertex: Vertex) -> int:
        """
        Returns the out-degree of a vertex.

        :param vertex: Vertex, the vertex

        :return: int, the out-degree of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        return len(self._successors[vertex])

    def get_outbound_edges(self, vertex: Vertex):
        """
        Returns a generator of the outbound edges of a vertex.

        :param vertex: Vertex, the vertex

        :return: generator, the outbound edges of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        for successor in self._successors[vertex]:
            yield vertex, successor

    def get_outbound_vertices(self, vertex: Vertex):
        """
        Returns a generator of the outbound vertices of a vertex.

        :param vertex: Vertex, the vertex

        :return: generator, the outbound vertices of the vertex

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        for successor in self._successors[vertex]:
            yield successor

    # ----------------------- #

    def add_vertex(self, vertex: Vertex):
        """
        Adds a vertex to the graph.

        :param vertex: Vertex, the vertex to add

        :raises GraphError: if the vertex already exists
        """

        if vertex in self._predecessors:
            raise GraphError("Vertex already exists!")

        self._predecessors[vertex] = []
        self._successors[vertex] = []

    def remove_vertex(self, vertex: Vertex):
        """
        Removes a vertex from the graph.

        :param vertex: Vertex, the vertex to remove

        :raises GraphError: if the vertex is not in the graph
        """

        if vertex not in self._predecessors:
            raise GraphError("Invalid vertex!")

        for predecessor in self._predecessors[vertex]:
            self._successors[predecessor].remove(vertex)

        for successor in self._successors[vertex]:
            self._predecessors[successor].remove(vertex)

        del self._predecessors[vertex]
        del self._successors[vertex]

    def add_edge(self, vertex_1: Vertex, vertex_2: Vertex, cost: int = None):
        """
        Adds an edge to the graph.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge
        :param cost: int, the cost of the edge (used in weighted graph) UNUSED IN THIS CLASS

        :raises GraphError: if one of the vertices is not in the graph or if the edge already exists
        """

        if vertex_1 not in self._predecessors or vertex_2 not in self._predecessors:
            raise GraphError("Invalid vertex!")

        if vertex_2 in self._successors[vertex_1]:
            raise GraphError("Edge already exists!")

        self._predecessors[vertex_2].append(vertex_1)
        self._successors[vertex_1].append(vertex_2)

    def remove_edge(self, vertex_1: Vertex, vertex_2: Vertex):
        """
        Removes an edge from the graph.

        :param vertex_1: Vertex, the first vertex of the edge
        :param vertex_2: Vertex, the second vertex of the edge

        :raises GraphError: if one of the vertices is not in the graph or if the edge does not exist
        """

        if vertex_1 not in self._predecessors or vertex_2 not in self._predecessors:
            raise GraphError("Invalid vertex!")

        if vertex_2 not in self._successors[vertex_1]:
            raise GraphError("Edge does not exist!")

        self._predecessors[vertex_2].remove(vertex_1)
        self._successors[vertex_1].remove(vertex_2)

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
                line = line.strip().split()

                if line[1] == "-1":
                    self.add_vertex(Vertex(int(line[0])))
                    continue

                vertex_1, vertex_2 = Vertex(int(line[0])), Vertex(int(line[1]))

                for vertex in [vertex_1, vertex_2]:
                    if vertex not in self._predecessors:
                        self.add_vertex(vertex)

                self.add_edge(vertex_1, vertex_2)

    def write_to_file(self, file_path: str):
        """
        Writes the graph to a file.

        :param file_path: str, the path to the file
        """

        with open(file_path, "w") as file:
            for vertex, predecessors in self._predecessors.items():
                if not predecessors and not self._successors[vertex]:
                    file.write(f"{vertex} -1")
                    if vertex != list(self._predecessors.keys())[-1]:
                        file.write("\n")
                    continue

                for predecessor in predecessors:
                    file.write(f"{predecessor} {vertex}")
                    if predecessor != predecessors[-1] or vertex != list(self._predecessors.keys())[-1]:
                        file.write("\n")

    # ----------------------- #

    def __str__(self) -> str:
        """
        Returns a string representation of the graph.

        :return: str, the string representation of the graph
        """

        string = f"{self.number_of_vertices} {self.number_of_edges}"
        for vertex, predecessors in self._predecessors.items():
            for predecessor in predecessors:
                if not predecessors and not self._successors[vertex]:
                    string += f"\n{vertex} -1"
                    continue

                string += f"\n{predecessor} -> {vertex}"

        return string

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.

        :return: str, the string representation of the graph
        """

        return f"DirectedGraph({self.number_of_vertices}, {self.number_of_edges})"
