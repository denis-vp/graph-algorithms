# Graph Algorithms CLI Application

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

This command-line application allows you to perform various graph algorithms on your input graph data. Whether you're a student studying graph theory, a data scientist analyzing networks, or just curious about exploring the world of graphs, this tool provides a versatile and easy-to-use solution.

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [Supported Algorithms](#supported-algorithms)
- [License](#license)

## Features

- Execute a variety of graph algorithms on your graph data.
- Support for both directed and undirected graphs.
- Support for both weighted and unweighted graphs.
- Generate a random graph based on user input.
- Import graphs from files.
- Export results in a user-friendly format.
- Well-documented and user-friendly interface.

## Usage

After launching the application, you will be prompted to select the type of graph you want to work with: **Weighted Directed** or **Unweighted Undirected**. Follow the appropriate instructions based on your choice.
Afterwards you must load a graph from a file. There already are graph files present but you can input your own if written in one of two ways:
  - Big format:
    - First line contains the number of vertices and the number of edges.
    - The vertices are numbered from 0 to n - 1.
    - The next lines contain the edges. Ex: 1 2 means that there is an edge from 1 to 2.
  - Small format:
    - The file contains the edges of the graph and the isolated vertices. No numer of vertices or number of edges is specified.
    - An edge is represented by two vertices. Ex: 1 2 means that there is an edge from 1 to 2.
    - An isolated vertex is represented by its number and -1. Ex: 1 -1 means that there is an isolated vertex with the number 1.
  - Weighted graphs:
    - For weighted graphs you just need to add the weight of the edge at the end of each line representing an edge.
    - Ex: 1 2 100 means that there is an edge from 1 to 2 with weight 100.
   
## Supported Algorithms

- Depth-First Search
- Breadth-First Search
- Tarjan Strongly Connected Components
- Kosaraju Connected Components
- Accessible vertices (DFS)
- Dijkstra's Algortihm: Lowest Cost Path
- Minimum Lenght Path (BFS)
- Matrix Multiplication: Lowest Cost Path
- Topological Sort: Number of Distinct Walks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This means that you are free to:

- **Use** the software for any purpose.
- **Modify** the software.
- **Distribute** the software.
- **Sublicense** the software.
- **Private** use.

Under the following conditions:

- The license and copyright notice must be included in all copies or substantial portions of the software.

This project is provided "as is" without any warranty, express or implied.
