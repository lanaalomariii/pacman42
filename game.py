import pygame
from sys import exit
pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption('Pacman')
BG = pygame.image.load('graphics/menu.png')
font = pygame.font.Font('graphics/font.ttf', 24)

def get_font(size):

def play():
    pygame.display.set_caption('Play')
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black") 
while True:
    screen.blit(display_screen, (0, 0))
    PLAY_MOUSE_POS = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()

