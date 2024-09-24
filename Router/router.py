import pygame 
import colors


SCREEN_WIDTH = 600 
SCREEN_HEIGHT = 600
TITLE = "Router"
GRID_COLOR = (126,126,126)

WIN = pygame.display.set_mode([SCREEN_WIDTH , SCREEN_HEIGHT])



class RouterMainWindow:


    def __init__(self , width : float = SCREEN_WIDTH , height : float = SCREEN_HEIGHT) -> None:
        self.__width = width 
        self.__height = height 
    
        
        pygame.display.set_caption(TITLE)
    

    def draw_grid(self, rows , width , **kwarg):
        
        gap = width // rows 

        color = kwarg.get("color" , GRID_COLOR)

        for i in range(rows): 
            pygame.draw.line(WIN , color, (i * gap  , 0 ) , (i * gap , width) , )

        for i in range(rows):  
            pygame.draw.line(WIN , color, (0 , i * gap ) , (width , i * gap))




