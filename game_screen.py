import pygame
from game_ import Game
from game.ghost import Ghost, GhostState, GhostType
from data.highscores import (MAX_NAME_LEN, load_highscores,
                             add_score, save_highscores)

TEXT_COLOR = (255, 255, 255)
END_IMAGES = {
        "won": "graphics/win.png",
        "lost": "graphics/lose.png",
        "time is up": "graphics/time_up.png"}
FPS = 60
MOVE_EVERY = 7

GHOST_DRAW_OFFSET = {
    GhostType.BLINKY: (0, 0),
    GhostType.PINKY: (3, 0),
    GhostType.INKY: (-3, 0),
    GhostType.CLYDE: (0, 3)
}
YELLOW = (255, 220, 0)
LIGHT = (235, 245, 235)
BACKGROUND = (0, 0, 0)
WALL_COLOR = (33, 33, 222)
DOT_COLOR = (255, 255, 255)
SUPER_DOT_COLOR = (255, 255, 255)
EDIBLE_TINT = (60, 60, 255, 140)
RESPAWNING_TINT = (40, 40, 40, 160)
GHOST_IMAGE_FILES = {
    GhostType.BLINKY: "blinky.png",
    GhostType.PINKY: "pinky.png",
    GhostType.INKY: "inky.png",
    GhostType.CLYDE: "clyde.png"
    }
DIRECTION_KEYS = {
    pygame.K_UP: "N",
    pygame.K_w: "N",
    pygame.K_DOWN: "S",
    pygame.K_s: "S",
    pygame.K_LEFT: "W",
    pygame.K_a: "W",
    pygame.K_RIGHT: "E",
    pygame.K_d: "E",
}
DIRECTION_ANGLES = {
    "E": 0,
    "N": 90,
    "W": 180,
    "S": 270,
}

NORTH_WALL = 1
EAST_WALL = 2
SOUTH_WALL = 4
WEST_WALL = 8


def scale_to_fit(image: pygame.Surface, max_size: int) -> pygame.Surface:
    """Scale an image
    Args:
        image: the image to scale
        max_size: maximum size if the largest side (width or height)
    Returns:
        The scaled image
    """
    width, height = image.get_size()
    scale = max_size / max(width, height)
    new_size = (max(1, round(width * scale)), max(1, round(scale * height)))
    return pygame.transform.smoothscale(image, new_size)


def tinted(image: pygame.Surface, color: tuple) -> pygame.Surface:
    """Apply a translucent color to an image
    Args:
        image: the image to tint
        color: the RGBA color used for tint
    Returns:
        A tinted copy of the image
    """
    tinted = image.copy()
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    overlay.fill(color)
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted


def load_images() -> tuple:
    """Load the player and ghost images
    Returns:
        the player image and the ghost images
    """
    player_original = pygame.image.load("graphics/pacman.png"
                                        ).convert_alpha()

    ghost_original = {}
    for ghost_type, filename in GHOST_IMAGE_FILES.items():
        image = pygame.image.load(
                f"graphics/{filename}").convert_alpha()
        ghost_original[ghost_type] = image
    return player_original, ghost_original


def scale_images(player_image: pygame.Surface,
                 ghost_images_o: dict, cell_size: int
                 ) -> tuple:
    """Scale the player and ghost images to the maze cell size
    The player image is also rotated for each direction
    Args:
        player_image: The original player image
        ghost_images_o: The original ghost images
        cell_size: The size of maze cell
    Returns:
        The scaled images for player and ghost
    """
    base = scale_to_fit(player_image, cell_size)

    player_images = {}
    for direction, angle in DIRECTION_ANGLES.items():
        player_images[direction] = pygame.transform.rotate(
                base, angle
                )

    ghost_images = {}
    for ghost_type, image in ghost_images_o.items():
        ghost_images[ghost_type] = scale_to_fit(
                image, cell_size
                )
    return player_images, ghost_images


def ghost_image(ghost: Ghost, ghost_images: dict
                ) -> pygame.Surface:
    """Return the image of a ghost tinted according to its state
    Args:
        ghost: the ghost to draw
        ghost_images: the scaled ghost images
    Returns:
        The ghost image with the appropriate effect applied
    """
    image = ghost_images[ghost.ghost_type]
    if ghost.state == GhostState.EDIBLE:
        return tinted(image, EDIBLE_TINT)
    if ghost.state == GhostState.RESPAWNING:
        return tinted(image, RESPAWNING_TINT)
    return image


