# def maini(): 
import pygame
import random
import sys

def crea_colonna(x):
    return {"x": x,"y": random.randint(-200, 0),"spazio": 190} # dizionario (posizione delle colonne)
colonne = [crea_colonna(500), crea_colonna(700)] # creo una lista di dizionari

def muovi_colonne():
    for colonna in colonne:
        colonna["x"] -= VEL_AVANZ
        
def disegna_colonne():
    for colonna in colonne:
        schermo.blit(tuboSu, (colonna["x"], colonna["y"]))
        schermo.blit(tuboGiu, (colonna["x"], colonna["y"] + tuboSu.get_height() + colonna["spazio"]))

pygame.init()

# importazione delle immagini 
schermo = pygame.display.set_mode((500,500))
sfondonotte = pygame.image.load("sfondonotte.png").convert()
sfondonotte = pygame.transform.scale(sfondonotte, (500, 500))
base2 = pygame.image.load("base2.png").convert()
base2 = pygame.transform.scale(base2, (600,100))
uccello = pygame.image.load("uccello.png")
# uccello = pygame.transform.scale(uccello, (80, 80)) - uso questa linea solo con altre skin
tuboGiu = pygame.image.load("tubo.png") #tubo che verra messo in basso
tuboSu= pygame.transform.flip(tuboGiu, False, True) #tubo rovescito che verrà messo in basso
gameover = pygame.image.load("gameover.png")
VEL_AVANZ = 3
FPS = 60 #frequenza per secondo

def aggiorna(): # la funzione aggiorna serve per rendere "fluido" il gioco
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def disegna():  # quesa funzione disegna oggetti sullo schermo anche a gioco avviato
    schermo.blit(sfondonotte, (0, 0))
    
    disegna_colonne()
    
    schermo.blit(base2, (base2x, 400))
    schermo.blit(uccello, (60, uccelloy))
    pygame.display.flip()

def hai_perso(): # qunado l'uccello va a contatto con la base2 o con il tetto verrà applicata questa funzione che mette in pausa il gioco facendo apparire la scritta "GameOver"
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
    global uccelloy, uccello_vely, base2x
    base2x = 0
    uccelloy = 200
    uccello_vely = 0

inizializza()

running = True

while running: #avvio del gioco
    muovi_colonne()
    
    base2x -= VEL_AVANZ
    if base2x < -45:
        base2x = 0
        
    uccello_vely += 1
    uccelloy += uccello_vely
    
    if colonne[0]['x'] < -60:  # per far ricomparire una colonna a sinistra dopo che ne è ucita una a destra
        colonne.pop(0)
        colonne.append(crea_colonna(400))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            uccello_vely = -10
            
        if event.type == pygame.QUIT: #chiusura del gioco quando
            running = False
            pygame.quit()
            sys.exit()
        
        
    if uccelloy >= 390 or uccelloy <= 10: #verifica se l'uccello va a contatto con la base2 o con il "soffito"
        hai_perso()
        

    disegna()
    aggiorna()

#main()

