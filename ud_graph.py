# Course: CS 261
# Author: Ian Docherty
# Assignment: Assignment 6
# Description: My implementation of an undirected, unweighted graph with no
#              loops and no duplicate edges

from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Adds a new vertex to the graph
        """

        # Add a vertex with no adjacent vertices
        self.adj_list[v] = []  # Initialize to empty list
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Adds the given edge to the graph. If either vertex does not exist
        yet in the graph, the vertex will be created first, then the edge
        will be created between the two vertices.
        """

        # Check if u and v refer to same vertex
        if u == v:
            return  # Do nothing

        # Check if edge already exists
        if u in self.adj_list and v in self.adj_list:
            if u in self.adj_list[v]:
                return  # Do nothing

        # Check if vertex u exists
        if u not in self.adj_list:
            self.add_vertex(u)

        # Check if vertex v exists
        if v not in self.adj_list:
            self.add_vertex(v)

        # Add v and u to each others adjacency lists
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Removes the given edge from the graph. If either vertices do not
        exist, or there is no edge between them , then nothing is done.
        """

        # Check if both vertices exist
        if v not in self.adj_list or u not in self.adj_list:
            return

        # Check if there is an edge between u and v
        if u not in self.adj_list[v] or v not in self.adj_list[u]:
            return

        # Remove u and v from each others adjacency lists
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Removes the given vertex and all connected edges incident to it.
        """

        # Check if vertex exists
        if v not in self.adj_list:
            return

        # Remove v from adjacency list of each of its neighbors
        for vertex in self.adj_list[v]:
            self.adj_list[vertex].remove(v)

        del self.adj_list[v]  # Delete v

    def get_vertices(self) -> []:
        """
        Returns a list of vertices in the graph (any order)
        """

        return [vertex for vertex in self.adj_list]

    def get_edges(self) -> []:
        """
        Returns a list of all edges in the graph (any order) as tuples of
        vertex pairs
        """
        all_edges = []  # Empty list to store all edges

        # Iterate through all edge pairs in graph
        for vertex1 in self.adj_list:
            for vertex2 in self.adj_list[vertex1]:

                # Check if reverse order edge is already stored
                if (vertex2, vertex1) not in all_edges:
                    all_edges.append((vertex1, vertex2))

        return all_edges

    def is_valid_path(self, path: []) -> bool:
        """
        Returns True if provided path is valid, False otherwise
        """

        # Check if path is empty
        if len(path) == 0:
            return True

        # Check if path has 1 element
        if len(path) == 1:
            return path[0] in self.adj_list

        # Iterate through elements in path
        for index in range(len(path) - 1):
            curr_vertex = path[index]
            next_vertex = path[index + 1]

            # Check if next element is adjacent to current element
            if next_vertex not in self.adj_list[curr_vertex]:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """

        # Check if given start vertex is in graph
        if v_start not in self.adj_list:
            return []  # Empty list

        # Initialize stack and result list for DFS traversal
        stack = deque()
        visited = []
        stack.append(v_start)

        # Perform traversal and record each vertex visited
        while len(stack) > 0:
            curr_vertex = stack.pop()  # Pop vertex from top

            # Add vertex to visited list
            if curr_vertex not in visited:
                visited.append(curr_vertex)

                # Check if end vertex found
                if curr_vertex == v_end:
                    return visited

                # Push each adjacent vertex to stack in reverse lexicographical order
                self.adj_list[curr_vertex].sort(reverse=True)
                for vertex in self.adj_list[curr_vertex]:
                    stack.append(vertex)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        return

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
      

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
       

   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()
    #
    #
    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print('{:<10}'.format(case), g.has_cycle())
