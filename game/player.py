from game.maze import Maze

class Player:
    """Represent the player character"""
    def __init__(self, maze: Maze, start:tuple[int, int]) -> None:
        """Initialize the player
        Args:
            maze: maze the player moves within
            start: starting position as (x, y)
        """
        self.maze = maze
        self.start_x, self.start_y = start
        self.x = self.start_x
        self.y = self.start_y
        self.lives = 3
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
