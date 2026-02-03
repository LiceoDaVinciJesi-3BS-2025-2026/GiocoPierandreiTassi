# def maini():
import pygame
import sys

pygame.init()

schermo = pygame.display.set_mode((500,500))
sfondo = pygame.image.load("sfondo.png").convert()
sfondo = pygame.transform.scale(sfondo, (500, 500))
base = pygame.image.load("base.png").convert()
base = pygame.transform.scale(base, (500,100))
uccello = pygame.image.load("uccello.png")
tubi = pygame.image.load("tubo.png")
FPS = 60
 
def inizializza():
    global schermo, base, uccello, tubi
    schermo.blit(sfondo, (0,0) )
    schermo.blit(base, (0,400))
    schermo.blit(uccello, (250, 250))
    pygame.display.flip()
 
class tubi:
    def __init__(self):
        
    
clock = pygame.time.Clock()

running = True

while running:
    clock.tick(FPS)
    inizializza()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    
pygame.quit()
sys.exit()

#main()