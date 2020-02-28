# Author: Matthew Manning
# Student ID: #000967779

# Vertex constructor
class Vertex:
    def __init__(self, id, data):
        self.id = id
        self.data = data


# Adjacency matrix used to build and return edges and return vertices.
# Vertices and edge indices stored in key-value pairs, edges stored in list
# Vertices dictionary and edge_indices O(N) space complexity, edges O(N^2) space complexity
class Graph:
    vertices = {}
    edges = []
    edge_indices = {}

    # Add vertex to graph, set default values for edges to 0 for length of edge_indices
    # O(N) time complexity
    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            self.vertices[vertex.id] = vertex.data
            for row in self.edges:
                row.append(0)
            self.edges.append([0] * (len(self.edges) + 1))
            self.edge_indices[vertex.id] = len(self.edge_indices)
            return True
        else:
            return False
            print('Vertex not added')

    # Connect two vertices with undirected edge
    # O(1) space time complexity, operation on a 2D list
    def add_edge(self, u, v, weight=1):
        if u in self.vertices and v in self.vertices:
            self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
            self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
            return True
        else:
            return False

    # Find the distance two vertices u and v using edge matrix built by add_edge function
    # O(1) time complexity
    def find_distance(self, u, v):
        distance = self.edges[u][v]
        return float(distance)

    # Print function to display edges as adjacency matrix
    # O(N^2) space-time complexity
    def print_graph(self):
        for v, i in self.edge_indices.items():
            print(str(v) + ' ', end=' ')
            for j in range(len(self.edges)):
                print(str(self.edges[i][j]) + ' ', end=' ')
            print(' ')

    #  Return key of vertex based off address entered. Locations unique so only first key found needs to be returned
    #  O(1) space-time complexity
    def find_key(self, value):
        return next((k for k, v in self.vertices.items() if v == value), None)
