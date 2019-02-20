from scipy.spatial import distance
import random
import math

unvisited = []
currentNeighbours = []
mazeDiff = 0
nodesExplored = 0
burningMaze = []
cellsOnFire = []
aboutBurningNeighbours = []
neighboursOfBurningToBurn = []
tempCellsOnFire = []

def setup_cells(rows, cols):
    # noting all the unvisited cells
    unvisited.clear()
    for row in range(rows):
        for col in range(cols):
            unvisited.append((row, col))

def neighboursDFSandA(current, rows, cols):  # finding all the neighbours of a node in DFS

    currentRow = current[0]
    currentCol = current[1]

    currentNeighbours.clear()


    # checking for the north neighbour
    if (currentRow - 1 >= 0 and burningMaze[currentRow - 1][currentCol] != 1):
        if ((currentRow - 1, currentCol) in unvisited and (currentRow - 1, currentCol) not in cellsOnFire):
            currentNeighbours.append((currentRow - 1, currentCol))

    # checking for the south neighbour
    if (currentRow + 1 <= rows - 1 and burningMaze[currentRow + 1][currentCol] != 1):
        if ((currentRow + 1, currentCol) in unvisited and (currentRow + 1, currentCol) not in cellsOnFire):
            currentNeighbours.append((currentRow + 1, currentCol))

    # checking for the east neighbour
    if (currentCol + 1 <= cols - 1 and burningMaze[currentRow][currentCol + 1] != 1):
        if ((currentRow, currentCol + 1) in unvisited and (currentRow, currentCol + 1) not in cellsOnFire):
            currentNeighbours.append((currentRow, currentCol + 1))

    # checking for the west neighbour
    if (currentCol - 1 >= 0 and burningMaze[currentRow][currentCol - 1] != 1):
        if ((currentRow, currentCol - 1) in unvisited and (currentRow, currentCol - 1) not in cellsOnFire):
            currentNeighbours.append((currentRow, currentCol - 1))



def neighboursOfBurning(current, rows, cols):  # finding all the neighbours of a node in DFS

    currentRow = current[0]
    currentCol = current[1]

    aboutBurningNeighbours.clear()


    # checking for the north neighbour
    if (currentRow - 1 >= 0 and burningMaze[currentRow - 1][currentCol] != 1):
        if ((currentRow - 1, currentCol) not in cellsOnFire):
            aboutBurningNeighbours.append((currentRow - 1, currentCol))

    # checking for the south neighbour
    if (currentRow + 1 <= rows - 1 and burningMaze[currentRow + 1][currentCol] != 1):
        if ((currentRow + 1, currentCol) not in cellsOnFire):
            aboutBurningNeighbours.append((currentRow + 1, currentCol))

    # checking for the east neighbour
    if (currentCol + 1 <= cols - 1 and burningMaze[currentRow][currentCol + 1] != 1):
        if ((currentRow, currentCol + 1) not in cellsOnFire):
            aboutBurningNeighbours.append((currentRow, currentCol + 1))

    # checking for the west neighbour
    if (currentCol - 1 >= 0 and burningMaze[currentRow][currentCol - 1] != 1):
        if ((currentRow, currentCol - 1) not in cellsOnFire):
            aboutBurningNeighbours.append((currentRow, currentCol - 1))


def neighboursToBurn(neighbourBurn, rows, cols):

    currentRow = neighbourBurn[0]
    currentCol = neighbourBurn[1]

    neighboursOfBurningToBurn.clear()

    # checking for the north neighbour
    if (currentRow - 1 >= 0 and burningMaze[currentRow - 1][currentCol] != 1):
        neighboursOfBurningToBurn.append((currentRow - 1, currentCol))

    # checking for the south neighbour
    if (currentRow + 1 <= rows - 1 and burningMaze[currentRow + 1][currentCol] != 1):
        neighboursOfBurningToBurn.append((currentRow + 1, currentCol))

    # checking for the east neighbour
    if (currentCol + 1 <= cols - 1 and burningMaze[currentRow][currentCol + 1] != 1):
        neighboursOfBurningToBurn.append((currentRow, currentCol + 1))

    # checking for the west neighbour
    if (currentCol - 1 >= 0 and burningMaze[currentRow][currentCol - 1] != 1):
        neighboursOfBurningToBurn.append((currentRow, currentCol - 1))


def calManhattanDis(current,end):
    return distance.cityblock(current, end)


def nextPopMan(priorityQueue, end):#an implementation of the priority queue

    shortestPoint = ()
    shortestDist = 0

    for point in priorityQueue:
        if point not in cellsOnFire:
            gOfX = calManhattanDis(point, end)
            gOfX
            if shortestDist == 0:
                shortestDist = gOfX
                shortestPoint = point
            elif shortestDist > gOfX:
                shortestDist = gOfX
                shortestPoint = point

    return shortestPoint



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


def setCellOnFire(rows, cols):

    tempCellsOnFire.clear()

    if not cellsOnFire:
        tempCellsOnFire.append((0,cols-1))
        return

    copyCellsOnFire = cellsOnFire
    for point in copyCellsOnFire:
        neighboursOfBurning(point, rows, cols)
        for neighbour in aboutBurningNeighbours:
            neighboursToBurn(neighbour, rows, cols)
            k = 0
            for tempNeighbour in neighboursOfBurningToBurn:
                if tempNeighbour in copyCellsOnFire:
                    k += 1

            power = 0.00
            power = math.pow((1/2),k)
            prob = 0.00
            prob = (1 - power)*10

            rand = random.randint(0,9)

            if rand <= prob:
                tempCellsOnFire.append(neighbour)


def mazeOnFire(newMaze):

    global burningMaze

    cellsOnFire.clear()

    burningMaze = newMaze

    rows = len(burningMaze)
    cols = len(burningMaze[0])

    backTrackPriority = []

    # pathWeights = []

    setup_cells(rows, cols)

    # start and end points of the maze
    start = (0, 0)
    end = (rows - 1, cols - 1)

    current = start

    print("The path to be take is: ")

    print(current)

    # traversing the neighbours

    while current != end:

        unvisited.remove(current)

        neighboursDFSandA(current, rows, cols)

        heuristic = calManhattanDis(current, end)  # finding the heuristic for every traversal

        try:
            if not currentNeighbours:

                if not backTrackPriority:
                    print("No path available!")
                    return
                else:
                    while not currentNeighbours:
                        current = nextPopMan(backTrackPriority, end)
                        backTrackPriority.remove(current)
                        neighboursDFSandA(current, rows, cols)
                        setCellOnFire(rows, cols)
                        for temp in tempCellsOnFire:
                            if temp not in cellsOnFire:
                                cellsOnFire.append(temp)

                        print(cellsOnFire)

                        if current in cellsOnFire:
                            print("Sorry, but you were burnt :( ")
                            return

            neighbor = leastPathChildMan(heuristic, current, end)
            backTrackPriority.append(current)
            current = neighbor
            print(current)
            setCellOnFire(rows, cols)
            for temp in tempCellsOnFire:
                if temp not in cellsOnFire:
                    cellsOnFire.append(temp)

            print(cellsOnFire)

            if current in cellsOnFire:
                print("Sorry, but you were burnt :( ")
                return

        except:
            print("No path available!")
            return
