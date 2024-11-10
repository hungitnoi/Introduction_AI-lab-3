import queue
import matplotlib.pyplot as plt

# Getting heuristics from file
def getHeuristics():
    heuristics = {}
    with open("heuristics.txt") as f:
        for i in f.readlines():
            node_heuristics_val = i.split()
            heuristics[node_heuristics_val[0]] = int(node_heuristics_val[1])
    return heuristics

def getCity():
    city = {}
    citiesCode = {}
    with open("cities.txt") as f:
        j = 1
        for i in f.readlines():
            node_city_val = i.split()
            
            # Check if the line has exactly three values
            if len(node_city_val) == 3:
                city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]
                citiesCode[j] = node_city_val[0]
                j += 1
            else:
                print(f"Skipping invalid line in cities.txt: {i.strip()}")
                
    return city, citiesCode

def createGraph():
    graph = {}
    with open("citiesGraph.txt") as file:
        for i in file.readlines():
            node_val = i.split()
            if node_val[0] in graph:
                graph[node_val[0]].append([node_val[1], int(node_val[2])])
            else:
                graph[node_val[0]] = [[node_val[1], int(node_val[2])]]
            
            if node_val[1] in graph:
                graph[node_val[1]].append([node_val[0], int(node_val[2])])
            else:
                graph[node_val[1]] = [[node_val[0], int(node_val[2])]]
    return graph

def GBFS(start_node, heuristics, graph, goal_node):
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((heuristics[start_node], start_node))
    path = []

    while not priorityQueue.empty():
        current = priorityQueue.get()[1]
        path.append(current)

        if current == goal_node:
            break

        for i in graph[current]:
            if i[0] not in path:
                priorityQueue.put((heuristics[i[0]], i[0]))
    
    return path

def Astar(start_node, heuristics, graph, goal_node):
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((heuristics[start_node], start_node, 0)) 
    came_from = {start_node: None} 
    g_score = {start_node: 0}  
    path = []

    while not priorityQueue.empty():
        _, current, current_g = priorityQueue.get()

   
        if current == goal_node:
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

       
        for neighbor, cost in graph[current]:
            tentative_g_score = current_g + int(cost)

          
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristics[neighbor]
                priorityQueue.put((f_score, neighbor, tentative_g_score))
                came_from[neighbor] = current

    return path

def drawMap(city, gbfs, astar, graph):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], color="gray")
    
    for i in range(len(gbfs) - 1):
        first = city[gbfs[i]]
        second = city[gbfs[i + 1]]
        plt.plot([first[0], second[0]], [first[1], second[1]], color="green")

    for i in range(len(astar) - 1):
        first = city[astar[i]]
        second = city[astar[i + 1]]
        plt.plot([first[0], second[0]], [first[1], second[1]], color="blue")

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.errorbar(1, 1, label="ASTAR", color="blue")
    plt.legend(loc="lower left")
    plt.show()

if __name__ == "__main__":
    heuristic = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode1 = int(input("Enter start node: "))
        inputCode2 = int(input("Enter goal node: "))

        if inputCode1 == 0 or inputCode2 == 0:
            break

        startCity = citiesCode[inputCode1]
        endCity = citiesCode[inputCode2]

        gbfs = GBFS(startCity, heuristic, graph, endCity)
        astar = Astar(startCity, heuristic, graph, endCity)
        print("GBFS => ", gbfs)
        print("Astar => ", astar)

        drawMap(city, gbfs, astar, graph)
