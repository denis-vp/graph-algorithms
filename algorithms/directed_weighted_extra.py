import heapq
import random
import numpy
from numpy import ndarray

from graph.directed_graph import GraphError, DirectedGraph
from graph.vertex import Vertex
from graph.weighted_directed_graph import WeightedDirectedGraph


def generate_rand_weighted_directed_graph(number_of_vertices: int, number_of_edges: int, graph: WeightedDirectedGraph):
    """
    Generates a random weighted directed graph with the given number of vertices and edges.

    :param number_of_vertices: int, the number of vertices in the graph
    :param number_of_edges: int, the number of edges in the graph
    :param graph: WeightedDirectedGraph, the graph to add the vertices and edges to

    :raises ValueError: if the number of edges is greater than the number of vertices squared
                        (the maximum number of edges)
    """

    if number_of_edges > number_of_vertices ** 2:
        raise ValueError("Too many edges!")

    vertices = []
    for vertex in range(number_of_vertices):
        vertex = Vertex(vertex)

        graph.add_vertex(vertex)
        vertices.append(vertex)

    added_edges = []
    current_number_of_edges = 0

    while current_number_of_edges < number_of_edges:
        start_vertex = random.choice(vertices)
        end_vertex = random.choice(vertices)

        if not (start_vertex, end_vertex) in added_edges:
            graph.add_edge(start_vertex, end_vertex, random.randint(1, 100))
            added_edges.append((start_vertex, end_vertex))

            current_number_of_edges += 1


def accessible_vertices_weighted_directed(graph: DirectedGraph, vertex: Vertex) -> set[Vertex]:
    """
    Finds all the vertices that are accessible from the given vertex in the given graph.

    :param graph: DirectedGraph, the graph to find the accessible vertices in
    :param vertex: Vertex, the vertex to find the accessible vertices from

    :return: set[Vertex], the set of accessible vertices

    :raises GraphError: if the given vertex is not in the graph
    """

    def dfs(graph: DirectedGraph, vertex: Vertex, visited: set[Vertex]):
        if vertex not in visited:
            visited.add(vertex)

            for neighbor in graph.get_outbound_vertices(vertex):
                dfs(graph, neighbor, visited)

    if not graph.is_vertex(vertex):
        raise GraphError("Vertex not in graph!")

    visited = set()
    dfs(graph, vertex, visited)

    return visited


def shortest_path_weighted_directed(graph: DirectedGraph, start: Vertex, end: Vertex) -> list[Vertex]:
    """
    Computes the shortest (min length) walk between start and end in graph.

    :param graph: DirectedGraph, the graph to find the shortest path in
    :param start: Vertex, the start point
    :param end: Vertex, the end point

    :return: list[Vertex], the shortest path between the start and end vertices
             [], empty list if no path exists

    :raises GraphError: if the start or end vertices are not in the graph
    """

    def bfs(graph: DirectedGraph, start: Vertex):
        dist = {start: 0}
        queue = [start]

        while queue:
            current = queue.pop(0)
            for neighbor in graph.get_outbound_vertices(current):
                if neighbor not in dist:
                    dist[neighbor] = dist[current] + 1
                    queue.append(neighbor)

        return dist

    if not graph.is_vertex(start) or not graph.is_vertex(end):
        raise GraphError("Vertex not in graph!")

    dist = bfs(graph, start)
    if end not in dist:
        return []

    walk = [end]
    current_length, current_vertex = dist[end], end
    while current_length:
        current_length -= 1
        for vertex in graph.get_inbound_vertices(current_vertex):
            if vertex in dist and dist[vertex] == current_length:
                current_vertex = vertex
                walk.append(current_vertex)
                break

    walk.reverse()
    return walk


