from ui.directed_weighted_ui import DirectedWeightedUi
from graph.undirected_graph import UndirectedGraph
from graph.weighted_directed_graph import WeightedDirectedGraph
from ui.undirected_ui import UndirectedUi

"""
    Author: Denis Vasile Pop
    Main module of the application. It is responsible for creating the graph and the UI and running the UI.
"""

if __name__ == "__main__":
    print("Choose the type of graph you want to work with: ")
    print("1. Weighted directed graph")
    print("2. Unweighted Undirected graph")

    option = int(input("Your option: "))
    if option == 1:
        graph = WeightedDirectedGraph()
        ui = DirectedWeightedUi(graph)
    elif option == 2:
        graph = UndirectedGraph()
        ui = UndirectedUi(graph)
    else:
        print("Invalid option. Defaulting to weighted directed.")
        graph = WeightedDirectedGraph()
        ui = DirectedWeightedUi(graph)

    ui.run_ui()
