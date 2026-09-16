from mazegenerator import MazeGenerator


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL = 15

DIRECTIONS = {"N": (NORTH, 0, -1),
              "E": (EAST, 1, 0),
              "S": (SOUTH, 0, 1),
              "W": (WEST, -1, 0)}


class MazeError(Exception):

    pass


class Maze:
    def __init__(self, size: tuple[int, int], seed: int, perfect: bool = False
                 ) -> None:
        width, height = size
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positve")
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.generate()

    def generate(self) -> None:
        try:
            self.generator = MazeGenerator(
                    size=(self.width, self.height),
                    perfect=self.perfect, seed=self.seed
                    )

        except Exception:
            raise MazeError("Maze generation failed")

        self.grid = self.generator.maze
        self.entry = self.generator.maze_entry
        self.exit = self.generator.maze_exit

    def can_move(self, x: int, y: int, direction: str) -> bool:
        wall, dx, dy = DIRECTIONS[direction]
        cell = self.grid[y][x]
        if cell & wall:
            return False
        new_x = x + dx
        new_y = y + dy
        if not (0 <= new_x < self.width):
            return False
        if not (0 <= new_y < self.height):
            return False
        if self.is_blocked(new_x, new_y):
            return False
        return True

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return passable neighbors of a cell.

        Args:
            x: Column index of the cell.
            y: Row index of the cell.
        Returns:
            A list of (x, y) coordinates of reachable neighboring cells.
        """
        result = []
        for direction, (wall, dx, dy) in DIRECTIONS.items():
            new_x, new_y = x + dx, y + dy
            if self.can_move(x, y, direction):
                result.append((new_x, new_y))
        return result

    def is_blocked(self, x: int, y: int) -> bool:
        return self.grid[y][x] == ALL
