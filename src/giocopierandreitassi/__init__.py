# def maini():
import pygame
import random
import sys

pygame.init()

schermo = pygame.display.set_mode((500,500))
sfondo = pygame.image.load("sfondo.png").convert()
sfondo = pygame.transform.scale(sfondo, (500, 500))
base = pygame.image.load("base.png").convert()
base = pygame.transform.scale(base, (600,100))
uccello = pygame.image.load("uccello.png")
tubo_giu = pygame.image.load("tubo.png")
tubo_su= pygame.transform.flip(tubo_giu, False, True)
gameover = pygame.image.load("gameover.png")
VEL_AVANZ = 3
FPS = 60


#class tubi: # con la classe tubi racchiudo tutte le funzioni che regloano il comportamento dei tubi
#    def __init__(self): # con questa funzione identifico il tubo, creando un modello che crei tutti i tubi.
#    self.x = 400
#    self.y = random.randint(-100, 500)
    
def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    
def disegna():
    schermo.blit(sfondo, (0, 0))
    schermo.blit(base, (basex, 400))
    schermo.blit(uccello, (60, uccelloy))
    pygame.display.flip()

def hai_perso():
    schermo.blit(gameover,(160, 200))
    aggiorna()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                
                return
        

def inizializza():
    global uccelloy, uccello_vely, basex
    basex = 0
    uccelloy = 200
    uccello_vely = 0


inizializza()

running = True

while running:

    basex -= VEL_AVANZ
    if basex < -45:
        basex = 0
        
    uccello_vely += 1
    uccelloy += uccello_vely
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            uccello_vely = -10
            
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
        
    if uccelloy >= 390 or uccelloy <= 10:
        hai_perso()
        

    disegna()
    aggiorna()

#main()
