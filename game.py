import pygame
from sys import exit


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Pacman')
BG = pygame.image.load('graphics/BG.png')
START_IMAGE = pygame.image.load('graphics/grey.png')


def get_font(size):
    return pygame.font.Font("graphics/font.ttf", size)


choice = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(BG, (0, 0))

    start_color = "yellow" if choice == 0 else "white"
    highscores_color = "yellow" if choice == 1 else "white"
    quit_color = "yellow" if choice == 2 else "white"

    MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
    START_IMAGE_RECT = START_IMAGE.get_rect(center=(640, 300))
    START_TEXT = get_font(60).render("START", True, start_color)
    START_RECT = START_TEXT.get_rect(center=(640, 300))
    HIGHSCORES_TEXT = get_font(60).render("HIGHSCORES", True, highscores_color)
    HIGHSCORES_RECT = HIGHSCORES_TEXT.get_rect(center=(640, 500))
    QUIT_TEXT = get_font(60).render("QUIT", True, quit_color)
    QUIT_RECT = QUIT_TEXT.get_rect(center=(640, 670))

    screen.blit(MENU_TEXT, MENU_RECT)
    screen.blit(START_IMAGE, START_IMAGE_RECT)
    screen.blit(START_TEXT, START_RECT)
    screen.blit(HIGHSCORES_TEXT, HIGHSCORES_RECT)
    screen.blit(QUIT_TEXT, QUIT_RECT)

    pygame.display.update()

