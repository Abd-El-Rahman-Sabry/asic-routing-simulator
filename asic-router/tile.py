from drawable import Drawable, DrawableShape
from enum import Enum
import colors
from config import PADDING, WIDTH, layer_color_map
from graphics import Graphics

class LayerOrientation(Enum):
    """
    Enum representing the orientation of a layer in the grid.

    Attributes:
        horizontal (int): Indicates a horizontal layer orientation.
        vertical (int): Indicates a vertical layer orientation.
        both (int): Indicates a layer that can route a net in both orientations horizontal and vertical.
    """
    horizontal = 0
    vertical = 1
    both = 2


class TileState(Enum):
    """
    Enum representing the various states a tile can have.

    Attributes:
        idle (int): Represents a tile in an idle state.
        closed (int): Represents a tile that is closed.
        open (int): Represents a tile that is open.
        barrier (int): Represents a tile that is a barrier.
        start (int): Represents a tile designated as the start of a route.
        end (int): Represents a tile designated as the end of a route.
    """
    idle = 0
    closed = 1
    open = 2
    barrier = 3
    start = 4
    end = 5


class TileType(Enum):
    """
    Enum representing the different types of tiles.

    Attributes:
        via (int): Represents a via tile.
        metal (int): Represents a metal tile.
        contact (int): Represents a contact tile.
    """
    via = 0
    metal = 1
    contact = 2


class Layer:
    """
    A class representing a layer in the grid.

    Attributes:
        index (int): The index of the layer.
        orientation (LayerOrientation): The orientation of the layer (horizontal/vertical).
    """

    def __init__(self, index, orientation) -> None:
        """
        Initializes the Layer with the given index and orientation.

        Args:
            index (int): The index of the layer.
            orientation (LayerOrientation): The orientation of the layer.
        """
        self.__index = index
        self.__orientation = orientation

    @property
    def index(self):
        """
        Returns the index of the layer.
        """
        return self.__index

    @property
    def orientation(self):
        """
        Returns the orientation of the layer.
        """
        return self.__orientation


