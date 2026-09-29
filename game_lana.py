from game.player import Player
from game.levels import LevelManager
from game.ghost import Ghost, GhostState, GhostType
from .pacgum_manager import PacgumManager, PacgumType
from .score import Score


class Game:
    def __init__(self, levels: list[dict], pacgum_count: int, level_max_time: float, lives: int, points_per_pacgum: int, points_per_super_pacgum: int, points_per_ghost: int) -> None:
        self.score = Score(points_per_pacgum, points_per_super_pacgum, points_per_ghost)
        self.level_manager = LevelManager(levels, pacgum_count, level_max_time)
        self.items = self.level_manager.items
        self.player = Player(self.level_manager.maze, self.level_manager.player_start_position(), lives)
        self.ghosts = self.create_ghosts()
        # cheat mode
        self.cheat_invincibility = False
        self.cheat_ghost_freeze = False

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
        self.items = self.level_manager.items
    
    def item_collection(self) -> None:
        collected_item = self.level_manager.items.collect((self.player.x, self.player.y))
        if collected_item == PacgumType.PACGUM:
            self.score.add_pacgum()
        elif collected_item == PacgumType.SUPER_PACGUM:
            self.score.add_super_pacgum()
            for ghost in self.ghosts:
                ghost.set_edible()


    def ghost_touch(self) -> None:
        for ghost in self.ghosts:
            if (ghost.x, ghost.y) != (self.player.x, self.player.y):
                continue
            if ghost.state == GhostState.EDIBLE:
                ghost.eaten()
                self.score.add_ghost()
            elif ghost.state == GhostState.NORMAL:
                if not self.cheat_invincibility:
                    self.player.lose_life()

    def skip_level(self) -> None:
        if not self.level_manager.next_level():  # last level so mark its as complete
            self.level_manager.items.pacgums.clear()
            self.level_manager.items.super_pacgums.clear()
        else:
            self.enter_level()
    def add_extra_life(self) -> None:
        self.player.lives += 1
