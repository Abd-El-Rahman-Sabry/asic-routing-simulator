import colors
import pygame
from initializer import Initializer
from enum import Enum

class DrawableShape(Enum): 
    rect    = 0
    circle  = 1 


class Drawable:
    """
    Represents a drawable object with a position, dimensions, and color.

    Attributes:
        x (float): The x-coordinate of the object.
        y (float): The y-coordinate of the object.
        width (float): The width of the object.
        height (float): The height of the object.
        color (tuple[int, int, int]): The color of the object, represented as an RGB tuple.
    """

    def __init__(self, x, y, width, height) -> None:
        """
        Initializes a Drawable object.

        Args:
            x (float): The x-coordinate of the object.
            y (float): The y-coordinate of the object.
            width (float): The width of the object.
            height (float): The height of the object.
        """
        self.__x: float = x
        self.__y: float = y
        self.__width: float = width
        self.__height: float = height
        self.__color: tuple[int, int, int] = colors.WHITE
        self.__shape = DrawableShape.rect

    @property
    def color(self):
        """
        Returns the current color of the object.

        Returns:
            tuple[int, int, int]: The RGB color of the object.
        """
        return self.__color

    @color.setter
    def color(self, new_color: tuple[int, int, int]) -> None:
        """
        Sets a new color for the object.

        Args:
            new_color (tuple[int, int, int]): The new RGB color.
        """
        self.__color = new_color

    @property
    def shape(self):
        """
        Returns the current shape of the object.

        Returns:
            DrawableShape: enum value of the shape to be drawn.
        """
        return self.__shape

    @shape.setter
    def shape(self, new_shape: DrawableShape) -> None:
        """
        Sets a new shape for the object.

        Args:
            new_color DrawbleShape: The new shape.
        """
        self.__shape = new_shape

    @property
    def x(self):
        """
        Returns the x-coordinate of the object.

        Returns:
            float: The x-coordinate.
        """
        return self.__x

    @x.setter
    def x(self, val):
        """
        Updates the x-coordinate of the object.

        Args:
            val (float): The new x-coordinate.
        """
        self.__x = val

    @property
    def y(self):
        """
        Returns the y-coordinate of the object.

        Returns:
            float: The y-coordinate.
        """
        return self.__y

    @y.setter
    def y(self, val):
        """
        Updates the y-coordinate of the object.

        Args:
            val (float): The new y-coordinate.
        """
        self.__y = val

    @property
    def width(self):
        """
        Returns the width of the object.

        Returns:
            float: The width.
        """
        return self.__width

    @width.setter
    def width(self, val):
        """
        Updates the width of the object.

        Args:
            val (float): The new width.
        """
        self.__width = val

    @property
    def height(self):
        """
        Returns the height of the object.

        Returns:
            float: The height.
        """
        return self.__height

    @height.setter
    def height(self, val):
        """
        Updates the height of the object.

        Args:
            val (float): The new height.
        """
        self.__height = val

    def draw(self):
        """
        Draws the object as a rectangle on the screen using Pygame.
        
        """
        if self.__shape == DrawableShape.rect:
            pygame.draw.rect(
                Initializer.win, self.color, (self.x, self.y, self.width, self.height), border_radius=0
            )

        elif self.__shape == DrawableShape.circle: 
            shift =8
            pygame.draw.circle(Initializer.win , self.color ,(self.x + shift - 1, self.y + shift + 2) , shift - 2)

        
