import pygame
from pygame.locals import *
from math import floor
from time import sleep
from random import randint

pygame.init()
display_info = pygame.display.Info()

amount_in_row = randint(2,20)
grid_dimension = randint(amount_in_row,randint(amount_in_row,amount_in_row*2))
height = grid_dimension
width = grid_dimension
if (display_info.current_w > display_info.current_h):
    smallest_side = display_info.current_h
else:
    smallest_side = display_info.current_w
grid_size = round(smallest_side/grid_dimension)
border_thickness = round(grid_size/8)

grid = [[None for x in range(width)] for y in range(height)]

empty = (255,255,255)
player_1 = (255,0,0)
player_2 = (0,0,255)
running = True
move = True
player = 1

screen = pygame.display.set_mode((smallest_side,smallest_side))

def rules(amount_in_row,grid_dimension):
    print("Win Condition:",amount_in_row,"in a row")
    print("Play Area:",grid_dimension,"x",grid_dimension)

def reset_game():
    amount_in_row = randint(2,20)
    grid_dimension = randint(amount_in_row,randint(amount_in_row,amount_in_row*2))
    height = grid_dimension
    width = grid_dimension
    if (display_info.current_w > display_info.current_h):
        smallest_side = display_info.current_h
    else:
        smallest_side = display_info.current_w
    grid_size = round(smallest_side/grid_dimension)
    border_thickness = round(grid_size/8)
    grid = [[None for x in range(width)] for y in range(height)]
    rules(amount_in_row,grid_dimension)
    return grid,amount_in_row,grid_dimension,height,width,smallest_side,grid_size,border_thickness

def make_move(grid_x,grid_y,player):
    #check if valid
    value = grid[grid_y][grid_x]
    if value == None:
        #do a move
        grid[grid_y][grid_x] = player
        return True
    else:
        return False
def draw_grid():
    for i in range(1,width):
        pygame.draw.rect(screen, (0,0,0), ((i*grid_size)-floor(border_thickness/2), 0, border_thickness, height*grid_size))
    for i in range(1,height):
        pygame.draw.rect(screen, (0,0,0), (0, (i*grid_size)-floor(border_thickness/2), width*grid_size, border_thickness))

def check_win(values):
    for i in range(len(values)-1): #match found horizontally
        a = 0
        for j in range(1,amount_in_row):
            try:
                if (values[i] == values[i+j]) and (values[i] != None) and (values[i+j] != None):
                    a += 1
                    if (a == amount_in_row-1):
                        return True
            except:
                pass
    return False

def game_check():
    #check for the correct amount in a row
    c = 0
    for y in range(height):
        values = []
        for x in range(width):
            values.append(grid[y][x])
            if grid[y][x] == None:
                c += 1
        current_state = check_win(values)
        if current_state:
            return True #match found horizontally
    for x in range(width):
        values = []
        for y in range(height):
            values.append(grid[y][x])
        current_state = check_win(values)
        if current_state:
            return True #match found vertically
    for x_start in range(width):
        values = []
        for x,y in zip(range(x_start,width),range(height-x_start)):
            values.append(grid[y][x])
        current_state = check_win(values)
        if current_state:
            return True #match found diagonally
    for y_start in range(height):
        values = []
        for x,y in zip(range(width-y_start),range(y_start,height)):
            values.append(grid[y][x])
        current_state = check_win(values)
        if current_state:
            return True #match found diagonally
    for x_start_backwards in range(width,-1,-1):
        values = []
        for x,y in zip(range(x_start_backwards-1,-1,-1),range(height-(width-x_start_backwards))):
            values.append(grid[y][x])
        current_state = check_win(values)
        if current_state:
            return True #match found diagonally
    for y_start_backwards in range(height,-1,-1):
        values = []
        for x,y in zip(range(width-1,(width-y_start_backwards)-1,-1),range(height-y_start_backwards,height)):
            values.append(grid[y][x])
        current_state = check_win(values)
        if current_state:
            return True #match found diagonally
    if c == 0:
        return True #Draw, no spaces left and no win
    return False #game continues, no win

def draw_screen():
    screen.fill(empty)
    for y in range(0,height):
        for x in range(0,width):
            location = [y,x]
            grid_state = grid[location[0]][location[1]]
            if grid_state == 1:
                pygame.draw.rect(screen, player_1, (location[1]*grid_size, location[0]*grid_size, grid_size, grid_size))
            elif grid_state == 2:
                pygame.draw.rect(screen, player_2, (location[1]*grid_size, location[0]*grid_size, grid_size, grid_size))
    draw_grid() 
    pygame.display.flip()

rules(amount_in_row,grid_dimension)
reset = False
while running:
    draw_screen() #update screen
    #check if game is over
    while (move) and (running): #wait for player move
        state = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if event.button == 1: #left click places move
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = floor(mouse_x/grid_size)
                    grid_y = floor(mouse_y/grid_size)
                    state = make_move(grid_x,grid_y,player) #check move
                elif event.button == 3: #right click resets the game
                    reset = True
                    state = True
            if event.type == QUIT:
                running = False
        if state:
            move = False
    if player == 1:
        player = 2
    else:
        player = 1
    move = True
    if reset != True:
        reset = game_check() #check if game is over
    if reset == True:
        draw_screen() #update screen
        print("Game over! Resetting")
        sleep(1)
        grid,amount_in_row,grid_dimension,height,width,smallest_side,grid_size,border_thickness = reset_game()
        reset = False
pygame.quit()
