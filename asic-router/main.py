import colors
import pygame 
from enum import Enum

from visualizer import *
from queue import PriorityQueue


router = RouterMainWindow()

ROWS = 50
LAYERS = 4

WIDTH = SCREEN_WIDTH // ROWS

CELL_HEIGTH = 1

CELL_MIN_WIDTH = 1
CELL_MAX_WIDTH = 2


layer_color_map = [
    colors.BLUE_NWELL,
    colors.DARK_GREEN,
    colors.MAGENTA_METAL2,
    colors.CYAN_METAL3,
    colors.GREEN_METAL4,
]


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
            WIN, self.color, (self.x, self.y, self.width, self.height), border_radius=0
        )


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


class Cell(Drawable):

    def __init__(self, x, y, width, height) -> None:
        super().__init__(x, y, width, height)


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

    def update_neighbors(self, grid):
        self.__neighbors.clear()

        # Same Layer
        step = 1

        if self.__layer.orientation == LayerOrientation.horizontal:

            # EAST
            if self.__col < ROWS - step and not (
                grid[self.__layer.index][self.__row][self.__col + step].state
                == TileState.barrier
            ):
                self.__neighbors.append(
                    grid[self.__layer.index][self.__row][self.__col + step]
                )
            # WEST
            if self.__col > step and not (
                grid[self.__layer.index][self.__row][self.__col - step].state
                == TileState.barrier
            ):
                self.__neighbors.append(
                    grid[self.__layer.index][self.__row][self.__col - step]
                )

        elif self.__layer.orientation == LayerOrientation.vertical:

            # South
            if self.__row < ROWS - step and not (
                grid[self.__layer.index][self.__row + step][self.__col].state
                == TileState.barrier
            ):
                self.__neighbors.append(
                    grid[self.__layer.index][self.__row + step][self.__col]
                )
            # North
            if self.__row > step and not (
                grid[self.__layer.index][self.__row - step][self.__col].state
                == TileState.barrier
            ):
                self.__neighbors.append(
                    grid[self.__layer.index][self.__row - step][self.__col]
                )

        # Different Layer

        # Up
        if self.__layer.index < LAYERS and not (
            grid[self.__layer.index + 1][self.__row][self.__col].state
            == TileState.barrier
        ):
            self.__neighbors.append(
                grid[self.__layer.index + 1][self.__row][self.__col]
            )
        # Down
        if self.__layer.index > 0 and not (
            grid[self.__layer.index - 1][self.__row][self.__col].state
            == TileState.barrier
        ):
            self.__neighbors.append(
                grid[self.__layer.index - 1][self.__row][self.__col]
            )

    def reset(self):
        self.__state = TileState.idle


def h(p0: tuple[float, float, float], p1: tuple[float, float, float]) -> float:
    x0, y0, z0 = p0
    x1, y1, z1 = p1

    return abs(x0 - x1) + abs(y0 - y1) + abs(z0 - z1)


def get_clicked_tile(pos, rows, width) -> tuple[int, int]:
    gap = width // rows

    x, y = pos

    col = y // gap
    row = x // gap

    return row % rows, col % rows


def build_cross_grid_layers(
    count, initial_orientation=LayerOrientation.horizontal
) -> list[Layer]:
    layers: list[Layer] = []

    for i in range(count + 1):
        if i % 2 == initial_orientation.value:
            layers.append(Layer(i, LayerOrientation.horizontal))
        else:
            layers.append(Layer(i, LayerOrientation.vertical))

    print([l.orientation for l in layers])

    return layers


def make_grid(rows, width, layers_count=0) -> list[list[list[Tile]]]:

    grid: list[list[list[Tile]]] = []

    tile_width = width // rows

    layers = build_cross_grid_layers(layers_count)

    for layer in layers:

        grid_layer = []

        for i in range(rows):

            grid_layer.append([])

            for j in range(rows):
                tile = Tile(i, j, layer, tile_width, TileType.metal)
                grid_layer[i].append(tile)

        grid.append(grid_layer)

    return grid


def reconstruct_path(came_from, current, update_function) -> list[Tile]:

    path = [current]
    current.type = TileType.contact
    prev = current

    while current in came_from:
        current = came_from[current]

        if prev.layer.index != current.layer.index:
            prev.type = TileType.via
            current.type = TileType.via

        prev = current
        path.append(current)
        update_function()

    path[-1].type = TileType.contact

    return path


def idlize_tiles(grid: list[list[list[Tile]]]):

    for grid_layer in grid:
        for row in grid_layer:
            for tile in row:
                if tile.state == TileState.closed or tile.state == TileState.open:
                    tile.set_idle_state()


