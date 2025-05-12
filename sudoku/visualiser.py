def isValid(board):
    for i in range(9):
        row = []
        col = []
        for j in range(9):
            if board[i][j] in row or board[j][i] in col:
                return False
            if board[i][j]!=0:
                row.append(board[i][j])
            if board[j][i]!=0:
                col.append(board[j][i])
        x1 = (i%3)*3
        y1 = (i//3)*3
        sq = []
        for x in range(x1,x1+3):
            for y in range(y1,y1+3):
                if board[y][x] in sq:
                    return False
                if board[y][x]!=0:
                    sq.append(board[y][x])
    return True


# def solveSudoku(board):
#     emptylocs = []
#     for y in range(len(board)):
#         for x in range(len(board[0])):

                

sudoku_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]



import pygame
import random
from os import system as sys

fps = 1000000
boardSize = 9
squareSize=40

SCREEN_HEIGHT = squareSize*boardSize
SCREEN_WIDTH = squareSize*boardSize
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (170,170,170)
LIGHT_GREY = (220,220,220)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE=(245, 167, 66)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption("Sudoku Solver")
b = [[0 for i in range(0,boardSize)]for i in range(0,boardSize)]
solving = False
selected = ()
current = []
empties = []
forward = True
tried = {}

def move():
    if forward:
        if current[0]==8 and current[1]==8:
            return
        if current[0]+1>=9:
            current[0]=0
            current[1]+=1
        else:
            current[0]+=1
    else:
        if current[0]==0 and current[1]==0:
            return
        if current[0]-1<0:
            current[0]=8
            current[1]-=1
        else:
            current[0]-=1

def findEmpty(board):
    global empties
    global tried
    empties=[]
    tried = {}
    for y in range(0,len(board)):
        for x in range(0,len(board)):
            if board[y][x]==0:
                empties.append([x,y])
                tried[(x,y)]=0




def drawSquare(screen, x, y, colour, width=squareSize, height=squareSize):
    pygame.draw.rect(screen, colour, pygame.Rect((x*width), (y*height), width, height))
    for i in range(4):
        pygame.draw.rect(screen, WHITE, ((x*width)-i,(y*height)-i,width+2,height+2), 1)

def writeText(text, screen, x, y, colour):
    t = font.render(text, True, colour)
    tRect = t.get_rect()
    tRect.center = (x, y)
    screen.blit(t, tRect)
    return tRect

def drawBoard(screen):
    for y in range(0,9):
        for x in range(0,9):
            drawSquare(screen, x,y,GREY)
    if selected!=():
        drawSquare(screen,selected[0],selected[1],ORANGE)
    if current!=[]:
        drawSquare(screen,current[0],current[1],RED)


def drawLines(screen):
    for i in range(3,7,3):
        pygame.draw.rect(screen,BLACK,(squareSize*i-2,0,2,SCREEN_HEIGHT))
        pygame.draw.rect(screen,BLACK,(0,squareSize*i-2,SCREEN_WIDTH,2))

def drawNumbers(screen):
    for y in range(0,boardSize):
        for x in range(0,boardSize):
            if(b[y][x]==0):
                continue
            if not solving:
                writeText(str(b[y][x]), screen, x*squareSize+(squareSize//2),y*squareSize+(squareSize//2),BLACK)
            else:
                if [x,y] not in empties:
                    writeText(str(b[y][x]), screen, x*squareSize+(squareSize//2),y*squareSize+(squareSize//2),BLACK)
                else:
                    writeText(str(b[y][x]), screen, x*squareSize+(squareSize//2),y*squareSize+(squareSize//2),WHITE)

def drawScreen(screen):
    screen.fill(WHITE)
    drawBoard(screen)
    drawLines(screen)
    drawNumbers(screen)
    pygame.display.update()

#b=sudoku_puzzle

while True:
    clock.tick(fps)
    drawScreen(screen)


    if solving:
        if isValid(b) and current==[8,8] and b[8][8]!=0:
            current=[]
            empties=[]
            tried={}
            solving=False
            continue

        if current not in empties:
            move()
        else:
            tried[(current[0],current[1])]+=1
            if tried[(current[0],current[1])]>9:
                if empties[0] == current:
                    current=[]
                    empties=[]
                    tried={}
                    solving=False
                    continue
                b[current[1]][current[0]]=0
                tried[(current[0],current[1])]=0
                forward=False
                move()
                continue
            b[current[1]][current[0]]=tried[(current[0],current[1])]
            if isValid(b):
                if not forward:
                    forward=True
                move()




    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if solving:
                continue
            if pygame.key.name(event.key).upper()=="RETURN":
                selected=()
                current=[0,0]
                findEmpty(b)
                solving=True
            if pygame.key.name(event.key).upper() == "R":
                b=[[0 for i in range(0,boardSize)]for i in range(0,boardSize)]
            if pygame.key.name(event.key).upper() in ['0','1','2','3','4','5','6','7','8','9']:
                if selected!=():
                    b[selected[1]][selected[0]]=int(pygame.key.name(event.key))
                    selected=()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if solving:
                continue
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            sq = (mouseX//squareSize, mouseY//squareSize)

            if event.button == 1: # left click
                selected=sq

            if event.button == 3: # right click
                pass


    pygame.display.update()
