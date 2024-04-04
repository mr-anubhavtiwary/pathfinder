# modules
import pygame
import sys
import math
from tkinter import messagebox, Tk

pygame.init()           # initialize pygame 

# defining the colors used
WHITE = (255, 255, 255)
DARKGREEN = (34, 108, 115)
LIGHTBLUE = (36, 227, 244)
LIGHTGREEN =(106, 248, 144)
DARKBLUE = (106, 122, 248)
BROWN = (76, 48, 37)
RED = (244, 36, 102)

# box class
class Box:
    def __init__(self, col, row):
        self.x = col
        self.y = row
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []    # all neighbours of the box
        self.prior = None       # last visited box
    
    # simple functions
    def get_pos(self):                      # returns the position of box
        return self.x, self.y
    
    def is_visited(self):                   # returns if box is visited or not
        return self.visited
    
    def is_queued(self):                    # returns if the bo is queued or not
        return self.queued
    
    def is_wall(self):                      # returns if the box is a wall or not
        return self.wall
    
    def is_start(self):                     # returns if the box is a start box or not
        return self.start
    
    def is_target(self):                    # returns if the box is a target box or not
        return self.target
    
    def get_prior(self):                    # returns the previous box of the current box
        return self.prior
    
    def set_visited(self, val):                  # marks the box as visited
        self.visited = val
    
    def set_queued(self, val):                   # marks the box as queued
        self.queued = val
    
    def set_wall(self, val):                     # marks the box as a wall
        self.wall = val
        
    def set_start(self, val):                    # marks the box as a start box
        self.start = val
        
    def set_target(self, val):                   # marks the box as a target box
        self.target = val
        
    def set_prior(self, prior):             # sets the prior of the box as given box
        self.prior = prior
    
    
    # def __lt__(self, other):
    #     return False
    
    # drawing individual boxes in window
    def draw(self, win, color, box_width, box_height):
        # subtracting 2 pixels to show border
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    # 4-way neighbour / 8-way neighbour
    def set_neighbours(self, grid, columns, rows):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])   # left box
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])    # right box
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])    # up box
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])    # down box
        # if self.x > 0 and self.y > 0:
        #     self.neighbours.append(grid[self.x - 1][self.y - 1])    # up-left
        # if self.x > 0 and self.y < rows - 1:
        #     self.neighbours.append(grid[self.x - 1][self.y + 1])    # up-right
        # if self.x < columns - 1 and self.y > 0:
        #     self.neighbours.append(grid[self.x + 1][self.y - 1])    # down-left
        # if self.x < columns - 1 and self.y < rows - 1:
        #     self.neighbours.append(grid[self.x + 1][self.y + 1])    # down-right

# heuristic function
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)      # manhattan distance

# handling mouse click events
def handle_mouse_click(event, grid, start_box_set, target_box_set, start_box, target_box, list, box_width, box_height):
    if event.button == 1 and not start_box_set:     # 1st left click
        col = event.pos[0] // box_width
        row = event.pos[1] // box_height
        # if start and target are not same and box is not a wall
        if not target_box_set or (target_box_set and (col, row) != target_box.get_pos() and not grid[col][row].is_wall()):
            start_box_col = col
            start_box_row = row
            start_box = grid[start_box_col][start_box_row]
            start_box.set_start(True)
            start_box.set_visited(True)
            start_box_set = True
            list.append(start_box)
        
    elif event.button == 1 and not target_box_set:      # 2nd left click
        col = event.pos[0] // box_width
        row = event.pos[1] // box_height
         # if start and target are not same and box is not a wall
        if not start_box_set or (start_box_set and (col, row) != start_box.get_pos() and not grid[col][row].is_wall()):
            target_box_col = col
            target_box_row = row
            target_box = grid[target_box_col][target_box_row]
            target_box.set_target(True)
            target_box_set = True
        
    elif event.button == 3:  # right-click to remove obstacles
        col = event.pos[0] // box_width
        row = event.pos[1] // box_height
        # remove start box
        if (col, row) == start_box.get_pos():
            start_box.set_start(False)
            start_box.set_visited(False)
            start_box_set = False
            list.remove(start_box)
            start_box = None
            
        # remove target box
        elif (col, row) == target_box.get_pos():
            target_box.set_target(False)
            target_box_set = False
            target_box = None
            
        # remove walls
        elif grid[col][row].is_wall():
            grid[col][row].set_wall(False)
        
        else:
            return start_box_set, target_box_set, start_box, target_box
        
    return start_box_set, target_box_set, start_box, target_box

# djikstra algorithm
def djikstra(list, start_box, target_box, path):
    if len(list):           # run till queue is not empty
        current_box = list.pop(0)           # remove the front box of the queue
        current_box.set_visited(True)           # mark the current box as visited
        
        if current_box == target_box:               # if target is found then retrace the path back to source
            while current_box.get_prior() != start_box:
                path.append(current_box.get_prior())
                current_box = current_box.get_prior()
            return False
        
        for neighbour in current_box.neighbours:        # iterate on all the valid neighbours of box
            if not neighbour.is_queued() and not neighbour.is_wall():
                neighbour.set_queued(True)              # queue the neighbour if its neither queued nor a wall
                neighbour.set_prior(current_box)        # assign the current box as prior of the neighbour
                list.append(neighbour)          # insert it in the queue
                                
    return True

