import colors
import pygame
from initializer import Initializer

class Drawable:

    def __init__(self, x, y, width, height) -> None:
        self.__x: float = x
        self.__y: float = y
        self.__width: float = width
        self.__height: float = height
        self.__color: tuple[int, int, int] = colors.WHITE

    @property
    def color(
        self,
    ):
        return self.__color

    @color.setter
    def color(self, new_color: tuple[int, int, int]) -> None:
        self.__color = new_color

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val):

        self.__y = val

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, val):
        self.__width = val

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, val):
        self.__height = val

    def draw(self):

        pygame.draw.rect(
            Initializer.win, self.color, (self.x, self.y, self.width, self.height), border_radius=0
        )
