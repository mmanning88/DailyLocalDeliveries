# Author: Matthew Manning
# Student ID: #000967779

import csv
from adjacencymatrix import Graph, Vertex

# Import location id, name, and address from csv file
# O(N) space-time complexity
with open('namefile.csv') as csv_name:
    readCSV = csv.reader(csv_name, delimiter=',')

    nameList = []
    for row in readCSV:
        nameID = int(row[0])
        name = str(row[1])
        address = str(row[2])

        list_table_values = [nameID, name, address]
        nameList.append(list_table_values)

# Import distances to be used with locations
# O(N) space-time complexity
with open('distances.csv') as csv_dist:
    readCSV = csv.reader(csv_dist, delimiter=',')

    distList = []
    for row in readCSV:
        distList.append(row)

# Create list of vertices from name list and add to graph data structure
# O(N) space-time complexity
g = Graph()  # Graph of all addresses with numeric keys
for i in nameList:
    addressID = i[0]
    address = i[2]
    newVertex = Vertex(addressID, address)
    g.add_vertex(newVertex)

# Add edges for each location using distance list
# O(N^2) space-time complexity || O(N*M) space complexity (matrix)
for i in range(len(distList)):
    for j in range(len(distList[i])):
        g.add_edge(i, j, distList[i][j])


