from game.player import Player
from game.levels import LevelManager
from game.ghost import Ghost, GhostState, GhostType
from .pacgum_manager import PacgumManager, PacgumType
from .score import Score

GHOST_TYPE = [GhostType.BLINKY, GhostType.PINKY, GhostType.INKY, GhostType.CLYDE]

class Game:
    def __init__(self, levels: list[dict], pacgum_count: int, level_max_time: float, lives: int, points_per_pacgum: int, points_per_super_pacgum: int, points_per_ghost: int) -> None:
        self.score = Score(points_per_pacgum, points_per_super_pacgum, points_per_ghost)
        self.level_manager = LevelManager(levels, pacgum_count, level_max_time)
        self.items = self.level_manager.items
        self.player = Player(self.level_manager.maze, self.level_manager.player_start_position(), lives)
        self.ghosts = self.create_ghosts()
        # cheat mode
        self.cheat_invincibility = False
        self.ghost_freeze = False

    def create_ghosts(self) -> list[Ghost]:
        positions = self.level_manager.ghost_start_positions()
        return [
                Ghost(self.level_manager.maze, positions[0], GhostType.BLINKY),
                Ghost(self.level_manager.maze, positions[1], GhostType.PINKY),
                Ghost(self.level_manager.maze, positions[2], GhostType.INKY),
                Ghost(self.level_manager.maze, positions[3], GhostType.CLYDE)
                ]
    def enter_level(self) -> None:
        self.player.maze = self.level_manager.maze
        start = self.level_manager.player_start_position()
        self.player.start_x, self.player.start_y = start
        self.player.respawn()
        self.player.direction = "N"
        self.ghosts = self.create_ghosts()

