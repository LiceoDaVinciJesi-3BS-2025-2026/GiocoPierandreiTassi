import sys
import random
import pygame

pygame.init()

schermo = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Prova")
sfondo = pygame.image.load("sfondo.png")
sfondo = pygame.transform.scale(sfondo, (800, 600))
iconaImpostazioni = pygame.image.load("impostazioni.png")
iconaImpostazioni = pygame.transform.scale(iconaImpostazioni, (50, 50))
uccello = pygame.image.load("uccello.png")
uccello = pygame.transform.scale(uccello, (27, 25))
base = pygame.image.load("base2.png")
base = pygame.transform.scale(base, (800, 100))
clock = pygame.time.Clock()
FPS = 30
Velocità = 5

def inizializza():
    global schermo, uccello, uccelloy, uccellox, basex  # <-- NECESSARIO per modificare la variabile globale
    schermo.blit(sfondo, (0, 0))
    uccellox = 100
    uccelloy = 300
    schermo.blit(uccello, (uccellox, uccelloy))
    basex = 0
    schermo.blit(base, (basex, 500))
    
def avanza():
    global basex  # <-- NECESSARIO per modificare la variabile globale
    basex -= Velocità
    if basex <= -800:
        basex = 0
    
def menu():
    global gioco  # <-- NECESSARIO per modificare la variabile globale

    schermo.blit(sfondo, (0, 0))  # <-- sfondo PRIMA del testo, altrimenti copre tutto

    text = pygame.font.SysFont("Arial", 50).render("MENU", True, (255, 255, 255))
    schermo.blit(text, (300, 50))
    testoGioca = pygame.font.SysFont("Arial", 30).render("GIOCA", True, (255, 255, 255))
    schermo.blit(testoGioca, (350, 200))
    schermo.blit(iconaImpostazioni, (700, 500))

menu()

running = True

while running:
    for event in pygame.event.get():  # <-- UN SOLO blocco eventi nel loop
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if 350 <= mouse_pos[0] <= 450 and 200 <= mouse_pos[1] <= 250:
                inizializza()  # <-- CHIAMATA alla funzione inizializza
            elif 700 <= mouse_pos[0] <= 750 and 500 <= mouse_pos[1] <= 550:
                print("Impostazioni")




    pygame.display.flip()  # <-- UN SOLO flip alla fine
    clock.tick(FPS)