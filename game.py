import pygame
from pygame.locals import *
from math import floor
from time import sleep

amount_in_row = 3
grid_dimension = 10
height = grid_dimension
width = grid_dimension
grid_size = 64
border_thickness = grid_size/8
grid = [[None for x in range(width)] for y in range(height)]

empty = (255,255,255)
player_1 = (255,0,0)
player_2 = (0,0,255)
running = True
move = True
player = 1

screen = pygame.display.set_mode((width*grid_size,height*grid_size))
pygame.init()

def reset_game():
    grid = [[None for x in range(width)] for y in range(height)]
    return grid

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
    a = 0
    for i in range(len(values)-1): #match found horizontally
        if (values[i] == values[i+1]) and (values[i] != None) and (values[i+1] != None):
            a += 1
            if (a == amount_in_row-1):
                return True
    return False

def game_check():
    #check for three in a row
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
    values = []
    for x,y in zip(range(width), range(height)):
        values.append(grid[y][x])
    current_state = check_win(values)
    if current_state:
        return True #match found diagonally from left top to right bottom
    values = []
    for x,y in zip(range(width-1,-1,-1),range(height)):
        values.append(grid[y][x])
    current_state = check_win(values)
    if current_state:
        return True #match found diagonally from right top to left bottom
    if c == 0:
        return True #Draw, no spaces left and no win
    return False
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
                    print(mouse_x,mouse_y)
                    grid_x = floor(mouse_x/grid_size)
                    grid_y = floor(mouse_y/grid_size)
                    print(grid_x,grid_y,player)
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
        grid = reset_game()
        reset = False
pygame.quit()
