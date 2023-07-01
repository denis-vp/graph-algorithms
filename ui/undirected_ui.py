import copy

from graph.directed_graph import GraphError
from graph.undirected_graph import UndirectedGraph
from graph.vertex import Vertex
from algorithms.undirected_extra import generate_rand_undirected_graph, connected_components_kosaraju_undirected
from ui.directed_weighted_ui import UiError


class UndirectedUi:

    def __init__(self, graph: UndirectedGraph):
        self.__graph = graph

        self.__original_graph = None
        self.__is_copy = False

    def run_ui(self):
        UndirectedUi.__print_title()

        options = {
            "1": self.__get_number_of_vertices,
            "2": self.__check_if_an_edge_exists,
            "3": self.__print_the_vertices,
            "4": self.__get_the_degree_of_a_vertex,
            "5": self.__print_the_edges_of_a_vertex,
            "6": self.__add_an_edge,
            "7": self.__remove_an_edge,
            "8": self.__add_a_vertex,
            "9": self.__remove_a_vertex,
            "10": self.__read_the_graph_from_a_file_big,
            "11": self.__read_the_graph_from_a_file,
            "12": self.__read_the_graph_from_a_file_big_with_weights,
            "13": self.__write_the_graph_to_a_file,
            "14": self.__get_connected_components,
            "c": self.__create_a_copy_of_the_graph,
            "u": self.__restore_the_original_graph,
            "r": self.__create_a_random_graph,
            "l": self.__load_a_premade_graph,
            "p": self.__print_the_graph,
            "x": UndirectedUi.__exit
        }

        while True:
            UndirectedUi.__print_menu()

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
            raise UiError(UndirectedUi.__make_red("Invalid edge!"))

        return Vertex(int(edge[0])), Vertex(int(edge[1]))

    # ----------------------- #

    @staticmethod
    def __make_red(text: str):
        return "\033[91m{}\033[00m".format(text)

    @staticmethod
    def __print_title():
        print()
        print("|-------------------------------|")
        print("|        Undirected Graph       |")
        print("|-------------------------------|")

    @staticmethod
    def __print_menu():
        print("\n1: Get the number of vertices")
        print("2: Check if an edge exists")
        print("3: Print the vertices")
        print(" ---------------------------------- ")
        print("4: Get the degree of a vertex")
        print("5: Print the edges of a vertex")
        print(" ---------------------------------- ")
        print("6: Add an edge")
        print("7: Remove an edge")
        print("8: Add a vertex")
        print("9: Remove a vertex")
        print(" ---------------------------------- ")
        print("10: Read the graph from a file big")
        print("11: Read the graph to a file (small)")
        print("12: Read the graph from a file big with weights")
        print("13: Write the graph to a file")
        print(" ---------------------------------- ")
        print("14: Get the connected components (Kosaraju)")
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
        vertex_1, vertex_2 = UndirectedUi.__get_edge()

        try:
            if self.__graph.is_edge(vertex_1, vertex_2):
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

    def __get_the_degree_of_a_vertex(self):
        vertex = UndirectedUi.__get_vertex()

        try:
            print(f"The degree of the vertex is: {self.__graph.get_degree(vertex)}")
        except GraphError as error:
            print(UndirectedUi.__make_red(str(error)))

    def __print_the_edges_of_a_vertex(self):
        vertex = UndirectedUi.__get_vertex()

        try:
            if edges := self.__graph.get_neighboring_edges(vertex):
                print("The edges of the vertex are:")
                for edge in edges:
                    vertex_1, vertex_2 = edge
                    print(f"{vertex_1} -- {vertex_2}")

            else:
                print("The vertex has no outbound edges!")

        except GraphError as error:
            print(UndirectedUi.__make_red(str(error)))

    # ----------------------- #

    def __add_an_edge(self):
        vertex_1, vertex_2 = UndirectedUi.__get_edge()

        try:
            self.__graph.add_edge(vertex_1, vertex_2)
        except GraphError as error:
            print(UndirectedUi.__make_red(str(error)))

    def __remove_an_edge(self):
        vertex_1, vertex_2 = UndirectedUi.__get_edge()

        try:
            self.__graph.remove_edge(vertex_1, vertex_2)
        except GraphError as error:
            print(UndirectedUi.__make_red(str(error)))

    def __add_a_vertex(self):
        vertex = UndirectedUi.__get_vertex()

        try:
            self.__graph.add_vertex(vertex)
        except GraphError as error:
            print(UndirectedUi.__make_red(str(error)))

    def __remove_a_vertex(self):
        vertex = UndirectedUi.__get_vertex()

        try:
            self.__graph.remove_vertex(vertex)
        except GraphError as error:
            print(UndirectedUi.__make_red(str(error)))

    # ----------------------- #

    def __read_the_graph_from_a_file_big(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_undirected/{file_name}"
        self.__graph.read_from_file_big(file_path)

        print("\nThe graph was successfully loaded from the file!")

    def __read_the_graph_from_a_file_big_with_weights(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_undirected/{file_name}"
        self.__graph.read_from_file_big_with_costs(file_path)

        print("\nThe graph was successfully loaded from the file!")

    def __read_the_graph_from_a_file(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_undirected/{file_name}"
        self.__graph.read_from_file(file_path)

        print("\nThe graph was successfully loaded from the file!")

    def __write_the_graph_to_a_file(self):
        file_name = input("\nEnter the file name: ")
        file_path = f"data/data_undirected/{file_name}"
        self.__graph.write_to_file(file_path)

        print("\nThe graph was successfully written to the file!")

    # ----------------------- #

    def __create_a_random_graph(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        number_of_vertices = int(input("\nEnter the number of vertices: "))
        number_of_edges = int(input("Enter the number of edges: "))
        generate_rand_undirected_graph(number_of_vertices, number_of_edges, self.__graph)

        print("\nRandom graph created!")

    def __load_a_premade_graph(self):
        if self.__graph.number_of_vertices:
            raise UiError("Graph already exists!")

        self.__graph.read_from_file_big("data/data_undirected/small.txt")

        print("\nGraph loaded!")

    # ----------------------- #

    def __get_connected_components(self):
        connected_components = connected_components_kosaraju_undirected(self.__graph)
        if not connected_components:
            print("The graph is empty!")
            return

        print(f"\nThe graph has {len(connected_components)} connected components:")
        for index, connected_component in enumerate(connected_components):
            print(f"Component {index + 1}: \n{connected_component}")

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

    @staticmethod
    def __exit():
        print("\nGoodbye!")
        exit()
