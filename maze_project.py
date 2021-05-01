import pygame
import random 
from collections import deque
import time

# SCREEN DIMENTION 🔳
SCREEN_WIDTH, SCREEN_HIGTH = 1080, 720
MAZE_WIDTH, MAZE_HIGHT = 750, 500
#Position the maze center
MAZE_X, MAZE_Y = (SCREEN_WIDTH - MAZE_WIDTH)/2, ((SCREEN_HIGTH - MAZE_HIGHT)/2) * 0.6
CELL_SIZE = 25
LINE_SIZE = 2
T = CELL_SIZE*0.1  #Tollerance to componsate line width

# DEFINED COLORS 🌈
WHITE = (255,255,255)
BLACK = (20,20,20)
RED = (255,0,0)
YELLOW = (133, 138, 12)
BLUE = (4, 5, 43)

# ASSIGNING COLORS 🎨
LINE_COLOR = WHITE
SCREEN_COLOR = BLUE
MAZE_COLOR = BLACK
PLAYER_COLOR = YELLOW

# PYGAME INTIALISING STUFFS ✨
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGTH))
pygame.init()

# FRAME SPEED🚀
clock = pygame.time.Clock()

# GRID DETAILS🔲
no_columns = MAZE_WIDTH // CELL_SIZE
no_rows = MAZE_HIGHT // CELL_SIZE
MAZE_SURFACE = pygame.Rect(MAZE_X, MAZE_Y, MAZE_WIDTH, MAZE_HIGHT)

# GAME TEXT🧾
global message
message = '[+]MAZE LOADING...'


# USE TO PERFORM BACKTRACKING 🎢
stack = []

# Movement dynamics 🤸‍♂️
moves = {'L': (-1,0), 'R': (+1,0), 'U': (0,-1), 'D': (0,+1)}

global count
count = 0

#Rendering 🎬
def render_screen():
    title = pygame.font.Font('freesansbold.ttf', 32)
    title_text = title.render(message, True, WHITE, BLUE)
    textRect = title_text.get_rect()
    textRect.center = (550, 650)
    screen.blit(title_text, textRect)
    pygame.display.flip()

#Draws square ⬛
def draw_rect(x, y, rect_color=PLAYER_COLOR):
    global count
    count += 1
    if isCreating:
        pygame.time.Clock().tick(500)
    else:
        pygame.time.Clock().tick(30)
    
    if isPlayMode and count%100 == 6:
        rect_color = BLACK
    pygame.draw.rect(screen, rect_color, (x+T, y+T, CELL_SIZE - T*2, CELL_SIZE - T*2))

# Cell class🔲
class Cell():
    def __init__(self, xy):
        x, y = xy
        self.xy = xy
        self.x = x
        self.y = y
        self.x_start_pixel = (x * CELL_SIZE) + MAZE_X 
        self.y_start_pixel = (y * CELL_SIZE) + MAZE_Y 
        
        # THIS CELL AND NEIGHBOUR CELLS INFORMATION 🙌
        self.next_cell = None
        self.chosen_neightbour = None
        self.isVisited = False
        self.isCurrent = False
        self.walls = {'U': True, 'R': True, 'D': True, 'L': True,}
        self.color = MAZE_COLOR

        # CELL CORNOR PIXEL POSTIONS 🚩
        self.left_top_pos = (self.x_start_pixel, self.y_start_pixel)
        self.right_top_pos = (self.x_start_pixel + CELL_SIZE, self.y_start_pixel)
        self.left_bot_pos = (self.x_start_pixel, self.y_start_pixel + CELL_SIZE)
        self.right_bot_pos = (self.x_start_pixel + CELL_SIZE , self.y_start_pixel + CELL_SIZE)

        #SOLUTION STUFFS
        self.isSol_visited = False
        self.sol_parent = None
        #To show the solution

    def draw_cell(self): #🎨
        if self.isVisited:
            if self.walls['U']: 
                x,y = self.left_top_pos, self.right_top_pos
                pygame.draw.line(screen, LINE_COLOR, x, y, width=LINE_SIZE)
            if self.walls['D']: 
                x,y = self.left_bot_pos, self.right_bot_pos
                pygame.draw.line(screen, LINE_COLOR, x, y, width=LINE_SIZE)
            if self.walls['L']: 
                x,y = self.left_top_pos, self.left_bot_pos
                pygame.draw.line(screen, LINE_COLOR, x, y, width=LINE_SIZE)
            if self.walls['R']: 
                x, y = self.right_top_pos, self.right_bot_pos
                pygame.draw.line(screen, LINE_COLOR, x, y, width=LINE_SIZE)

        if self.isCurrent:
            self.isVisited = True
            self.isCurrent = False
            draw_rect(self.x_start_pixel, self.y_start_pixel)
        

    #👈
    def chose_one_neightbour(self):  
        poss_moves = []
        for m in moves:
            x, y = moves[m]
            if (self.x+x, self.y+y) in grid and not grid[(self.x+x, self.y+y)].isVisited:
                poss_moves.append((grid[(self.x+x, self.y+y)], m))
        self.next_cell, self.chosen_neightbour = random.choice(poss_moves) if poss_moves else (None, None)
        return self.next_cell
    
wall_counter = {'U': 'D', 'D': 'U', 'L': 'R', 'R':'L'}
# Carves walls 🔨
def carve_wall(current_cell, next_cell):
    current_cell.walls[current_cell.chosen_neightbour] = False
    next_cell.walls[wall_counter[current_cell.chosen_neightbour]] = False


