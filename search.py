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
import math
#sdfsdf

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

    path = nearest_neighbor(maze.getStart(), maze.getObjectives())

    total_path = []
    start = maze.getStart()

    while path:
        end = path.pop(0)
        return_value = bfs_path(start, end, maze)
        total_path.append(return_value[0])
        num_states_explored += return_value[1]
        start = end

    final_path = []
    for i in total_path:
        for j in range(0, len(i) - 1):
            final_path.append(i[j])
    last_path = total_path[len(total_path)-1]
    last_spot = last_path[len(last_path)-1]
    final_path.append(last_spot)
    print(final_path)
    return final_path, num_states_explored


def bfs_path(start, end, maze):
    #Initialize the num_states_explored as 0
    num_states_explored = 0

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

    meta[start] = None
    open_set.append(start)

    #While we can still explore
    while open_set:

        #Look at the first element in the queue, we now have started to explore
        #that state
        subroute = open_set.pop(0)

        #If it's our objective, that's all we need in an unweighted graph
        if (subroute == end):
            return make_path(subroute, meta),num_states_explored

        num_states_explored += 1
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


def nearest_neighbor(start, goals):
    result_list = []

    new_start = start

    while goals:

        new_list = []
        mini = -1
        for i in goals:
            new_list.append(a_star_heuristic(new_start, i))

            mini = min(new_list)

        index = 0
        for i in range(0, len(new_list)):
            if(new_list[i] == mini):
                index = i
                break

        new_start = goals.pop(i)
        result_list.append(new_start)

    return result_list


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

#https://www.geeksforgeeks.org/best-first-search-informed-search/


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

    #This dictionary is to used keep the information needed to get the
    #PriorityQ going, is a 3-tuple (distance from start using best path, manhattan distance)
    spot_information = dict()

    #Get starting point, initalize it's dict value so that we know when to stop
    #Going back and looking, putting it on the stack to start us off
    start = maze.getStart()
    meta[start] = None
    spot_information[start] = (0, distance_away(start, end), 0)

    #Priority Considers the sum of the cost to get there and Manhattan
    open_set.put( (spot_information[start][0] + spot_information[start][1], start) )

    #While we can still explore
    while open_set:
        subroute_tuple = open_set.get(0)
        subroute = subroute_tuple[1]

        num_states_explored += 1

        if (subroute == end):
            return make_path(subroute, meta),num_states_explored

        for neighbor in maze.getNeighbors(subroute[0], subroute[1]):

            #Update our information dictionary
            if(neighbor not in spot_information):
                #Update dictionary using previous value and hueristic (Manhattan) and making it unvisited
                spot_information[neighbor] = (spot_information[subroute][0] + 1 , distance_away(neighbor, end) , 0)
                meta[neighbor] = subroute

            #Our dictionary value needs to be replaced because we found a better route
            elif(spot_information[neighbor][0] > spot_information[subroute][0] + 1):
                spot_information[neighbor] = (spot_information[subroute][0] + 1, distance_away(neighbor, end),spot_information[neighbor][2])
                meta[neighbor] = subroute

            #We've seen this before
            if(spot_information[neighbor][2] == 2):
                continue

            #We haven't looked at this yet
            if(spot_information[neighbor][2] == 0):
                spot_information[neighbor] = (spot_information[neighbor][0], spot_information[neighbor][1], 1)
                open_set.put( (spot_information[neighbor][0] + spot_information[neighbor][1], neighbor) )

        spot_information[subroute] = (spot_information[subroute][0], spot_information[subroute][1], 2)



    #If we can't find a path, num_states_explored should be every possible
    #coordinate
    return [], num_states_explored


#https://en.wikipedia.org/wiki/A*_search_algorithms

def a_star_heuristic(spot, end):
    #Who knows
    #Pythagorean distance
    return math.hypot(spot[1] - end[1], spot[0] - end[0])

def astar(maze):

    num_states_explored = 0

    end = maze.getObjectives()[0]
    start = maze.getStart()

    closed_set = set()

    open_set = PriorityQueue()
    track_set = set()

    came_from = dict()
    came_from[start] = None

    gScore = dict()

    dimensions = maze.getDimensions()

    for i in range(0, dimensions[0]):
        for j in range(0, dimensions[1]):
            if(maze.isWall(i, j)):
                gScore[(i, j)] = -1
            else:
                gScore[(i, j)] = 10000000

    gScore[start] = 0

    fScore = dict()

    for i in range(0, dimensions[0]):
        for j in range(0, dimensions[1]):
            if(maze.isWall(i, j)):
                fScore[(i, j)] = -1
            else:
                fScore[(i, j)] = 10000000

    fScore[start] = a_star_heuristic(start, end)


    open_set.put( (fScore[start], start) )
    track_set.add(start)

    while open_set:
        current_tuple = open_set.get(0)

        current = current_tuple[1]
        track_set.remove(current)

        num_states_explored += 1

        if (current == end):
            return make_path(current, came_from), num_states_explored
            #return [], 0

        closed_set.add(current)

        for neighbor in maze.getNeighbors(current[0], current[1]):
            if neighbor in closed_set:
                continue

            tentative_gScore = gScore[current] + 1

            if neighbor not in track_set:

                came_from[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + a_star_heuristic(neighbor, end)

                open_set.put(  (fScore[neighbor], neighbor)  )
                track_set.add(neighbor)

            elif tentative_gScore >= gScore[neighbor]:
                continue

            came_from[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + a_star_heuristic(neighbor, end)

    return [], 0
