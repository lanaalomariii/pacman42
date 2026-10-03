from .maze import Maze, DIRECTIONS
from enum import Enum
import time
import random


OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}


class GhostState(Enum):
    """Possible states of a ghost"""
    NORMAL = "normal"  # chase player
    EDIBLE = "edible"  # move away from player
    RESPAWNING = "respawning"  # return to start position


class GhostType(Enum):
    """Types of ghosts"""
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class Ghost:
    """Represent a ghost character"""
    def __init__(self, maze: Maze, start: tuple[int, int],
                 ghost_type: GhostType) -> None:
        """Initialize the ghost
        Args:
            maze: Maze where the ghost moves
            start: starting position as (x, y)
            ghost_type: type of the ghost
        """
        self.maze = maze
        self.start_x, self.start_y = start
        self.x = self.start_x
        self.y = self.start_y
        self.direction = "N"
        self.state = GhostState.NORMAL
        self.ghost_type = ghost_type
        self.respawn_time = 0.0
        self.edible_until = 0.0

    def move(self, direction: str) -> bool:
        """Move the ghost if the requested direction is possible
        Args:
            direction: N, E, S, W
        Returns:
            True if the ghost moved, otherwise False
        """
        if not self.maze.can_move(self.x, self.y, direction):
            return False
        self.x, self.y = self.maze.get_next_position(
                self.x, self.y, direction)
        self.direction = direction
        return True

    def respawn(self) -> None:
        """Move the ghost back to its starting position"""
        self.x = self.start_x
        self.y = self.start_y

    def compute_distance(self, position: tuple[int, int],
                         target: tuple[int, int]) -> int:
        """Compute the manhattan distance between two positions
        Args:
            position: position as (x, y)
            target: Target position as (x, y)
        Returns:
            The manhattan distance between the positions
        """
        position_x, position_y = position
        target_x, target_y = target
        return abs(position_x - target_x) + abs(position_y - target_y)

    def get_directions(self) -> list[str]:
        """Returns a list of directions available that can be used"""

        return [d for d in DIRECTIONS if self.maze.can_move(self.x, self.y, d)]

    def choose_direction(self, target: tuple[int, int]) -> str | None:
        """Choose the direction that gets the ghost closest to the target
        Args:
            target: target position as (x, y)
        Returns:
            the direction with the minimum distance
            or None if no move is possible"""
        directions = self.get_directions()
        if not directions:
            return None
        directions = [d for d in directions if d !=
                      OPPOSITE.get(self.direction)] or directions
        dicpos: dict[str, int] = {}
        for d in directions:
            new_position = self.maze.get_next_position(self.x, self.y, d)
            dicpos[d] = self.compute_distance(new_position, target)
        best_direction, _ = min(dicpos.items(), key=lambda item: item[1])
        return best_direction

    def choose_farthest_direction(self, target: tuple[int, int]) -> str | None:
        """Choose the direction that gets the ghost farthest to the target
        Args:
            target: target position as (x, y)
        Returns:
            the direction with the maximum distance
            or None if no move is possible"""
        dicpos: dict[str, int] = {}
        directions = self.get_directions()
        if not directions:
            return None
        for d in directions:
            new_position = self.maze.get_next_position(self.x, self.y, d)
            dicpos[d] = self.compute_distance(new_position, target)
        best_direction, _ = max(dicpos.items(), key=lambda item: item[1])
        return best_direction

    def chase(self, target: tuple[int, int]) -> None:
        """Move the ghost towards the target
        Args:
            target: target position as (x, y)
        """
        direction = self.choose_direction(target)
        if direction is not None:
            self.move(direction)

    def edible(self, target: tuple[int, int]) -> None:
        """Move the ghost away from the target
        Args:
            target: target position as (x, y)
            """
        direction = self.choose_farthest_direction(target)
        if direction is not None:
            self.move(direction)

    def eaten(self) -> None:
        """set ghost as respawning after being eaten"""
        self.state = GhostState.RESPAWNING
        self.respawn_time = time.time() + 5

    def update_respawn(self, position: tuple[int, int]) -> None:
        """respawn the ghost after waiting time"""
        if self.state == GhostState.RESPAWNING:
            if time.time() >= self.respawn_time:
                self.respawn()
                if time.time() < self.edible_until:
                    self.state = GhostState.EDIBLE
                else:
                    self.state = GhostState.NORMAL
                self.chase(position)

    def set_edible(self) -> None:
        """set a ghost as edible"""
        if self.state != GhostState.RESPAWNING:
            self.state = GhostState.EDIBLE
            self.edible_until = time.time() + 8

    def update_edible(self) -> None:
        """Return the ghost to normal state when edible duration ends"""
        if self.state == GhostState.EDIBLE:
            if time.time() >= self.edible_until:
                self.state = GhostState.NORMAL

    def get_target_position(self, player_position: tuple[int, int],
                            player_direction: str,
                            moves: int = 4) -> tuple[int, int]:
        """Calculate a target position ahead of the player
        Args:
            player_position: the player's current position
            player_direction: the player's current direction
            moves: number of cells to move ahead of the player
        Returns:
            the calculated position ahead of the player
        """
        d, dx, dy = DIRECTIONS[player_direction]  # PINKY
        x, y = player_position
        new = (x + dx * moves, y + dy * moves)
        return new

    def choose_random_direction(self) -> str | None:
        """Choose a random direction from the available
        Returns:
            A random valid direction or None if the gost has no where to go
        """
        directions = self.get_directions()  # INKY
        if not directions:
            return None
        return random.choice(directions)

    def move_normal(self, player_position: tuple[int, int],
                    player_direction: str) -> None:
        """Movement logic when the ghost is in NORMAL state
            Args:
                player_position: the player's current position
                player_direction: the player's current direction
            """
        if self.ghost_type == GhostType.PINKY:
            target = self.get_target_position(
                    player_position, player_direction)
            self.chase(target)
        elif self.ghost_type == GhostType.INKY:
            directions = self.get_directions()
            if len(directions) > 1:
                if random.random() < 0.4:
                    direction = self.choose_random_direction()
                    if direction is not None:
                        self.move(direction)
                else:
                    self.chase(player_position)
            elif len(directions) == 1:
                self.move(directions[0])
        elif self.ghost_type == GhostType.CLYDE:
            distance = self.compute_distance((self.x, self.y), player_position)
            if distance > 8:
                self.chase(player_position)
            else:
                self.chase((self.start_x, self.start_y))

        else:
            self.chase(player_position)

    def move_ghost(self, player_position: tuple[int, int],
                   player_direction: str) -> None:
        """Choose the ghost movement based on its current state
            Args:
                player_position: the player's current position
                player_direction: the player's current direction
        """
        if self.state == GhostState.NORMAL:
            self.move_normal(player_position, player_direction)
        elif self.state == GhostState.EDIBLE:
            self.update_edible()
            if self.state == GhostState.EDIBLE:
                self.edible(player_position)
        elif self.state == GhostState.RESPAWNING:
            self.update_respawn(player_position)