def a_star_router(
    grid: list[list[Tile]], start: Tile, end: Tile, update_function
) -> list[Tile]:
    count = 0
    open_set = PriorityQueue()
    came_from = {}

    g_score = {
        tile: float("inf") for grid_layer in grid for row in grid_layer for tile in row
    }
    g_score[start] = 0

    f_score = {
        tile: float("inf") for grid_layer in grid for row in grid_layer for tile in row
    }
    f_score[start] = h(start.get_position(), end.get_position())
    open_set.put((f_score[start], count, start))

    visited = {start}

    while not open_set.empty():

        current: Tile = open_set.get()[2]
        visited.remove(current)

        if current == end:
            idlize_tiles(grid)
            path = reconstruct_path(came_from, current, update_function)
            start.type = TileType.contact
            end.type = TileType.contact
            print("Done")
            return path

        for n in current.neighbors:

            current_g_score = g_score[current] + 1

            if current_g_score < g_score[n]:
                came_from[n] = current
                g_score[n] = current_g_score
                f_score[n] = current_g_score + h(n.get_position(), end.get_position())

                if n not in visited:
                    count += 1
                    open_set.put((f_score[n], count, n))
                    visited.add(n)
                    n.set_open_state()

        update_function()

        if current != start:
            current.set_closed_state()

    return []


def draw_random_cell(grid):

    for m in range(100):

        x_l, y_l = len(grid[0]), len(grid[0])
        x = np.random.randint(0, x_l - CELL_MAX_WIDTH)
        y = np.random.randint(0, y_l - CELL_HEIGTH)

        w = np.random.randint(CELL_MIN_WIDTH, CELL_MAX_WIDTH)

        x -= x % CELL_MAX_WIDTH
        y -= y % CELL_HEIGTH
        s = x
        e = s + w

        print(s, e)
        cell_layer = grid[0]

        for i in range(s, e):
            for j in range(y, y + CELL_HEIGTH):
                cell_layer[i][j].padding = 0
                cell_layer[i][j].color = colors.BLACK_CONTACT
                cell_layer[i][j].set_barrier_state()


def drawer(grid, current_layer):
    WIN.fill(colors.WHITE)
    for grid_layer in grid:
        for row in grid_layer:
            for tile in row:
                tile.draw()
    # router.draw_grid(ROWS * 2 , SCREEN_WIDTH , color=colors.GOLDENROD)
    router.draw_grid(ROWS // CELL_HEIGTH, SCREEN_WIDTH)
    draw_ui(current_layer)

    pygame.display.update()


def draw_ui(current_layer):
    font = pygame.font.SysFont("Arial", 13)

    height = 150
    width = 0.8 * height
    x_s, y_s = 0, SCREEN_HEIGHT - height

    pygame.draw.rect(WIN, colors.BEIGE_FILL_LAYER, [x_s, y_s, width, height])

    for i in range(len(layer_color_map)):
        text = font.render(f"METAL {i + 1}", False, colors.BLACK_CONTACT)
        w, h = text.get_size()
        WIN.blit(text, (x_s, y_s + 10 + i * h))
        small_r_w = SCREEN_WIDTH // ROWS
        pygame.draw.rect(
            WIN,
            layer_color_map[i],
            [x_s + max(w, 50), y_s + 15 + i * h, small_r_w, small_r_w],
        )

    text = font.render(f"VIA", False, colors.BLACK_CONTACT)
    w, h = text.get_size()

    y_cursor = y_s + 15 + len(layer_color_map) * h
    WIN.blit(text, (x_s, y_cursor - 5))
    small_r_w = SCREEN_WIDTH // ROWS
    pygame.draw.rect(
        WIN, colors.SILVER_VIA, [x_s + max(w, 50), y_cursor, small_r_w, small_r_w]
    )

    y_cursor += h

    text = font.render(
        f"Current Layer : {current_layer+1}", False, colors.BLACK_CONTACT
    )
    w, h = text.get_size()

    WIN.blit(text, (x_s, y_cursor + 5))


def main():
    pygame.font.init()

    grid = make_grid(ROWS, SCREEN_WIDTH, LAYERS)

    start = None
    end = None

    running = True

    current_layer = 0

    # draw_random_cell(grid)
    while running:

        drawer(grid, current_layer)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                r, c = get_clicked_tile(pos, ROWS, SCREEN_WIDTH)
                clicked_tile = grid[current_layer][r][c]

                if start is None:
                    clicked_tile.color = colors.RED
                    start = clicked_tile

                elif end is None and start is not None:
                    clicked_tile.color = colors.BLUE
                    end = [clicked_tile]

                else:
                    clicked_tile.color = colors.BLUE
                    end.append(clicked_tile)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_layer += 1
                    current_layer = min(LAYERS, current_layer)
                    draw_ui(current_layer)
                if event.key == pygame.K_DOWN:
                    current_layer -= 1
                    current_layer = max(1, current_layer)
                    draw_ui(current_layer)

                if event.key == pygame.K_SPACE:

                    if start is not None and end is not None:
                        for grid_layer in grid:
                            for row in grid_layer:
                                for tile in row:
                                    tile.update_neighbors(grid)

                        paths = []

                        for e in end:
                            p = a_star_router(
                                grid, start, e, lambda: drawer(grid, current_layer)
                            )
                            paths += p

                        paths = list(set(paths))
 
                        for p in paths:
                            p.state = TileState.barrier
                            p.make_path()

                        start = None
                        end = None

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
