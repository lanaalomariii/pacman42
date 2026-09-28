import time
from .pacgum_manager import PacgumManager
from .maze import Maze

class LevelManager:
    def __init__(self, levels: list[dict], pacgum_count: int, level_max_time: float) -> None:
        """Initialize the level manage
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
        configs = self.get_current_level_configs()
        height = configs["height"]
        width = configs["width"]
        seed = configs["seed"]
        return Maze((width, height), seed)

    def has_next_level(self) -> bool:
        return self.current_level + 1 < len(self.levels)
    def next_level(self) -> bool:
        if not self.has_next_level():
            return False
        self.current_level += 1
        self.maze = self.build_maze_level()
        self.items = PacgumManager(self.maze, self.pacgum_count)
        self.start_time = time.time()
        return True

    def time_remaining(self) -> float:
        elapsed = time.time() - self.start_time
        return max(0.0, self.level_max_time - elapsed)
    def is_level_complete(self) -> bool:
        return not self.items.pacgums
    def is_won(self) -> bool:
        return self.is_level_complete() and not self.has_next_level()
    def player_start_position(self) -> tuple[int, int]:
        return (self.maze.width // 2, self.maze.height // 2)
    def ghost_start_positions(self) -> list[tuple[int, int]]:
        return self.maze.get_corner_positions()
