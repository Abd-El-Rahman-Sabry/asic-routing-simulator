import pygame
from config import SCREEN_WIDTH , SCREEN_HEIGHT

WIN = None 

class Initializer: 

    win = None 

    def __init__(self):
        """
        Initialize the simulator and the pygame window

        """
        pygame.init()
        pygame.font.init()

        Initializer.win = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


    def __new__(cls):
        if not hasattr(cls , 'instance'): 
            cls.instance = super(Initializer , cls).__new__(cls)
        return cls.instance 

        


    