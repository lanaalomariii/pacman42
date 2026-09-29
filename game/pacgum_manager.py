from enum import Enum
from .maze import Maze
import random
from collections import deque


class PacgumType(Enum):
    """Types of Pacgums"""
    PACGUM = "pacgum"
    SUPER_PACGUM = "super_pacgum"


class PacgumManager:
    """Manage pacgums and super-pacgums"""
    def __init__(self, maze: Maze, start: tuple[int, int],
                 pacgum_count: int = 42) -> None:
        """Initialize the pacgum manager
        Args:
            maze: the maze where pacgums will be placed
            start: the player's starting position
            pacgum_count: number of pacgums to place
        """
        self.maze = maze
        self.pacgum_count = pacgum_count
        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()
        self.reachable = self.get_reachable_cells(start)
        self.place_super_pacgums()
        self.place_pacgums()

    def get_reachable_cells(self, start: tuple[int, int]
                            ) -> set[tuple[int, int]]:
        """Return all cell reachable from the starting position"""
        reachable = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for n in self.maze.get_neighbors(x, y):
                if n not in reachable:
                    reachable.add(n)
                    queue.append(n)
        return reachable

    def place_super_pacgums(self) -> None:
        """Place super-pacgums on the 4 corners of the maze"""
        corners = self.maze.get_corner_positions()
        for x, y in corners:
            self.super_pacgums.add((x, y))

    def place_pacgums(self) -> None:
        """Place pacgums randomly on cells not used by super-pacgums"""
        available = []
        for c in self.reachable:
            if c not in self.super_pacgums:
                available.append(c)
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
