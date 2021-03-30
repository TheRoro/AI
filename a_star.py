from heapq import heappush, heappop
import math

cities_dict = {
    "Arad": 0, "Bucharest": 1, "Craiova": 2, "Dobreta": 3, "Eforie": 4, "Fagaras": 5, "Giurgiu": 6, "Hirsova": 7, "Iasi": 8, "Lugoj": 9, "Mehadia": 10, "Neamt": 11, "Oradea": 12, "Pitesti": 13, "Rimnicu Vilcea": 14, "Sibiu": 15, "Timisoara": 16, "Urziceni": 17, "Vaslui": 18, "Zerind": 19
}

dist_heuristic = [
    366, 0, 160, 242, 161, 178, 77, 151, 226, 244, 241, 234, 380, 98, 193, 253, 329, 80, 199, 374
]

city_names = [
    "Arad", "Bucharest", "Craiova", "Dobreta", "Eforie", "Fagaras", "Giurgiu", "Hirsova", "Iasi", "Lugoj", "Mehadia", "Neamt", "Oradea", "Pitesti", "Rimnicu Vilcea", "Sibiu", "Timisoara", "Urziceni", "Vaslui", "Zerind"
]

n_cities = len(city_names)

for i in range(n_cities):
    print(city_names[i], " ", dist_heuristic[i])

def a_star(G, s):
    n = len(G)
    visited = [False]*n
    pred = [None]*n
    cost = [math.inf]*n
    queue = []
    heappush(queue, (0, s))
    cost[s] = 0

    while len(queue) > 0:
        g, u = heappop(queue)
        visited[u]
        for v, w in G[u]:
            if not visited[v]:
                f = g + w
                if f + dist_heuristic[v] < cost[v] + dist_heuristic[u]:
                    cost[v] = f
                    pred[v] = u
                    heappush(queue, (f, v))

    return pred, cost

adj_names = [
    [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)], #Arad
    [("Urziceni", 85), ("Giurgiu", 90), ("Pitesti", 101), ("Fagaras", 211)], #Bucharest
    [("Pitesti", 138), ("Rimnicu Vilcea", 146), ("Dobreta", 120)], #Craiova
    [("Mehadia", 75), ("Craiova", 120)], #Dobreta
    [("Hirsova", 86)], #Eforie
    [("Sibiu", 99), ("Bucharest", 211)], #Fagaras
    [("Bucharest", 90)], #Giurgiu
    [("Urziceni", 98), ("Eforie", 86)], #Hirsova
    [("Neamt", 87), ("Vaslui", 92)], #Iasi
    [("Timisoara", 111), ("Mehadia", 70)], #Lugoj
    [("Lugoj", 70), ("Dobreta", 75)], #Mehadia
    [("Iasi", 87)], #Neamt
    [("Zerind", 71), ("Sibiu", 151)], #Oradea
    [("Rimnicu Vilcea", 97), ("Bucharest", 101), ("Craiova", 138)], #Pitesti
    [("Sibiu", 80), ("Pitesti", 97), ("Craiova", 146)], #Rimnicu Vilcea
    [("Fagaras", 99), ("Rimnicu Vilcea", 80), ("Arad", 140), ("Oradea", 151)], #Sibiu
    [("Arad", 118), ("Lugoj", 111)], #Timisoara
    [("Hirsova", 98), ("Vaslui", 142), ("Bucharest", 85)], #Urziceni
    [("Iasi", 92), ("Urziceni", 142)], #Vaslui
    [("Oradea", 71), ("Arad", 75)], #Zerind
]

adj = []

for el in adj_names:
    neigh = []
    for i in range(len(el)):
        city = (cities_dict[el[i][0]], el[i][1])
        neigh.append(city)
    adj.append(neigh)

start = "Timisoara" #starting city
finish = "Bucharest" #Finish city
start = cities_dict[start]
finish = cities_dict[finish]

#The Algorithm returns the array of predecesors and the cost from the starting city to all the cities
pred, cost = a_star(adj, start)

print("Cost:")
for i in range(len(cost)):
    if(i == finish):
        print(city_names[start], "->", city_names[i], ":", cost[i])

print("\nPath:")
def build_path(pred):
    path = []
    v = finish
    while v != None:
        path.append(city_names[v])
        v = pred[v]
    path.reverse()
    return path

path = build_path(pred)
print(path)