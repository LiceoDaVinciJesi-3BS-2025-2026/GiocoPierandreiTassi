# def maini(): 
import pygame
import random
import sys

class Colonna:
    def __init__(self, x):
        self.x = x
        self.spazio = 200
        self.y = random.randint(-200, 0)

    def muovi(self):
        self.x -= VEL_AVANZ

    def disegna(self):
        schermo.blit(tuboSu, (self.x, self.y))
        schermo.blit(tuboGiu,(self.x, self.y + tuboSu.get_height() + self.spazio)) # l'ho fatto con chat
        
pygame.init()

# importazione delle immagini
schermo = pygame.display.set_mode((500,500))
sfondo = pygame.image.load("sfondo.png").convert()
sfondo = pygame.transform.scale(sfondo, (500, 500))
base = pygame.image.load("base.png").convert()
base = pygame.transform.scale(base, (600,100))
uccello = pygame.image.load("uccello.png")
tuboGiu = pygame.image.load("tubo.png") #tubo che verra messo in basso
tuboSu= pygame.transform.flip(tuboGiu, False, True) #tubo rovescito che verrà messo in basso
gameover = pygame.image.load("gameover.png")
VEL_AVANZ = 3
FPS = 60 #frequenza per secondo


#class tubi: # con la classe tubi racchiudo tutte le funzioni che regloano il comportamento dei tubi
#    def __init__(self): # con questa funzione identifico il tubo, creando un modello che crei tutti i tubi.
#    self.x = 400
#    self.y = random.randint(-100, 500)
    
def aggiorna(): # la funzione aggiorna serve per rendere "fluido" il gioco
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def disegna():  # quesa funzione disegna oggetti sullo schermo anche a gioco avviato
    schermo.blit(sfondo, (0, 0))
    
    for colonna in colonne:
        colonna.disegna()
    
    schermo.blit(base, (basex, 400))
    schermo.blit(uccello, (60, uccelloy))
    pygame.display.flip()

def hai_perso(): # qunado l'uccello va a contatto con la base o con il tetto verrà applicata questa funzione che mette in pausa il gioco facendo apparire la scritta "GameOver"
    schermo.blit(gameover,(160, 200))
    aggiorna()
    
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  # con questo if rendiamo la chiusura del gioco efficacie anche quando è in atto questa funzione
                running = False
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # riavvia / inizializza il gioco quando si preme spazio dopo il gameover
                inizializza()
                
                return
        

def inizializza(): #riporta tutti gli oggetti alla posizione iniziale
    global uccelloy, uccello_vely, basex
    basex = 0
    uccelloy = 200
    uccello_vely = 0

colonne = [Colonna(500),Colonna(700)]

inizializza()

running = True

while running: #avvio del gioco
    for colonna in colonne:
       colonna.muovi()
    
    basex -= VEL_AVANZ
    if basex < -45:
        basex = 0
        
    uccello_vely += 1
    uccelloy += uccello_vely
    
    if colonne[0].x < -60:  # per far ricomparire una colonna a sinistra dopo che ne è ucita una a
        colonne.pop(0)
        colonne.append(Colonna(400))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            uccello_vely = -10
            
        if event.type == pygame.QUIT: #chiusura del gioco quando
            running = False
            pygame.quit()
            sys.exit()
        
        
    if uccelloy >= 390 or uccelloy <= 10: #verifica se l'uccello va a contatto con la base o con il "soffito"
        hai_perso()
        

    disegna()
    aggiorna()

#main()
