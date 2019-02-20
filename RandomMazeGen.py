import random

#Generating a random maze
def mazeGen(m) :

    maze = [[0 for i in range(m)] for j in range(m)]

    for i in range(m):
        for j in range(m):
            x=random.uniform(0,1)
            if(x < 0.8):
                maze[i][j]= 0
            else:
                maze[i][j]= 1
    maze[m-1][m-1] = 6
    maze[0][0] = 0
    return maze
