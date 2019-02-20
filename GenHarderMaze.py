from random import choice
import time
from RandomMazeGen import mazeGen
from scipy.spatial import distance

unvisited = []
currentNeighbours = []

def creatMaze(mazeDim):  # method for creating the maze
    newMaze = mazeGen(mazeDim)
    return newMaze


def setup_cells(rows, cols):
    # noting all the unvisited cells
    unvisited.clear()
    for row in range(rows):
        for col in range(cols):
            unvisited.append((row, col))
    pointsInMatrix = []

    for point in unvisited:
        if point != (0, 0) and point != (rows - 1, cols - 1):
            pointsInMatrix.append(point)

    return pointsInMatrix


def neighboursDFSandA(newMaze, current,rows,cols):#finding all the neighbours of a node in DFS

        currentRow = current[0]
        currentCol = current[1]

        currentNeighbours.clear()

        #checking for the north neighbour
        if (currentRow - 1 >= 0 and newMaze[currentRow-1][currentCol] != 1):
            if((currentRow-1, currentCol) in unvisited):
                currentNeighbours.append((currentRow-1,currentCol))

        # checking for the south neighbour
        if (currentRow + 1 <= rows-1  and newMaze[currentRow+1][currentCol] != 1):
            if ((currentRow + 1, currentCol) in unvisited):
                currentNeighbours.append((currentRow+1, currentCol))

        # checking for the east neighbour
        if (currentCol + 1 <= cols-1  and newMaze[currentRow][currentCol+1] != 1):
            if ((currentRow, currentCol+1) in unvisited):
                currentNeighbours.append((currentRow, currentCol+1))

        # checking for the west neighbour
        if (currentCol - 1 >= 0  and newMaze[currentRow][currentCol-1] != 1):
            if ((currentRow, currentCol-1) in unvisited):
                currentNeighbours.append((currentRow, currentCol-1))

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


def solveMazeAManH(newMaze,rows,cols):

    startTime = time.time()

    backTrackPriority = []

    setup_cells(rows, cols)

    # start and end points of the maze
    start = (0, 0)
    end = (rows - 1, cols - 1)

    current = start

    print("The path to be take is: ")

    print(current)

    frinLength = 0

    # traversing the neighbours
    while current != end:

        unvisited.remove(current)

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
            print(current)
            frinLength += 1

        except:
            print("No path Found!")
            return 0

    return frinLength

    endTime = time.time()

    print("The time taken to solve the maze using A* with manhattan distance: ")
    print(startTime - endTime)


def generateHardMaze(newMazes):

    rows = len(newMazes)
    cols = len(newMazes[0])

    print("Solving the original maze!")
    fringLength = solveMazeAManH(newMazes, rows, cols)
    print("Creating new harder Maze:")

    pFlag = True
    pCout = 0

    while pFlag:

        count = 0
        flag = True

        while flag:

            point = choice(setup_cells(rows, cols))

            if (newMazes[point[0]][point[1]] == 1):
                newMazes[point[0]][point[1]] = 0
            else:
                newMazes[point[0]][point[1]] = 1

            if (fringLength < solveMazeAManH(newMazes, rows, cols)):
                print("Harder Maze--------------------")
                for i in range(len(newMazes)):
                    print(newMazes[i])
                print('Fringe Length for Harder maze')
                print(fringLength)
                #print(newMazes)
                fringLength = solveMazeAManH(newMazes, rows, cols)
                count = 0


            else:
                count += 1
                if count >= 10:
                    flag = False
        print(fringLength)
        print("one")
        newMazes = creatMaze(rows)
        pCout += 1
        if pCout >= 100:
            pFlag = False

