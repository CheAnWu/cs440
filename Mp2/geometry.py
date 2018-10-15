# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
from const import *
import numpy as np
import time

def computeCoordinate(start, length, angle):
    """Compute the end coordinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to counter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """

    #Change this line, only to check if program actually works with human input
    # angle = angle /100.0
    angle = math.radians(angle)


    delX = length * math.cos(angle)
    delY = length * math.sin(angle)

    endX = start[0] + delX
    endY = start[1] - delY

    return (endX, endY)

def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """

    for joint in armPos:
        for obstacle in obstacles:

            if( (doesPointTouchCircle(joint[0], obstacle) or doesPointTouchCircle(joint[1], obstacle) ) == True ):
                print("BAD TOUCH")
                return True
            closestPointOnLine = closestPointOnLineHelper(joint, obstacle)

            if(isPointOnArmLine(closestPointOnLine, joint)):
                # print(closestPointOnLine)
                if(doesPointTouchCircle(closestPointOnLine, obstacle) ):
                    print("BAD TOUCH")
                    return True

    return False

def closestPointOnLineHelper(armLine, obstacle):
    '''
    delta_x = armLine[0][0] - armLine[1][0]
    delta_y = armLine[1][1] - armLine[0][1]
    c_sqaured = delta_x**2 + delta_y**2

    nx = ((obstacle[0]-armLine[0][0])*delta_x + (obstacle[1]-armLine[1][0])*delta_y) / c_sqaured

    return (delta_x * nx + armLine[0][0], delta_y*nx + armLine[1][0])
    '''
    x1 = armLine[0][0]
    y1 = armLine[0][1]

    x2 = armLine[1][0]
    y2 = armLine[1][1]

    x3 = obstacle[0]
    y3 = obstacle[1]

    u = ((x3-x1)*(x2-x1) + (y3-y1)*(y2-y1)) /((math.hypot(armLine[1][0] - armLine[0][0], armLine[1][1] - armLine[0][1]))**2)

    return (x1 + u*(x2-x1), y1 + u*(y2-y1))

def isPointOnArmLine(point, armLine):
    x_coord = [armLine[0][0], armLine[1][0]]
    y_coord = [armLine[0][1], armLine[1][1]]

    x_right = max(x_coord)
    x_left = min(x_coord)

    y_top = max(y_coord)
    y_bot = min(y_coord)

    if(x_left <= point[0] and x_right >= point[0]):
        if(y_bot <= point[1] and y_top >= point[1]):
            return True

    return False

def doesPointTouchCircle(armEnd, circle):

    dist = math.hypot(armEnd[0] - circle[0], armEnd[1] - circle[1])

    radius = circle[2]

    #Is the distance less or equal to the radius -> is arm in circle
    if (dist <= radius):
        return True
    else:
        return False

def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for goal in goals:
        if(doesPointTouchCircle(armEnd, goal) == True):
            return True

    return False

def isJointWithinWindow(joint, window):

    if(joint[0][0] > window[0] or joint[0][0] < 0):
        return False
    elif(joint[0][1] > window[1] or joint[0][1] < 0):
        return False

    if(joint[1][0] >= window[0] or joint[1][0] < 0):
        return False
    elif(joint[1][1] > window[1] or joint[1][1] < 0):
        return False


    return True

def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """


    for joint in armPos:
        if(isJointWithinWindow(joint, window) == False):
            return False

    return True
