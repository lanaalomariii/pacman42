from .maze import Maze, DIRECTIONS
from enum import Enum


class GhostState(Enum):
    """Possible states of a ghost"""
    CHASE = "chase"
    FLEE = "flee"
    EATEN = "eaten"


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
        """
        self.maze = maze
        self.start_x, self.start_y = start
        self.x = self.start_x
        self.y = self.start_y
        self.direction = "N"
        self.state = GhostState.CHASE
        self.ghost_type = ghost_type

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
        dicpos: dict[str, int] = {}
        directions = self.get_directions()
        if not directions:
            return None
        for d in directions:
            new_position = self.maze.get_next_position(self.x, self.y, d)
            dicpos[d] = self.compute_distance(new_position, target)
        best_direction, _ = min(dicpos.items(), key=lambda item: item[1])
        return best_direction
