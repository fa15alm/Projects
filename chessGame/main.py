#### ADDED FEATURE TO DRAG PIECES ####


# ---------------------------------- IMPORTS ---------------------------------- #
import pygame, os, copy

# --------------------------------- CONSTANTS --------------------------------- #
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SQUARE_SIDE = SCREEN_WIDTH/8
FPS = 100

LIGHT_SQUARE_COLOUR = (189, 151, 230)
DARK_SQUARE_COLOUR = (149, 69, 237)
CHOSEN_SQUARE_COLOUR = (189, 191, 33)
POSSIBLE_MOVE_SQUARE_COLOUR = (35, 219, 57)
KING_IN_CHECK_SQUARE_COLOUR = (219, 15, 15)
POSSIBLE_MOVE_CIRCLE_RADIUS=15

# --------------------------------- VARIABLES --------------------------------- #
possibleMoveHighlight = True
possibleMoveMode = 1


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption('Chess')

s1 = ()
buttonDown = ()
trackMouse = False

whiteTurn = True
blackTurn = False

moved = []

board = []
pawnMovedLast = ()
running = True

# ------------------------------- GUI FUNCTIONS ------------------------------- #
def loadImages(path):
    imageDict = {}
    for filename in os.listdir(path):
        if filename.endswith('.png'):
            p = os.path.join(path, filename)
            key = filename[:-4]
            imageDict[key] = pygame.transform.scale(pygame.image.load(p), (SQUARE_SIDE, SQUARE_SIDE))
    return imageDict

pieces = loadImages('assets')

def drawSquare(screen, x, y, colour, width=SQUARE_SIDE, height=SQUARE_SIDE):
    pygame.draw.rect(screen, colour, pygame.Rect((x*width), (y*height), width, height))