class Tile(Drawable):
    """
    A class representing a tile in the grid, which is drawable and has specific states and types.

    Attributes:
        row (int): The row index of the tile.
        col (int): The column index of the tile.
        layer (Layer): The layer the tile belongs to.
        width (int): The width of the tile.
        type (TileType): The type of the tile (via, metal, contact).
        state (TileState): The current state of the tile (idle, open, closed, etc.).
        neighbors (list): A list of neighboring tiles.
    """

    def __init__(self, row, col, layer, width, type=TileType.metal, **kwargs) -> None:
        """
        Initializes the Tile with its position, layer, type, and other properties.

        Args:
            row (int): The row index of the tile.
            col (int): The column index of the tile.
            layer (Layer): The layer the tile belongs to.
            width (int): The width of the tile.
            type (TileType, optional): The type of the tile (default is metal).
            kwargs: Additional keyword arguments (e.g., padding).
        """
        self.__row = row
        self.__col = col
        self.__layer: Layer = layer
        self.__neighbors = []
        self.__state = TileState.idle
        self.__type = type
        self.__width = width
        super().__init__(row * width, col * width, width, width)
        self.__padding = kwargs.get("padding", 0)
        self.color = None

    def draw(self):
        """
        Draws the tile on the screen with appropriate styling based on its type and state.

        The drawing properties change depending on whether the tile is a via, contact, or metal.
        The tile's size and position are adjusted based on the layer's orientation.
        """
        padding = self.__padding
        self.height = WIDTH
        self.width = WIDTH
        self.y = self.__col * self.__width - padding
        self.x = self.__row * self.__width - padding
        
        # Adjustments based on tile type
        if self.__type == TileType.via:
            self.color = colors.SILVER_VIA
            self.height = WIDTH - 4
            self.width = WIDTH - 4
            self.y = self.__col * self.__width - padding + 2
            self.x = self.__row * self.__width - padding + 2

        elif self.__type == TileType.contact:
            self.color = colors.BLACK_CONTACT
            self.height = WIDTH - 4
            self.width = WIDTH - 4
            self.y = self.__col * self.__width - padding + 2
            self.x = self.__row * self.__width - padding + 2

        elif self.__type == TileType.metal:
            padding = PADDING
            if self.__layer.orientation == LayerOrientation.vertical:
                self.height = self.__width - 2 * padding
                self.y = self.__col * self.__width + padding
            elif self.__layer.orientation == LayerOrientation.horizontal:
                self.width = self.__width - 2 * padding
                self.x = self.__row * self.__width + padding

        # Draw the tile if it has a color
        if self.color is not None:
            if self.state == TileState.start: 
                Graphics.draw_text("Start" , self.x , self.y  - 10 , 14)
                self.shape = DrawableShape.circle 

            elif self.state == TileState.end: 
                Graphics.draw_text("End" , self.x , self.y  - 10 , 14)
                self.shape = DrawableShape.circle 
            else : 
                self.shape = DrawableShape.rect

            return super().draw()

    @property
    def type(self) -> TileType:
        """
        Returns the type of the tile.
        """
        return self.__type

    @type.setter
    def type(self, t: TileType) -> None:
        """
        Sets the type of the tile.

        Args:
            t (TileType): The new type of the tile.
        """
        self.__type = t

    @property
    def state(self) -> TileState:
        """
        Returns the current state of the tile.
        """
        return self.__state

    @state.setter
    def state(self, s: TileState) -> None:
        """
        Sets the state of the tile.

        Args:
            s (TileState): The new state of the tile.
        """
        self.__state = s

    @property
    def padding(self):
        """
        Returns the padding value for the tile.
        """
        return self.__padding

    @padding.setter
    def padding(self, s: int) -> None:
        """
        Sets the padding value for the tile.

        Args:
            s (int): The new padding value.
        """
        self.__padding = s

    @property
    def layer(self):
        """
        Returns the layer the tile belongs to.
        """
        return self.__layer

    @property
    def neighbors(self) -> list:
        """
        Returns the list of neighboring tiles.
        """
        return self.__neighbors

    @neighbors.setter
    def neighbors(self, s: list):
        """
        Sets the list of neighboring tiles.

        Args:
            s (list): The list of neighboring tiles.
        """
        self.__neighbors = s

    def clear_neighbors(self):
        """
        Clears the list of neighbors for the tile.
        """
        self.__neighbors.clear()

    def get_cordinates(self):
        """
        Returns the screen coordinates (x, y) of the tile.

        Returns:
            tuple: The (x, y) coordinates of the tile.
        """
        return self.x, self.y

    def get_position(self):
        """
        Returns the position of the tile in terms of row, column, and layer index.

        Returns:
            tuple: A tuple (row, col, layer_index) representing the tile's position.
        """
        return self.__row, self.__col, self.__layer.index

    def set_closed_state(self):
        """
        Sets the tile to the closed state and removes its color.
        """
        self.color = None
        self.__state = TileState.closed

    def set_idle_state(self):
        """
        Sets the tile to the idle state and removes its color.
        """
        self.color = None
        self.__state = TileState.idle

    def set_open_state(self):
        """
        Sets the tile to the open state and assigns it a green color.
        """
        self.color = colors.GREEN
        self.__state = TileState.open

    def set_start_state(self):
        """
        Sets the tile to the start state.
        """
        self.__state = TileState.start

    def set_barrier_state(self):
        """
        Sets the tile to the barrier state.
        """
        self.__state = TileState.barrier

    def set_end_state(self):
        """
        Sets the tile to the end state.
        """
        self.__state = TileState.end

    def make_path(self):
        """
        Sets the color of the tile to the color associated with its layer.
        """
        self.color = layer_color_map[self.__layer.index]



    def reset(self):
        """
        Resets the tile to its idle state.
        """
        self.__state = TileState.idle