def player_movement(xy, keyPress):
    global message
    x, y = xy
    if grid[xy].walls[keyPress]:
        message = '[+] Press CRTL to auto complete'
        render_screen()
        return xy
    message =  '#MAZE_GAME'
    mX, mY = moves[keyPress]
    last = wall_counter[keyPress]
    draw_rect(grid[(x,y)].x_start_pixel, grid[(x,y)].y_start_pixel, rect_color=MAZE_COLOR)
    x, y = x+mX, y+mY
    draw_rect(grid[(x,y)].x_start_pixel, grid[(x,y)].y_start_pixel, rect_color=PLAYER_COLOR)
    render_screen()

    while True:
        poss_moves = []
        for w in grid[(x,y)].walls:
            if not grid[(x,y)].walls[w] and w != last:
                poss_moves.append(w)
        if len(poss_moves) == 1:
            mX, mY = moves[poss_moves[0]]
            draw_rect(grid[(x,y)].x_start_pixel, grid[(x,y)].y_start_pixel, rect_color=MAZE_COLOR)
            x, y = x+mX, y+mY
            draw_rect(grid[(x,y)].x_start_pixel, grid[(x,y)].y_start_pixel, rect_color=PLAYER_COLOR)
            last = wall_counter[poss_moves[0]]
            render_screen()
        
            
        else:
            if len(poss_moves) < 1:
                message = '[+] Press CRTL to auto complete'
            return((x,y))

def solution(xy):
    stack = deque()
    stack.append(grid[xy])
    while stack:
        curr =  stack.popleft()
        if curr.xy == (0,0):
            break
        for w in curr.walls:
            if not curr.walls[w]:
                mX, mY = moves[w]
                x, y = curr.xy
                pygame.draw.rect(screen, YELLOW, (curr.x_start_pixel+10, curr.y_start_pixel+10, CELL_SIZE - 20, CELL_SIZE - 20))
                render_screen()
                if not grid[(x+mX, y+mY)].isSol_visited:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quitGame()
                    grid[(x+mX, y+mY)].sol_parent = curr.xy
                    grid[(x+mX, y+mY)].isSol_visited =  True
                    stack.append(grid[(x+mX, y+mY)])
    maze_render()
    render_screen()
    sol = []
    sol.append((0,0))
    sX, sY = (0,0)
    while grid[(sX, sY)].xy != (xy):
        sol.append(grid[(sX, sY)].sol_parent)
        sX, sY = sol[-1]
    return sol
    

def maze_render():
    #FULL SCREEN COLOR ⬛
    screen.fill(SCREEN_COLOR)

    #MAZE BG COLOR 🧊
    pygame.draw.rect(screen, MAZE_COLOR, MAZE_SURFACE)

    #Draws all walls 🧱
    for x in range(no_columns):
        for y in range(no_rows):
            grid[(x,y)].draw_cell()
    x,y = (grid[(0,0)].x_start_pixel, grid[(0,0)].y_start_pixel)
    pygame.draw.line(screen, BLACK, (x,y), (x+CELL_SIZE, y+CELL_SIZE))
    pygame.draw.line(screen, BLACK, (x, y+CELL_SIZE), (x+CELL_SIZE,y))


next_cell = None
stack = []
isCreating = True
# isCreating = False
isPlayMode =  False
running = True

grid = {}
# DEFINIG EACH CELL IN THE GRID 🧱
for x in range(no_columns):
    for y in range(no_rows):
        grid[(x,y)] = Cell((x,y))
current_cell = grid[(0,0)]
sol = []


#🏃‍♂️ 
while running:   
    maze_render()

    #Maze creating 🎈
    if isCreating:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False

        current_cell.isCurrent = True
        next_cell = current_cell.chose_one_neightbour()
        if next_cell != None:
            stack.append(current_cell)
            carve_wall(current_cell, next_cell)
            current_cell = next_cell
        
        elif len(stack) > 0:
            current_cell = stack.pop()
        else:
            #Once the maze is completed, the stack gets empty, game play starts
            isCreating, isPlayMode = False, True
            playerX, playerY = (no_columns -1, no_rows -1)
            playerCell = grid[(playerX, playerY)]
            grid[(0,0)].color = WHITE
            

            message = '#MAZE_GAME'


    #Play Mode 🎮
    elif isPlayMode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (playerX == 0 and playerY == 0):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX, playerY = player_movement((playerX , playerY), 'L')
                    playerCell = grid[(playerX , playerY)]
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX, playerY = player_movement((playerX , playerY), 'R')
                    playerCell = grid[(playerX, playerY)]
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    playerX, playerY = player_movement((playerX , playerY), 'U')
                    playerCell = grid[(playerX, playerY)]
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    playerX, playerY = player_movement((playerX , playerY), 'D')
                    playerCell = grid[(playerX, playerY)]
                elif event.key in  (pygame.K_LCTRL, pygame.K_RCTRL):
                    message = '[+]SOLUTION'
                    isPlayMode = False
                    sol = solution((playerX, playerY))
                    continue
        draw_rect(playerCell.x_start_pixel, playerCell.y_start_pixel)
            
    else:
        for s in sol[::-1]:
            x, y = s
            pygame.draw.rect(screen, RED, (grid[(x,y)].x_start_pixel+10, grid[(x,y)].y_start_pixel+10, CELL_SIZE - 20, CELL_SIZE - 20))
            time.sleep(0.1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitGame()

        running = False

    render_screen()
pygame.quit()
