def drawBackground(screen):
    moves = []
    if s1 != ():
        moves = cleanPossibleMoves(s1)
    for y in range(8):
        for x in range(8):
            if (x, y) == s1:
                drawSquare(screen, x, y, CHOSEN_SQUARE_COLOUR)
                continue
            if x%2==0 and y%2==0 or x%2!=0 and y%2!=0:
                drawSquare(screen, x, y, LIGHT_SQUARE_COLOUR)
            else:
                drawSquare(screen, x, y, DARK_SQUARE_COLOUR)
            if possibleMoveHighlight and ((x, y) in moves):
                if possibleMoveMode == 0:
                    drawSquare(screen, x, y, POSSIBLE_MOVE_SQUARE_COLOUR)
                else:
                    pygame.draw.circle(screen, POSSIBLE_MOVE_SQUARE_COLOUR, ((x*SQUARE_SIDE)+(SQUARE_SIDE//2), (y*SQUARE_SIDE)+(SQUARE_SIDE//2)), POSSIBLE_MOVE_CIRCLE_RADIUS, POSSIBLE_MOVE_CIRCLE_RADIUS)
            if board[y][x].endswith('K'):
                if isChecked(board[y][x][0]):
                    drawSquare(screen, x, y, KING_IN_CHECK_SQUARE_COLOUR)

def drawPieces(screen):
    mouseX, mouseY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != '':
                if trackMouse and (x, y) == buttonDown:
                    if board[buttonDown[1]][buttonDown[0]].startswith('w' if whiteTurn else 'b'):
                        screen.blit(pieces[board[y][x]], (mouseX-(SQUARE_SIDE//2), mouseY-(SQUARE_SIDE//2)))
                        continue
                screen.blit(pieces[board[y][x]], (x*SQUARE_SIDE, y*SQUARE_SIDE))
                moves = []
                if s1 != ():
                    moves = cleanPossibleMoves(s1)
                if (x, y) in moves:
                    if possibleMoveMode == 0:
                        drawSquare(screen, x, y, POSSIBLE_MOVE_SQUARE_COLOUR)
                    else:
                        pygame.draw.circle(screen, POSSIBLE_MOVE_SQUARE_COLOUR, ((x*SQUARE_SIDE)+(SQUARE_SIDE//2), (y*SQUARE_SIDE)+(SQUARE_SIDE//2)), POSSIBLE_MOVE_CIRCLE_RADIUS, POSSIBLE_MOVE_CIRCLE_RADIUS)


def writeText(text, screen, x, y, colour=(0, 0, 0)):
    t = font.render(text, True, colour)
    tRect = t.get_rect()
    tRect.center = (x, y)
    screen.blit(t, tRect)
    return tRect

# ------------------------------- GAME FUNCTIONS ------------------------------- #
 
def changeTurn():
    global whiteTurn
    global blackTurn
    whiteTurn = not whiteTurn
    blackTurn = not blackTurn

def newBoard():
    return [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP'for i in range(8)],
            [''for i in range(8)],
            [''for i in range(8)],
            [''for i in range(8)],
            [''for i in range(8)],
            ['wP' for i in range(8)],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

board = newBoard()
                
def calculateMoves(coords, board=board):
    x = coords[0]
    y = coords[1]
    moves = []
    p = board[y][x][-1].lower()
    colour = board[y][x][0]

    if p == 'n':    #------------------------------- KNIGHT
        moves.append((x+1, y+2))
        moves.append((x+1, y-2))
        moves.append((x-1, y+2))
        moves.append((x-1, y-2))
        moves.append((x+2, y+1))
        moves.append((x+2, y-1))
        moves.append((x-2, y+1))
        moves.append((x-2, y-1))
    if p == 'r' or p == 'q':    #----------------------------------------- ROOK AND QUEEN
        for i in range(1, 8):
            if not(-1<x+i<8):
                break
            if board[y][x+i] == '':
                moves.append((x+i, y))
            elif board[y][x+i].startswith(colour):
                break
            else:
                moves.append((x+i, y))
                break
        for i in range(1, 8):
            if not(-1<x-i<8):
                break
            if board[y][x-i] == '':
                moves.append((x-i, y))
            elif board[y][x-i].startswith(colour):
                break
            else:
                moves.append((x-i, y))
                break
        for i in range(1, 8):
            if not(-1<y+i<8):
                break
            if board[y+i][x] == '':
                moves.append((x, y+i))
            elif board[y+i][x].startswith(colour):
                break
            else:
                moves.append((x, y+i))
                break
        for i in range(1, 8):
            if not(-1<y-i<8):
                break
            if board[y-i][x] == '':
                moves.append((x, y-i))
            elif board[y-i][x].startswith(colour):
                break
            else:
                moves.append((x, y-i))
                break
    if p == 'b' or p == 'q': #--------------------------------- BISHOP AND QUEEN
        for i in range(1, 8):
            if not(-1<y+i<8) or not(-1<x+i<8):
                break
            if board[y+i][x+i] == '':
                moves.append((x+i, y+i))
            elif board[y+i][x+i].startswith(colour):
                break
            else:
                moves.append((x+i, y+i))
                break
        for i in range(1, 8):
            if not(-1<y-i<8) or not(-1<x-i<8):
                break
            if board[y-i][x-i] == '':
                moves.append((x-i, y-i))
            elif board[y-i][x-i].startswith(colour):
                break
            else:
                moves.append((x-i, y-i))
                break
        for i in range(1, 8):
            if not(-1<y+i<8) or not(-1<x-i<8):
                break
            if board[y+i][x-i] == '':
                moves.append((x-i, y+i))
            elif board[y+i][x-i].startswith(colour):
                break
            else:
                moves.append((x-i, y+i))
                break
        for i in range(1, 8):
            if not(-1<y-i<8) or not(-1<x+i<8):
                break
            if board[y-i][x+i] == '':
                moves.append((x+i, y-i))
            elif board[y-i][x+i].startswith(colour):
                break
            else:
                moves.append((x+i, y-i))
                break
    if p == 'k': # --------------------------------------------------KING
        moves.append((x+1, y+1))
        moves.append((x+1, y))
        moves.append((x+1, y-1))
        moves.append((x, y+1))
        moves.append((x, y-1))
        moves.append((x-1, y+1))
        moves.append((x-1, y))
        moves.append((x-1, y-1))
        # Short Castling
        shortCastle = 0
        if (colour+'K' not in moved) and (colour+'R' not in moved):
            if board[7 if colour=='w' else 0][6] == '' and board[7 if colour=='w' else 0][5] == '':
                for i in range(0, 3):
                    bCopy = copy.deepcopy(board)
                    bCopy[y][x] = ''
                    bCopy[y][x+i] = colour+'K'
                    if not(isChecked(colour, bCopy)):
                        shortCastle+=1
                if shortCastle==3:
                    moves.append((x+2, y))
        # Long Castling
        longCastle = 0
        if (colour+'K' not in moved) and (colour+'R' not in moved):
            if board[7 if colour=='w' else 0][1] == '' and board[7 if colour=='w' else 0][2] == '' and board[7 if colour=='w' else 0][3] == '':
                for i in range(0, 3):
                    bCopy = copy.deepcopy(board)
                    bCopy[y][x] = ''
                    bCopy[y][x-i] = colour+'K'
                    if not(isChecked(colour, bCopy)):
                        longCastle+=1
                if longCastle==3:
                    moves.append((x-2, y))

    if p == 'p': #---------------------------------------------------- PAWN
        
        if colour=='w':
            if y==6: # SECOND ROW / NOT MOVED YET
                if board[y-2][x] == '':
                    moves.append((x, y-2))
            if board[y-1][x] == '':
                moves.append((x, y-1))
            if 0<y<9:
                if 0<x<9:
                    if board[y-1][x-1].startswith('b'):
                        moves.append((x-1, y-1))
                if -2<x<7:
                    if board[y-1][x+1].startswith('b'):
                        moves.append((x+1, y-1))
        else:
            if y==1: # SECOND ROW / NOT MOVED YET
                if board[y+2][x] == '':
                    moves.append((x, y+2))
            if board[y+1][x] == '':
                moves.append((x, y+1))
            if 0<y<9:
                if 0<x<9:
                    if board[y+1][x-1].startswith('w'):
                        moves.append((x-1, y+1))
                if -2<x<7:
                    if board[y+1][x+1].startswith('w'):
                        moves.append((x+1, y+1))
        # EN PASSANT
        if colour == 'w' and y == 3:
            if (x+1, y) == pawnMovedLast and board[y-1][x+1] == '':
                moves.append((x+1, y-1))
            if (x-1, y) == pawnMovedLast and board[y-1][x-1] == '':
                moves.append((x-1, y-1))
        if colour == 'b' and y == 4:
            if (x+1, y) == pawnMovedLast and board[y+1][x+1] == '':
                moves.append((x+1, y+1))
            if (x-1, y) == pawnMovedLast and board[y+1][x-1] == '':
                moves.append((x-1, y+1))
                

    movesFinal = []
    for move in moves:
        if (0<=move[0]<8 and 0<=move[1]<8) and not(board[move[1]][move[0]].startswith(colour)):
            movesFinal.append(move)

    return movesFinal

def cleanPossibleMoves(pos):
    try:
        moves = calculateMoves(pos)
        x = pos[0]
        y = pos[1]
        colour = board[y][x][0]
        newMoves = []
        for move in moves:
            bCopy = copy.deepcopy(board)
            bCopy[move[1]][move[0]] = bCopy[y][x]
            bCopy[y][x] = ''
            if isChecked(colour, bCopy):
                continue
            newMoves.append(move)
        return newMoves
    except:
        return []

def isChecked(colour, board=board):
    squaresAttacked = []
    for y in range(len(board)):
        for x in range(len(board)):
            if ((colour == 'w') and (board[y][x].startswith('b'))) or ((colour == 'b') and (board[y][x].startswith('w'))):
                x = calculateMoves((x, y), board)
                for move in x:
                    if move not in squaresAttacked:
                        squaresAttacked.append(move)
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == colour + 'K':
                if (x, y) in squaresAttacked:
                    return True
                else:
                    return False
    raise Exception('Couldnt find enemy king.')


def isCheckmate(colour, board=board):
    possibleMoves = []
    for y in range(len(board)):
        for x in range(len(board)):
            if (board[y][x].startswith(colour)):
                x = cleanPossibleMoves((x, y))
                for move in x:
                    if move not in possibleMoves:
                        possibleMoves.append(move)
    if len(possibleMoves) == 0:
        return True
    return False

# --------------------------------- GAME LOOP --------------------------------- #

while True:
    pygame.display.set_caption('Chess     ' + (('Black\'s Turn') if blackTurn else ('White\'s Turn')))
    if isCheckmate('b') or isCheckmate('w'):
        clock.tick(FPS)
        drawBackground(screen)
        drawPieces(screen)
        dim = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        dim.set_alpha(128)                
        dim.fill((180,180,180))           
        screen.blit(dim, (0,0))
        if isCheckmate('b'):
            writeText('Checkmate! White wins!', screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100)
        else:
            writeText('Checkmate! Black wins!', screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100)
        aRect = writeText('Play Again!', screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2+100, POSSIBLE_MOVE_SQUARE_COLOUR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if aRect.collidepoint(event.pos):
                        board = newBoard()
        if running:
            pygame.display.update()
            continue
        else:
            break
    clock.tick(FPS)
    drawBackground(screen)
    drawPieces(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                trackMouse = False
                x = int(event.pos[0]//SQUARE_SIDE)
                y = int(event.pos[1]//SQUARE_SIDE)
                if (x, y) in cleanPossibleMoves(s1):
                    colour = board[s1[1]][s1[0]][0]
                    if board[s1[1]][s1[0]] not in moved:
                        moved.append(board[s1[1]][s1[0]])
                    if board[s1[1]][s1[0]].endswith('K'):
                        if x == s1[0]+2:                   # SHORT CASTLE
                            board[s1[1]][s1[0]+2] = board[s1[1]][s1[0]]
                            board[s1[1]][s1[0]] = ''
                            board[s1[1]][s1[0]+1] = board[y][7]
                            board[y][7] = ''
                            changeTurn()
                            continue
                        if x == s1[0]-2:                   # LONG CASTLE
                            board[s1[1]][s1[0]-2] = board[s1[1]][s1[0]]
                            board[s1[1]][s1[0]] = ''
                            board[s1[1]][s1[0]-1] = board[y][0]
                            board[y][0] = ''
                            changeTurn()
                            continue
                    if board[s1[1]][s1[0]].endswith('P'): # EN PASSANT
                        if x == s1[0] and (s1[1] == y-2 or s1[1] == y+2):
                            pawnMovedLast = (x, y)
                        elif colour == 'w' and y == 2 and s1[1] == 3 and (x == s1[0]-1 or x == s1[0]+1) and board[y][x]=='':
                            board[y][x] = board[s1[1]][s1[0]]
                            board[s1[1]][s1[0]] = ''
                            board[y+1][x] = ''
                            changeTurn()
                            pawnMovedLast = ()
                            continue
                        elif colour == 'b' and y == 5 and s1[1] == 4 and (x == s1[0]-1 or x == s1[0]+1) and board[y][x]=='':
                            board[y][x] = board[s1[1]][s1[0]]
                            board[s1[1]][s1[0]] = ''
                            board[y-1][x] = ''
                            changeTurn()
                            pawnMovedLast = ()
                            continue
                    else:
                        pawnMovedLast = ()
                    lastBoard = copy.deepcopy(board)
                    board[y][x] = board[s1[1]][s1[0]]
                    board[s1[1]][s1[0]] = ''
                    s1 = ()
                    changeTurn()
                if (x, y) not in cleanPossibleMoves(s1) and s1 != (x, y):
                    s1 = ()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = int(event.pos[0]//SQUARE_SIDE)
                y = int(event.pos[1]//SQUARE_SIDE)
                buttonDown = (x, y)
                trackMouse = True
                if s1 == ():
                    if board[y][x].startswith('w' if whiteTurn else 'b'):
                        s1 = buttonDown
                else:
                    if board[y][x].startswith(board[s1[1]][s1[0]]):
                        s1 = buttonDown
    if running:
        pygame.display.update()
    else:
        break
