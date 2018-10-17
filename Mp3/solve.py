import numpy as np
from queue import PriorityQueue
from pythonds.basic.stack import Stack
import copy


"""
    Implement me!!!!!!!
    The solve function takes in a set of constraints. The first dimension is the axis
    to which the constraints refer to. The second dimension is the list of constraints
    for some axis index pair. The third demsion is a single constraint of the form 
    [i,j] which means a run of i js. For example, [4,1] would correspond to a block
    [1,1,1,1].

    The return value of this function should be a numpy array that satisfies all
    of the constraints.


	A puzzle will have the constraints of the following format:


	array([
		[list([[4, 1]]), 
		 list([[1, 1], [1, 1], [1, 1]]),
         list([[3, 1], [1, 1]]), 
		 list([[2, 1]]), 
		 list([[1, 1], [1, 1]])],
        [list([[2, 1]]), 
		 list([[1, 1], [1, 1]]), 
		 list([[3, 1], [1, 1]]),
         list([[1, 1], [1, 1]]), 
		 list([[5, 1]])]
		], dtype=object)

	And a corresponding solution may be:

	array([[0, 1, 1, 1, 1],
		   [1, 0, 1, 0, 1],
		   [1, 1, 1, 0, 1],
		   [0, 0, 0, 1, 1],
		   [0, 0, 1, 0, 1]])



	Consider a more complicated set of constraints for a colored nonogram.

	array([
	   [list([[1, 1], [1, 4], [1, 2], [1, 1], [1, 2], [1, 1]]),
        list([[1, 3], [1, 4], [1, 3]]), 
		list([[1, 2]]),
        list([[1, 4], [1, 1]]), 
		list([[2, 2], [2, 1], [1, 3]]),
        list([[1, 2], [1, 3], [1, 2]]), 
		list([[2, 1]])],
       [list([[1, 3], [1, 4], [1, 2]]),
        list([[1, 1], [1, 4], [1, 2], [1, 2], [1, 1]]),
        list([[1, 4], [1, 1], [1, 2], [1, 1]]), 
		list([[1, 2], [1, 1]]),
        list([[1, 1], [2, 3]]), 
		list([[1, 2], [1, 3]]),
        list([[1, 1], [1, 1], [1, 2]])]], 
		dtype=object)

	And a corresponding solution may be:

	array([
		   [0, 1, 4, 2, 1, 2, 1],
		   [3, 4, 0, 0, 0, 3, 0],
		   [0, 2, 0, 0, 0, 0, 0],
		   [4, 0, 0, 0, 0, 0, 1],
		   [2, 2, 1, 1, 3, 0, 0],
		   [0, 0, 2, 0, 3, 0, 2],
		   [0, 1, 1, 0, 0, 0, 0]
		 ])


    """

# passes in a row/col from the constraints list and returns all possible configurations
def findPossibleValues(result, state, pointsNeeded, dimension):
    if (len(state) > dimension):
        return result

    # constraints satisfied. Fill with 0s and return
    if (len(pointsNeeded) == 0):
        while (len(state) < dimension):
            state.append(0)
        result.append(state)
        return result

    # add '1' elements and recurse
    a = state.copy()
    aPointsNeeded = pointsNeeded.copy()
    for i in range(pointsNeeded[0][0]):
        a.append(1)
    del aPointsNeeded[0]

    # too big, this route doesn't work
    if (len(a) > dimension):
        return result

    # snug fit and done
    if (len(a) == dimension):
        if (len(aPointsNeeded) == 0):
            result.append(a)
            return result
        else:
            return result

    a.append(0)
    result = findPossibleValues([], a, aPointsNeeded.copy(), dimension)

    # add a 0 element to next spot
    b = state.copy()
    b.append(0)

    # snug fit and done
    if (len(b) == dimension):
        if (len(pointsNeeded) == 0):
            result.append(b)
            return result
        else:
            return result

    resultB = findPossibleValues([], b, pointsNeeded.copy(), dimension)

    for val in resultB:
        result.append(val)

    return result


def findValuesHelper(constraintAxis, dimension):
    values = []
    for val in constraintAxis:
        curr_list = findPossibleValues([], [], val.copy(), dimension)
        values.append(curr_list)

    return values

#don't need anymore
def leastConstrainingValue(solutionArray, variable):
    minInconsistencies = 999
    index = -1

    for i in range(len(variable)):
        val = variable[i]
        inconsistencies = countInconsistencies(solutionArray, val)

        if (inconsistencies < minInconsistencies):
            index = i
            minInconsistencies = inconsistencies

    return index


def countInconsistencies(solutionArray, val):
    inconsistencies = 0
    for i in range(len(solutionArray)):
        if(solutionArray[i] != val[i] and solutionArray[i] != -1):
            inconsistencies += 1
    return inconsistencies

#can be used whenever
def fillSolutionMatrixWithDefiniteValues(rowVariables, colVariables, solutionMatrix):
    i = 0
    for rowIndex in rowVariables:
        possibilities = len(rowIndex)
        if possibilities == 1:
            solutionMatrix[i] = rowIndex[0]
        i += 1

    i = 0
    for colIndex in colVariables:
        possibilities = len(colIndex)
        if possibilities == 1:
            solutionMatrix[:, i] = colIndex[0]
        i += 1

    return solutionMatrix

