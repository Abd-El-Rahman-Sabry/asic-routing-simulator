

import colors
from config import WIDTH
import config
from initializer import Initializer
import pygame 
import time 


class Graphics: 

    # Must be initialized 
    update = None


    @staticmethod 
    def line(s  , e  , mili_sec_delay = 1 , color = 255) -> None:
        x_s , y_s= s.get_cordinates() 
        x_e , y_e= e.get_cordinates()
        shift = WIDTH / 2
        win = Initializer.win
        pygame.draw.line(win , (color if color <= 255 else 255 , 0 , 0) , (x_s + shift , y_s  + shift), (x_e + shift , y_e + shift) , config.LINE_WIDTH) 
        pygame.display.update()
        time.sleep(mili_sec_delay/1000)

    @staticmethod 
    def visualize_path(tiles ): 
        for tile in tiles: 
            tile.make_path() 


    @staticmethod 

    def draw_text(s : str , x : int , y : int , font_size = 12): 
        font = pygame.font.SysFont("Arial", font_size)
        text = font.render(s , True , colors.RED)
        w , h = text.get_size() 
        Initializer.win.blit(text , (x , y - h //2 ))

