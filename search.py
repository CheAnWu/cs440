# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

from queue import *

def makeTrueDistChart(maze, goals, start):
    goalsAndStart = goals.copy()
    goalsAndStart.insert(0, start)
    fullChart = [[0 for x in range(0, len(goalsAndStart))] for x in range(0, len(goalsAndStart))]

    for i in range(len(goalsAndStart)):

        for j in range(i,len(goalsAndStart)):

            if (i == j):
                fullChart[i][j] = 0
            else:
                value = preComputationAstar(maze, goals[i-1], goals[j-1])
                #print(goals[i-1], goals[j-1], value)
                fullChart[i][j] = value
                fullChart[j][i] = value

    return fullChart




#returns dist from one goal node to another
def preComputationAstar(maze, start, end):
    closed_set = set()

    open_set = PriorityQueue()
    track_set = set()

    came_from = dict()
    came_from[start] = None

    gScore = dict()

    dimensions = maze.getDimensions()

    for i in range(0, dimensions[0]):
        for j in range(0, dimensions[1]):
            if (maze.isWall(i, j)):
                gScore[(i, j)] = -1
            else:
                gScore[(i, j)] = 10000000

    gScore[start] = 0

    fScore = dict()

    for i in range(0, dimensions[0]):
        for j in range(0, dimensions[1]):
            if (maze.isWall(i, j)):
                fScore[(i, j)] = -1
            else:
                fScore[(i, j)] = 10000000

    fScore[start] = distance_away(start, end)

    open_set.put((fScore[start], start))
    track_set.add(start)

    while open_set:
        current_tuple = open_set.get(0)

        current = current_tuple[1]
        track_set.remove(current)

        if (current == end):
            return len(make_path(current, came_from))

        closed_set.add(current)

        for neighbor in maze.getNeighbors(current[0], current[1]):
            if neighbor in closed_set:
                continue

            tentative_gScore = gScore[current] + 1

            if neighbor not in track_set:

                came_from[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + distance_away(neighbor, end)

                open_set.put((fScore[neighbor], neighbor))
                track_set.add(neighbor)

            elif tentative_gScore >= gScore[neighbor]:
                continue

            came_from[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + distance_away(neighbor,end)

    return 100000

def nearest_neighbor(start, goals):
    result_list = []

    new_start = start

    while goals:

        new_list = []
        mini = -1
        for i in goals:
            new_list.append(distance_away(new_start, i))

            mini = min(new_list)

        index = 0
        for i in range(0, len(new_list)):
            if(new_list[i] == mini):
                index = i
                break

        new_start = goals.pop(i)
        result_list.append(new_start)

    return result_list

def search(maze, searchMethod):
    return {
        "bfs": bfs(maze),
        "dfs": dfs(maze),
        "greedy": greedy(maze),
        "astar": astar(maze),
    }.get(searchMethod, [])


def bfs(maze):

    #BFS is Implemented with a queue
    #A lot of code is borrowed from the Wiki for bfs

    #Initialize the num_states_explored as 0
    num_states_explored = 0

    #This method returns an array of all objectives, this just grabs the first
    end = maze.getObjectives()[0]

    #This is my fake queue
    open_set = list()

    #Needed in order to tell if we've seen a state or not
    closed_set = set()

    #Very helpful in finding the path back
    #If we make every coordinate map to the coordinate that got it there
    #We can iterate through the dictionary backwards to get our backwards path
    meta = dict()

    #Get starting point, initalize it's dict value so that we know when to stop
    #Going back and looking, putting it on the queue to start us off
    start = maze.getStart()
    meta[start] = None
    open_set.append(start)

    #While we can still explore
    while open_set:

        #Look at the first element in the queue, we now have started to explore
        #that state
        subroute = open_set.pop(0)
        num_states_explored += 1

        #If it's our objective, that's all we need in an unweighted graph
        if (subroute == end):
            return make_path(subroute, meta),num_states_explored

        #Get the neighbors so we can check up on them eventually
        for neighbor in maze.getNeighbors(subroute[0], subroute[1]):

            #If we've already seen it, move along
            if neighbor in closed_set:
                continue

            #If we have a new entry, map it in the dictionary and add it to queue
            if neighbor not in open_set:
                meta[neighbor] = subroute
                open_set.append(neighbor)

        #We are now done exploring this coordinate
        closed_set.add(subroute)

    #If we can't find a path, num_states_explored should be every possible
    #coordinate
    return [], num_states_explored

###########################################################
# Helper method for retracing your steps
#
# Input:
# spot: coordinate of where we want to know the path too
# meta: The dictionary that tells us where to retrace
#
# Return:
# An array/list of our path from start to spot
#
###########################################################

def make_path(spot, meta):

    #Initialize our staring list
    moves_made = list()

    #Add our ending spot
    moves_made.append(spot)

    #Go through and find the coordinate that got you there and add it
    while meta[spot] != None:
        spot = meta[spot]
        moves_made.append(spot)

    # Using this method, we start with our end and end with our start,
    # So we need to reverse it
    moves_made.reverse()

    return moves_made


def dfs(maze):
    #DFS is Implemented with a stack
    #A lot of code is borrowed from the Wiki for dfs

    #Initialize the num_states_explored as 0
    num_states_explored = 0

    #This method returns an array of all objectives, this just grabs the first
    end = maze.getObjectives()[0]

    #This is my fake Stack
    open_set = list()

    #Needed in order to tell if we've seen a state or not
    closed_set = set()

    #Very helpful in finding the path back
    #If we make every coordinate map to the coordinate that got it there
    #We can iterate through the dictionary backwards to get our backwards path
    meta = dict()

    #Get starting point, initalize it's dict value so that we know when to stop
    #Going back and looking, putting it on the stack to start us off
    start = maze.getStart()
    meta[start] = None
    open_set.append(start)

    #While we can still explore
    while open_set:

        #Look at the most recently add coord in the stack, we now have started
        #to explore that state
        subroute = open_set.pop(len(open_set) - 1)
        num_states_explored += 1

        #If it's our objective, that's all we need in an unweighted graph
        if (subroute == end):
            return make_path(subroute, meta),num_states_explored

        #Get the neighbors so we can check up on them eventually
        for neighbor in maze.getNeighbors(subroute[0], subroute[1]):

            #If we've already seen it, move along
            if neighbor in closed_set:
                continue

            #If we have a new entry, map it in the dictionary and add it to queue
            if neighbor not in open_set:
                meta[neighbor] = subroute
                open_set.append(neighbor)

        #We are now done exploring this coordinate
        closed_set.add(subroute)

    #If we can't find a path, num_states_explored should be every possible
    #coordinate
    return [], num_states_explored

def distance_away(spot, end):
    return abs(end[0]-spot[0]) + abs(end[1]-spot[1])


def greedy(maze):
    #Greedy is Implemented with a PriorityQ

    #Initialize the num_states_explored as 0
    num_states_explored = 0

    #This method returns an array of all objectives, this just grabs the first
    end = maze.getObjectives()[0]

    open_set = PriorityQueue()

    #Needed in order to tell if we've seen a state or not
    closed_set = set()

    #Very helpful in finding the path back
    #If we make every coordinate map to the coordinate that got it there
    #We can iterate through the dictionary backwards to get our backwards path
    meta = dict()

    spot_information = dict()

    #Get starting point, initalize it's dict value so that we know when to stop
    #Going back and looking, putting it on the stack to start us off
    start = maze.getStart()
    meta[start] = None
    spot_information[start] = (0, distance_away(start, end), 0)

    #print(start)

    open_set.put( (spot_information[start][0] + spot_information[start][1], start) )

    #While we can still explore
    while open_set:
        subroute_tuple = open_set.get(0)
        subroute = subroute_tuple[1]

        num_states_explored += 1
        #print(subroute[1])

        if (subroute == end):
            return make_path(subroute, meta),num_states_explored

        for neighbor in maze.getNeighbors(subroute[0], subroute[1]):

            if(neighbor not in spot_information):
                spot_information[neighbor] = (spot_information[subroute][0] + 1 , distance_away(neighbor, end) , 0)
                meta[neighbor] = subroute

            elif(spot_information[neighbor][0] > spot_information[subroute][0] + 1):
                spot_information[neighbor] = (spot_information[subroute][0] + 1, distance_away(neighbor, end),spot_information[neighbor][2])
                meta[neighbor] = subroute

            if(spot_information[neighbor][2] == 2):
                continue

            if(spot_information[neighbor][2] == 0):
                spot_information[neighbor] = (spot_information[neighbor][0], spot_information[neighbor][1], 1)
                open_set.put( (spot_information[neighbor][0] + spot_information[neighbor][1], neighbor) )

        spot_information[subroute] = (spot_information[subroute][0], spot_information[subroute][1], 2)



    #If we can't find a path, num_states_explored should be every possible
    #coordinate
    return [], num_states_explored


def longest_length_2(graph, leng, root):

    lengths = []

    #print(graph)
    flag = True
    for i in graph:
        #print(i)
        if(i[0] == root):
            flag = False
            graph.remove(i)
            sum = i[2] + longest_length_2(graph, i[2], i[1])
            lengths.append(sum)
            #print(lengths)
        elif(i[1] == root):
            flag = False
            graph.remove(i)
            sum = i[2] + longest_length_2(graph, i[2], i[0])
            lengths.append(sum)
            #print(lengths)


    if(flag):
        return 0

    if(root == 0):
        max1 = max(lengths)
        lengths.remove(max1)
        if(len(lengths) == 0):
            return max1
        max2 = max(lengths)
        return max1+ max2

    return (max(lengths))





def a_star_heuristic(spot, goals, maze):
    #Who knows
    #LUKASKNOWS

    '''
    chart = makeTrueDistChart(maze, goals.copy(), spot)


    rep_graph = Graph(len(goals) + 1)

    for i in range(0, len(chart)):
        for j in range(i, len(chart[0])):
            rep_graph.addEdge(i, j, chart[i][j])
    Kruskal_findMST(rep_graph)
    baby = longest_length_2(rep_graph.graph[len(goals)+1:len(goals)+1 + len(goals)].copy(), 0, 0 )
    #print (baby)
    return baby - len(goals)
    '''





    x_coord = spot

    left = []
    right = []

    for i in goals:
        if(i[0] < x_coord[0]):
            left.append(i)
        else:
            right.append(i)

    left_most = spot
    for i in left:
        if(abs(x_coord[0] - i[0]) > abs(x_coord[0] - left_most[0])):
            left_most = i

    right_most = spot
    for i in right:
        if(abs(x_coord[0] - i[0]) > abs(x_coord[0] - right_most[0])):
            right_most = i

    left_right_dist = -1
    if( abs(x_coord[0] - right_most[0]) > abs(x_coord[0] - left_most[0])):
        left_right_dist = abs(x_coord[0] - left_most[0])* 2 + abs(x_coord[0] - right_most[0])
    else:
        left_right_dist = abs(x_coord[0] - left_most[0]) + abs(x_coord[0] - right_most[0])*2


    top = []
    bot = []

    for i in goals:
        if(i[1] < x_coord[1]):
            bot.append(i)
        else:
            top.append(i)

    top_most = spot
    for i in top:
        if(abs(x_coord[1] - i[1]) > abs(x_coord[1] - top_most[1])):
            top_most = i

    bot_most = spot
    for i in bot:
        if(abs(x_coord[1] - i[1]) > abs(x_coord[1] - bot_most[1])):
            bot = i

    top_bot_dist = -1
    if( abs(x_coord[0] - bot_most[0]) > abs(x_coord[0] - top_most[0])):
        top_bot_dist = abs(x_coord[0] - top_most[0])* 2 + abs(x_coord[0] - bot_most[0])
    else:
        top_bot_dist = abs(x_coord[0] - top_most[0]) + abs(x_coord[0] - bot_most[0])*2

    return 1.8*(left_right_dist + top_bot_dist)

def astar(maze):

    num_states_explored = 0

    start = maze.getStart()

    open_set = PriorityQueue()

    gScore = dict()

    seen = dict()

    dimensions = maze.getDimensions()

    for i in range(0, dimensions[0]):
        for j in range(0, dimensions[1]):
            if(maze.isWall(i, j)):
                gScore[(i, j)] = -1

            else:
                gScore[(i, j)] = 10000000
                seen[(i, j)] = False

    gScore[start] = 0

    fScore = dict()

    for i in range(0, dimensions[0]):
        for j in range(0, dimensions[1]):
            if(maze.isWall(i, j)):
                fScore[(i, j)] = -1
            else:
                fScore[(i, j)] = 10000000

    goals = maze.getObjectives()

    chart = makeTrueDistChart(maze, goals, maze.getStart())

    rep_graph = Graph(len(goals) + 1)

    for i in range(0, len(chart)):
        for j in range(i, len(chart[0])):
            rep_graph.addEdge(i, j, chart[i][j])

    Kruskal_findMST(rep_graph)
    #print(rep_graph.graph)

    fScore[start] = a_star_heuristic(start, goals, maze)

    open_set.put( (fScore[start], [start], goals.copy(), set() ) )

    while open_set:

        current_tuple = open_set.get(0)

        current_path = current_tuple[1]
        current_goals = current_tuple[2]

        #print("goals:", current_goals)
        visited = current_tuple[3]

        last_spot = current_path[-1]

        if(seen[last_spot] == False):
            num_states_explored += 1
            print(num_states_explored)
            seen[last_spot] = True

        #print(current_path)
        #print("Goals: ", current_goals)

        if (last_spot in current_goals):
            current_goals.remove(last_spot)
            visited = set()


        if(len(current_goals) == 0):
            return current_path, num_states_explored

        visited.add(last_spot)

        for neighbor in maze.getNeighbors(last_spot[0], last_spot[1]):
            if neighbor in visited:
                continue

            neighbor_path  = current_path.copy()
            neighbor_path.append(neighbor)

            neighbor_goals = current_goals.copy()

            neighbor_visited = visited.copy()

            h_value = len(neighbor_path) + a_star_heuristic(neighbor, neighbor_goals, maze)

            open_set.put( (h_value, neighbor_path, neighbor_goals, neighbor_visited ) )

    return [], 0

#Obtained from https://www.geeksforgeeks.org/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/
class Graph:

    def __init__(self,vertices):
        self.V= vertices #No. of vertices
        self.graph = [] # default dictionary
                                # to store graph


    # function to add an edge to graph
    def addEdge(self,u,v,w):
        self.graph.append([u,v,w])

    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        # Attach smaller rank tree under root of
        # high rank tree (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot

        # If ranks are same, then make one as root
        # and increment its rank by one
        else :
            parent[yroot] = xroot
            rank[xroot] += 1

def Kruskal_findMST(input_graph):

    final_MST = []

    index = 0
    e_index = 0

    input_graph.graph = sorted(input_graph.graph, key=lambda item: item[2])

    parent = []

    rank = []

    for node in range(input_graph.V):
        parent.append(node)
        rank.append(0)

    while (e_index < input_graph.V - 1):
        u,v,w = input_graph.graph[index]
        index = index + 1
        x = input_graph.find(parent, u)
        y = input_graph.find(parent, v)


        if (x != y):
            e_index += 1
            final_MST.append([u,v,w])
            input_graph.union(parent, rank, x, y)
    # print the contents of result[] to display the built MST
    #print ("Following are the edges in the constructed MST")
    #for u,v,weight in final_MST:
        #print str(u) + " -- " + str(v) + " == " + str(weight)
        #print ("%d -- %d == %d" % (u,v,weight))
