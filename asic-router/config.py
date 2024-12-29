import colors

# Cost for transitioning between layers
VIA_COST = 2


# Heuristic function for A*

def heuristic(p0: tuple[float, float, float], p1: tuple[float, float, float]) -> float:
    """
    Heuristic function for A*.

    Args:
        p0 (tuple[float, float, float]): Start coordinates.
        p1 (tuple[float, float, float]): End coordinates.

    Returns:
        float: The heuristic value.
    """
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    return abs(x0 - x1) + abs(y0 - y1) +  VIA_COST *abs(z0 - z1) 


# Window Settings
SCREEN_WIDTH = 600  # Width of the application window
SCREEN_HEIGHT = 600  # Height of the application window

ROWS = 30  # Number of rows in the grid
WIDTH = SCREEN_WIDTH // ROWS  # Width of each cell in the grid

TITLE = "Router"  # Title of the application window

GRID_COLOR = (126, 126, 126)  # Color of the grid lines

LAYERS = 5  # Number of layers in the grid

# Cell Settings
CELL_HEIGTH = 1  # Height of each cell
CELL_MIN_WIDTH = 1  # Minimum width of each cell
CELL_MAX_WIDTH = 2  # Maximum width of each cell
PADDING = 6  # Padding between cells

# Layers Colors
LINE_WIDTH = 2  # Width of the lines in the grid

# Mapping of layer indices to colors
layer_color_map = [
    colors.BLUE_NWELL,
    colors.DARK_GREEN,
    colors.MAGENTA_METAL2,
    colors.CYAN_METAL3,
    colors.GREEN_METAL4,
]
