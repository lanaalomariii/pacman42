from game.player import Player
from game.levels import LevelManager
from game.ghost import Ghost, GhostState, GhostType
from game.pacgum_manager import PacgumType
from game.score import Score


class Game:
    """Manage the game logic"""
    def __init__(self, levels: list[dict], pacgum_count: int,
                 level_max_time: float, lives: int,
                 points_per_pacgum: int,
                 points_per_super_pacgum: int,
                 points_per_ghost: int) -> None:
        """Initialize the game and its components
        Args:
            levels: list of level configs, each with width, height, seed
            pacgum_count: Number of pacgums in the first level
            level_max_time: Maximum time allowed for each level
            lives: number of lives the player starts with
            points_per_pacgum: Points awarded for collecting a pacgum
            points_per_super_pacgum: Points awarded for collecting super-pacgum
            points_per_ghost: Points awarded for eating a ghost
        """
        self.score = Score(points_per_pacgum,
                           points_per_super_pacgum,
                           points_per_ghost)
        self.level_manager = LevelManager(levels, pacgum_count, level_max_time)
        self.player = Player(self.level_manager.maze,
                             self.level_manager.player_start_position(), lives)
        self.ghosts = self.create_ghosts()
        # cheat mode
        self.cheat_invincibility = False
        self.cheat_ghost_freeze = False

    def create_ghosts(self) -> list[Ghost]:
        """Create the four ghosts for the current level.
        Returns:
            A list of four ghosts (Blinky, Pinky, Inky, Clyde)
        """
        positions = self.level_manager.ghost_start_positions()
        return [
                Ghost(self.level_manager.maze, positions[0], GhostType.BLINKY),
                Ghost(self.level_manager.maze, positions[1], GhostType.PINKY),
                Ghost(self.level_manager.maze, positions[2], GhostType.INKY),
                Ghost(self.level_manager.maze, positions[3], GhostType.CLYDE)
                ]

    def enter_level(self) -> None:
        """Set up the player, ghosts and items for the new level"""
        self.player.maze = self.level_manager.maze
        start = self.level_manager.player_start_position()
        self.player.start_x, self.player.start_y = start
        self.player.respawn()
        self.player.direction = "N"
        self.ghosts = self.create_ghosts()

    def item_collection(self) -> None:
        """Check and apply pacgum or super-pacgum collection"""
        collected_item = self.level_manager.items.collect(
                (self.player.x, self.player.y))
        if collected_item == PacgumType.PACGUM:
            self.score.add_pacgum()
        elif collected_item == PacgumType.SUPER_PACGUM:
            self.score.add_super_pacgum()
            for ghost in self.ghosts:
                ghost.set_edible()

    def ghost_touch(self) -> None:
        """Check collisions between the player and each ghost"""
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
        """Skip to the next level or complete the last level"""
        if not self.level_manager.next_level():  # last level mark as complete
            self.level_manager.items.pacgums.clear()
            self.level_manager.items.super_pacgums.clear()
        else:
            self.enter_level()

    def add_extra_life(self) -> None:
        """Give the player one extra life"""
        self.player.lives += 1

    def move_player(self, direction: str) -> None:
        """Move the player in the given direction
        Args:
            direction: Direction of movement
            """
        self.player.move(direction)

    def move_ghosts(self) -> None:
        """Move every ghost unless the ghost freeze cheat is active"""
        if self.cheat_ghost_freeze:
            return
        for ghost in self.ghosts:
            ghost.move_ghost((self.player.x, self.player.y),
                             self.player.direction)

    def update(self, player_direction: str | None) -> str:
        """Update the game state.
        Args:
            player_direction: Direction requested by player.
        Returns:
            The current game status: "playing", "lost", "won" or "time is up".
        """
        if self.level_manager.time_remaining() <= 0:
            return "time is up"
        if player_direction is not None:
            self.move_player(player_direction)
        self.move_ghosts()
        self.item_collection()
        self.ghost_touch()
        if not self.player.is_alive():
            return "lost"
        if (
                self.level_manager.is_level_complete()
                and self.level_manager.has_next_level()
                ):
            self.level_manager.next_level()
            self.enter_level()
        elif self.level_manager.is_won():
            return "won"
        return "playing"
