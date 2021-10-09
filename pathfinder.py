import pygame as pg

# red is obstable = 1
# green is start point = 2
# yellow is goal = 3
# white is path taken by algorithm = 4

# mode is a variable that determines what the user is currently trying to draw (look above for different moves)
#global mode
mode = 1

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

def main():
    # window
    pg.font.init()
    #define font
    myfont = pg.font.SysFont('Comic Sans MS', 11)
    startFont = myfont.render("Start",False,(0,0,0))
    goalFont = myfont.render("Goal",False,(0,0,0)) 
    obFont = myfont.render("Simulate",False,(0,0,0)) 
    pg.init()
    mode = 1
    screen = pg.display.set_mode([400,300])
    createGrid(13,13)

    run = True
    while run:
        #drawGrid(screen,BLACK,30)
        for event in pg.event.get():

            if event.type==pg.QUIT:
                run=False
            else:
                
                
                #if event.type==pg.NOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:

                    pos = pg.mouse.get_pos()
                    pos_x = pos[0]//(20+5)
                    pos_y = pos[1] //(20+5)

                    # catch error if user click outside of "drawing zone"
                    if (pos_x < 13):
                        grid[pos_y][pos_x] = mode
                    else:
                        #check if user clicked start button
                        if (350 < pos[0] < 390) and (20 < pos[1] < 50):
                            mode = 2
                        #goal button
                        elif(350 < pos[0] < 390) and (20 < pos[1] < 130):
                            mode = 3
                        # start the simulation button button
                        elif(350 < pos[0] < 390) and (20 < pos[1] < 210):
                            
                            # fetch the start and goal position
                            start_pos = find_start(grid)
                            goal_pos = find_goal(grid)
                            pathfinder(grid,start_pos,goal_pos)
        screen.fill(WHITE)
        
        drawGrid(screen,BLACK,20,5,5,grid)
        
        # draw text + buttons
        screen.blit(startFont,(350,5))
        startButton = Button(40,30,2,350,20,screen,GREEN)

        screen.blit(goalFont,(350,75))
        goalButton = Button(40,30,3,350,100,screen,YELLOW)
        
        screen.blit(obFont,(350,150))
        obButton = Button(40,30,1,350,180,screen,RED)

        

        pg.display.update()

#class for all the drawing buttons
class Button():
    def __init__(self,width,height,mode,posx,posy,screen,color):
        self.width = width
        self.height = height
        self.mode = mode
        self.posx = posx
        self.posy = posy
        self.screen = screen     
        self.color = color
        rect = pg.Rect(posx,posy,width,height)
        pg.draw.rect(screen,color,rect)

# node class for all the nodes in grid      
class Node():
    def __init__(self,position=None,parent=None):
        self.position = position
        self.parent = parent

        self.f = 0
        self.h = 0
        self.g = 0

    # function used to override pythons default object comparison
    
    def __eq__(self,other):
        if self.position == other.position:
            return True
        else:
            return False

# function to find the start points position
 
def find_start(grid):
    for i in range(len(grid)):
        for z in range(len(grid[0])):
            if grid[i][z] == 2:
                return (i,z)
# function to find the goals position
def find_goal(grid):
    for i in range(len(grid)):
        for z in range(len(grid[0])):
            if grid[i][z] == 3:
                return (i,z)

def pathfinder(grid,start_pos,goal_pos):
    # open list and close list
    open_list = []
    close_list = []
    children_pos = ((-1,0),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1),(0,1),(1,0))
    # make the start and goal an object
    start = Node(start_pos)
    goal = Node(goal_pos)
    start.g = 0
    start.h = (start.position[0] - goal.position[0])**2 + (start.position[1] - goal.position[1])**2
    start.f = start.h
    open_list.append(start)
    current = open_list[0]
    while (len(open_list) > 0):
        # find node with lowest f value and make it curreent note to expand on later 
        for count,item in enumerate(open_list):
            if item.f < current.f:
                current = item
                close_list.append(current)
                open_list.pop(count)
        
        # if found goal
        if current == goal:
            # reverse the path and color it
            print("FOUND GOAL")
            tmp = current.parent
            while (tmp.parent is not None):
                print("tmp = ",tmp.position)
                grid[tmp.position[0]][tmp.position[1]] = 4
                tmp = tmp.parent
            break
        # generate child
        for child in children_pos:
                y_pos = child[0] + current.position[0]
                x_pos = child[1] + current.position[1]

                if 13 < x_pos or x_pos < 0:
                    continue
                if 13 < y_pos or y_pos < 0:
                    continue

                childNode = Node((y_pos,x_pos),current)
                # check if child is already visited 
                for node in close_list:
                    if node == childNode:
                        continue

                childNode.g = (abs(start.position[0] - childNode.position[0])**2) + (abs(start.position[1] - childNode.position[1])**2)
                childNode.h = (abs(goal.position[0] - childNode.position[0])**2) + (abs(goal.position[1] - childNode.position[1])**2)
                childNode.f = childNode.h
                
                # check if child is in openlist
                for node in open_list:
                    if node == childNode:
                            if childNode.f > current.f:
                     
                                continue
                    
                open_list.append(childNode)

#draw the grids on the window
def drawGrid(win,color,size,sx,sy,grid):
    syy = 0
    for y in range(13):
        sxx=sx
        for x in range(13):
            
            if grid[y][x] == 1:
                color = RED
            elif grid[y][x] == 2:
                color = GREEN
            elif grid[y][x] == 3:
                color = YELLOW
            elif grid[y][x] == 4:
                color = WHITE
            else:
                color=(0,0,0)
            rect = pg.Rect((x*size+sxx),(y*size+syy),size,size)
            pg.draw.rect(win,color,rect)
            sxx+=sx

        syy+=sy
    
#function that creates 2d list of the map
def createGrid(colDim,rowDim):
    global grid
    grid=[]
    for row in range(rowDim):
        grid.append([])
        for col in range(colDim):
            grid[row].append(0)


if __name__ == "__main__":
    main()