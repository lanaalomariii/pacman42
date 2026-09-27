class Score:
    """Manage the player's score"""
    def __init__(self, points_per_pacgum: int = 10,
                 points_per_super_pacgum: int = 50,
                 points_per_ghost: int = 200) -> None:
        """Initialize the score manager
        Args:
            points_per_pacgum: points earned per regular pacgum
            points_per_super_pacgum: points earned per super-pacgum
            points_per_ghost: points earned per ghost eaten
        """
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.score_value = 0

    def add_pacgum(self) -> None:
        """Add points for collecting a pacgum"""
        self.score_value += self.points_per_pacgum

    def add_super_pacgum(self) -> None:
        """Add points for collecting a super-pacgum"""
        self.score_value += self.points_per_super_pacgum

    def add_ghost(self) -> None:
        """Add points for eating an edible ghost"""
        self.score_value += self.points_per_ghost

    def get_score(self) -> int:
        """Returns the current score"""
        return self.score_value
