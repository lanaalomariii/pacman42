import pygame
from game_ import Game
from game.ghost import Ghost, GhostState, GhostType
from data.highscores import MAX_NAME_LEN, load_highscores, add_score, save_highscores
HIGHSCORE_FILE = "highscores.json" #tt
TEXT_COLOR = (255, 255, 255)
END_IMAGES = {
        "won": "graphics/win.png",
        "lost": "graphics/lose.png",
        "time is up":"graphics/time_up.png"}
FPS = 60
MOVE_EVERY = 9

GHOST_DRAW_OFFSET = {
    GhostType.BLINKY: (0,0),
    GhostType.PINKY: (3,0),
    GhostType.INKY: (-3, 0),
    GhostType.CLYDE: (0,3)
}
YELLOW = (255, 220, 0)
LIGHT = (235, 245, 235)
BACKGROUND = (135, 170, 140)
WALL_COLOR = (255, 255, 255)
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
    width, height = image.get_size()
    scale = max_size / max(width, height)
    new_size = (max(1, round(width * scale)), max(1, round(scale * height)))
    return pygame.transform.smoothscale(image, new_size)

def tinted(image: pygame.Surface, color: tuple[int, int, int, int]) -> pygame.Surface:
    tinted = image.copy()
    overlay = pygame.Surface(image.get_size(), pygame.SRCALPHA) 
    overlay.fill(color)
    tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT) 
    return tinted

def load_images() -> tuple[pygame.Surface, dict[GhostType, pygame.Surface]]:
    player_raw = pygame.image.load("graphics/pacman.png").convert_alpha()

    ghost_raw = {
            ghost_type: pygame.image.load(f"graphics/{filename}").convert_alpha()
            for ghost_type, filename in GHOST_IMAGE_FILES.items()
            }
    return player_raw, ghost_raw

def scale_images(player_raw: pygame.Surface, ghost_raw: dict[GhostType, pygame.Surface], cell_size: int ) -> tuple[dict[str, pygame.Surface], dict[GhostType, pygame.Surface]]:
    base = scale_to_fit(player_raw, cell_size)

    player_images = {
            direction: pygame.transform.rotate(base, angle)
            for direction, angle in DIRECTION_ANGLES.items()
            }
    ghost_images = {
            ghost_type: scale_to_fit(image, cell_size)
            for ghost_type, image in ghost_raw.items()
            }
    return player_images, ghost_images
def ghost_image(ghost: Ghost, ghost_images: dict[GhostType, pygame.Surface]) -> pygame.Surface:
    image = ghost_images[ghost.ghost_type]
    if ghost.state == GhostState.EDIBLE:
        return tinted(image, EDIBLE_TINT)
    if ghost.state == GhostState.RESPAWNING:
        return tinted(image, RESPAWNING_TINT)
    return image

def compute_layout(game: Game, width: int, height: int) -> tuple[int, int, int]:
    maze = game.level_manager.maze
    cell_size = min(width // maze.width, height // maze.height)
    offset_x = (width - cell_size * maze.width) // 2
    offset_y = (height - cell_size * maze.height) // 2
    return cell_size, offset_x, offset_y
def draw_maze(screen: pygame.Surface, game: Game, cell_size: int, offset_x: int, offset_y: int) -> None:

    maze = game.level_manager.maze

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]
            px = offset_x + x * cell_size
            py = offset_y + y * cell_size
            if cell & NORTH_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px, py), (px+ cell_size, py), 2)
            if cell & SOUTH_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px, py + cell_size), (px+ cell_size, py + cell_size), 2)
            if cell & WEST_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px, py), (px, py + cell_size), 2)
            if cell & EAST_WALL:
                pygame.draw.line(screen, WALL_COLOR, (px+ cell_size, py), (px+ cell_size, py + cell_size), 2)

