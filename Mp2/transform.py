
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    alphalimit, betalimit = arm.getArmLimit()
    print(arm.getArmLimit())
    # numrows = int(abs(alphalimit[1] - alphalimit[0])//int(granularity)) + 1
    # numcols = int(abs(betalimit[1] - betalimit[0])//int(granularity)) + 1

    bounds = angleToIdx([alphalimit[1], betalimit[1]], [alphalimit[0], betalimit[0]], granularity)
    numrows = bounds[0]
    numcols = bounds[1]

    print(bounds[0], bounds[1])
    maze_arr = [[0 for x in range(numcols)] for y in range(numrows)]

    start_angles = arm.getArmAngle()
    start_angles = [(start_angles[0] - alphalimit[0])//granularity + 1, (start_angles[1] - betalimit[0])//granularity + 1]
    print("sp", start_angles)

    for i in range(numrows):
        for j in range(numcols):
            arm.setArmAngle(((i * math.floor(granularity) + alphalimit[0]), (j * math.floor(granularity) + betalimit[0])))
            # print(arm.getArmAngle())
            if not isArmWithinWindow(arm.getArmPos(), window):
                maze_arr[i][j] = '%'
                print("HElo")
            elif doesArmTouchObstacles(arm.getArmPos(), obstacles):
                maze_arr[i][j] = '%'
                print("HElo")
            elif doesArmTouchGoals(arm.getEnd(), goals):
                maze_arr[i][j] = '.'
            else:
                maze_arr[i][j] = ' '


    maze_arr[start_angles[0]][start_angles[1]] = 'P'
    print(maze_arr)
    print(granularity)

    mazeobj = Maze(maze_arr, list([alphalimit[0], betalimit[0]]), granularity)

    return mazeobj


def transformCoord(i, j, alphalimit, betalimit, granularity):
    x = (i * math.floor(granularity) + alphalimit[0])
