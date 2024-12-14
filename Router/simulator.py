import colors
from config import LAYERS, ROWS, SCREEN_WIDTH
from graphics import Graphics
from grid import Grid
import pygame
from initializer import Initializer
from router import Router
from ui import UI

class RouterSimulator:
    """
    A class to simulate router operations in a grid-based layout.

    Attributes:
        update_method (function): A static reference to the method responsible for drawing the simulation.
        _grid (Grid): The grid object representing the layers and tiles.
        _ui (UI): The user interface for interacting with the simulation.
        _current_layer (int): The index of the current layer in the grid.
        _router (Router): The router instance used for routing tiles.

    Methods:
        __init__(self, grid: Grid, router: Router):
            Initializes the RouterSimulator with the grid and router objects.
        
        _drawer_stack(self, context=""):
            Draws the current grid and user interface on the screen.

        upper_layer(self):
            Increases the current layer index to move up to the next layer.

        bottm_layer(self):
            Decreases the current layer index to move down to the previous layer.

        get_clicked_tile(pos, rows, width) -> tuple[int, int]:
            Converts the mouse click position to row and column indices of the clicked tile.

        loop(self):
            Main simulation loop that listens for events and updates the simulation.
    """
    
    update_method = None 

    def __init__(self, grid: Grid, router: Router):
        """
        Initializes the RouterSimulator with the provided grid and router objects.

        Args:
            grid (Grid): The grid object to be used in the simulation.
            router (Router): The router instance responsible for routing tiles.
        """
        self._grid: Grid = grid
        self._ui = UI()
        self._current_layer = 0
        self._router: Router = router
        RouterSimulator.update_method = self._drawer_stack
        Graphics.update = lambda: self._drawer_stack("Graphics Drawer")

    def _drawer_stack(self, context=""):
        """
        Draws the current grid and user interface on the window.

        Args:
            context (str, optional): A string that can be used to differentiate drawing contexts. Defaults to an empty string.
        """
        if context != "":
            pass 
        Initializer.win.fill(colors.SLATE_GRAY)
        self._ui.draw_grid(color=(100, 0, 0, 0)) 
        self._grid.draw() 
        self._ui.draw_ui() 
        pygame.display.update()

    def upper_layer(self):
        """
        Increases the current layer index to move up to the next layer, updating the UI.
        """
        self._current_layer += 1
        self._current_layer = min(LAYERS, self._current_layer)
        self._ui.update_current_layer(self._current_layer)
        self._ui.draw_ui()

    def bottm_layer(self):
        """
        Decreases the current layer index to move down to the previous layer, updating the UI.
        """
        self._current_layer -= 1
        self._current_layer = max(1, self._current_layer)
        self._ui.update_current_layer(self._current_layer)
        self._ui.draw_ui()

    @staticmethod
    def get_clicked_tile(pos, rows, width) -> tuple[int, int]:
        """
        Converts the mouse click position to row and column indices of the clicked tile.

        Args:
            pos (tuple[int, int]): The mouse click position (x, y).
            rows (int): The number of rows in the grid.
            width (int): The width of the grid.

        Returns:
            tuple[int, int]: The (row, column) indices of the clicked tile.
        """
        gap = width // rows
        x, y = pos
        col = y // gap
        row = x // gap
        return row % rows, col % rows

    def loop(self):
        """
        Main simulation loop that listens for events and updates the simulation.

        This loop handles quitting the simulation, navigating between layers, and routing tiles
        when the spacebar is pressed. Mouse clicks are used to select start and end tiles for routing.
        """
        running = True
        start = None
        end = None
        edge_trigger_flg = True  

        while running:
            self._drawer_stack()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if pygame.mouse.get_pressed()[0]:
                    if edge_trigger_flg: 
                        pos = pygame.mouse.get_pos()
                        r, c = RouterSimulator.get_clicked_tile(pos, ROWS, SCREEN_WIDTH)
                        clicked_tile = self._grid.layers()[self._current_layer][r][c]

                        if start is None:
                            clicked_tile.color = colors.RED
                            start = clicked_tile

                        elif end is None and start is not None:
                            clicked_tile.color = colors.BLUE
                            end = [clicked_tile]

                        else:
                            clicked_tile.color = colors.BLUE
                            end.append(clicked_tile)

                        edge_trigger_flg = False 
                else:
                    edge_trigger_flg = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.upper_layer()
                    if event.key == pygame.K_DOWN:
                        self.bottm_layer()

                    if event.key == pygame.K_SPACE:
                        self._router.fan_out_route(start, end)
                        start = None
                        end = None
            pygame.display.update()

        pygame.quit()
