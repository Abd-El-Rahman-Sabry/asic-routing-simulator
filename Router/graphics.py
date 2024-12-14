

from config import WIDTH
from initializer import Initializer
from tile import Tile
import pygame 
import time 


class Graphics: 

    # Must be initialized 
    update = None


    @staticmethod 
    def line(s : Tile , e : Tile , mili_sec_delay = 1 , color = 255) -> None:
        x_s , y_s= s.get_cordinates() 
        x_e , y_e= e.get_cordinates()
        shift = WIDTH / 2
        win = Initializer.win
        pygame.draw.line(win , (color if color <= 255 else 255 , 0 , 0) , (x_s + shift , y_s  + shift), (x_e + shift , y_e + shift)) 
        pygame.display.update()
        time.sleep(mili_sec_delay/1000)

    @staticmethod 

    def visualize_path(tiles : list[Tile]): 
        for tile in tiles: 
            tile.make_path() 

