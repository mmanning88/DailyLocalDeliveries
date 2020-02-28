# Author: Matthew Manning
# Student ID: #000967779

import csv
from hashtable import HashTable
from locationAndDistances import g
from datetime import datetime
from datetime import timedelta


# Creates truck object that can hold packages, go to different vertexes on Graph g, and update hashTable
class Truck:
    def __init__(self):
        self.packages_held = []
        self.location_index = 0
        self.location = '4001 South 700 East'
        self.distance_traveled = 0  # Variable to keep track of total miles driven a single truck object
        self.speed = 18
        self.current_time = '08:00 AM'

    # Add package item to truck item's package_held list.
    # Packages will not be loaded if they are on-route or have already been delivered
    # O(1) space-time complexity
    def add_package(self, package):
        temp_package = hashTable.search(package)
        if len(self.packages_held) >= 16:
            print('Truck is full')
        elif temp_package.status == 'On-Route':
            print('Package ' + str(package) + ' already on another truck')
            return None
        elif temp_package.status == 'Delivered':
            print('Package ' + str(package) + ' already delivered')
            return None
        elif isinstance(temp_package, Package):
            temp_package.status = 'On-Route'
            temp_package.all_details[8] = 'On-Route'
            temp_package.timestamp_start = self.current_time
            temp_package.all_details[9] = self.current_time
            self.packages_held.append(temp_package)

    # Creates a set of vertices that the truck must visit in order to deliver all packages held on truck
    # O(N) space-time complexity
    def create_path(self):
        new_path = set()
        for i in range(len(self.packages_held)):
            if g.find_key(self.packages_held[i].status) != 'Delivered':
                new_path.add(g.find_key(self.packages_held[i].address))
        return new_path

    # Move truck from one location to another, updating truck distance and time and each package's timestamp,
    # if truck contains package that matches destination's location, package will be delivered, if truck is at hub
    # and package was delivered, package is removed
    # O(N) time complexity
    def go_to_address(self, destination):
        if self.location in g.vertices.get(destination):
            print('Already at location')
            return None
        else:
            # Add distance to distance_traveled and add time it took to current_time and update package to current time
            temp_distance = g.find_distance(self.location_index, destination)
            seconds_to_add = (((temp_distance / self.speed) * 60) * 60)  # convert distance traveled to total seconds
            time_str = self.current_time
            format_time = '%I:%M %p'  # 12-Hour:Minute Period format
            self.location = g.vertices.get(destination)
            self.location_index = g.find_key(self.location)
            self.current_time = ((datetime.strptime(time_str, format_time)
                                  + timedelta(seconds=seconds_to_add)).time()).strftime('%I:%M %p')
            self.distance_traveled += temp_distance

        # Update status for delivered packages if address on package matches truck's current location
        # O(N) time complexity
        for i in range(len(self.packages_held)):
            if self.packages_held[i].address == self.location and self.packages_held[i].address != 'Delivered':
                hashTable.search(self.packages_held[i].packageID).status = 'Delivered'
                hashTable.search(self.packages_held[i].packageID).all_details[8] = 'Delivered'
                hashTable.search(self.packages_held[i].packageID).timestamp_delivered = self.current_time
                hashTable.search(self.packages_held[i].packageID).all_details[10] = self.current_time
        self.packages_held = [package for package in self.packages_held if package.status != 'Delivered']


# Creates a package item that will hold all information about a package through delivery process
class Package:
    def __init__(self, packageID, address, city, state, zip_code, deadline, weight, special_notes, status,
                 timestamp_start, timestamp_delivered):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = status
        self.timestamp_start = timestamp_start
        self.timestamp_delivered = timestamp_delivered
        self.all_details = [self.packageID, self.address, self.city, self.state,
                            self.zip_code, self.deadline, self.weight, self.special_notes, self.status,
                            self.timestamp_start, self.timestamp_delivered]


# Import package information and add to hashTable.
with open('packagefile.csv') as csv_package:
    readCSV = csv.reader(csv_package, delimiter=',')

    hashTable = HashTable()
    truck1 = Truck()
    truck2 = Truck()
    for row in readCSV:
        temp_packageID = int(row[0])
        temp_address = str(row[1])
        temp_city = str(row[2])
        temp_state = str(row[3])
        temp_zip_code = str(row[4])
        temp_deadline = str(row[5])
        temp_weight = int(row[6])
        temp_special_notes = str(row[7])
        temp_status = 'At Hub'
        if 'Delayed on flight' in temp_special_notes:
            temp_time_hub = '09:05 AM'
        else:
            temp_time_hub = '08:00 AM'
        temp_time_delivered = ''
        row = Package(temp_packageID, temp_address, temp_city, temp_state, temp_zip_code, temp_deadline, temp_weight,
                      temp_special_notes, temp_status, temp_time_hub, temp_time_delivered)
        hashTable.add(temp_packageID, row)


