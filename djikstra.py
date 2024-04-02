import pygame
import sys
from tkinter import messagebox, Tk

pygame.init()

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
    
    # drawing individual boxes in window
    def draw(self, win, color, box_width, box_height):
        # subtracting 2 pixels to show border
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

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

# handling mouse click events
def handle_mouse_click(event, grid, start_box_set, target_box_set, start_box, target_box, queue, box_width, box_height, start_box_col, start_box_row, target_box_col, target_box_row):
    if event.button == 1 and not start_box_set:     # 1st left click
        start_box_col = event.pos[0] // box_width
        start_box_row = event.pos[1] // box_height
        start_box = grid[start_box_col][start_box_row]
        start_box.start = True
        start_box.visited = True
        start_box_set = True
        queue.append(start_box)
        
    elif event.button == 1 and not target_box_set:      # 2nd left click
        target_box_col = event.pos[0] // box_width
        target_box_row = event.pos[1] // box_height
        target_box = grid[target_box_col][target_box_row]
        target_box.target = True
        target_box_set = True
        
    return start_box_set, target_box_set, start_box, target_box, start_box_col, start_box_row, target_box_col, target_box_row

def main():
    # initializing window size
    window_width = 700
    window_height = 700
    
    # set window name
    pygame.display.set_caption("PATHFINDER")
    window = pygame.display.set_mode((window_width, window_height))
    
    # initializing variables
    columns = 50
    rows = 50
    
    box_width = window_width // columns
    box_height = window_height // rows
    
    grid = [[Box(col, row) for row in range(rows)] for col in range(columns)]
    for col in range(columns):
        for row in range(rows):
            grid[col][row].set_neighbours(grid, columns, rows)
            
    queue = []                      # for neighbours
    path = []                       # for final path
    start_box_set = False
    target_box_set = False
    begin_search = False
    searching = True
    start_box = None
    start_box_col = None
    start_box_row = None
    target_box_col = None
    target_box_row = None
    target_box = None
    
    # main game start
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_box_set, target_box_set, start_box, target_box, start_box_col, start_box_row, target_box_col, target_box_row = handle_mouse_click(event, grid, start_box_set, target_box_set, start_box, target_box, queue, box_width, box_height, start_box_col, start_box_row, target_box_col, target_box_row)
            
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                # draw wall
                if event.buttons[0]:
                    col = x // box_width
                    row = y // box_height
                    # avoiding start and target points
                    if(col == start_box_col and row == start_box_row):
                        continue
                    if(col == target_box_col and row == target_box_row):
                        continue 
                    
                    grid[col][row].wall = True
                        
            # algorithm initialization key = space
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and target_box_set:
                    begin_search = True
        
        # Djikstra algorithm
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                
                if current_box == target_box:
                    searching = False
                    
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Alert", "No path Found!")
                    searching = False
        
        # creating blank window
        window.fill((120, 120, 120))
        
        # putting colors for all objects
        for col in range(columns):
            for row in range(rows):
                box = grid[col][row]
                box.draw(window, (255, 255, 255), box_width, box_height)
                
                if box.queued:
                    box.draw(window, (34, 108, 115), box_width, box_height)
                if box.visited:
                    box.draw(window, (36, 227, 244), box_width, box_height)
                if box in path:
                    box.draw(window, (106, 248, 144), box_width, box_height)
                if box.start:
                    box.draw(window, (106, 122, 248), box_width, box_height)
                if box.wall:
                    box.draw(window, (76, 48, 37), box_width, box_height)
                if box.target:
                    box.draw(window, (244, 36, 102), box_width, box_height)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
