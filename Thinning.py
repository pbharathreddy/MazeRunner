import time
import random
import math
import numpy as np
from scipy.spatial import distance

unvisited = []
currentNeighbours = []
thinnigUnvisited = []
matrixPoints = []
originalMaze = []
removeIndex = []
pathTakenForThinner = []
currentNeighboursss = []


def setup_cells(rows, cols):
    # noting all the unvisited cells
    unvisited.clear()
    for row in range(rows):
        for col in range(cols):
            unvisited.append((row, col))

def setup_cellssss(rows, cols):
    # noting all the unvisited cells
    thinnigUnvisited.clear()
    for row in range(rows):
        for col in range(cols):
            thinnigUnvisited.append((row, col))

def CountOne():
    count = 0
    for i in range(len(originalMaze)):
        for j in range(len(originalMaze[0])):
            if originalMaze[i][j] == 1:
                count = count + 1

    p = random.randint(1, 10)
    f = (p / 10) * count
    return math.ceil(f)

def calManhattanDis(current,end):
    return distance.cityblock(current, end)


def leastPathChildMan(heuristic, current, end):#finds the next child which is closest to the end node using manhattan distance

    hOfX = heuristic
    shortestPoint = ()
    shortestDist = 0

    for point in currentNeighbours:
        gOfX = calManhattanDis(current,point) + calManhattanDis(point,end)
        fOfX = gOfX + hOfX
        if shortestDist == 0:
            shortestDist = fOfX
            shortestPoint = point
        elif shortestDist > fOfX:
            shortestDist = fOfX
            shortestPoint = point

    return shortestPoint

def nextPopMan(priorityQueue, end):#an implementation of the priority queue

    shortestPoint = ()
    shortestDist = 0

    for point in priorityQueue:
        gOfX = calManhattanDis(point, end)
        if shortestDist == 0:
            shortestDist = gOfX
            shortestPoint = point
        elif shortestDist > gOfX:
            shortestDist = gOfX
            shortestPoint = point

    return shortestPoint


def updateCurrMaza():

    fraction = CountOne()
    print(fraction)
    k = 0
    while k < fraction:

        tempPoints = matrixPoints
        point = random.choice(tempPoints)
        tempPoints.remove(point)
        if (originalMaze[point[0]][point[1]] == 1):
            removeIndex.append(point)
            originalMaze[point[0]][point[1]] = 0
            k += 1

def neighboursDFSandAsss(newMaze, current, rows, cols):  # finding all the neighbours of a node in DFS

    currentRow = current[0]
    currentCol = current[1]

    currentNeighbours.clear()

    # checking for the north neighbour
    if (currentRow - 1 >= 0 and newMaze[currentRow - 1][currentCol] != 1):
        if ((currentRow - 1, currentCol) in thinnigUnvisited):
            currentNeighboursss.append((currentRow - 1, currentCol))

    # checking for the south neighbour
    if (currentRow + 1 <= rows - 1 and newMaze[currentRow + 1][currentCol] != 1):
        if ((currentRow + 1, currentCol) in thinnigUnvisited):
            currentNeighboursss.append((currentRow + 1, currentCol))

    # checking for the east neighbour
    if (currentCol + 1 <= cols - 1 and newMaze[currentRow][currentCol + 1] != 1):
        if ((currentRow, currentCol + 1) in thinnigUnvisited):
            currentNeighboursss.append((currentRow, currentCol + 1))

    # checking for the west neighbour
    if (currentCol - 1 >= 0 and newMaze[currentRow][currentCol - 1] != 1):
        if ((currentRow, currentCol - 1) in thinnigUnvisited):
            currentNeighboursss.append((currentRow, currentCol - 1))

def neighboursDFSandA(newMaze, current, rows, cols):  # finding all the neighbours of a node in DFS

    currentRow = current[0]
    currentCol = current[1]

    currentNeighbours.clear()

    # checking for the north neighbour
    if (currentRow - 1 >= 0 and newMaze[currentRow - 1][currentCol] != 1):
        if ((currentRow - 1, currentCol) in unvisited):
            currentNeighbours.append((currentRow - 1, currentCol))

    # checking for the south neighbour
    if (currentRow + 1 <= rows - 1 and newMaze[currentRow + 1][currentCol] != 1):
        if ((currentRow + 1, currentCol) in unvisited):
            currentNeighbours.append((currentRow + 1, currentCol))

    # checking for the east neighbour
    if (currentCol + 1 <= cols - 1 and newMaze[currentRow][currentCol + 1] != 1):
        if ((currentRow, currentCol + 1) in unvisited):
            currentNeighbours.append((currentRow, currentCol + 1))

    # checking for the west neighbour
    if (currentCol - 1 >= 0 and newMaze[currentRow][currentCol - 1] != 1):
        if ((currentRow, currentCol - 1) in unvisited):
            currentNeighbours.append((currentRow, currentCol - 1))

