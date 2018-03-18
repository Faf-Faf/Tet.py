"""
Main game unit
"""

import pygame

# Найстройка повторения клавиш
KEY_DELAY = 100
KEY_INTERVAL = 100

# Цветовые константы
C_BKGROUND   = (   0,   0,   0)
C_RSTAIR     = ( 255, 255, 255)

# Size constants
SZ_CELL     = 30
SZ_G_BORDER = 10
SZ_OFFSET   = [30, 20, 30, 20]

G_WIDTH  = 30

class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.size = screen.get_size()
        self.decor = TronDec(screen)
        self.gsize = (G_WIDTH, int((self.size[1] - SZ_OFFSET[0] 
                               - SZ_OFFSET[2] 
                               - SZ_G_BORDER)/SZ_CELL)) # Glass size in cells
        self.decor.SetGRect((SZ_OFFSET[3] + SZ_G_BORDER, 
                             SZ_OFFSET[0],
                             self.gsize[0] * SZ_CELL,
                             self.gsize[1] * SZ_CELL))
        self.glass = Glass(self.decor, self.gsize)

    def MakeScene(self):
        self.glass.AddShape(RStair(self.glass, 10))

    def Draw(self):
        self.glass.Draw()
    

class Decorator:
    def __init__(self, screen):
        self.screen = screen
        self.grect = pygame.Rect(0, 0, 0, 0)

    def SetGRect(self, new_rect):
        self.grect = new_rect

    def DrawCell(self, x, y, color):
        pass



class TronDec(Decorator):
    def __init__(self, screen):
        Decorator.__init__(self, screen)

    def DrawCell(self, x, y, color):
        x = self.grect[0] + x * SZ_CELL
        y = self.grect[1] + y * SZ_CELL
        pygame.draw.rect(self.screen, color, (x, y, x + SZ_CELL, y + SZ_CELL), 2)



class Glass:
    def __init__(self, decor, size):   
        self.decor = decor
        self.size = size
        self.aShape = None   # Active shape in the glass

    def Draw(self):
        # Draw all glass lines
        # Draw active shape
        if self.aShape != None:
            self.aShape.Draw()

    def AddShape(self, shape):
        self.aShape = shape

class Shape:
    def __init__(self, glass):
        self.glass = glass
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.color = 0
        self.form = []
        self.pose = 0
        self.poses = []

    def Draw(self):
        for y, l in enumerate(self.form):
            for x, c in enumerate(l):
                if c == 1:
                    self.glass.decor.DrawCell(self.x + x, self.y + y, self.color)

    def Move(self):
        pass

    def Rotate(self):
        pass

    def Drop(self):
        pass

class RStair(Shape):
    def __init__(self, glass, x):
        Shape.__init__(self, glass)
        self.x = x
        self.poses.append([[0,1,1],[1,1,0]])   # Horizontal pose
        self.poses.append([[1,0],[1,1],[0,1]]) # Vertical pose
        self.color = C_RSTAIR
        self.form = self.poses[self.pose]
        



def grp_init(size):
    """
    Initializes Graphics.

    Pygame initialize. Creates application window.

    Returns screen - main surface of application.
    """
    pygame.init()

    screen=pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Tet.py")

    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)

    return screen



def run():
    """
    Executes application.

    Creates context of application and runs event loop processing
    """
    screen = grp_init((1600, 900))
    clock = pygame.time.Clock()
    
    scr = Screen(screen)
    scr.MakeScene()

    done = False

    # -------- Main Program Loop -----------
    while not done:

        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                continue

            # Обработать нажатия клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # quit 
                    done = True
                    continue

        # --- Game logic should go here

        # --- Screen-clearing code goes here
        screen.fill(C_BKGROUND)

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        
        # --- Drawing code should go here      
        scr.Draw()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()



if __name__ == "__main__":
    run()