# depth first search algorithm
def dfs(list, start_box, target_box, path):
    if len(list):           # run till stack is not empty
        current_box = list.pop()            # remove the top box of the stack
        current_box.set_visited(True)           # mark the current box as visited
        
        if current_box == target_box:               # if target is found then retrace the path back to source
            while current_box.get_prior() != start_box:
                path.append(current_box.get_prior())
                current_box = current_box.get_prior()
            return False
        
        for neighbour in current_box.neighbours:                # iterate on all the valid neighbours of box
            if not neighbour.is_queued() and not neighbour.is_wall():
                neighbour.set_queued(True)              # queue the neighbour if its neither queued nor a wall
                neighbour.set_prior(current_box)        # assign the current box as prior of the neighbour
                list.append(neighbour)          # insert it in the stack

    return True

# breadth first search algorithm
def bfs(list, start_box, target_box, path):
    if len(list):
        current_box = list.pop(0)            # remove the front box of the queue
        current_box.set_visited(True)            # mark the current box as visited
        
        if current_box == target_box:               # if target is found then retrace the path back to source
            while current_box.get_prior() != start_box:
                path.append(current_box.get_prior())
                current_box = current_box.get_prior()
            return False
        
        for neighbour in current_box.neighbours:
            if not neighbour.is_queued() and not neighbour.is_wall():
                neighbour.set_queued(True)              # queue the neighbour if its neither queued nor a wall
                neighbour.set_prior(current_box)        # assign the current box as prior of the neighbour
                list.append(neighbour)          # insert it in the queue
                
    return True

# Pathfinding algorithm initilization
def initialize(begin_search, list, start_box, target_box, path):
    if begin_search == 1:
        searching = djikstra(list, start_box, target_box, path)
        if(not searching):
            return 0    # stop algorithm
        
    elif begin_search == 2:
        searching = dfs(list, start_box, target_box, path)
        if(not searching):
            return 0
        
    elif begin_search == 3:
        searching = bfs(list, start_box, target_box, path)
        if(not searching):
            return 0
    
    return begin_search


def main():
    # initializing window size
    window_width = 700
    window_height = 700
    
    # set window name
    pygame.display.set_caption("PATHFINDER")
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    
    # initializing variables
    columns = 50
    rows = 50
    
    box_width = window_width // columns
    box_height = window_height // rows
    
    grid = [[Box(col, row) for row in range(rows)] for col in range(columns)]
    for col in range(columns):
        for row in range(rows):
            grid[col][row].set_neighbours(grid, columns, rows)
            
    list = []                      # for neighbours
    path = []                       # for final path
    start_box_set = False           # to check if start box is assigned or not
    target_box_set = False          # to check if target box is assigned or not
    begin_search = 0                # search start key(1, 2, 3, 4)
    start_box = None                # start box object
    target_box = None               # target box object
    
    # main iterator start(keeps the pygame window open until closed)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           # to exit pygame window
                pygame.quit()
                sys.exit()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:      # all mouse button press operations
                start_box_set, target_box_set, start_box, target_box = handle_mouse_click(event, grid, start_box_set, target_box_set, start_box, target_box, list, box_width, box_height)
            
            elif event.type == pygame.MOUSEMOTION:          # mouse motion for drawing the wall
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                # draw wall
                if event.buttons[0]:
                    col = x // box_width
                    row = y // box_height
                    # avoiding start and target points
                    if(col, row) != start_box.get_pos():
                        if(col, row) != target_box.get_pos(): 
                            grid[col][row].set_wall(True)
                        
            # keyboard input
            elif event.type == pygame.KEYDOWN:
                # reset using key = r
                if event.key == pygame.K_r:
                    main()
                
                # algorithms initialization keys
                elif event.key == pygame.K_0 and target_box_set:    # stop the current executing algorithm
                    begin_search = 0
                elif event.key == pygame.K_1 and target_box_set:    # djikstra algorithm
                    begin_search = 1
                elif event.key == pygame.K_2 and target_box_set:    # depth first search algorithm
                    begin_search = 2
                elif event.key == pygame.K_3 and target_box_set:    # breadth first search algorithm
                    begin_search = 3
                elif event.key == pygame.K_4 and target_box_set:    # (A*) algorithm
                    begin_search = 4
        
        # pathfinding algorithms initialization
        begin_search = initialize(begin_search, list, start_box, target_box, path)
        
        # when no path is found
        if len(list) == 0 and begin_search:
            Tk().wm_withdraw()
            messagebox.showinfo("Alert", "No path Found!")
            begin_search = 0
        
        # creating blank window
        window.fill((120, 120, 120))
        
        # putting colors for all objects
        for col in range(columns):
            for row in range(rows):
                box = grid[col][row]
                box.draw(window, WHITE, box_width, box_height)
                
                if box.is_queued():
                    box.draw(window, DARKGREEN, box_width, box_height)
                if box.is_visited():
                    box.draw(window, LIGHTBLUE, box_width, box_height)
                if box in path:
                    box.draw(window, LIGHTGREEN, box_width, box_height)
                if box.is_start():
                    box.draw(window, DARKBLUE, box_width, box_height)
                if box.is_wall():
                    box.draw(window, BROWN, box_width, box_height)
                if box.is_target():
                    box.draw(window, RED, box_width, box_height)
        
        pygame.display.flip()
        # pygame.time.delay(100)

if __name__ == "__main__":
    main()

