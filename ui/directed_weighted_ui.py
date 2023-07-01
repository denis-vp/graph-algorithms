import copy
from texttable import Texttable

from graph.directed_graph import GraphError
from graph.vertex import Vertex
from graph.weighted_directed_graph import WeightedDirectedGraph
from algorithms.directed_weighted_extra import generate_rand_weighted_directed_graph, \
    strongly_connected_tarjan_weighted_directed, accessible_vertices_weighted_directed, shortest_path_weighted_directed, \
    lowest_cost_path_matrix_weighted_directed, number_of_distinct_minimum_cost_walks_weighted_directed, \
    number_of_distinct_walks_weighted_directed, get_path_from_matrix


class UiError(Exception):
    pass


class DirectedWeightedUi:

    def __init__(self, graph: WeightedDirectedGraph):
        self.__graph = graph

        self.__original_graph = None
        self.__is_copy = False

    def run_ui(self):
        DirectedWeightedUi.__print_title()

        options = {
            "1": self.__get_number_of_vertices,
            "2": self.__check_if_an_edge_exists,
            "3": self.__print_the_vertices,
            "4": self.__get_the_in_degree_of_a_vertex,
            "5": self.__get_the_out_degree_of_a_vertex,
            "6": self.__print_the_inbound_edges_of_a_vertex,
            "7": self.__print_the_outbound_edges_of_a_vertex,
            "8": self.__get_the_cost_of_an_edge,
            "9": self.__modify_the_cost_of_an_edge,
            "10": self.__add_an_edge,
            "11": self.__remove_an_edge,
            "12": self.__add_a_vertex,
            "13": self.__remove_a_vertex,
            "14": self.__read_the_graph_from_a_file_big,
            "15": self.__read_the_graph_from_a_file,
            "16": self.__write_the_graph_to_a_file,
            "17": self.__get_all_accessible_vertices,
            "18": self.__get_shortest_path_two_vertices,
            "19": self.__get_strongly_connected_components_tarjan,
            "20": self.__number_of_isolated_vertices,
            "21": self.__lowest_cost_path_matrix_multiplication,
            "22": self.__number_of_distinct_minimum_cost_walks,
            "23": self.__number_of_distinct_walks,
            "c": self.__create_a_copy_of_the_graph,
            "u": self.__restore_the_original_graph,
            "r": self.__create_a_random_graph,
            "l": self.__load_a_premade_graph,
            "p": self.__print_the_graph,
            "x": DirectedWeightedUi.__exit
        }

        while True:
            DirectedWeightedUi.__print_menu()

            command = input("\nEnter a command: ")

            try:
                options[command]()

            except UiError as error:
                print(self.__make_red(str(error)))

            except KeyError as error:
                print(self.__make_red(f"Invalid command: {error}!"))

            except Exception as error:
                print(self.__make_red(f"Invalid command: {error}!"))

    # ----------------------- #

    @staticmethod
    def __get_vertex() -> Vertex:
        return Vertex(int(input("\nEnter a vertex: ")))

    @staticmethod
    def __get_edge() -> tuple[Vertex, Vertex]:
        edge = input("\nEnter an edge: ").split(" ")
        if len(edge) != 2:
            raise UiError(DirectedWeightedUi.__make_red("Invalid edge!"))

        return Vertex(int(edge[0])), Vertex(int(edge[1]))

    # ----------------------- #

    @staticmethod
    def __make_red(text: str):
        return "\033[91m{}\033[00m".format(text)

    @staticmethod
    def __print_title():
        print()
        print("|-------------------------------|")
        print("|  Graph - Directed - Weighted  |")
        print("|-------------------------------|")

    @staticmethod
    def __print_menu():
        print("\n1: Get the number of vertices")
        print("2: Check if an edge exists")
        print("3: Print the vertices")
        print(" ---------------------------------- ")
        print("4: Get the in degree of a vertex")
        print("5: Get the out degree of a vertex")
        print("6: Print the inbound edges of a vertex")
        print("7: Print the outbound edges of a vertex")
        print(" ---------------------------------- ")
        print("8: Get the cost of an edge")
        print("9: Modify the cost of an edge")
        print(" ---------------------------------- ")
        print("10: Add an edge")
        print("11: Remove an edge")
        print("12: Add a vertex")
        print("13: Remove a vertex")
        print(" ---------------------------------- ")
        print("14: Read the graph from a file big")
        print("15: Read the graph to a file (small)")
        print("16: Write the graph to a file")
        print(" ---------------------------------- ")
        print("17: Get all accessible vertices from a vertex")
        print("18: Get the shortest path between two vertices")
        print("19: Get strongly connected components (Tarjan)")
        print("20: Get the number of isolated vertices")
        print("21: Get lowest cost walk between two vertices (Matrix multiplication)")
        print("22: Get the number of distinct minimum cost walks between two vertices")
        print("23: Get the number of distinct walks between two vertices")
        print(" ---------------------------------- ")
        print("c: Create a copy of the graph and operate on it")
        print("u: Restore to the original graph")
        print(" ---------------------------------- ")
        print("r: Create a random graph")
        print("l: Load a premade graph")
        print("p: Print the graph")
        print("x: Exit")

    # ----------------------- #

    def __get_number_of_vertices(self):
        if number_of_vertices := self.__graph.number_of_vertices:
            print(f"\nThe number of vertices is: {number_of_vertices}")

        else:
            print("\nThe graph is empty!")

    def __check_if_an_edge_exists(self):
        start_vertex, end_vertex = DirectedWeightedUi.__get_edge()

        try:
            if self.__graph.is_edge(start_vertex, end_vertex):
                print("The edge exists!")
            else:
                print("The edge does not exist!")
        except GraphError:
            print("The edge does not exist!")

    def __print_the_vertices(self):
        if vertices := self.__graph.vertices:
            print("\nThe vertices are:")
            for vertex in vertices:
                print(vertex)

        else:
            print("\nThe graph is empty!")

    # ----------------------- #

    def __get_the_out_degree_of_a_vertex(self):
        vertex = DirectedWeightedUi.__get_vertex()

        try:
            print(f"The out degree of the vertex is: {self.__graph.get_out_degree(vertex)}")
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __get_the_in_degree_of_a_vertex(self):
        vertex = DirectedWeightedUi.__get_vertex()

        try:
            print(f"The in degree of the vertex is: {self.__graph.get_in_degree(vertex)}")
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __print_the_outbound_edges_of_a_vertex(self):
        vertex = DirectedWeightedUi.__get_vertex()

        try:
            if edges := self.__graph.get_outbound_edges(vertex):
                print("The outbound edges of the vertex are:")
                for edge in edges:
                    start_vertex, end_vertex = edge
                    print(f"{start_vertex} -> {end_vertex}")

            else:
                print("The vertex has no outbound edges!")

        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __print_the_inbound_edges_of_a_vertex(self):
        vertex = DirectedWeightedUi.__get_vertex()

        try:
            if edges := self.__graph.get_inbound_edges(vertex):
                print("The inbound edges of the vertex are:")
                for edge in edges:
                    start_vertex, end_vertex = edge
                    print(f"{start_vertex} -> {end_vertex}")

            else:
                print("The vertex has no inbound edges!")

        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    # ----------------------- #

    def __get_the_cost_of_an_edge(self):
        start_vertex, end_vertex = DirectedWeightedUi.__get_edge()

        try:
            print(f"The cost of the edge is: {self.__graph.get_edge_cost(start_vertex, end_vertex)}")
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __modify_the_cost_of_an_edge(self):
        start_vertex, end_vertex = DirectedWeightedUi.__get_edge()
        cost = int(input("Enter the new cost: "))

        try:
            self.__graph.set_edge_cost(start_vertex, end_vertex, cost)
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    # ----------------------- #

    def __add_an_edge(self):
        start_vertex, end_vertex = DirectedWeightedUi.__get_edge()
        cost = int(input("Enter the cost: "))

        try:
            self.__graph.add_edge(start_vertex, end_vertex, cost)
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __remove_an_edge(self):
        start_vertex, end_vertex = DirectedWeightedUi.__get_edge()

        try:
            self.__graph.remove_edge(start_vertex, end_vertex)
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __add_a_vertex(self):
        vertex = DirectedWeightedUi.__get_vertex()

        try:
            self.__graph.add_vertex(vertex)
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    def __remove_a_vertex(self):
        vertex = DirectedWeightedUi.__get_vertex()

        try:
            self.__graph.remove_vertex(vertex)
        except GraphError as error:
            print(DirectedWeightedUi.__make_red(str(error)))

    # ----------------------- #

    def __read_the_graph_from_a_file_big(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_weighted_directed/{file_name}"
        self.__graph.read_from_file_big(file_path)

        print("\nThe graph was successfully loaded from the file!")

    def __read_the_graph_from_a_file(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_weighted_directed/{file_name}"
        self.__graph.read_from_file(file_path)

        print("\nThe graph was successfully loaded from the file!")

    def __write_the_graph_to_a_file(self):
        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_weighted_directed/{file_name}"
        self.__graph.write_to_file(file_path)

        print("\nThe graph was successfully written to the file!")

    # ----------------------- #

    def __create_a_random_graph(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        number_of_vertices = int(input("\nEnter the number of vertices: "))
        number_of_edges = int(input("Enter the number of edges: "))
        generate_rand_weighted_directed_graph(number_of_vertices, number_of_edges, self.__graph)

        print("\nRandom graph created!")

    def __load_a_premade_graph(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        self.__graph.read_from_file_big("data/data_weighted_directed/small.txt")

        print("\nGraph loaded!")

    # ----------------------- #

    def __create_a_copy_of_the_graph(self):
        if self.__is_copy:
            raise UiError("Graph already has a copy!")

        if not self.__graph.number_of_vertices:
            raise UiError("Graph is empty!")

        self.__original_graph = self.__graph
        self.__graph = copy.deepcopy(self.__graph)
        self.__is_copy = True

        print("\nGraph copy created!")

    def __restore_the_original_graph(self):
        if not self.__is_copy:
            raise UiError("Graph has no copy!")

        self.__graph = self.__original_graph
        self.__original_graph = None
        self.__is_copy = False

        print("\nGraph restored!")

    # ----------------------- #

    def __print_the_graph(self):
        if graph := str(self.__graph):
            if graph[0] == "0":
                print("\nThe graph is empty!")
                return

            print("\nThe graph is:")
            print(graph)

        else:
            print("\nThe graph is empty!")

    def __get_all_accessible_vertices(self):
        vertex = DirectedWeightedUi.__get_vertex()

        visited_vertices = accessible_vertices_weighted_directed(self.__graph, vertex)

        print(f"\nThere are {len(visited_vertices)} accessible vertices from the vertex {vertex}:")
        for visited_vertex in visited_vertices:
            print(f"-> {visited_vertex}")

    def __get_shortest_path_two_vertices(self):
        start_vertex = Vertex(int(input("\nEnter the start vertex: ")))
        end_vertex = Vertex(int(input("Enter the end vertex: ")))

        shortest_path = shortest_path_weighted_directed(self.__graph, start_vertex, end_vertex)

        if not shortest_path:
            print("\nThere is no path between the vertices!")
            return

        print(f"\nThe shortest path between the vertices {start_vertex} and {end_vertex} is:")
        for vertex in shortest_path:
            print(f"-> {vertex}")

    def __get_strongly_connected_components_tarjan(self):
        strongly_connected_components = strongly_connected_tarjan_weighted_directed(self.__graph)
        if not strongly_connected_components:
            print("\nThe graph is empty!")
            return

        print(f"\nThere are {len(strongly_connected_components)} strongly connected components:")
        for index, strongly_connected_component in enumerate(strongly_connected_components):
            print(f"Component {index + 1}: \n{strongly_connected_component}")

    def __number_of_isolated_vertices(self):
        number = 0
        for vertex in self.__graph.vertices:
            if self.__graph.get_out_degree(vertex) == 0 and self.__graph.get_in_degree(vertex) == 0:
                number += 1
        print(f"\nThere are {number} isolated vertices.")

    def __lowest_cost_path_matrix_multiplication(self):
        start_vertex = Vertex(int(input("\nEnter the start vertex: ")))
        end_vertex = Vertex(int(input("Enter the end vertex: ")))

        path, matrices = lowest_cost_path_matrix_weighted_directed(self.__graph, start_vertex, end_vertex)

        print("\nIntermediate matrices:")
        for index, matrix in enumerate(matrices):
            print(f"Matrix {index + 1}:")
            table = Texttable()
            table.set_cols_align(["c"] * len(matrix))
            for row in matrix:
                table.add_row(row)
            print(table.draw() + "\n")

        while True:
            start_vertex = Vertex(int(input("\nEnter the start vertex: ")))
            end_vertex = Vertex(int(input("Enter the end vertex: ")))

            if start_vertex.value == -1 or end_vertex.value == -1:
                break

            path = get_path_from_matrix(self.__graph, matrices[-1], start_vertex, end_vertex)

            if not path:
                print("\nThere is no path between the vertices!")

            else:
                path_length = matrices[-1][start_vertex.value][end_vertex.value]
                print(f"\nThe lowest cost path between the vertices {start_vertex} and {end_vertex} "
                        f"has the length {path_length} and is:")
                for vertex in path:
                    print(f"-> {vertex}")

    def __number_of_distinct_minimum_cost_walks(self):
        start_vertex = Vertex(int(input("\nEnter the start vertex: ")))
        end_vertex = Vertex(int(input("Enter the end vertex: ")))

        number = number_of_distinct_minimum_cost_walks_weighted_directed(self.__graph, start_vertex, end_vertex)

        if number == 1:
            print(f"\nThere is 1 distinct minimum cost walk between the vertices {start_vertex} and {end_vertex}.")
        else:
            print(f"\nThere are {number} distinct minimum cost walks between the vertices {start_vertex} and {end_vertex}.")

    def __number_of_distinct_walks(self):
        start_vertex = Vertex(int(input("\nEnter the start vertex: ")))
        end_vertex = Vertex(int(input("Enter the end vertex: ")))

        number = number_of_distinct_walks_weighted_directed(self.__graph, start_vertex, end_vertex)

        if number == 1:
            print(f"\nThere is 1 distinct walk between the vertices {start_vertex} and {end_vertex}.")
        else:
            print(f"\nThere are {number} distinct walks between the vertices {start_vertex} and {end_vertex}.")

    @staticmethod
    def __exit():
        print("\nGoodbye!")
        exit()
