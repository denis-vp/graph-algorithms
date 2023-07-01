import random
import sys

from graph.undirected_graph import UndirectedGraph
from graph.vertex import Vertex


def generate_rand_undirected_graph(number_of_vertices: int, number_of_edges: int, graph: UndirectedGraph):
    """
    Generates a random undirected graph with the given number of vertices and edges.

    :param number_of_vertices: int, the number of vertices in the graph
    :param number_of_edges: int, the number of edges in the graph
    :param graph: UndirectedGraph, the graph to add the vertices and edges to

    :raises ValueError: if the number of edges is greater than the number of vertices squared
    """

    if number_of_edges > number_of_vertices * (number_of_vertices - 1) // 2:
        raise ValueError("Too many edges!")

    vertices = []
    for vertex in range(number_of_vertices):
        vertex = Vertex(vertex)

        graph.add_vertex(vertex)
        vertices.append(vertex)

    added_edges = []
    current_number_of_edges = 0

    while current_number_of_edges < number_of_edges:
        vertex_1 = random.choice(vertices)
        vertex_2 = random.choice(vertices)

        if not (vertex_1, vertex_2) in added_edges and not (vertex_2, vertex_1) in added_edges:
            graph.add_edge(vertex_1, vertex_2)
            added_edges.append((vertex_1, vertex_2))
            added_edges.append((vertex_2, vertex_1))

            current_number_of_edges += 1


def connected_components_kosaraju_undirected(graph: UndirectedGraph) -> list[UndirectedGraph]:
    """
    Returns the connected components of the given graph using Kosaraju's algorithm.

    :param graph: UndirectedGraph, the graph to find the connected components of

    :return: list[UndirectedGraph], the connected components of the graph,
             each connected component is a graph
    """

    default_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(100000000)

    def dfs(graph: UndirectedGraph, vertex: Vertex, visited: set[Vertex], processed: list[Vertex]):
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                dfs(graph, neighbor, visited, processed)
        processed.append(vertex)

    # using dfs generate the processed stack
    # processed is used to keep track of the order in which the vertices are processed
    processed = []
    visited = set()
    for vertex in graph.vertices:
        if vertex not in visited:
            visited.add(vertex)
            dfs(graph, vertex, visited, processed)

    visited = set()
    queue = []

    connected_components = []

    # using the processed set/stack, generate the connected components
    # the order in which the vertices are processed is important
    while processed:
        processed_vertex = processed.pop()

        # if the vertex has not been visited, it is part of a new connected component
        if processed_vertex not in visited:
            connected_component = UndirectedGraph()

            queue.append(processed_vertex)
            visited.add(processed_vertex)

            # search for all the vertices that are connected to the current vertex
            while queue:
                current_vertex = queue.pop(0)

                if not connected_component.is_vertex(current_vertex):
                    connected_component.add_vertex(current_vertex)

                # add all the neighbors of the current vertex to the queue
                # and search for all the vertices that are connected to the neighbors
                for neighbor in graph.get_neighbors(current_vertex):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

                        # used to create the connected component
                        if not connected_component.is_vertex(neighbor):
                            connected_component.add_vertex(neighbor)

                    # used to create the connected component
                    if not connected_component.is_edge(current_vertex, neighbor):
                        connected_component.add_edge(current_vertex, neighbor)

            # add the connected component to the list of connected components
            connected_components.append(connected_component)

    sys.setrecursionlimit(default_limit)

    return connected_components

