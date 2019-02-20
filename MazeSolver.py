import sys
import time
from random import choice
from RandomMazeGen import mazeGen
from scipy.spatial import distance
from BurningMaze import mazeOnFire
from GenHarderMaze import generateHardMaze
from Thinning import solveThinningA

DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class Maze():

    def __init__(self, mazeDim):

        self.unvisited = []
        self.currentNeighbours = []
        self.mazeDim = mazeDim
        self.newMaze = []
        self.mazeDiff = 0
        self.nodesExplored = 0

    def creatMaze(self): #method for creating the maze

        self.newMaze = mazeGen(self.mazeDim)
        for i in range(len(self.newMaze)):
            print(self.newMaze[i]) #shows the newly created maze

    def setup_cells(self, rows, cols):

        #noting all the unvisited cells
        self.unvisited.clear()
        for row in range(rows):
            for col in range(cols):
                self.unvisited.append((row, col))

    def neighboursDFSandA(self,current,rows,cols):#finding all the neighbours of a node in DFS

        currentRow = current[0]
        currentCol = current[1]

        self.currentNeighbours.clear()

        #checking for the north neighbour
        if (currentRow - 1 >= 0 and self.newMaze[currentRow-1][currentCol] != 1):
            if((currentRow-1, currentCol) in self.unvisited):
                self.currentNeighbours.append((currentRow-1,currentCol))

        # checking for the south neighbour
        if (currentRow + 1 <= rows-1  and self.newMaze[currentRow+1][currentCol] != 1):
            if ((currentRow + 1, currentCol) in self.unvisited):
                self.currentNeighbours.append((currentRow+1, currentCol))

        # checking for the east neighbour
        if (currentCol + 1 <= cols-1  and self.newMaze[currentRow][currentCol+1] != 1):
            if ((currentRow, currentCol+1) in self.unvisited):
                self.currentNeighbours.append((currentRow, currentCol+1))

        # checking for the west neighbour
        if (currentCol - 1 >= 0  and self.newMaze[currentRow][currentCol-1] != 1):
            if ((currentRow, currentCol-1) in self.unvisited):
                self.currentNeighbours.append((currentRow, currentCol-1))

    def solveMazeDFS(self): #Solves the maze using DFS

        startTime = time.time()

        rows = len(self.newMaze)
        cols = len(self.newMaze[0])
        backTrack = []

        self.setup_cells(rows,cols)

        #start and end points of the maze
        start = (0,0)
        end = (rows-1,cols-1)

        current = start

        print("The path to be take is: ")

        print(current)

        #traversing the neighbours
        try:
            while current !=  end:

                self.unvisited.remove(current)
                self.neighboursDFSandA(current, rows, cols)

                if not self.currentNeighbours:

                    if not backTrack:
                        print("No path available!")
                    else:
                        while not self.currentNeighbours:
                            current = backTrack.pop()
                            self.neighboursDFSandA(current, rows, cols)

                neighbor = choice(self.currentNeighbours)
                backTrack.append(current)
                current = neighbor
                print(current)
        except:
            print("No path found")

        endTime = time.time()

        print("Time taken to solve the map using DFS: ")
        print(startTime - endTime)#finding the time required to solve the maze using DFS

    def neighboursBFS(self,current,rows,cols):#finding the south and east nodes for BFS

        currentRow = current[0]
        currentCol = current[1]
        south = 2
        east = 1

        self.currentNeighbours.clear()

        # checking for the south neighbour
        if (currentRow + 1 <= rows-1  and self.newMaze[currentRow+1][currentCol] != 1):
            if ((currentRow + 1, currentCol) in self.unvisited):
                self.currentNeighbours.append((currentRow+1, currentCol))#the south is the weigh for the moving in south direction

        # checking for the east neighbour
        if (currentCol + 1 <= cols-1  and self.newMaze[currentRow][currentCol+1] != 1):
            if ((currentRow, currentCol+1) in self.unvisited):
                self.currentNeighbours.append((currentRow, currentCol+1))#the east is the weight for moving in the east direction

        # checking for the west neighbour
        if (currentCol - 1 >= 0 and self.newMaze[currentRow][currentCol - 1] != 1):
            if ((currentRow, currentCol - 1) in self.unvisited):
                self.currentNeighbours.append((currentRow, currentCol - 1))

        # checking for the north neighbour
        if (currentRow - 1 >= 0 and self.newMaze[currentRow - 1][currentCol] != 1):
            if ((currentRow - 1, currentCol) in self.unvisited):
                self.currentNeighbours.append((currentRow - 1, currentCol))

    def solveMazeBFS(self):

        startTime = time.time()

        rows = len(self.newMaze)
        cols = len(self.newMaze[0])
        backTrackQue = []

        self.setup_cells(rows, cols)

        # start and end points of the maze
        start = (0,0)
        end = (rows - 1, cols - 1)

        current = start

        print("The path to be take is: ")

        print(current)

        # traversing the neighbours
        while current != end:

            self.unvisited.remove(current)
            self.neighboursBFS(current, rows, cols)

            if ((current[0],current[1]+1) in self.currentNeighbours and (current[0],current[1]+1) not in backTrackQue ):
                backTrackQue.append((current[0],current[1]+1))
                #print(backTrackQue)
            if ((current[0]+1,current[1]) in self.currentNeighbours and (current[0]+1,current[1]) not in backTrackQue):
                backTrackQue.append((current[0]+1,current[1]))
                #print(backTrackQue)
            if(((current[0],current[1]+1) not in self.currentNeighbours) and (current[0]+1,current[1]) not in self.currentNeighbours):
                if ((current[0], current[1] - 1) in self.currentNeighbours):
                    backTrackQue.append((current[0], current[1] - 1))
                elif ((current[0] - 1, current[1]) in self.currentNeighbours):
                    backTrackQue.append((current[0] - 1, current[1]))

            try:
                current = backTrackQue.pop(0)
                print(current)
            except:
                print("No path found!")

        endTime = time.time()

        print("The time taken to compute BFS: ")
        print(startTime - endTime)

    def calEuclidDis(self, current, end):#function to calculate the euclidian distance
        return distance.euclidean(current, end)


    def calManhattanDis(self,current,end):
        return distance.cityblock(current, end)


    def leastPathChildEuc(self, heuristic, current, end):##finds the next child which is closest to the end node using euclidian distance

        hOfX = heuristic
        shortestPoint = ()
        shortestDist = 0

        for point in self.currentNeighbours:
            gOfX = self.calEuclidDis(current,point) + self.calEuclidDis(point,end)
            fOfX = gOfX + hOfX
            if shortestDist == 0:
                shortestDist = fOfX
                shortestPoint = point
            elif shortestDist > fOfX:
                shortestDist = fOfX
                shortestPoint = point

        return shortestPoint


    def leastPathChildMan(self, heuristic, current, end):#finds the next child which is closest to the end node using manhattan distance

        hOfX = heuristic
        shortestPoint = ()
        shortestDist = 0

        for point in self.currentNeighbours:
            gOfX = self.calManhattanDis(current,point) + self.calManhattanDis(point,end)
            fOfX = gOfX + hOfX
            if shortestDist == 0:
                shortestDist = fOfX
                shortestPoint = point
            elif shortestDist > fOfX:
                shortestDist = fOfX
                shortestPoint = point

        return shortestPoint


    def nextPopMan(self, priorityQueue, end):#an implementation of the priority queue

        shortestPoint = ()
        shortestDist = 0

        for point in priorityQueue:
            gOfX = self.calManhattanDis(point, end)
            gOfX
            if shortestDist == 0:
                shortestDist = gOfX
                shortestPoint = point
            elif shortestDist > gOfX:
                shortestDist = gOfX
                shortestPoint = point

        return shortestPoint



    def nextPopEuc(self, priorityQueue, end):#an implementation of the priority queue

        shortestPoint = ()
        shortestDist = 0

        for point in priorityQueue:
            gOfX = self.calEuclidDis(point, end)
            gOfX
            if shortestDist == 0:
                shortestDist = gOfX
                shortestPoint = point
            elif shortestDist > gOfX:
                shortestDist = gOfX
                shortestPoint = point

        return shortestPoint


    def solveMazeAEuc(self):

        startTime = time.time()

        rows = len(self.newMaze)
        cols = len(self.newMaze[0])
        backTrackPriority = []

        pathWeights = []

        self.setup_cells(rows, cols)

        # start and end points of the maze
        start = (0, 0)
        end = (rows - 1, cols - 1)

        current = start

        print("The path to be take is: ")

        print(current)

        # traversing the neighbours
        try:
            while current != end:

                self.unvisited.remove(current)

                self.neighboursDFSandA(current, rows, cols)

                heuristic = self.calEuclidDis(current, end)#finding the heuristic for every traversal

                if not self.currentNeighbours:

                    if not backTrackPriority:
                        print("No path available!")
                    else:
                        while not self.currentNeighbours:
                            current = self.nextPopEuc(backTrackPriority, end)
                            backTrackPriority.remove(current)
                            self.neighboursDFSandA(current, rows, cols)

                neighbor = self.leastPathChildEuc(heuristic, current, end)
                backTrackPriority.append(current)
                current = neighbor
                print(current)
        except:
            print("No path Found!")

        endTime = time.time()

        print("The time taken to solve the maze using A* with euclidian distance: ")
        print(startTime-endTime)


    def solveMazeAMan(self):

        startTime = time.time()

        rows = len(self.newMaze)
        cols = len(self.newMaze[0])

        backTrackPriority = []

        self.setup_cells(rows, cols)

        # start and end points of the maze
        start = (0, 0)
        end = (rows - 1, cols - 1)

        current = start

        print("The path to be take is: ")

        print(current)

        frinLength = 0

        # traversing the neighbours
        while current != end:

            self.unvisited.remove(current)

            self.neighboursDFSandA(current, rows, cols)

            heuristic = self.calManhattanDis(current, end)  # finding the heuristic for every traversal

            try:
                if not self.currentNeighbours:

                    if not backTrackPriority:
                        print("No path available!")
                        return 0
                    else:
                        while not self.currentNeighbours:
                            current = self.nextPopMan(backTrackPriority, end)
                            backTrackPriority.remove(current)
                            self.neighboursDFSandA(current, rows, cols)

                neighbor = self.leastPathChildMan(heuristic, current, end)
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


    def callMazeOnFire(self):
        mazeOnFire(self.newMaze)


    def genHardMaze(self):
        tempMaze = self.newMaze
        generateHardMaze(tempMaze)


    def thinningA(self):
        solveThinningA(self.newMaze)



if __name__=="__main__":

    mazeDim = int(input("Enter the dimensions of the maze: "))

    #calling the maze call to generate the new maze
    maze = Maze(mazeDim)

    exitApp = False

    input("Hit enter to start solving the matrix:-----------")
    #calling the solve function
    while not exitApp:

        print("New Maze")
        maze.creatMaze()

        switch = int(input("Enter 1 for A*(manhatten distance), 2 for A*(euclidian distance), 3 for BFS, 4 for DFS, 5 for setting the maze on fire, 6 for generating harder mazes, 7 to implement thinning A* and 8 to EXIT: "))

        if switch==1:
            maze.solveMazeAMan()
        elif switch==2:
            maze.solveMazeAEuc()
        elif switch==3:
            maze.solveMazeBFS()
        elif switch==4:
            maze.solveMazeDFS()
        elif switch==5:
            maze.callMazeOnFire()
        elif switch == 6:
            maze.genHardMaze()
        elif switch==7:
            print("solving maze using A*: ")
            maze.solveMazeAMan()
            print("Thinning the matrix: ")
            maze.thinningA()
        elif switch==8:
            exitApp = True
        else:
            print("Please enter a valid input!!")




