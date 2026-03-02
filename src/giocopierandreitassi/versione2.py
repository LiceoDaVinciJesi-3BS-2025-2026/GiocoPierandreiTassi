import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
sfondo = pygame.image.load("sfondo.png")
sfondo = pygame.transform.scale(sfondo, (800, 600))
livello1_img = pygame.image.load("livello1.png")
livello1_img = pygame.transform.scale(livello1_img, (70, 100))

#----------------------menu--------------------------
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Menu", True, (255, 255, 255))
        screen.blit(sfondo, (0, 0))
        screen.blit(text, (320, 30))
        screen.blit(livello1_img, (365, 200))
        pygame.display.flip()

#----------------------livello 1--------------------------
def livello1():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("Livello 1", True, (255, 255, 255))
        screen.blit(sfondo, (0, 0))
        screen.blit(text, (320, 30))
        pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(sfondo, (0, 0))
    pygame.display.flip()

    menu()