def compute_layout(game: Game, width: int, height: int
                   ) -> tuple[int, int, int]:
    """Compute the cell size and drawing offset of the current maze
    Args:
        game: the current game instance
        width: the screen width
        height: the screen height
    Returns:
        A tuple containing the cell size, horizontal offset and vertical offset
    """
    maze = game.level_manager.maze
    cell_size = min(width // maze.width, height // maze.height)
    offset_x = (width - cell_size * maze.width) // 2
    offset_y = (height - cell_size * maze.height) // 2
    return cell_size, offset_x, offset_y


def draw_maze(screen: pygame.Surface, game: Game, cell_size: int,
              offset_x: int, offset_y: int) -> None:
    """Draw the maze wall as lines
    Args:
        screen: the surface to draw on
        game: the current game instance
        cell_size: size of one maze cell
        offset_x: horizontal offset of the maze
        offset_y: vertical offset of the maze
    """
    maze = game.level_manager.maze

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            px = offset_x + x * cell_size
            py = offset_y + y * cell_size
            if cell & NORTH_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px, py),
                                 (px + cell_size, py), 3)
            if cell & SOUTH_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px, py + cell_size),
                                 (px + cell_size, py + cell_size), 3)
            if cell & WEST_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px, py),
                                 (px, py + cell_size), 3)
            if cell & EAST_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px + cell_size, py),
                                 (px + cell_size, py + cell_size), 3)