def solveUsingAMansss(newMaze):

    rows = len(newMaze)
    cols = len(newMaze[0])

    backTrackPriority = []

    frinLength = 0

    setup_cells(rows, cols)

    # start and end points of the maze
    start = (0, 0)
    end = (rows - 1, cols - 1)

    current = start

    pathTakenForThinner.append(current)
    # traversing the neighbours
    # try:
    while current != end:
        unvisited.remove(current)
        # print(self.currentNeighbours)

        neighboursDFSandA(newMaze, current, rows, cols)
        heuristic = calManhattanDis(current, end)  # finding the heuristic for every traversal

        try:
            if not currentNeighbours:

                if not backTrackPriority:
                    print("No path available!")
                    return 0

                else:
                    while not currentNeighbours:
                        current = nextPopMan(backTrackPriority, end)
                        backTrackPriority.remove(current)
                        neighboursDFSandA(newMaze, current, rows, cols)

            neighbor = leastPathChildMan(heuristic, current, end)
            backTrackPriority.append(current)
            current = neighbor
            frinLength += 1
        except:
            print("No path Found!")
            return 0
    return frinLength


def solveUsingAMan(newMaze):

    startt = time.time()

    rows = len(newMaze)
    cols = len(newMaze[0])

    backTrackPriority = []

    frinLength = 0

    setup_cells(rows, cols)

    # start and end points of the maze
    start = (0, 0)
    end = (rows - 1, cols - 1)

    current = start

    print("The path to be take is: ")

    print(current)
    pathTakenForThinner.append(current)
    # traversing the neighbours
    # try:
    while current != end:
        unvisited.remove(current)
        # print(self.currentNeighbours)

        neighboursDFSandA(newMaze, current, rows, cols)
        heuristic = calManhattanDis(current, end)  # finding the heuristic for every traversal

        try:
            if not currentNeighbours:

                if not backTrackPriority:
                    return 0

                else:
                    while not currentNeighbours:
                        current = nextPopMan(backTrackPriority, end)
                        print(current)
                        backTrackPriority.remove(current)
                        neighboursDFSandA(newMaze, current, rows, cols)

            neighbor = leastPathChildMan(heuristic, current, end)
            backTrackPriority.append(current)
            current = neighbor
            print(current)
            frinLength += 1
        except:
            return 0

    return frinLength


    endTime = time.time()

    print("The time taken to solve the maze using A* with manhattan distance: ")
    print(startt - endTime)

def solveThinningA(newMaze):

    rows = len(newMaze)
    cols = len(newMaze[0])

    global matrixPoints

    for row in range(rows):
        for col in range(cols):
            matrixPoints.append((row, col))

    temp = newMaze

    global originalMaze

    originalMaze = newMaze

    updateCurrMaza()

    print(originalMaze)

    print("path for the simpler maze!")

    fringeLength = solveUsingAMan(originalMaze)

    for point in removeIndex:
        temp[point[0]][point[1]] = 1

    backTrackPriority = []

    # start and end points of the maze
    start = (0, 0)
    end = (rows - 1, cols - 1)

    current = start

    print("The path to be take is: ")

    print(current)

    setup_cellssss(rows,cols)
    # traversing the neighbours
    try:
        while current != end:

            thinnigUnvisited.remove(current)

            neighboursDFSandAsss(temp, current, rows, cols)


            if not currentNeighboursss:

                if not backTrackPriority:
                    print("No path available for this heuristic!")
                    return
                else:
                    while not currentNeighboursss:
                        current = nextPopMan(backTrackPriority, end)
                        backTrackPriority.remove(current)
                        neighboursDFSandA(newMaze, current, rows, cols)
            tempMat = []
            c=0
            neighbour = ()
            for x in currentNeighboursss:
                tempMat = np.array(temp)
                tempMat = tempMat[x[0]:rows, x[1]:cols]
                if c==0 :
                    tempLen = solveUsingAMansss(tempMat) + len(backTrackPriority)
                    neighbour = x
                    c+=1
                else:
                    if solveUsingAMansss(tempMat) + len(backTrackPriority) < tempLen:
                        neighbour = x

            backTrackPriority.append(current)
            current = neighbour
            print(current)

    except:
        print("No path Found with the following heuristic!")
        return



