import sys
import pygame


WIDTH, HEIGHT = 1280, 720
YELLOW = (255, 221, 0)
WHITE = (235, 243, 255)
DARK = (15, 15, 30)
DARK_BLUE = (15, 25, 70)
LABELS = ["START GAME", "HIGHSCORES", "INSTRUCTIONS", "EXIT"]
BUTTON_W = 250
BUTTON_H = 56
BUTTON_GAP = 16
BUTTON_CY = 668
BUTTON_X0 = (WIDTH - (len(LABELS)
                      * BUTTON_W + (len(LABELS) - 1) * BUTTON_GAP)) // 2

INSTRUCTIONS = [
        "Move: Arrow keys",
        "Eat pacgums to increase your score",
        "Eat all pacgums to win the level",
        "Super-pacgums make ghosts edible",
        "You have 3 lives",
        "Avoid ghosts unless they are edible",
        "Touch a non edible ghost costs one life",
        "Eating an edible ghost gives bonus point",
        "Each level has 90 seconds time limit",
        "Press ESC or ENTER or SPACE to go back"
        ]


def button_rect(index: int) -> pygame.Rect:
    """Return the rectangle of a menu button
    Args:
        index: position of the button in the menu
    Returns:
        the rectangle covering that button
    """
    x = BUTTON_X0 + index * (BUTTON_W + BUTTON_GAP)
    return pygame.Rect(x, BUTTON_CY - BUTTON_H // 2, BUTTON_W, BUTTON_H)


def draw_menu(screen: pygame.Surface,
              background: pygame.Surface,
              title_font: pygame.font.Font,
              label_font: pygame.font.Font, choice: int) -> None:
    """Draw the main menu and highlight the selected option
    Args:
        screen: the surface on which to draw the menu
        background: the background image of the menu
        title_font: the font used for the menu title
        label_font: the font used for the button labels
        choice: the index of the currently selected button
    """
    screen.blit(background, (0, 0))
    title = title_font.render("PAC-MAN", True, YELLOW)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 88)))
    for i, label in enumerate(LABELS):
        rect = button_rect(i)
        selected = i == choice
        color = YELLOW if selected else DARK_BLUE
        pygame.draw.rect(screen, color, rect, border_radius=12)
        text_color = DARK if selected else WHITE
        text = label_font.render(label, True, text_color)
        screen.blit(text, text.get_rect(center=rect.center))


def run_menu(screen: pygame.Surface, background: pygame.Surface) -> int:
    """Run the main menu and handle user input
    Args:
        screen: The surface on which to display the menu
        background: The background image
    Returns:
        The index of the chosen button in LABELS
    """
    clock = pygame.time.Clock()
    title_font = pygame.font.Font("graphics/font.ttf", 90)
    label_font = pygame.font.Font("graphics/font.ttf", 18)
    choice = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return len(LABELS) - 1

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_UP,
                                 pygame.K_a, pygame.K_w):
                    choice = (choice - 1) % len(LABELS)
                elif event.key in (pygame.K_RIGHT, pygame.K_DOWN,
                                   pygame.K_d, pygame.K_s):
                    choice = (choice + 1) % len(LABELS)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return choice
        draw_menu(screen, background, title_font, label_font, choice)
        pygame.display.update()
        clock.tick(60)


def run_instructions(screen: pygame.Surface,
                     background: pygame.Surface) -> None:
    """Display the instructions screen and handle user input
    Args:
        screen: The surface to draw
        background: The background image
    """
    clock = pygame.time.Clock()
    title_font = pygame.font.Font("graphics/font.ttf", 50)
    line_font = pygame.font.Font("graphics/font.ttf", 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_RETURN,
                                 pygame.K_ESCAPE, pygame.K_SPACE):
                    return
        screen.blit(background, (0, 0))
        panel = pygame.Rect(180, 160, 920, 500)
        pygame.draw.rect(screen, DARK_BLUE, panel, border_radius=20)
        title = title_font.render("INSTRUCTIONS", True, YELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        for i, line in enumerate(INSTRUCTIONS):
            text = line_font.render(line, True, WHITE)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 220 + i * 40)))
        pygame.display.update()
        clock.tick(60)
