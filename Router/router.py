class Router:

    def __init__(self, grid):
        self.__grid = grid

    def route(self, start, end):
        return NotImplementedError

    def run(self, start, ends: list[object]):
        return NotImplementedError
