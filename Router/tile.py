from drawable import Drawable
from enum import Enum
import colors 
from config import WIDTH , layer_color_map

class LayerOrientation(Enum):
    horizontal = 0
    vertical = 1


class TileState(Enum):

    idle = 0
    closed = 1
    open = 2
    barrier = 3
    start = 4
    end = 5


class TileType(Enum):
    via = 0
    metal = 1
    contact = 2


class Layer:

    def __init__(self, index, orientation) -> None:
        self.__index = index
        self.__orientation = orientation

    @property
    def index(
        self,
    ):
        return self.__index

    @property
    def orientation(self):
        return self.__orientation




class Tile(Drawable):

    def __init__(self, row, col, layer, width, type=TileType.metal, **kwargs) -> None:
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

        padding = self.__padding
        self.height = WIDTH
        self.width = WIDTH
        self.y = self.__col * self.__width - padding
        self.x = self.__row * self.__width - padding
        
        if self.__type == TileType.via:
            self.color = colors.SILVER_VIA
            self.height = WIDTH - 4
            self.width = WIDTH - 4
            self.y = self.__col * self.__width - padding + 2
            self.x = self.__row * self.__width - padding + 2

        if self.__type == TileType.contact:
            self.color = colors.BLACK_CONTACT
            self.height = WIDTH - 4
            self.width = WIDTH - 4
            self.y = self.__col * self.__width - padding + 2
            self.x = self.__row * self.__width - padding + 2

        if self.__type == TileType.metal:
            padding = 4
            if self.__layer.orientation == LayerOrientation.vertical:

                self.height = self.__width - 2 * padding
                self.y = self.__col * self.__width + padding

            elif self.__layer.orientation == LayerOrientation.horizontal:

                self.width = self.__width - 2 * padding
                self.x = self.__row * self.__width + padding

        if self.color is not None:
            return super().draw()

    @property
    def type(self) -> TileType:
        return self.__type

    @type.setter
    def type(self, t: TileType) -> None:
        if t == TileType.metal:
            self.__padding = 4
        else:
            self.__padding = 0
        self.__type = t

    @property
    def state(self) -> TileState:
        return self.__state

    @state.setter
    def state(self, s: TileState) -> None:
        self.__state = s

    @property
    def padding(self):
        return self.__padding

    @padding.setter
    def padding(self, s: int) -> None:
        self.__padding = s

    @property
    def layer(
        self,
    ):
        return self.__layer

    @property
    def neighbors(self) -> list:
        return self.__neighbors

    @neighbors.setter
    def neighbors(self, s: list) -> None:
        self.__neighbors = s

    def clear_neighbors(self): 
        self.__neighbors.clear() 

    def get_cordinates(
        self,
    ):
        return self.x, self.y

    def get_position(self):
        return self.__row, self.__col, self.__layer.index

    def set_closed_state(self):
        self.color = None
        self.__state = TileState.closed

    def set_idle_state(self):
        self.color = None
        self.__state = TileState.idle

    def set_open_state(self):
        self.color = colors.GREEN
        self.__state = TileState.open

    def set_start_state(self):
        self.__state = TileState.start

    def set_barrier_state(self):
        self.__state = TileState.barrier

    def set_end_state(
        self,
    ):
        self.__state = TileState.end

    def make_path(self):
        self.color = layer_color_map[self.__layer.index]

    def __lt__(self, op):
        return False


    def reset(self):
        self.__state = TileState.idle