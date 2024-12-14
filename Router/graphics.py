

import colors
from config import WIDTH
from initializer import Initializer
from tile import Tile
import pygame 

class Graphics: 

    update = None

    @staticmethod 
    def line(s : Tile , e : Tile) -> None:
        x_s , y_s= s.get_cordinates() 
        x_e , y_e= e.get_cordinates()
        shift = WIDTH /2
        win = Initializer.win
        pygame.draw.line(win , colors.RED , (x_s + shift , y_s  + shift), (x_e + shift , y_e + shift)) 

