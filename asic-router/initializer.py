import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE



class Initializer:
    """
    A class to initialize and manage the game window and Pygame settings.

    Attributes:
        win (pygame.Surface): The Pygame window/screen surface.
    """

    win = None

    def __init__(self):
        """
        Initialize the Pygame library and create the game window.
        Sets up the display mode, window caption, and initializes fonts.
        """
        pygame.init()  # Initialize Pygame modules
        pygame.font.init()  # Initialize Pygame fonts

        # Set up the game window and store the reference in 'win'
        Initializer.win = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(TITLE)  # Set the window title

    def __new__(cls):
        """
        Ensure that only one instance of the Initializer class is created.
        
        Returns:
            Initializer: The singleton instance of the Initializer class.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Initializer, cls).__new__(cls)
        return cls.instance  # Return the singleton instance