def strongly_connected_tarjan_weighted_directed(graph: WeightedDirectedGraph) -> list[WeightedDirectedGraph]:
    """
    Finds the strongly connected components of the given graph using Tarjan's algorithm.

    :param graph: DirectedGraph, the graph to find the strongly connected components of

    :return: list[WeightedDirectedGraph], the list of strongly connected components
    """

    def implementation(vertex: Vertex, discovery_time, low: list, discovered: list, stack_member: list,
                       stack: list, graph: WeightedDirectedGraph, connected_components: list):

        discovered[vertex.value] = discovery_time
        low[vertex.value] = discovery_time
        discovery_time += 1

        stack_member[vertex.value] = True
        stack.append(vertex.value)

        for neighbor in graph.get_outbound_vertices(vertex):
            if discovered[neighbor.value] == -1:
                implementation(neighbor, discovery_time, low, discovered, stack_member, stack,
                               graph, connected_components)
                low[vertex.value] = min(low[vertex.value], low[neighbor.value])
            elif stack_member[neighbor.value]:
                low[vertex.value] = min(low[vertex.value], discovered[neighbor.value])

        extracted_value = -1
        if low[vertex.value] == discovered[vertex.value]:
            new_component = WeightedDirectedGraph()

            while extracted_value != vertex.value:
                extracted_value = stack.pop()
                extracted_vertex = Vertex(extracted_value)
                new_component.add_vertex(extracted_vertex)
                stack_member[extracted_value] = False

                for neighbor in graph.get_outbound_vertices(extracted_vertex):
                    if neighbor in new_component.vertices:
                        try:
                            new_component.add_edge(extracted_vertex, neighbor,
                                                   graph.get_edge_cost(extracted_vertex, neighbor))
                        except GraphError:
                            pass

                for neighbor in graph.get_inbound_vertices(extracted_vertex):
                    if neighbor in new_component.vertices:
                        try:
                            new_component.add_edge(neighbor, extracted_vertex,
                                                   graph.get_edge_cost(neighbor, extracted_vertex))
                        except GraphError:
                            pass

            connected_components.append(new_component)

    discovery_time = 0
    discovered = [-1] * graph.number_of_vertices
    low = [-1] * graph.number_of_vertices
    stack_member = [False] * graph.number_of_vertices
    stack = []

    connected_components = []
    for vertex in graph.vertices:
        if discovered[vertex.value] == -1:
            implementation(vertex, discovery_time, low, discovered, stack_member, stack,
                           graph, connected_components)

    return connected_components


def lowest_cost_path_matrix_weighted_directed(graph: WeightedDirectedGraph, start: Vertex, end: Vertex) -> tuple[list[Vertex], list[ndarray]]:
    """
    Computes the lowest cost path between start and end in graph.
    Utilizes the matrix multiplication algorithm.

    :param graph: WeightedDirectedGraph, the graph to find the lowest cost path in
    :param start: Vertex, the start point
    :param end: Vertex, the end point

    :return: list[Vertex], the lowest cost path between the start and end vertices
             [], empty list if no path exists

    :raises GraphError: if the start or end vertices are not in the graph
                        if a negative cycle is detected
    """

    if not graph.is_vertex(start) or not graph.is_vertex(end):
        raise GraphError("Vertex not in graph!")

    # list used to store the intermediate matrices
    intermediate_matrices = []

    # compute the adjacency matrix
    adj_matrix = numpy.full((graph.number_of_vertices, graph.number_of_vertices), numpy.inf)
    for vertex in graph.vertices:
        for neighbor in graph.get_outbound_vertices(vertex):
            # check for negative cycles
            if vertex == neighbor and graph.get_edge_cost(vertex, neighbor) < 0:
                raise GraphError("Negative cycle detected!")

            adj_matrix[vertex.value][neighbor.value] = graph.get_edge_cost(vertex, neighbor)

        adj_matrix[vertex.value][vertex.value] = 0

    intermediate_matrices.append(adj_matrix.copy())

    # compute the intermediate matrices
    for power in range(1, graph.number_of_vertices):
        result = numpy.full((graph.number_of_vertices, graph.number_of_vertices), numpy.inf)

        # compute the result matrix / "multiply" the previous intermediate matrix with the adjacency matrix
        for i in range(graph.number_of_vertices):
            for j in range(graph.number_of_vertices):
                for k in range(graph.number_of_vertices):
                    result[i][j] = min(result[i][j], intermediate_matrices[power - 1][i][k] + adj_matrix[k][j])

        intermediate_matrices.append(result)

        # check for negative cycles
        if numpy.any(numpy.diagonal(result) < 0):
            raise GraphError("Negative cycle detected!")

    walk = []
    # check if there is a path between the start and end vertices
    if intermediate_matrices[-1][start.value][end.value] == numpy.inf:
        return walk, intermediate_matrices

    # build the path
    walk.append(start)
    current_vertex = start
    visited = set()
    while current_vertex != end:
        visited.add(current_vertex)
        for neighbor in graph.get_outbound_vertices(current_vertex):
            # check for negative cycles
            if neighbor in visited and neighbor != current_vertex:
                raise GraphError("Negative cycle detected!")

            if intermediate_matrices[-1][current_vertex.value][end.value] ==\
               intermediate_matrices[-1][neighbor.value][end.value] + graph.get_edge_cost(current_vertex, neighbor):

                walk.append(neighbor)
                current_vertex = neighbor
                break

    return walk, intermediate_matrices


