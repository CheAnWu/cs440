import numpy as np
from queue import PriorityQueue


#passes in a row/col from the constraints list and returns all possible configurations
def findPossibleValues(result, state, pointsNeeded, dimension):

    if(len(state) > dimension):
        return result

    #constraints satisfied. Fill with 0s and return
    if(len(pointsNeeded) == 0):
        while(len(state) < dimension):
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


    #add a 0 eleemnt to next spot
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


def solve(constraints):
    print("We starting")
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

    rowValues = findValuesHelper(constraints[0], dim1)
    colValues = findValuesHelper(constraints[1], dim0)

    solutionMatrix = np.zeros(dim0, dim1)

    # Prioritized queue for order of adding to solution matrix based on possibilities
    # Each tuple has the (number of possibilities, index of either col or row, boolean is row)
    checkOrder = PriorityQueue()

    i = 0
    for rowIndex in rowValues:
        possibilities = len(rowIndex)
        if possibilities == 1:
            solutionMatrix[i] = rowIndex[0]
        else:
            checkOrder.put((possibilities,  i, True))
            i += 1

    i = 0
    for colIndex in colValues:
        possibilities = len(colIndex)
        if possibilities == 1:
            solutionMatrix[:, i] = colIndex[0]
        else:
            checkOrder.put((possibilities, i, False))
            i += 1

    checkedValues = []

    while not checkOrder.empty():
        nextVal = checkOrder.get()





    """
    solution = np.zeros((dim0, dim1))
    solution.fill(-1)

    notComplete = True
    rowsArray = np.array(dim0)

    #for counting how much possible starting values it could have
    #go through rows
    for i in range(dim0):
        curr_list = constraints[0][i]
        totalDots = 0
        for tuple in curr_list:
            totalDots += tuple[0]
        numIterations = 1 + dim0 - (len(curr_list) - 1 + totalDots)
    """

    return 1

    # np.random.randint(2, size=(dim0, dim1))
