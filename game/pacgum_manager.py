from enum import Enum
from .maze import Maze
import random


class PacgumType(Enum):
    """Types of Pacgums"""
    PACGUM = "pacgum"
    SUPER_PACGUM = "super_pacgum"


class PacgumManager:
    """Manage pacgums and super-pacgums"""
    def __init__(self, maze: Maze, pacgum_count: int = 42) -> None:
        """Initialize the pacgum manager
        Args:
            maze: the maze where pacgums will be placed
            pacgum_count: number of pacgums to place
        """
        self.maze = maze
        self.pacgum_count = pacgum_count
        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()
        self.place_super_pacgums()
        self.place_pacgums()

    def place_super_pacgums(self) -> None:
        """Place super-pacgums on the 4 corners of the maze"""
        corners = self.maze.get_corner_positions()
        for x, y in corners:
            if not self.maze.is_blocked(x, y):
                self.super_pacgums.add((x, y))

    def place_pacgums(self) -> None:
        """Place pacgums randomly on cells not used by super-pacgums"""
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
        """Collect a pacgum at a given position if present
        Args:
            position: (x, y) to check
        Returns:
            Type of collected item or None"""
        if position in self.pacgums:
            self.pacgums.remove(position)
            return PacgumType.PACGUM
        if position in self.super_pacgums:
            self.super_pacgums.remove(position)
            return PacgumType.SUPER_PACGUM
        return None

    def all_collected(self) -> bool:
        """Returns whether all pacgums and super-pacgums are collected"""
        return not self.pacgums and not self.super_pacgums
