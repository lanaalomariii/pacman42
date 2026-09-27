from enum import Enum
from .maze import Maze
import random


class PacgumType(Enum):
    PACGUM = "pacgum"
    SUPER_PACGUM = "super_pacgum"


class PacgumManager:
    def __init__(self, maze: Maze, pacgum_count: int) -> None:
        self.maze = maze
        self.pacgum_count = pacgum_count
        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()
        self.place_super_pacgums()
        self.place_pacgums()

    def get_corner_positions(self) -> list[tuple[int, int]]:
        return [(0, 0), (self.maze.width - 1, 0),
                (0, self.maze.height - 1),
                (self.maze.width - 1, self.maze.height - 1)]

    def place_super_pacgums(self) -> None:
        corners = self.get_corner_positions()
        for x, y in corners:
            if not self.maze.is_blocked(x, y):
                self.super_pacgums.add((x, y))

    def place_pacgums(self) -> None:
        available = []
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if (
                        not self.maze.is_blocked(x, y)
                        and (x, y) not in self.super_pacgums
                        ):
                    available.append((x, y))
        random.shuffle(available)
        self.pacgums = set(available[:self.pacgum_count])

    def collect(self, position: tuple[int, int]) -> PacgumType | None:
        if position in self.pacgums:
            self.pacgums.remove(position)
            return PacgumType.PACGUM
        if position in self.super_pacgums:
            self.super_pacgums.remove(position)
            return PacgumType.SUPER_PACGUM
        return None

    def all_collected(self) -> bool:
        return not self.pacgums and not self.super_pacgums