def getMostConstrainedVariable(variableList):
    minVals = 999
    solutionVar = -1
    index = -1

    maxVals = 0

    i = 0
    for var in variableList:
        numVals = len(var)
        if( numVals < minVals and numVals > 1):
            minVals = numVals
            solutionVar = var
            index = i
        if( numVals > maxVals):
            maxVals = numVals
        i += 1
    if(minVals == 999):
        print("No possible vars")
    if(maxVals == 1):
        print("Only 1 options")

    return index, solutionVar

#returns 0 if invalid, 1 if completed, and 2 for standard
def allVarsHaveVals(rowVariables, colVariables):
    allOnes = True
    for var in rowVariables:
        if(len(var) == 0):
            return 0
        elif(len(var) > 1):
            allOnes = False
    for var in colVariables:
        if(len(var) == 0):
            return 0
        elif(len(var) > 1):
            allOnes = False
    if(allOnes):
        return 1
    return 2


def prune(rowVariables, colVariables, isRow, solutionMatrix):
    hasChanged = False

    if(isRow):
        i = 0
        for var in rowVariables:
            before = len(var)
            var = [x for x in var if (countInconsistencies(solutionMatrix[i], x)) == 0]
            after = len(var)

            if(before != after):
                hasChanged = True
                rowVariables[i] = var
            i += 1
    else:
        i = 0
        for col in colVariables:
            before = len(col)
            col = [x for x in col if (countInconsistencies(solutionMatrix[:,i], x)) == 0]
            after = len(col)

            if (before != after):
                hasChanged = True
                colVariables[i] = col

            i += 1
    return hasChanged, rowVariables, colVariables



def removeImpossibleValues(rowVariables, colVariables, solutionMatrix):
    i = 0
    for rowIndex in rowVariables:
        for possibilityIndex in range(len(rowIndex)):
            testval = rowIndex[possibilityIndex]
            assert len(testval) == len(solutionMatrix[i])
            for k in range(len(solutionMatrix[i])):
                if solutionMatrix[i][k] != -1 and solutionMatrix[i][k] != testval[k]:
                    rowIndex.pop(possibilityIndex)
                    break
        i += 1

    i = 0
    for colIndex in colVariables:
        for possibilityIndex in range(len(colIndex)):
            testval = colIndex[possibilityIndex]
            assert len(testval) == len(solutionMatrix[:, i])
            for k in range(len(solutionMatrix[:, i])):
                if solutionMatrix[:, i][k] != -1 and solutionMatrix[:, i][k] != testval[k]:
                    colIndex.pop(possibilityIndex)
                    break
        i += 1

    return solutionMatrix





def solve(constraints):


    dim0 = len(constraints[0])
    dim1 = len(constraints[1])

    rowVariables = findValuesHelper(constraints[0], dim1)
    colVariables = findValuesHelper(constraints[1], dim0)

    solutionMatrix = np.empty((dim0, dim1))
    solutionMatrix.fill(-1)

    # fill solution matrix with values of domain size 1
    solutionMatrix = fillSolutionMatrixWithDefiniteValues(rowVariables, colVariables, solutionMatrix)

    # toss out impossible values
    solutionMatrix = removeImpossibleValues(rowVariables, colVariables, solutionMatrix)

    #screenshot = (isRow, varIdx, RowVar, ColVar, solutionMatrix)
    screenshots = Stack()

    index, currVar = getMostConstrainedVariable(rowVariables)
    print(solutionMatrix)

    while(1): #while a var still has > 1 value
        print("new iteration")
        #right now isRows is hard coded to 'True'
        rowcopy = copy.deepcopy(rowVariables)
        colcopy = copy.deepcopy(colVariables)
        solCopy = copy.deepcopy(solutionMatrix)
        temp = (True, index, rowcopy, colcopy, solCopy)
        screenshots.push( temp )

        currVal = currVar[0]
        currVar = [currVal]
        rowVariables[index] = currVar

        if(countInconsistencies(solutionMatrix[index], currVal) > 0):
            print("Something went wrong")

        #Put value into solution Matrix
        solutionMatrix[index] = currVal
        isRow = False
        hasChanged = True

        #Prune until no values change
        while(hasChanged):
            hasChanged, rowVariables, colVariables = prune(rowVariables, colVariables, isRow, solutionMatrix.copy())
            if(allVarsHaveVals(rowVariables, colVariables) == 0):
                break
            fillSolutionMatrixWithDefiniteValues(rowVariables, colVariables, solutionMatrix)
            isRow = not isRow


        #if var has 0 vals, then backtrack
        temp = allVarsHaveVals(rowVariables, colVariables)

        #Backtrack
        if(temp == 0):
            while(True):
                #one of the values have to be true. This shouldn't happen
                if(screenshots.isEmpty()):
                    print("Oh shit, empty")
                lastSave = screenshots.pop()
                print("popped screenshots")
                isRow = lastSave[0]
                varIdx = lastSave[1]
                rowVariables = lastSave[2]
                print(rowVariables)
                colVariables = lastSave[3]
                solutionMatrix = lastSave[4]
                print(solutionMatrix)

                print(rowVariables[varIdx])

                rowVariables[varIdx].pop(0)

                print(rowVariables[varIdx])

                if(len(rowVariables[varIdx]) > 0 ):
                    print("Got info, back up a step")
                    index = varIdx
                    currVar = rowVariables[varIdx]
                    break

            continue


        #finished! All variables have 1 value
        if(temp == 1):
            print("Hell yeah! We finished")
            break

        #take a screenshot at end?

        #finally, move to the nextNode
        print("end of while loop, getting new value")
        index, currVar = getMostConstrainedVariable(rowVariables)



    return solutionMatrix


