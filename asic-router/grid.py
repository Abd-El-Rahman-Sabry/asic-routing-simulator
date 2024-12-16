from drawable import Drawable
from tile import Tile, LayerOrientation, TileState, TileType, Layer
from config import ROWS, WIDTH, LAYERS

class Grid(Drawable):
    """
    Represents a grid structure composed of multiple layers of tiles.

    Attributes:
        _grid (list[list[list[Tile]]]): The 3D grid containing layers of tiles.
    """

    def __init__(self):
        """
        Initializes a Grid object.
        """
        self._grid: list[list[list[Tile]]] = []

    def build_grid(self):
        """
        Builds the grid structure. Must be implemented in subclasses.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def update_tile_neighbors(self, tile):
        """
        Updates the neighbors of a given tile. Must be implemented in subclasses.

        Args:
            tile (Tile): The tile whose neighbors are to be updated.

        Raises:
            NotImplementedError: If not implemented in a subclass.
        """
        raise NotImplementedError

    def layers(self):
        """
        Returns the grid layers.

        Returns:
            list[list[list[Tile]]]: The grid layers.
        """
        return self._grid

    def idlize_tiles(self):
        """
        Sets tiles in the grid to an idle state if they are open or closed.
        """
        for grid_layer in self._grid:
            for row in grid_layer:
                for tile in row:
                    if tile.state == TileState.closed or tile.state == TileState.open:
                        tile.set_idle_state()


    def draw(self):
        """
        Draws all tiles in the grid.
        """
        for grid_layer in self._grid:
            for row in grid_layer:
                for tile in row:
                    tile.draw()


class CrossGrid(Grid):
    """
    Represents a cross-layer grid structure with specific layer orientations.
    """

    def __init__(self):
        """
        Initializes a CrossGrid object and builds the grid structure.
        """
        super().__init__()
        self.build_grid()

    def build_grid(self):
        """
        Builds the cross-layer grid with specific dimensions and tile types.
        """
        tile_width = WIDTH
        layers = self.build_cross_grid_layers(LAYERS)

        for layer in layers:
            grid_layer = []

            for i in range(ROWS):
                grid_layer.append([])

                for j in range(ROWS):
                    tile = Tile(i, j, layer, tile_width, TileType.metal)
                    grid_layer[i].append(tile)

            self._grid.append(grid_layer)

    def build_cross_grid_layers(
        self, count, initial_orientation=LayerOrientation.horizontal
    ) -> list[Layer]:
        """
        Creates a list of layers with alternating orientations.

        Args:
            count (int): The number of layers to create.
            initial_orientation (LayerOrientation): The orientation of the first layer.

        Returns:
            list[Layer]: A list of layers with alternating orientations.
        """
        layers: list[Layer] = []

        for i in range(count + 1):
            if i % 2 == initial_orientation.value:
                layers.append(Layer(i, LayerOrientation.horizontal))
            else:
                layers.append(Layer(i, LayerOrientation.vertical))

        return layers

    def update_tile_neighbors(self, tile: Tile):
        """
        Updates the neighbors of a given tile based on its position and orientation.

        Args:
            tile (Tile): The tile whose neighbors are to be updated.
        """
        tile.clear_neighbors()

        row, col, index = tile.get_position()

        # Same Layer
        step = 1

        if tile.layer.orientation == LayerOrientation.horizontal:

            # EAST
            if col < ROWS - step and not (
                self._grid[index][row][col + step].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row][col + step]
                )
            # WEST
            if col > step and not (
                self._grid[index][row][col - step].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row][col - step]
                )

        elif tile.layer.orientation == LayerOrientation.vertical:

            # South
            if row < ROWS - step and not (
                self._grid[index][row + step][col].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row + step][col]
                )
            # North
            if row > step and not (
                self._grid[index][row - step][col].state
                == TileState.barrier
            ):
                tile.neighbors.append(
                    self._grid[index][row - step][col]
                )

        # Different Layer

        # Up
        if index < LAYERS and not (
            self._grid[index + 1][row][col].state
            == TileState.barrier
        ):
            tile.neighbors.append(
                self._grid[index + 1][row][col]
            )
        # Down
        if index > 0 and not (
            self._grid[index - 1][row][col].state
            == TileState.barrier
        ):
            tile.neighbors.append(
                self._grid[index - 1][row][col]
            )