def draw_items(screen: pygame.Surface, game: Game, cell_size: int, offset_x: int, offset_y: int) -> None:
    items = game.level_manager.items
    for x, y in items.pacgums:
        cx = offset_x + x * cell_size + cell_size // 2 
        cy = offset_y + y * cell_size + cell_size // 2 
        pygame.draw.circle(screen, DOT_COLOR, (cx, cy), max(2, cell_size // 8))
    for x, y in items.super_pacgums:
        cx = offset_x + x * cell_size + cell_size // 2 
        cy = offset_y + y * cell_size + cell_size // 2 
        pygame.draw.circle(screen, SUPER_DOT_COLOR, (cx, cy), max(4, cell_size // 4))

def draw_player(screen: pygame.Surface, game: Game, player_images: dict[str, pygame.Surface], cell_size: int, offset_x: int, offset_y: int) -> None: 
    image = player_images.get(game.player.direction, player_images["E"])
    px = offset_x + game.player.x * cell_size
    py = offset_y + game.player.y * cell_size
    rect = image.get_rect(center=(px+ cell_size // 2, py + cell_size // 2)) 
    screen.blit(image, rect)

def draw_ghosts(screen: pygame.Surface, game: Game, ghost_images: dict[GhostType, pygame.Surface], cell_size: int, offset_x: int, offset_y: int) -> None:
    for ghost in game.ghosts:
        image = ghost_image(ghost, ghost_images) 
        dx, dy = GHOST_DRAW_OFFSET[ghost.ghost_type] 
        px = offset_x + ghost.x * cell_size + dx 
        py = offset_y + ghost.y * cell_size + dy 
        rect = image.get_rect(center=(px+ cell_size // 2, py + cell_size // 2))
        screen.blit(image, rect)

def draw_centered_text(screen, text, size, center_y, color = TEXT_COLOR):
    font = pygame.font.Font(None, size)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen.get_width() // 2, center_y))
    screen.blit(surface, rect)

def ask_name(screen, status, score):
    clock=  pygame.time.Clock()
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
            elif (event.unicode and (event.unicode.isalnum() or event.unicode == " ") and len(name) < MAX_NAME_LEN):
                name += event.unicode

        screen.blit(background, (0,0))
        draw_centered_text(screen, f"Score: {score}", 64, 440, YELLOW)
        draw_centered_text(screen, "Enter your name", 38, 497, LIGHT)
        pygame.draw.rect(screen, (40, 55, 45), box, border_radius=12)
        pygame.draw.rect(screen, YELLOW, box,3, border_radius=12)

        draw_centered_text(screen, name,58, box.centery)
        draw_centered_text(screen, "Press Enter to continue", 32,650, LIGHT)
        pygame.display.update()


def run_game(screen: pygame.Surface, config: dict) -> str: 
    game = Game(levels=config["levels"], pacgum_count=config["pacgum"], level_max_time=config["level_max_time"], lives=config["lives"], points_per_pacgum=config["points_per_pacgum"], points_per_super_pacgum=config["points_per_super_pacgum"], points_per_ghost=config["points_per_ghost"]) 
    clock = pygame.time.Clock() 
    player_raw,ghost_raw = load_images() 
    player_images= {} 
    ghost_images = {} 
    last_cell_size = -1 
    width, height = screen.get_size()
    pending_direction = None 
    frame_count=0
    while True:
        clock.tick(FPS) 
        frame_count+= 1 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return "quit" 
            if event.type == pygame.KEYDOWN: 
                if event.key in DIRECTION_KEYS: 
                    pending_direction = DIRECTION_KEYS[event.key] 
                elif event.key == pygame.K_ESCAPE: 
                    return "menu"
        if frame_count% MOVE_EVERY == 0:
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
            player_images, ghost_images = scale_images(player_raw, ghost_raw, cell_size)
            last_cell_size = cell_size


        screen.fill(BACKGROUND)
        draw_maze(screen, game, cell_size, offset_x, offset_y) 
        draw_items(screen, game, cell_size, offset_x, offset_y) 
        draw_player(screen, game, player_images,cell_size, offset_x, offset_y)
        draw_ghosts(screen, game, ghost_images, cell_size, offset_x, offset_y)
        pygame.display.update()



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Pac-Man")
    config = {
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "level_max_time": 90,
    "levels": [
        {"width": 19, "height": 19, "seed": 42},
        {"width": 21, "height": 21, "seed": 142},
        {"width": 21, "height": 21, "seed": 242},
        {"width": 21, "height": 21, "seed": 342},
        {"width": 21, "height": 21, "seed": 442},
        {"width": 21, "height": 21, "seed": 542},
        {"width": 21, "height": 21, "seed": 642},
        {"width": 21, "height": 21, "seed": 742},
        {"width": 21, "height": 21, "seed": 842},
        {"width": 21, "height": 21, "seed": 942},
    ],
}
    run_game(screen, config)
    pygame.quit()
