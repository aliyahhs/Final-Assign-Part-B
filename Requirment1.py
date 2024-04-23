#Import libraries of python for plot and visualize graph using networkx library
import networkx as nx
import matplotlib.pyplot as plt

class Intersection:     #Class for representing an intersection
    def __init__(self, intersection_id):
        self.id = intersection_id
        self.connected_roads = []       #List to add roads in list

    def add_road(self, road_id):        #Add road method
        self.connected_roads.append(road_id)

# Class for representing a road
class Road:     #Road class to add roads that are edges
    def __init__(self, road_id, road_name, length):
        # Parameters for roads
        self.id = road_id
        self.road_name = road_name
        self.length = length

# Class for representing a road network graph
class RoadNetworkGraph:         #RoadNetworkGraph class to create road network
    def __init__(self):
        self.intersections = {}  #Dictionary to store intersections
        self.roads = {}          #Dictionary to store roads
        self.next_road_id = 1    #ID counter for roads

    def add_intersection(self, intersection_id):    #Add intersections method to add intersection
        if intersection_id not in self.intersections:       #If intersection is not then add intersection
            self.intersections[intersection_id] = Intersection(intersection_id)

    def add_road(self, road_id, road_name, length):  #Add road function to add roads in network
        self.roads[road_id] = Road(road_id, road_name, length)  #Add roads by calling Road object
        return road_id

    def connect_intersection_to_road(self, intersection_id, road_id): #Connect intersection with road function
        if intersection_id in self.intersections and road_id in self.roads:
            intersection = self.intersections[intersection_id]
            intersection.add_road(road_id)  #Add road in intersection with id

    def visualize_graph(self):  #Visualize graph function to visualize graph
        G = nx.DiGraph()  #Create a directed graph object

        #Add nodes for intersections
        for intersection_id in self.intersections: #For loop to add intersection in graph
            G.add_node(intersection_id)

        # Add edges for roads
        for road_id, road in self.roads.items():    #for loop to add roads in graph that connects with intersection
            for intersection_id in self.intersections:
                if road_id in self.intersections[intersection_id].connected_roads:
                    G.add_edge(intersection_id, road_id, road_name=f"{road.road_name} (ID: {road.id})", length=road.length)  # Add edge with id,name,length,congestion level in graph

        # isualize the graph
        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G, scale=5)
        nx.draw(G, pos, with_labels=True, node_size=400, node_color='skyblue', font_size=7, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{G.edges[u, v]['road_name']} ({G.edges[u, v]['length']} KM)" for u, v in G.edges()}, font_size=10, font_color='red')
        plt.title("Road Network Graph")
        plt.show()

    def ensure_vertex_connectivity(self):  #Function to make sure at least one vertex is connected with other to make the whole graph connected
        for intersection_id in self.intersections:
            if not self.intersections[intersection_id].connected_roads:
                print("Intersection", intersection_id, "is not connected to any road.")
                break

    def find_shortest_path(self, start_intersection_id, end_intersection_id):   #Function to find the shortest path between the desired start till the end of the path
        G = nx.Graph()
        for road_id, road in self.roads.items():
            for intersection_id in self.intersections:
                if road_id in self.intersections[intersection_id].connected_roads:
                    G.add_edge(intersection_id, road_id, weight=road.length)

        if nx.has_path(G, start_intersection_id, end_intersection_id):  #check if there is a path between the start and end intersections
            shortest_path = nx.shortest_path(G, source=start_intersection_id, target=end_intersection_id, weight='weight')  # Find the shortest path
            return shortest_path
        else:
            return None

    def routing_suggestions(self, start_intersection_id, end_intersection_id):  #function to provide routing suggestions from start to end intersections
        shortest_path = self.find_shortest_path(start_intersection_id, end_intersection_id)
        if shortest_path:
            suggestions = []
            for i in range(len(shortest_path) - 1):
                intersection_id = shortest_path[i]
                road_id = shortest_path[i + 1]
                for connected_road_id in self.intersections[intersection_id].connected_roads:
                    if connected_road_id == road_id:
                        road = self.roads[road_id]
                        suggestions.append(road.road_name)
                        break
            return suggestions
        else:
            return None  #Return None if no path is found


road_network = RoadNetworkGraph()   #Create a road network graph

#Add 5 intersections
for i in range(1, 6):
    road_network.add_intersection(i)

#Add 5 roads and connect them to intersections
road_network.add_road(1, "Anwar st", 10)
road_network.add_road(2, "AlQudarat st", 15)
road_network.add_road(3, "Sheikh Zayed st", 8)
road_network.add_road(4, "Khaleej AlArab st", 12)
road_network.add_road(5, "Qarm st", 7)

#Connect intersections to roads
road_network.connect_intersection_to_road(1, 4)
road_network.connect_intersection_to_road(1, 2)
road_network.connect_intersection_to_road(2, 3)
road_network.connect_intersection_to_road(3, 4)
road_network.connect_intersection_to_road(4, 5)

road_network.visualize_graph()      #Visualize the road network graph

road_network.ensure_vertex_connectivity()       #Ensure vertex connectivity

#Test cases: Find the shortest path between two intersections
start_intersection_id = 3
end_intersection_id = 5
shortest_path = road_network.find_shortest_path(start_intersection_id, end_intersection_id)
if shortest_path:
    print("Shortest Path:", shortest_path)
else:
    print("No path between the intersections.")

#Provide routing suggestions for the given start and end intersection
suggestions = road_network.routing_suggestions(start_intersection_id, end_intersection_id)
if suggestions:
    print("Routing Suggestions:", suggestions)
else:
    print("No routing suggestions available.")

