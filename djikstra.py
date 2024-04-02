from tkinter import messagebox, Tk
import pygame
import sys
window_width = 500
window_height = 500

window = pygame.display.set_mode((window_width, window_height))
columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows

grid = []
queue = []
path = []

class Box:
    # indices for position in box
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
    
    # drawing individual boxes in window
    def draw(self, win, color):
        # subtracting 2 pixels to show border
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))
    
    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])
            
            
# create grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)
    
# set neightbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()
    


def main():
    begin_search = False
    target_box_set = False
    start_box_set = False
    searching = True
    start_box = None
    target_box = None
           
    
    while True:
        for event in pygame.event.get():
            #quit window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start_box_set == False:
                i = x // box_width
                j = y // box_height
                start_box = grid[i][j]
                start_box.start = True
                start_box.visited = True
                start_box_set = True
                queue.append(start_box)
                
            # for target point
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and target_box_set == False:
                i = x // box_width
                j = y // box_height
                target_box = grid[i][j]
                target_box.target = True
                target_box_set = True
                
            # Mouse controls
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                # draw wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True

            
            # start algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True
           
        # djikstra algorithm     
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
        
        
        
        # fill with black color in border
        window.fill((120, 120, 120))
        
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (255, 255, 255))
                
                if box.queued:
                    box.draw(window, (34, 108, 115))
                if box.visited:
                    box.draw(window, (36, 227, 244))
                if box in path:
                    box.draw(window, (106, 248, 144))
                    
                    
                if box.start:
                    box.draw(window, (106, 122, 248))
                if box.wall:
                    box.draw(window, (76, 48, 37))
                if box.target:
                    box.draw(window, (244, 36, 102))
                
        pygame.display.flip()
    
main()