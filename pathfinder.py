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
    startFont =myfont.render("Start",False,(0,0,0))
    goalFont =myfont.render("Goal",False,(0,0,0)) 
    obFont =myfont.render("Obstacle",False,(0,0,0)) 
    pg.init()
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
                if pg.mouse.get_pressed()[0]:#MOUSEBUTTONDOWN:

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
                        #obstacle button
                        elif(350 < pos[0] < 390) and (20 < pos[1] < 210):
                            mode = 1
                
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