import colors
from config import LAYERS, ROWS, SCREEN_WIDTH
from graphics import Graphics
from grid import Grid 
import pygame
from initializer import Initializer
from router import Router
from tile import TileState
from ui import UI 

class RouterSimulation:
    update_method = None 

    def __init__(self , grid : Grid , router : Router):
        self._grid : Grid  = grid
        self._ui = UI()
        self._current_layer = 0 
        self._router : Router = router
        RouterSimulation.update_method = self._drawer_stack  
        Graphics.update = self._drawer_stack

    def _drawer_stack(self):
        Initializer.win.fill(colors.SLATE_GRAY)
        self._ui.draw_grid(color = (100 ,0 ,0 , 0 )) 
        self._grid.draw() 
        self._ui.draw_ui() 

    def upper_layer(self,): 
        self._current_layer += 1
        self._current_layer = min(LAYERS, self._current_layer)
        self._ui.update_current_layer(self._current_layer)
        self._ui.draw_ui()

    def bottm_layer(self): 
        self._current_layer -= 1
        self._current_layer = max(1, self._current_layer)
        self._ui.update_current_layer(self._current_layer)
        self._ui.draw_ui()
    
    @staticmethod
    def get_clicked_tile(pos, rows, width) -> tuple[int, int]:
        gap = width // rows

        x, y = pos

        col = y // gap
        row = x // gap

        return row % rows, col % rows

    def loop(self):
        
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
                    if edge_trigger_flg : 
                        pos = pygame.mouse.get_pos()
                        r, c = RouterSimulation.get_clicked_tile(pos, ROWS, SCREEN_WIDTH)
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
                else : 
                    edge_trigger_flg = True 

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.upper_layer()
                    if event.key == pygame.K_DOWN:
                        self.bottm_layer() 

                    if event.key == pygame.K_SPACE:
                        self._router.run(start , end)
                        start = None
                        end = None
            pygame.display.update()

        pygame.quit()