# At starting vertex, finds vertex closest. Will then go to that vertex and repeat process until all vertices are
# visited. Each time a closest vertex is found, add to path
# O(N^2) time complexity
def nearest_neighbor(graph, created_path):
    start_vertex = 0  # Path will always start at 0
    shortest_distance = {}
    unvisited_vertices = list(created_path)
    unvisited_vertices.insert(0, start_vertex)
    path = []

    # Initially set all vertex distances other than start to infinity, start node distance set to 0
    # O(N) space-time complexity
    for v in unvisited_vertices:
        shortest_distance[v] = float("inf")
    shortest_distance[start_vertex] = 0

    # Find current neighbors of vertex
    # O(N) space-time complexity
    def find_neighbors(cp):
        neighbors = []
        for v in cp:
            if v not in path:
                neighbors.append(v)
        return neighbors
    # Main logic of algorithm, set current vertex as vertex with least distance (Vertex 0 by default), reset distance
    # values to infinity for each unvisted vertex. Using neighbors list generated by find_neighbors,
    # find the shortest distance between current vertex and neighbors. Append current vertex to path and then remove
    # from unvisited vertices
    # O(N^2) space-time complexity
    while unvisited_vertices:
        curr_vertex = min(unvisited_vertices, key=lambda vertex: shortest_distance[vertex])
        for v in unvisited_vertices:
            shortest_distance[v] = float("inf")
        for neighbor in find_neighbors(created_path):
            if graph.find_distance(curr_vertex, neighbor) < shortest_distance[neighbor]:
                shortest_distance[neighbor] = graph.find_distance(curr_vertex, neighbor)
        path.append(curr_vertex)
        unvisited_vertices.remove(curr_vertex)

    path.insert(len(path), 0)  # At starting vertex to end of path
    path.pop(0)
    return path


# Creates an object to group addresses that are close together
class AddressGroup:
    def __init__(self):
        self.address_indexes = []

    def add_index(self, index):
        self.address_indexes.append(index)


# Major regions of city defined and locations that fall in each region are added to address group
north = AddressGroup()
central = AddressGroup()
southwest = AddressGroup()
southeast = AddressGroup()
north_addresses = [1, 6, 12, 8, 19, 25]
central_addresses = [2, 4, 5, 7, 9, 11, 13, 14, 15, 17, 18]
southwest_addresses = [3, 10, 16, 23]
southeast_addresses = [20, 21, 22, 24, 26]

# Each region has address list added to list held in object
# O(N) space time complexity for each loop
for address in north_addresses:
    north.add_index(address)
for address in central_addresses:
    central.add_index(address)
for address in southwest_addresses:
    southwest.add_index(address)
for address in southeast_addresses:
    southeast.add_index(address)

# Heuristic package loading. If package has deadline, loaded first. If multiple package go to same address,
# load on same truck together

# Truck 1 first trip
# O(N) space-time complexity
for package in hashTable.sort_keys():
    if hashTable.search(package).deadline == '9:00:00':
        truck1.add_package(package)
    if hashTable.search(package).deadline == '10:30:00' and hashTable.search(package).status == 'At Hub' \
            and g.find_key(hashTable.search(package).address) in southeast.address_indexes \
            and truck1.current_time == hashTable.search(package).timestamp_start \
            and 'Can only be' not in hashTable.search(package).special_notes:
        truck1.add_package(package)
    if g.find_key(hashTable.search(package).address) in southwest.address_indexes and hashTable.search(package).status == 'At Hub':
        truck1.add_package(package)
truck1.add_package(20)
truck1.add_package(21)
truck1.add_package(19)
truck1.add_package(24)
truck1.go_to_address(21)  # Fulfilling constraint for package that has earliest deadline
for location in nearest_neighbor(g, truck1.create_path()):
    truck1.go_to_address(location)

# Truck 2 first trip, loads packages that must be on truck 2
# O(N) space-time complexity
for package in hashTable.sort_keys():
    if g.find_key(hashTable.search(package).address) in north.address_indexes and hashTable.search(package).status == 'At Hub' \
            and 'Wrong address' not in hashTable.search(package).special_notes:
        truck2.add_package(package)
    if 'Can only be' in hashTable.search(package).special_notes and hashTable.search(package).status == 'At Hub':
        truck2.add_package(package)
for location in nearest_neighbor(g, truck2.create_path()):
    truck2.go_to_address(location)

# Truck 1 second trip
# O(N) space-time complexity
for package in hashTable.sort_keys():
    if hashTable.search(package).deadline == '10:30:00' and hashTable.search(package).status == 'At Hub' \
            or hashTable.search(package).timestamp_start == "09:05 AM":
        truck1.add_package(package)
for location in nearest_neighbor(g, truck1.create_path()):
    truck1.go_to_address(location)

# Truck 1 third trip, corrects address in package 9
# O(N) space-time complexity
for package in hashTable.sort_keys():
    if hashTable.search(package).status == 'At Hub':
        truck1.add_package(package)
    if 'Wrong address' in hashTable.search(package).special_notes \
            and datetime.strptime(truck1.current_time , '%I:%M %p') > datetime.strptime('10:20 AM', '%I:%M %p'):
        hashTable.search(package).address = '410 S State St'
        hashTable.search(package).all_details[1] = '410 S State St'
for location in nearest_neighbor(g, truck1.create_path()):
    truck1.go_to_address(location)

# Check to see if all packages are delivered, for loop goes through each package and adds True to delivered list if
# packaged was delivered or false if otherwise. Only if all packages are delivered will message print.
# O(N) space-time complexity
delivered = []
for package in hashTable.sort_keys():
    if hashTable.search(package).status == 'Delivered':
        delivered.append(True)
    else:
        delivered.append(False)
if all(delivered):
    print('All packages delivered, program executed successfully.')
print('Total distance traveled by all trucks: ' + str(truck1.distance_traveled + truck2.distance_traveled))


