from .maze import Maze


class Player:
    """Represent the player character"""
    def __init__(self, maze: Maze, start: tuple[int, int],
                 lives: int = 3) -> None:
        """Initialize the player
        Args:
            maze: maze the player moves within
            start: starting position as (x, y)
        """
        self.maze = maze
        self.start_x, self.start_y = start
        self.x = self.start_x
        self.y = self.start_y
        self.lives = lives
        self.direction = "N"

    def move(self, direction: str) -> bool:
        """move the player if the requested direction is possible
        Args:
            direction: the direction N, E , S , W
        Returns:
            True if the move succeeded, False if there is a wall"""
        if not self.maze.can_move(self.x, self.y, direction):
            return False
        self.x, self.y = self.maze.get_next_position(self.x, self.y, direction)
        self.direction = direction
        return True

    def respawn(self) -> None:
        """Move the player back to the starting position"""
        self.x = self.start_x
        self.y = self.start_y

    def is_alive(self) -> bool:
        """Return True if the player still has lives"""
        return self.lives > 0

    def lose_life(self) -> None:
        """Remove one life and respawn if the player is still alive"""
        if not self.is_alive():
            return
        self.lives -= 1
        if self.is_alive():
            self.respawn()