def draw_items(screen: pygame.Surface,
               game: Game, cell_size: int,
               offset_x: int, offset_y: int) -> None:
    """Draw pacgums and super-pacgums on the screen
    Args:
        screen: the surface to draw on
        game: the current game instance
        cell_size: size of one maze cell
        offset_x: horizontal offset of the maze
        offset_y: vertical offset of the maze
    """
    items = game.level_manager.items
    for x, y in items.pacgums:
        cx = offset_x + x * cell_size + cell_size // 2
        cy = offset_y + y * cell_size + cell_size // 2
        pygame.draw.circle(screen, DOT_COLOR, (cx, cy), max(2, cell_size // 8))
    for x, y in items.super_pacgums:
        cx = offset_x + x * cell_size + cell_size // 2
        cy = offset_y + y * cell_size + cell_size // 2
        pygame.draw.circle(screen, SUPER_DOT_COLOR,
                           (cx, cy), max(4, cell_size // 4))


def draw_player(screen: pygame.Surface,
                game: Game, player_images: dict,
                cell_size: int, offset_x: int, offset_y: int) -> None:
    """Draw the player at its current maze position
    Args:
        screen: the surface to draw on
        game: the current game instance
        player_images: Image of the player for each direction
        cell_size: size of one maze cell
        offset_x: horizontal offset of the maze
        offset_y: vertical offset of the maze
    """
    image = player_images.get(game.player.direction, player_images["E"])
    px = offset_x + game.player.x * cell_size
    py = offset_y + game.player.y * cell_size
    rect = image.get_rect(center=(px + cell_size // 2, py + cell_size // 2))
    screen.blit(image, rect)


def draw_ghosts(screen: pygame.Surface,
                game: Game,
                ghost_images: dict,
                cell_size: int, offset_x: int, offset_y: int) -> None:
    """Draw all ghosts at their current maze positions
    Args:
        screen: the surface to draw on
        game: the current game instance
        ghost_images: Image of the ghosts
        cell_size: size of one maze cell
        offset_x: horizontal offset of the maze
        offset_y: vertical offset of the maze
    """
    for ghost in game.ghosts:
        image = ghost_image(ghost, ghost_images)
        dx, dy = GHOST_DRAW_OFFSET[ghost.ghost_type]
        px = offset_x + ghost.x * cell_size + dx
        py = offset_y + ghost.y * cell_size + dy
        rect = image.get_rect(
                center=(px + cell_size // 2, py + cell_size // 2))
        screen.blit(image, rect)


def draw_centered_text(screen: pygame.Surface, text: str, size: int,
                       center_y: int, color: tuple = TEXT_COLOR) -> None:
    """Draw text centered horizontally on the screen
    Args:
        screen: The surface on which to draw the text
        text: the text to display
        size: the font size
        center_y: the vertical position of the text center
        color: the color of the text
    """
    font = pygame.font.Font("graphics/font.ttf", size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen.get_width() // 2, center_y))
    screen.blit(surface, rect)


def ask_name(screen: pygame.Surface, status: str, score: int) -> None | str:
    """Display the end of game screen and let the player type name
    Args:
        screen: the surface on which to display the screen
        status: how the game ended: "won", "lost" or "time is up"
        score: the final score of the player
    Returns:
        The name typed by player or None if the window was closed
    """
    clock = pygame.time.Clock()
    name = ""
    background = pygame.image.load(END_IMAGES[status]).convert()
    box = pygame.Rect(440, 530, 400, 70)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if name.strip():
                    return name.strip()
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            elif (
                    event.unicode and (
                        event.unicode.isalnum()
                        or event.unicode == " "
                        )
                    and len(name) < MAX_NAME_LEN
                    ):
                name += event.unicode

        screen.blit(background, (0, 0))
        draw_centered_text(screen, f"Score: {score}", 48, 440, YELLOW)
        draw_centered_text(screen, "Enter your name", 30, 497, LIGHT)
        pygame.draw.rect(screen, (0, 0, 0), box, border_radius=12)
        pygame.draw.rect(screen, YELLOW, box, 3, border_radius=12)

        draw_centered_text(screen, name, 34, box.centery)
        draw_centered_text(screen, "Press Enter to continue", 24, 650, LIGHT)
        pygame.display.update()


def pause_menu(screen: pygame.Surface) -> str:
    options = ["Resume", "Return to Menu"]
    selected = 0
    clock = pygame.time.Clock()
    background = pygame.image.load("graphics/Pause.png")
    background.set_alpha(150)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        draw_centered_text(screen, "Pause Menu", 70, 160, LIGHT)
        for i, option in enumerate(options):
            color = YELLOW if i == selected else LIGHT
            draw_centered_text(screen, option, 40, 400 + i * 100, color)
        pygame.display.update()


def draw_hud(screen: pygame.Surface, game: Game, font: pygame.font.Font) -> None:
    score_text = font.render(f"Score: {game.score.get_score()}", True,
    (255, 255, 255))
    score_rect = score_text.get_rect(topleft=(5, 5))
    screen.blit(score_text, score_rect)

    lives_text = font.render(f"Lives: {game.player.lives}", True,
                                 (255, 255, 255)
                            )
    lives_rect = lives_text.get_rect(topleft=(5, 40))
    screen.blit(lives_text, lives_rect)
    time_left = int(game.level_manager.time_remaining())
    time_text = font.render(f"Time: {time_left}", True,
    (255, 255, 255))
    time_rect = time_text.get_rect(topleft=(5, 75))
    screen.blit(time_text, time_rect)


def highscore_menu(screen: pygame.Surface) -> str:
    clock = pygame.time.Clock()
    pause_font = pygame.font.Font("graphics/font.ttf", 30)
    scores = load_highscores("highscores.json")
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return "menu"
        screen.fill((0, 0, 0))
        panel = pygame.Rect(180, 160, 920, 530)
        pygame.draw.rect(screen, YELLOW, panel, width=3, border_radius=20)
        draw_centered_text(screen, "High Scores", 70, 100, YELLOW)
        for i, entry in enumerate(scores):
            y = 250 + i * 40
            name_text = pause_font.render(entry["name"], True, LIGHT)
            name_rect = name_text.get_rect(topleft=(400, y))
            screen.blit(name_text, name_rect)
            score_text = pause_font.render(str(entry["score"]), True, LIGHT)
            score_rect = score_text.get_rect(topright=(800, y))
            screen.blit(score_text, score_rect)
        pygame.display.update()


def run_game(screen: pygame.Surface, config: dict) -> str:
    """Run the game loop
    Args:
        screen: the surface on which to draw the game
        config: the game configuration
    Returns:
        The state after the game ends
    """
    game = Game(levels=config["levels"],
                pacgum_count=config["pacgum"],
                level_max_time=config["level_max_time"],
                lives=config["lives"],
                points_per_pacgum=config["points_per_pacgum"],
                points_per_super_pacgum=config["points_per_super_pacgum"],
                points_per_ghost=config["points_per_ghost"])
    HIGHSCORE_FILE = config["highscore_filename"]
    clock = pygame.time.Clock()
    player_original, ghost_original = load_images()
    hud_font = pygame.font.Font("graphics/font.ttf", 20)
    player_images = {}
    ghost_images = {}
    last_cell_size = -1
    width, height = screen.get_size()
    pending_direction = None
    frame_count = 0
    maze_surface = None
    maze_level = -1
    while True:
        clock.tick(FPS)
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in DIRECTION_KEYS:
                    pending_direction = DIRECTION_KEYS[event.key]
                elif event.key == pygame.K_ESCAPE:
                    game.pause()
                    result = pause_menu(screen)
                    if result == "Return to Menu":
                        return "menu"
                    game.resume()

        if frame_count % MOVE_EVERY == 0:
            status = game.update(pending_direction)
            if status in ("lost", "won", "time is up"):
                final_score = game.score.get_score()
                name = ask_name(screen, status, final_score)
                if name:
                    scores = load_highscores(HIGHSCORE_FILE)
                    scores = add_score(scores, name, final_score)
                    save_highscores(HIGHSCORE_FILE, scores)
                return "menu"
        cell_size, offset_x, offset_y = compute_layout(game, width, height)
        if cell_size != last_cell_size:
            player_images, ghost_images = scale_images(
                    player_original, ghost_original, cell_size)
            last_cell_size = cell_size
        if (maze_surface is None
            or maze_level != game.level_manager.current_level):
            maze_surface = pygame.Surface((width, height))
            maze_surface.fill(BACKGROUND)
            draw_maze(maze_surface, game, cell_size, offset_x, offset_y)
            maze_level = game.level_manager.current_level
        screen.blit(maze_surface, (0, 0))
        draw_items(screen, game, cell_size, offset_x, offset_y)
        draw_player(screen, game, player_images, cell_size, offset_x, offset_y)
        draw_ghosts(screen, game, ghost_images, cell_size, offset_x, offset_y)
        draw_hud(screen, game, hud_font)
        pygame.display.update()
