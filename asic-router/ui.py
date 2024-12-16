import colors
import pygame
from graphics import Graphics
from initializer import Initializer 
from config import SCREEN_HEIGHT, SCREEN_WIDTH, WIDTH , ROWS , GRID_COLOR , layer_color_map

class UI (): 

    update = None 

    def __init__(self, ):
        self.__current_layer = 0
        self.__current_status = "" 
        UI.update = self 
    
    def update_current_layer(self, layer): 
        self.__current_layer = layer 


    def draw_grid(self, **kwarg):

        gap = SCREEN_WIDTH // ROWS

        color = kwarg.get("color", GRID_COLOR)
        win  = Initializer.win 
        for i in range(ROWS):
            pygame.draw.line(
                win,
                color,
                (i * gap, 0),
                (i * gap, SCREEN_WIDTH),
            )

        for i in range(ROWS):
            pygame.draw.line(win, color, (0, i * gap), (SCREEN_WIDTH, i * gap))

    def draw_ui(self): 
        self._draw_side_layers_info()
        self._draw_bottom_info()
        self._draw_status()

    def _draw_bottom_info(self): 
        font = pygame.font.SysFont("Arial", 13)
        win = Initializer.win 
        height = 20
        width  = SCREEN_WIDTH
        x_s, y_s = 0, SCREEN_HEIGHT - height

        pygame.draw.rect(win, colors.BEIGE_FILL_LAYER, [x_s, y_s, width, height])



    def set_status(self , status): 
        self.__current_status = status 


    def _draw_status(self):
        h = SCREEN_HEIGHT
        Graphics.draw_text(f"Status : {self.__current_status}" , 20 , SCREEN_HEIGHT - 10  , 15) 
        

    def _draw_side_layers_info(self):
        font = pygame.font.SysFont("Arial", 13)
        win = Initializer.win 
        height = 180
        width = 85
        x_s, y_s = 0, SCREEN_HEIGHT - height

        pygame.draw.rect(win, colors.BEIGE_FILL_LAYER, [x_s, y_s, width, height])

        for i in range(len(layer_color_map)):
            text = font.render(f"METAL {i + 1}", False, colors.BLACK_CONTACT)
            w, h = text.get_size()
            win.blit(text, (x_s, y_s + 10 + i * h))
            small_r_w = SCREEN_WIDTH // ROWS
            pygame.draw.rect(
                win,
                layer_color_map[i],
                [x_s + max(w, 50), y_s + 15 + i * h, small_r_w, small_r_w],
            )

        text = font.render("VIA", False, colors.BLACK_CONTACT)
        w, h = text.get_size()

        y_cursor = y_s + 15 + len(layer_color_map) * h
        win.blit(text, (x_s, y_cursor - 5))
        small_r_w = SCREEN_WIDTH // ROWS
        pygame.draw.rect(
            win, colors.SILVER_VIA, [x_s + max(w, 50), y_cursor, small_r_w, small_r_w]
        )

        y_cursor += h
        font = pygame.font.SysFont("Arial", 10)
        text = font.render("CONTACT", False, colors.BLACK_CONTACT)
        w, h = text.get_size()

        y_cursor = y_s + 45 + len(layer_color_map) * h
        win.blit(text, (x_s, y_cursor ))
        small_r_w = SCREEN_WIDTH // ROWS
        pygame.draw.rect(
            win, colors.BLACK_CONTACT, [x_s + max(w, 50), y_cursor, small_r_w, small_r_w]
        )

        y_cursor += h

        font = pygame.font.SysFont("Arial", 13)

        text = font.render(
            f"Current Layer : {self.__current_layer +1}", False, colors.BLACK_CONTACT
        )
        w, h = text.get_size()

        win.blit(text, (x_s, y_cursor + 5))        