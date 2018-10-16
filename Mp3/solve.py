import numpy as np
from queue import PriorityQueue


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
    inconsistencies = 0;
    for i in range(len(solutionArray)):
        if(solutionArray[i] != val[i]):
            inconsistencies += 1
    return inconsistencies


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



def removeImpossibleValues(colVariables, rowVariables, solutionMatrix):
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

def addAllTuplesToQueue(rowVariables, colVariables, checkOrder):
    i = 0
    for rowIndex in rowVariables:
        possibilities = len(rowIndex)
        checkOrder.put((possibilities, i, True, []))
        i += 1

    i = 0
    for colIndex in colVariables:
        possibilities = len(colIndex)
        checkOrder.put((possibilities, i, False, []))
        i += 1

    return checkOrder



def solve(constraints):
    """
    Implement me!!!!!!!
    This function takes in a set of constraints. The first dimension is the axis
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

    dim0 = len(constraints[0])
    dim1 = len(constraints[1])

    rowVariables = findValuesHelper(constraints[0], dim1)
    colVariables = findValuesHelper(constraints[1], dim0)

    solutionMatrix = np.empty((dim0, dim1))
    solutionMatrix.fill(-1)

    # Prioritized queue for order of adding to solution matrix based on possibilities
    # Each tuple has the (number of possibilities, variable index, boolean is row,
    #  (previous variable index, prev is row, list of value indexes tried))
    checkOrder = PriorityQueue()

    # fill solution matrix with values of domain size 1
    solutionMatrix = fillSolutionMatrixWithDefiniteValues(rowVariables, colVariables, solutionMatrix)

    # toss out impossible values
    solutionMatrix = removeImpossibleValues(colVariables, rowVariables, solutionMatrix)

    checkOrder = addAllTuplesToQueue(rowVariables, colVariables, checkOrder)


#No longer need this with new implementation
    for rowIndex in range(len(rowVariables)):
        solutionMatrix[rowIndex] = rowVariables[rowIndex][0]


    checkedValueStack = []

    while not checkOrder.empty():
        currTuple = checkOrder.get()
        varIndex = currTuple[1]
        isRow = currTuple[2]
        attempted = currTuple[3]
        toAttempt = [x for x in range(currTuple[0]) if x not in attempted]

        leastConstrainedValueIndex = 0;
        if(isRow):
            currVar = rowVariables[varIndex]
            leastConstrainedValueIndex = leastConstrainingValue(solutionMatrix[varIndex], currVar)
        else:
            currVar = colVariables[varIndex]
            leastConstrainedValueIndex = leastConstrainingValue(solutionMatrix[:, varIndex], currVar)

        if leastConstrainedValueIndex not in attempted:
            toAttempt.remove(leastConstrainedValueIndex)
            toAttempt.insert(0, leastConstrainedValueIndex) # try least constrained value first

        if isRow:
            solutionFound = False
            for x in toAttempt:
                array = rowVariables[varIndex][x]
                attempted.append(x)
                numInconsistencies = countInconsistencies(solutionMatrix[varIndex], array)
                if(numInconsistencies == 0):
                    solutionMatrix[varIndex] = array
                    solutionFound = True
                    newTuple = (currTuple[0], currTuple[1], currTuple[2], attempted)
                    checkedValueStack.append(newTuple)
                    break

            if not solutionFound:
                # backtrack
                #I don't think we need to add current tuple as the previous one will add it
                #However, we may need to reset its attempts
                newTuple = (currTuple[0], currTuple[1], currTuple[2], [])
                checkOrder.put(newTuple)
                prevTuple = -1
                if(len(checkedValueStack) == 0):
                    print("that's fucked")
                else:
                    prevTuple = checkedValueStack.pop()

                #TypeError: '<' not supported between ints and tuples
                checkOrder.put(prevTuple)

        else:
            solutionFound = False
            for x in toAttempt:
                array = colVariables[varIndex][x]
                attempted.append(x)
                arrayFits = True
                for i in range(len(solutionMatrix[:, varIndex])):
                    if solutionMatrix[:, varIndex][i] != array[i]:
                        arrayFits = False
                if arrayFits:
                    solutionMatrix[:, varIndex] = array
                    solutionFound = True
                    newTuple = (currTuple[0], currTuple[1], currTuple[2], attempted)
                    checkedValueStack.append(newTuple)
                    break
            if not solutionFound:
                # backtrack
                newTuple = (currTuple[0], currTuple[1], currTuple[2], [])
                checkOrder.put(newTuple)
                prevTuple = -1
                if(len(checkedValueStack) == 0 ):
                    print("that's fucked")
                else:
                    prevTuple = checkedValueStack.pop()
                checkOrder.put(prevTuple)

    return 1


