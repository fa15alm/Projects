import pygame, random


width = 20
height = 15
squareSize = 20

SCREEN_HEIGHT = height*squareSize
SCREEN_WIDTH = width*squareSize

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (170,170,170)
LIGHT_GREY = (220,220,220)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

cells = [[0 for i in range(width)]for i in range(height)]

def drawSquare(screen, x, y, colour, width=squareSize, height=squareSize):
    pygame.draw.rect(screen, colour, pygame.Rect((x*width)+1, (y*height)+1, width-2, height-2))

def drawScreen(screen):
    screen.fill(GREY)
    for y in range(height):
        for x in range(width):
            if(cells[y][x]):
                drawSquare(screen, x, y, WHITE)
            else:
                drawSquare(screen, x, y, BLACK)
    pygame.display.update()


playing = False

def getNeighbourAmounts():
    neighbours = [[0 for i in range(width)]for i in range(height)]
    for y in range(height):
        for x in range(width):
            for x1 in range(x-1,x+2):
                for y1 in range(y-1,y+2):
                    if x1>=0 and x1 < width and y1>=0 and y1<height and not(y1==y and x1==x):
                        neighbours[y][x]+=cells[y1][x1]
    return neighbours



def gameOfLife():
    global cells
    n = getNeighbourAmounts()
    for y in range(height):
        for x in range(width):
            current = cells[y][x]
            cn = n[y][x]
            if current:
                if cn==2 or cn==3:
                    continue
                cells[y][x] = 0
                continue
            if cn==3:
                cells[y][x] = 1


fps = 8

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)
pygame.display.set_caption("Game of Life")


while True:
    clock.tick(fps)
    drawScreen(screen)

    if playing:
        gameOfLife()



    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not playing:
                cells=[[0 for i in range(width)]for i in range(height)]
        
            if event.key == pygame.K_SPACE:
                playing = not playing
                if playing:
                    pygame.display.set_caption("Game of Life - Playing")
                else:
                    pygame.display.set_caption("Game of Life")

            if event.key == pygame.K_RETURN and not playing:
                gameOfLife()

            if event.key == pygame.K_f and not playing:
                for y in range(height):
                    for x in range(width):
                        cells[y][x] = random.randint(0, 1)

        if event.type == pygame.MOUSEBUTTONDOWN and not playing:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            sq = (mouseX//squareSize, mouseY//squareSize)

            if event.button == 1: # left click
                cells[sq[1]][sq[0]] ^= 1

            if event.button == 3: # right click
                pass
