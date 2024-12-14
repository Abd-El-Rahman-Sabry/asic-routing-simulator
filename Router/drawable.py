import colors
import pygame
from initializer import Initializer


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
        pygame.draw.rect(
            Initializer.win, self.color, (self.x, self.y, self.width, self.height), border_radius=0
        )