def get_path_from_matrix(graph: WeightedDirectedGraph, matrix: ndarray, start: Vertex, end: Vertex) -> list[Vertex]:
    if not graph.is_vertex(start) or not graph.is_vertex(end):
        raise GraphError("Vertex not in graph!")

    walk = []
    if matrix[start.value][end.value] == numpy.inf:
        return walk

    walk.append(start)
    current_vertex = start
    visited = set()
    while current_vertex != end:
        visited.add(current_vertex)
        for neighbor in graph.get_outbound_vertices(current_vertex):
            # check for negative cycles
            if neighbor in visited and neighbor != current_vertex:
                raise GraphError("Negative cycle detected!")

            if matrix[current_vertex.value][end.value] ==\
               matrix[neighbor.value][end.value] + graph.get_edge_cost(current_vertex, neighbor):

                walk.append(neighbor)
                current_vertex = neighbor
                break

    return walk


def number_of_distinct_minimum_cost_walks_weighted_directed(graph: WeightedDirectedGraph, start: Vertex, end: Vertex) -> int:
    """
    Computes the number of distinct minimum cost walks between start and end in graph.
    Utilizes Dijkstra's algorithm.

    :param graph: WeightedDirectedGraph, the graph to find the number of distinct minimum cost walks in
    :param start: Vertex, the start point
    :param end: Vertex, the end point

    :return: int, the number of distinct minimum cost walks between the start and end vertices
    """

    if not graph.is_vertex(start) or not graph.is_vertex(end):
        raise GraphError("Vertex not in graph!")

    # initialize the distances and counts dictionaries
    distances = {vertex: numpy.inf for vertex in graph.vertices}
    counts = {vertex: 0 for vertex in graph.vertices}

    # initialize the priority queue with (cost, vertex) pairs
    queue = [(0, start)]
    distances[start] = 0
    counts[start] = 1

    while queue:
        current_cost, current_vertex = heapq.heappop(queue)

        # ignore outdated entries (we already found a better path to the vertex)
        if current_cost > distances[current_vertex]:
            continue

        for neighbor in graph.get_outbound_vertices(current_vertex):
            new_cost = current_cost + graph.get_edge_cost(current_vertex, neighbor)

            # if we found a better path to the neighbor, update the distances and counts dictionaries
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                counts[neighbor] = counts[current_vertex]
                heapq.heappush(queue, (new_cost, neighbor))

            # if we found another path with the same cost, update the counts dictionary
            elif new_cost == distances[neighbor]:
                counts[neighbor] += counts[current_vertex]

    return counts[end]


def number_of_distinct_walks_weighted_directed(graph: WeightedDirectedGraph, start: Vertex, end: Vertex) -> int:
    """
    Computes the number of distinct walks between start and end in graph.

    :param graph: WeightedDirectedGraph, the graph to find the number of distinct walks in
    :param start: Vertex, the start point
    :param end: Vertex, the end point

    :return: int, the number of distinct walks between the start and end vertices
    """

    def topological_sort(graph: WeightedDirectedGraph):

        def dfs(vertex: Vertex, visited: set[Vertex], ordering: list[Vertex]):
            visited.add(vertex)
            for neighbor in graph.get_outbound_vertices(vertex):
                if neighbor not in visited:
                    dfs(neighbor, visited, ordering)
            ordering.append(vertex)

        visited = set()
        ordering = []

        for vertex in graph.vertices:
            if vertex not in visited:
                dfs(vertex, visited, ordering)

        ordering.reverse()
        return ordering

    if not graph.is_vertex(start) or not graph.is_vertex(end):
        raise GraphError("Vertex not in graph!")

    ordering = topological_sort(graph)

    # initialize the counts dictionary
    counts = {vertex: 0 for vertex in graph.vertices}
    counts[start] = 1

    # iterate through the vertices in topological order
    for vertex in ordering:
        # update the counts dictionary for each neighbor of the current vertex
        for neighbor in graph.get_outbound_vertices(vertex):
            counts[neighbor] += counts[vertex]

    return counts[end]
