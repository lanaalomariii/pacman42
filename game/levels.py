import time
import random
from .pacgum_manager import PacgumManager
from .maze import Maze


class LevelManager:
    """Manage progression through the levels"""
    def __init__(self, levels: list[dict], pacgum_count: int,
                 level_max_time: float) -> None:
        """Initialize the level manager
        Args:
            levels: list of level configs, each with width,height,seed
            pacgum_count: number of pacgums per level
            level_max_time: time limit per level in seconds
        """
        self.levels = levels
        self.pacgum_count = pacgum_count
        self.level_max_time = level_max_time
        self.current_level = 0
        self.maze = self.build_maze_level()
        self.items = PacgumManager(self.maze, self.pacgum_count)
        self.start_time = time.time()

    def get_current_level_configs(self) -> dict[str, int]:
        """Return the configuration of current level"""
        return self.levels[self.current_level]

    def build_maze_level(self) -> Maze:
        """Build the maze for a level
        Returns:
            a new maze built from that level's config
        """
        configs = self.get_current_level_configs()
        height = configs["height"]
        width = configs["width"]
        if self.current_level == 0:
            seed = configs["seed"]
        else:
            seed = random.randint(0, 10000)
        return Maze((width, height), seed)

    def has_next_level(self) -> bool:
        """Check whether there is a level after the current one"""
        return self.current_level + 1 < len(self.levels)

    def next_level(self) -> bool:
        """Move to the next level if exists
        Rebuilds the maze and items for the new level
        Returns:
            True if a next level was loaded, False if no level remained"""
        if not self.has_next_level():
            return False
        self.current_level += 1
        self.maze = self.build_maze_level()
        self.items = PacgumManager(self.maze, self.pacgum_count)
        self.start_time = time.time()
        return True

    def time_remaining(self) -> float:
        """Return the number of seconds remaining
        before the current level times out"""
        elapsed = time.time() - self.start_time
        return max(0.0, self.level_max_time - elapsed)

    def is_level_complete(self) -> bool:
        """Check whether all pacgums in the current level are collected"""
        return self.items.all_collected()

    def is_won(self) -> bool:
        """Check whether the player finished the final level
        Return True if the current level is the last one and it is completed"""
        return self.is_level_complete() and not self.has_next_level()

    def player_start_position(self) -> tuple[int, int]:
        """Return a valid starting position center of the maze.
        If the center cell is blocked move right until an open cell is found"""
        x = self.maze.width // 2
        y = self.maze.height // 2
        while self.maze.is_blocked(x, y) and x < self.maze.width - 1:
            x += 1
        return (x, y)

    def ghost_start_positions(self) -> list[tuple[int, int]]:
        """Return the starting positions for four ghosts"""
        return self.maze.get_corner_positions()
