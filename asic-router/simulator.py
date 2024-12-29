import colors
from config import LAYERS, ROWS, SCREEN_WIDTH, VIA_COST
from from_json import RouteLoader
from graphics import Graphics
from grid import Grid
import pygame
from initializer import Initializer
from router import Router
from tile import TileState
from ui import UI
import random 

from threading import Thread , Semaphore
from control_window import ControlWindow

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
        self.__start = None
        self.__end = None
        self.__routes = None

        assert VIA_COST >= 1 

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
        self._current_layer = max(0, self._current_layer)
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
    
    def generate_routes(self): 
        self._router.disable_graphics_updates() 
        for i in range(3): 
            print(i)
            x  = random.randint(0 , ROWS -1 )
            y  = random.randint(0 , ROWS -1 )
            z  = random.randint(0 , LAYERS -1 )

            start = self._grid.layers()[z][x][y]

            if start.state == TileState.barrier: 
                continue 

            count_end = random.randint(1 , 10)
            print(count_end)
            ends = []

            for i in range(count_end): 

                            x  = random.randint(0 , ROWS -1 )
                            y  = random.randint(0 , ROWS -1 )
                            z  = random.randint(0 , LAYERS -1 )

                            tile = self._grid.layers()[z][x][y]

                            if tile.state == TileState.barrier: 
                                continue 
                            else : 
                                ends.append(tile)
            print(ends)
            if len(ends) == 0 : 
                continue 

            self._router.fan_out_route(start , ends)

            self._ui.set_status(f"currently building a random route {i /10 }%")
            
    def build_control_menu(self): 
        win = ControlWindow() 
        win.addButton("Run" , lambda : print("Run"))
        win.addButton("Run" , lambda : print("Run"))
        win.addButton("Run" , lambda : print("Run"))
        win.show_controller()

    def run(self):
        sim = Thread(target=self.loop)
        menu = Thread(target=self.build_control_menu)

        sim.start() 
        menu.start()

        sim.join()
        menu.join()

    def load_route_from_json(self, json): 
        obj = RouteLoader(json)
        routes = obj.routes 
        self.__routes = routes 


    def __apply_json_routes(self): 
        for route in self.__routes: 
            
            start_point  = route[0]

            x , y , layer = start_point

            tile = self._grid.layers()[layer][x][y]


            tile.state = TileState.start 
            tile.color = colors.RED
            self.__start = tile 
             
            route_ends = []
            for end_point in route[1:]: 
                x , y , layer = end_point
                end_tile = self._grid.layers()[layer][x][y]
                end_tile.color = colors.BLUE
                end_tile.state = TileState.end 
                route_ends.append(end_tile)

            self.__end = route_ends


        

        



            

    def loop(self):
        """
        Main simulation loop that listens for events and updates the simulation.

        This loop handles quitting the simulation, navigating between layers, and routing tiles
        when the spacebar is pressed. Mouse clicks are used to select start and end tiles for routing.
        """
        running = True
        edge_trigger_flg = True  

        startup = False 

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

                        if self.__start is None:
                            clicked_tile.color = colors.RED
                            self.__start = clicked_tile
                            self.__start.state = TileState.start

                        elif self.__end is None and self.__start is not None:
                            clicked_tile.color = colors.BLUE
                            self.__end = [clicked_tile]
                            clicked_tile.state = TileState.end

                        else: 
                            clicked_tile.color = colors.BLUE
                            clicked_tile.state = TileState.end
                            self.__end.append(clicked_tile)

                        edge_trigger_flg = False 
                else:
                    edge_trigger_flg = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.upper_layer()
                    if event.key == pygame.K_DOWN:
                        self.bottm_layer()

                    if event.key == pygame.K_q: 
                        self.generate_routes() 

                    if event.key == pygame.K_SPACE:
                        self._router.fan_out_route(self.__start, self.__end)
                        self.__start.state = TileState.barrier
                        for e in self.__end: 
                            e.state = TileState.barrier     
                        self.__start = None
                        self.__end = None

            if not startup: 
                if self.__routes: 
                    self.__apply_json_routes()
                startup = True  
            pygame.display.update()

        pygame.quit()
