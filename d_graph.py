# Course: CS261 - Data Structures
# Author: Ian Docherty
# Assignment: Assignment 6
# Description: My implementation of a directed, weighted graphs that does not
#              allow duplicate edges or loops. The graph is represented using
#              an adjacency matrix.

import heapq
from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a single vertex to the graph
        """

        # Add zero to each row
        for src in range(self.v_count):
            self.adj_matrix[src].append(0)

        # Add extra row and fill with zeroes
        self.adj_matrix.append([0])
        for _ in range(self.v_count):
            self.adj_matrix[self.v_count].append(0)

        self.v_count += 1  # Increment vertex count
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds an edge to the graph with the given source vertex, destination
        vertex, and weight
        """

        # Check if src vertex exists
        if src < 0 or src >= self.v_count:
            return

        # Check if dst vertex exists
        if dst < 0 or dst >= self.v_count:
            return

        # Check if weight is valid
        if weight < 1 or src == dst:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes the given edge from teh graph
        """

        # Check if src vertex exists
        if src < 0 or src >= self.v_count:
            return

        # Check if dst vertex exists
        if dst < 0 or dst >= self.v_count:
            return

        # Remove edge if it currently exists
        if self.adj_matrix[src][dst] > 0:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph
        """
        return [vertex for vertex in range(self.v_count)]

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph in the format (src, dst, weight)
        """
        edges = []

        # Iterate over all edges in the graph
        for src in range(self.v_count):
            for dst in range (self.v_count):
                weight = self.adj_matrix[src][dst]

                # Only add edge if it has positive weight
                if weight > 0:
                    edges.append((src, dst, weight))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Returns True if the given sequence of vertices represents a valid path
        and False otherwise. An empty path is considered valid.
        """

        # Check if given path is valid
        if len(path) == 0:
            return True

        # Iterate through given path and check for validity
        for index in range(len(path) - 1):
            path_src = path[index]
            path_dst = path[index + 1]

            # Check if edge exists
            if self.adj_matrix[path_src][path_dst] == 0:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices in the order they are visited in a
        DFS traversal from the given start vertex to the optional given
        end vertex. Vertices are explored in ascending order if a choice
        must be made about which vertex to explore next.
        """

        # Check if start vertex is in the graph
        if v_start < 0 or v_start >= self.v_count:
            return []  # Return empty list

        stack = deque()
        visited = []
        stack.append(v_start)

        # Iterate through each vertex and perform DFS
        while len(stack) > 0:
            curr_vertex = stack.pop()

            if curr_vertex not in visited:
                visited.append(curr_vertex)

                # Check if end vertex has been reached
                if curr_vertex == v_end:
                    return visited

                # Add each neighbor of current vertex to a temp list
                temp_list = []
                for vertex in range(self.v_count):

                    # Check if vertex is a neighbor to current vertex
                    if self.adj_matrix[curr_vertex][vertex] > 0:
                        temp_list.append(vertex)

                # Add each neighbor to the stack in descending order
                temp_list.sort(reverse=True)
                for vertex in temp_list:
                    stack.append(vertex)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Returns a list of vertices in the order they are visited in a
        BFS traversal from the given start vertex to the optional given
        end vertex. Vertices are explored in ascending order if a choice
        must be made about which vertex to explore next.
        """

        # Check if start vertex is in the graph
        if v_start < 0 or v_start >= self.v_count:
            return []  # Return empty list

        queue = deque()
        visited = []
        queue.append(v_start)

        # Iterate through each vertex and perform BFS
        while len(queue) > 0:
            curr_vertex = queue.popleft()

            if curr_vertex not in visited:
                visited.append(curr_vertex)

            # Check if end vertex has been found
            if curr_vertex == v_end:
                return visited

            # Add each neighbor of current vertex to a temp list
            temp_list = []
            for vertex in range(self.v_count):

                # Check if vertex is a neighbor to current vertex
                if self.adj_matrix[curr_vertex][vertex] > 0:
                    temp_list.append(vertex)

            # Add each neighbor to the stack in descending order
            temp_list.sort()
            for vertex in temp_list:
                if vertex not in visited:
                    queue.append(vertex)

        return visited

    def has_cycle(self):
        """
        Returns True if there is at least one cycle in the graph, otherwise
        returns False. Uses a BFS and Kahn's Algorithm to determine if there
        are any cycles present.
        """

        # Count the incoming degree of each vertex
        in_degrees = []  # Count of incoming edges
        queue = deque()  # Queue of vertices with no incoming edges

        for col in range(self.v_count):
            deg_count = 0
            for row in range(self.v_count):

                if self.adj_matrix[row][col] > 0:
                    deg_count += 1

            if deg_count == 0:
                queue.append(col)

            in_degrees.append(deg_count)

        visited_count = 0  # Used to count number of visited vertices

        # Perform BFS modified for Kahn's Algorithm
        while len(queue) > 0:
            curr_vertex = queue.popleft()
            visited_count += 1

            # Decrease in-degree of all neighbor vertices by 1
            for vertex in range(self.v_count):

                # Check if vertex is a neighbor
                if self.adj_matrix[curr_vertex][vertex] > 0:
                    in_degrees[vertex] -= 1

                    if in_degrees[vertex] == 0:
                        queue.append(vertex)

        # Graph contains cycle if vertices visited not equal to actual number of vertices
        if visited_count != self.v_count:
            return True

        return False

    def dijkstra(self, src: int) -> []:
        """
        Uses Dijkstra's Algorithm to find and return the shortest path from the
        given source vertex to each vertex in the graph. If a vertex is
        disconnected from the src subgraph, then its distance is marked as 'inf'.
        """

        # Initialize shortest paths to infinity
        shortest_paths = []
        for _ in range(self.v_count):
            shortest_paths.append(float('inf'))

        # Initialize priority queue with src vertex having a distance of zero
        p_queue = [(0, src)]

        # Perform Dijkstra's Algorithm
        while len(p_queue) > 0:
            curr_dist, curr_vertex = heapq.heappop(p_queue)

            # Check if current vertex has been visited
            if shortest_paths[curr_vertex] == float('inf'):
                shortest_paths[curr_vertex] = curr_dist

                for successor in range(self.v_count):
                    if self.adj_matrix[curr_vertex][successor] > 0:
                        dist = self.adj_matrix[curr_vertex][successor]
                        heapq.heappush(p_queue, (curr_dist + dist, successor))

        return shortest_paths


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)
    #
    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    #
    #
    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))
    #
    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')
    #

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    g.add_edge(4, 0, 99)
    print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    #
    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')

    # edges = [(0, 1, 10), (1, 4, 15), (2, 1, 23), (2, 3, 1), (4, 3, 1)]
    # g = DirectedGraph(edges)
    # print(g)
    # print(g.has_cycle_bfs())
