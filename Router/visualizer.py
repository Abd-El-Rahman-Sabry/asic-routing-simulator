import pygame

# Constants for screen dimensions and title
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TITLE = "Router"
GRID_COLOR = (126, 126, 126)

# Initialize the pygame window
WIN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class RouterMainWindow:
    """
    A class representing the main window of the router simulation, handling window initialization
    and grid drawing.

    Attributes:
        __width (float): The width of the window.
        __height (float): The height of the window.
    """

    def __init__(self, width: float = SCREEN_WIDTH, height: float = SCREEN_HEIGHT) -> None:
        """
        Initializes the main window with the specified dimensions.

        Args:
            width (float): The width of the window (default is SCREEN_WIDTH).
            height (float): The height of the window (default is SCREEN_HEIGHT).
        """
        self.__width = width
        self.__height = height

        # Set the window title
        pygame.display.set_caption(TITLE)

    def draw_grid(self, rows, width, **kwarg):
        """
        Draws a grid on the window with the specified number of rows and tile width.

        Args:
            rows (int): The number of rows in the grid.
            width (int): The width of the grid.
            kwarg: Additional keyword arguments (e.g., color for the grid lines).
            
        Keyword Args:
            color (tuple): The color of the grid lines (default is GRID_COLOR).
        """
        gap = width // rows  # Calculate the space between grid lines

        # Retrieve the grid line color, defaulting to GRID_COLOR
        color = kwarg.get("color", GRID_COLOR)

        # Draw vertical grid lines
        for i in range(rows):
            pygame.draw.line(
                WIN,
                color,
                (i * gap, 0),  # Start at the top of the screen
                (i * gap, width),  # End at the bottom of the screen
            )

        # Draw horizontal grid lines
        for i in range(rows):
            pygame.draw.line(WIN, color, (0, i * gap), (width, i * gap))  # Start from left to right
