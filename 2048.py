import pygame.time
from pygame.locals import *
from constants import *
from random import *

BOARD_SIZE = 4
TOTAL_POINTS = 0
DEFAULT_SCORE = 2




pygame.init()

SURFACE = pygame.display.set_mode((400,500),0,32)
pygame.display.set_caption("game")

myfont = pygame.font.SysFont("monospace",40)
scorefont = pygame.font.SysFont("monospace",30)

tileMatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
undoMat = []

def main(fromLoaded = False):
    
    if not fromLoaded:
        placeRandomTile()
        placeRandomTile()
    printMatrix()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if checkIfCanGo() == True:
                if event.type == KEYDOWN:
                    if isArrow(event.key):
                        rotations = getRotations(event.key)
                        addToUndo()
                        for i in range(0,rotations):
                            rotateMatrixClockwise()

                        if canMove():
                            moveTiles()
                            mergeTiles()
                            placeRandomTile()

                        for j in range(0,(4-rotations)%4):
                            rotateMatrixClockwise()
                            
                        printMatrix()
            else: # just checking wait
                printGameOver()

            if event.type == KEYDOWN:
                global BOARD_SIZE

                if event.key == pygame.K_r:
                 
                    reset()
                if 50<event.key and 56 > event.key:
                    
                    BOARD_SIZE = event.key - 48
                    reset()
                if event.key == pygame.K_s:
                   
                    saveGameState()
                elif event.key == pygame.K_l:
                    loadGameState()
                    
                elif event.key == pygame.K_u:
                    undo()
                   
        pygame.display.update()



#  functions
#  This module helps in check that it is possible to move or not  

def canMove():
    for i in range(0,BOARD_SIZE):
        for j in range(1,BOARD_SIZE):
            if tileMatrix[i][j-1] == 0 and tileMatrix[i][j] > 0:
                return True 
            elif (tileMatrix[i][j-1] == tileMatrix[i][j]) and tileMatrix[i][j-1] != 0:
                return True
    return False
    # This module moves 
def moveTiles():
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE-1):
            
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:
                for k in range(j,BOARD_SIZE-1):
                    tileMatrix[i][k] = tileMatrix[i][k+1]
                tileMatrix[i][BOARD_SIZE-1] = 0


# this is used for merging

def mergeTiles():
    global TOTAL_POINTS

    for i in range(0,BOARD_SIZE):
        for k in range(0,BOARD_SIZE-1):
            if tileMatrix[i][k] == tileMatrix[i][k+1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k]*2
                tileMatrix[i][k+1] = 0 # this was not intailized so the k value was going out the range value so by this we ever we merge the files it assigns the present value to zero and merge the number with the ahead value 
                TOTAL_POINTS += tileMatrix[i][k]
                moveTiles()


#  this module helps in getting an random tile 
def placeRandomTile():
    c = 0
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE):
            if tileMatrix[i][j] == 0:
                c += 1
    
    k = floor(random() * BOARD_SIZE * BOARD_SIZE)
    print("click")

    while tileMatrix[floor(k/BOARD_SIZE)][k%BOARD_SIZE] != 0:
        k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    tileMatrix[floor(k/BOARD_SIZE)][k%BOARD_SIZE] = 2



#  this is used to get floor value out of the given value to the module
def floor(n):
    return int(n - (n % 1 ))  
# This module is used to print the given matrix
def printMatrix():
        SURFACE.fill(BLACK)
        global BOARD_SIZE
        global TOTAL_POINTS

        for i in range(0,BOARD_SIZE):
            for j in range(0,BOARD_SIZE):
                pygame.draw.rect(SURFACE,getColor(tileMatrix[i][j]),(i*(400/BOARD_SIZE),j*(400/BOARD_SIZE)+100,400/BOARD_SIZE,400/BOARD_SIZE))
                label = myfont.render(str(tileMatrix[i][j]),1,(255,255,255))
                label2 = scorefont.render("YourScore:"+str(TOTAL_POINTS),1,(255,255,255))
                SURFACE.blit(label,(i*(400/BOARD_SIZE)+30,j*(400/BOARD_SIZE)+130))
                SURFACE.blit(label2,(10,20))


# We can call this an checker module

def checkIfCanGo():
    for i in range(0,BOARD_SIZE ** 2): # This was having an error as that is 4 power of 2
        if tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE] == 0:
            return True
    
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE-1):
            if tileMatrix[i][j] == tileMatrix[i][j+1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j+1][i]:
                return True
    return False

# This module return an matrix rather than we can call it an list 
def convertToLinearMatrix():

    mat = []
    for i in range(0,BOARD_SIZE ** 2):
        mat.append(tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE])

    mat.append(TOTAL_POINTS)
    return mat

#  this module is the main reason to make the covert linearn function 
def addToUndo():
    undoMat.append(convertToLinearMatrix())   
#  This module is used to mix up the matrix after a button/ move is done by the user
def rotateMatrixClockwise():
    for i in range(0,int(BOARD_SIZE/2)):
        for k in range(i,BOARD_SIZE- i- 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

            tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
            tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
            tileMatrix[i][k] = temp4

# when you dont have any place in the matrix or you are out of move then this module is called so it is in the else part of the main func
def printGameOver():
    global TOTAL_POINTS

    SURFACE.fill(BLACK)

    label = scorefont.render("GameOver!",1,(255,255,255))
    label2 = scorefont.render("Score : "+str(TOTAL_POINTS),1,(255,255,255))
    label3 = myfont.render("press 'R' to play again!! ",1,(255,255,255))

    SURFACE.blit(label,(50,100))
    SURFACE.blit(label2,(50,200))
    SURFACE.blit(label3,(50,300))

# This module is tot reset

def reset():
    global TOTAL_POINTS
    global tileMatrix

    TOTAL_POINTS = 0
    SURFACE.fill(BLACK)
    tileMatrix = [[0 for i in range(0,BOARD_SIZE)] for j in range(0,BOARD_SIZE) ]
    main()

#  this saves the state of moves
def saveGameState():
    f = open("savedata","w")

    line1 = " ".join([str(tileMatrix[floor(x/BOARD_SIZE)][x%BOARD_SIZE]) for x in range(0,BOARD_SIZE ** 2)])
    f.write(line1+"\n")
    f.write(str(BOARD_SIZE)+"\n")
    f.write(str(TOTAL_POINTS))
    f.close

# this module is used to get the last move
def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()

        for i in range(0,BOARD_SIZE ** 2):
            tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE] = mat[i]
        global TOTAL_POINTS 
        TOTAL_POINTS  = mat[BOARD_SIZE ** 2]

        printMatrix()

def loadGameState():
    global TOTAL_POINTS
    global BOARD_SIZE
    global tileMatrix

    f = open("savedata","r")

    mat = (f.readline()).split(' ',BOARD_SIZE ** 2)
    BOARD_SIZE = int(f.readline())
    TOTAL_POINTS = int(f.readline())

    for i in range(0,BOARD_SIZE ** 2):
        tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE] = int(mat[i])

    f.close()

    main(True)


# This help you find the which arrow is clicked by the user
def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)

def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2 
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3

# calling the main
main()
