# Import libraries of python for plot and visualize graph using networkx library
import networkx as nx
import matplotlib.pyplot as plt


# Intersection Class to add intersections in graph
class Intersection:
    # Method Initialization for class
    def __init__(self, intersection_id):
        self.id = intersection_id
        # List to add roads in list
        self.connected_roads = []
        # List to add houses in list
        self.connected_houses = []

    # Add road method
    def add_road(self, road_id):
        self.connected_roads.append(road_id)

    # Add houses method
    def add_house(self, house_id):
        self.connected_houses.append(house_id)


# Road class to add roads that are edges
class Road:
    # Initialization method for road class
    def __init__(self, road_id, road_name, length):
        # parameters for roads
        self.id = road_id
        self.road_name = road_name
        self.length = length


# House class to add houses at intersections
class House:
    def __init__(self, house_id, intersection_id):
        self.id = house_id
        self.intersection_id = intersection_id


# RoadNetworkGraph class to create road network
class RoadNetworkGraph:
    # Method initialization for class
    def __init__(self):
        # Dictionary to add intersections
        self.intersections = {}
        # dictionary to add roads
        self.roads = {}
        # dictionary to add houses
        self.houses = {}
        self.next_road_id = 1
        self.next_house_id = 1
        # Directed Graph
        self.G = nx.DiGraph()

    # Add intersections method to add intersection
    def add_intersection(self, intersection_id):
        # If intersection is not then add intersention
        if intersection_id not in self.intersections:
            self.intersections[intersection_id] = Intersection(intersection_id)

    # Add road function to add roads in network
    def add_road(self, road_name):
        road_id = self.next_road_id
        # Increment road id by 1 everytime road add in network
        self.next_road_id += 1
        # add roads by calling Road object
        self.roads[road_id] = Road(road_id, road_name, 1)  # Set length to 1 for simplicity
        return road_id

    # Add house function to add houses in network
    def add_house(self, intersection_id):
        house_id = self.next_house_id
        # Increment house id by 1 everytime house add in network
        self.next_house_id += 1
        # add houses by calling House object
        self.houses[house_id] = House(house_id, intersection_id)
        return house_id

    # Connect intersection with road function
    def connect_intersection_to_road(self, intersection_id, road_id):
        if intersection_id in self.intersections and road_id in self.roads:
            intersection = self.intersections[intersection_id]
            # add road in intersection with id
            intersection.add_road(road_id)

    # Connect intersection with houses function
    def connect_house_to_intersection(self, house_id, intersection_id):
        if house_id in self.houses and intersection_id in self.intersections:
            intersection = self.intersections[intersection_id]
            # add houses in intersection with id
            intersection.add_house(house_id)

    # Visualize graph function to visualize graph
    def visualize_graph(self, figsize=(15, 15)):
        # clear function to clear previous data
        self.G.clear()

        # For loop to add intersection in graph
        for intersection_id in self.intersections:
            self.G.add_node(intersection_id)

        # For loop to add roads in graph that connects with intersection
        for road_id, road in self.roads.items():
            for intersection_id in self.intersections:
                # If road find in intersection
                if road_id in self.intersections[intersection_id].connected_roads:
                    # Add egde with id,name,length in graph
                    self.G.add_edge(intersection_id, road_id, road_name=road.road_name, length=road.length)

        # loop to add houses in houses
        for house_id, house in self.houses.items():
            # add node with house id
            self.G.add_node(house_id)
            # add edge with house id in intersection
            self.G.add_edge(house_id, house.intersection_id)

        # plot figure size
        plt.figure(figsize=figsize)
        # to view the edge large and big scale = 10
        pos = nx.spring_layout(self.G, scale=10)

        # dictionary to add labels of egdes
        edge_labels = {}
        # loop to add labels to edges
        for u, v in self.G.edges():
            if isinstance(u, int) and isinstance(v, int):
                label = "House"
            edge_labels[(u, v)] = label

        # draw graph
        nx.draw(self.G, pos, with_labels=True, node_size=400, node_color='skyblue', font_size=7, font_weight='bold')
        # draw edge
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, font_size=10, font_color='red')

        # plot the graph
        plt.title("Road Network Graph with Houses")
        plt.show()

    # function to make sure atleast one vertex is connect with other to make graph connected
    def ensure_vertex_connectivity(self):
        # loop for intersections
        for intersection_id in self.intersections:
            # If not intersection connected with other
            if not self.intersections[intersection_id].connected_roads:
                road_id = 1  # Assuming road_id 1 always exists
                # connect it with intersection
                self.connect_intersection_to_road(intersection_id, road_id)

    # function to distribute packages from source to destination
    def distribute_packages(self):
        # input for enter packages
        num_packages = int(input("Enter the number of packages to deliver: "))
        # loop to iterate packages
        for i in range(num_packages):
            print(f"Package {i + 1}:")
            # input to enter source
            start_house = int(input("Enter starting house ID: "))
            # input to enter destination
            end_house = int(input("Enter ending house ID: "))
            # if condition to find path between vertex
            if nx.has_path(self.G, start_house, end_house):
                # find shortest path between source and destination
                shortest_path = nx.shortest_path(self.G, source=start_house, target=end_house, weight='length')
                # find shortest path length between source and destination
                shortest_path_length = nx.shortest_path_length(self.G, source=start_house, target=end_house,
                                                               weight='length')
                # print shortest path and length
                print("Shortest path from House", start_house, "to House", end_house, ":", shortest_path)
                print("Shortest path length:", shortest_path_length)
            # else print no path between vertex
            else:
                print("No valid path between the specified houses.")


# Create a road network graph
road_network = RoadNetworkGraph()

# Add 5 intersections
for i in range(1, 6):
    road_network.add_intersection(i)

# Add 5 roads and connect them to intersections
road_network.add_road("Anwar st")
road_network.add_road("AlQudarat st")
road_network.add_road("Sheikh Zayed st")
road_network.add_road("Khaleej AlArab st")
road_network.add_road("Qarm st")

# Connect intersections to roads
road_network.connect_intersection_to_road(1, 4)
road_network.connect_intersection_to_road(1, 2)
road_network.connect_intersection_to_road(2, 3)
road_network.connect_intersection_to_road(3, 4)
road_network.connect_intersection_to_road(4, 5)

# Add 5 houses and connect them to intersections
for i in range(1, 6):
    road_network.add_house(i)
    road_network.connect_house_to_intersection(i, i)

road_network.visualize_graph()  # Visualize the road network graph

road_network.ensure_vertex_connectivity()  # Ensure vertex connectivity

road_network.distribute_packages()  # Distribute packages

