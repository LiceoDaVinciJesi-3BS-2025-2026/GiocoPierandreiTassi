#def main():
import pygame
import random
import sys

<<<<<<< HEAD
=======
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

>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7
pygame.init()

# importazione delle immagini 
schermo = pygame.display.set_mode((500,500))
sfondonotte = pygame.image.load("sfondonotte.png").convert()
sfondonotte = pygame.transform.scale(sfondonotte, (500, 500))
base2 = pygame.image.load("base2.png").convert()
base2 = pygame.transform.scale(base2, (600,100))
uccello = pygame.image.load("uccello.png")
<<<<<<< HEAD
tuboGiu = pygame.image.load("tubo.png")
tuboSu = pygame.transform.flip(tuboGiu, False, True)
=======
# uccello = pygame.transform.scale(uccello, (80, 80)) - uso questa linea solo con altre skin
tuboGiu = pygame.image.load("tubo.png") #tubo che verra messo in basso
tuboSu= pygame.transform.flip(tuboGiu, False, True) #tubo rovescito che verrà messo in basso
>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7
gameover = pygame.image.load("gameover.png")
font = pygame.font.SysFont('Comic Sans MS', 32)
livello = 0
VEL_AVANZ = 3
FPS = 60

<<<<<<< HEAD


def crea_coppia_tubi(x):
    """Crea una coppia di tubi (uno sopra e uno sotto) con lo spazio in mezzo"""
    spazio = 200
    y_apertura = random.randint(100, 250)  # Punto centrale dove sarà lo spazio
    
    # Tubo superiore (rivolto verso il basso)
    tubo_superiore = {
        'x': x,
        'y': 0,  # Parte dall'alto dello schermo
        'altezza': y_apertura - spazio // 2,  # Altezza fino all'inizio dello spazio
        'tipo': 'superiore',
        'larghezza': tuboSu.get_width(),
        'punteggiato': False  # Aggiungi subito questa chiave
    }
    
    # Tubo inferiore (rivolto verso l'alto)
    tubo_inferiore = {
        'x': x,
        'y': y_apertura + spazio // 2,  # Inizia dopo lo spazio
        'altezza': 500 - (y_apertura + spazio // 2),  # Altezza fino alla base
        'tipo': 'inferiore',
        'larghezza': tuboGiu.get_width(),
        'punteggiato': False  # Aggiungi subito questa chiave
    }
    
    return [tubo_superiore, tubo_inferiore]

def muovi_tubo(tubo):
    """Muove il tubo verso sinistra"""
    tubo['x'] -= VEL_AVANZ

def disegna_tubo(tubo):
    """Disegna un singolo tubo sullo schermo"""
    if tubo['tipo'] == 'superiore':
        # Crea un'immagine del tubo superiore scalata
        tubo_scalato = pygame.transform.scale(tuboSu, (tubo['larghezza'], tubo['altezza']))
        schermo.blit(tubo_scalato, (tubo['x'], tubo['y']))
    else:  # inferiore
        # Crea un'immagine del tubo inferiore scalata
        tubo_scalato = pygame.transform.scale(tuboGiu, (tubo['larghezza'], tubo['altezza']))
        schermo.blit(tubo_scalato, (tubo['x'], tubo['y']))

def controlla_collisione(uccello_x, uccello_y, uccello_largh, uccello_alt, tubo):
    """Verifica se l'uccello collide con un tubo"""
    tubo_x = tubo['x']
    tubo_y = tubo['y']
    tubo_largh = tubo['larghezza']
    tubo_altezza = tubo['altezza']
    
    # Verifica sovrapposizione rettangolare
    if (uccello_x + uccello_largh > tubo_x and 
        uccello_x < tubo_x + tubo_largh and
        uccello_y + uccello_alt > tubo_y and
        uccello_y < tubo_y + tubo_altezza):
        return True
    
    return False

def aggiorna_punteggio():
    """Aggiorna il punteggio quando l'uccello supera un tubo"""
    global punteggio
    for tubo in tubi:
        # Controlla se l'uccello ha superato il tubo e non è stato ancora contato
        if tubo['x'] + tubo['larghezza'] < 60 and not tubo['punteggiato']:
            punteggio += 0.5  # Ogni coppia di tubi conta come 1 punto (0.5 per ciascun tubo)
            tubo['punteggiato'] = True  # Evita di contare più volte lo stesso tubo

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def disegna():
    schermo.blit(sfondo, (0, 0))
    
    for tubo in tubi:
        disegna_tubo(tubo)
=======
def aggiorna(): # la funzione aggiorna serve per rendere "fluido" il gioco
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def disegna():  # quesa funzione disegna oggetti sullo schermo anche a gioco avviato
    schermo.blit(sfondonotte, (0, 0))
    
    disegna_colonne()
>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7
    
    schermo.blit(base2, (base2x, 400))
    schermo.blit(uccello, (60, uccelloy))
    
    # Mostra il punteggio (converti in int per mostrare numeri interi)
    testo_punteggio = font.render(f"Punteggio: {int(punteggio)}", True, (255, 255, 255))
    schermo.blit(testo_punteggio, (180, 10))   
    pygame.display.flip()

<<<<<<< HEAD
def hai_perso():
    schermo.blit(gameover, (160, 200))
=======
def hai_perso(): # qunado l'uccello va a contatto con la base2 o con il tetto verrà applicata questa funzione che mette in pausa il gioco facendo apparire la scritta "GameOver"
    schermo.blit(gameover,(160, 200))
>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7
    aggiorna()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                return

def inizializza():
    global uccelloy, uccello_vely, basex, tubi, punteggio
    basex = 0
    uccelloy = 200
    uccello_vely = 0
    punteggio = 0
    
    # Crea le coppie di tubi
    tubi = []
    coppia1 = crea_coppia_tubi(500)
    coppia2 = crea_coppia_tubi(750)
    
    tubi.extend(coppia1)
    tubi.extend(coppia2)

def hai_vinto():
    schermo.fill((0, 0, 0))  # Schermo nero per indicare la vittoria
    testo_vittoria = font.render("Hai vinto!", True, (255, 255, 255))
    schermo.blit(testo_vittoria, (200, 10))
    testo_menu = font.render("TORNA AL MENU", True, (255, 255, 255))
    
    # Posizione del testo
    pos_x = 130
    pos_y = 200
    schermo.blit(testo_menu, (pos_x, pos_y))
    
    # Crea un rettangolo per il testo (per rilevare i click)
    rect_menu = testo_menu.get_rect(topleft=(pos_x, pos_y))
    
    aggiorna()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                return
            
            # Rileva il click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verifica se il click è dentro il rettangolo del testo
                if rect_menu.collidepoint(mouse_pos):
                    menu()  # Chiama la funzione menu
                    return

def livello1():
    livello = 1
    global uccelloy, uccello_vely, basex
    
    inizializza()
    running = True

    while running:
        # Muovi i tubi
        for tubo in tubi:
            muovi_tubo(tubo)
        
        basex -= VEL_AVANZ + livello  # La base si muove più velocemente con l'aumentare del livello
        if basex < -45:
            basex = 0
            
        uccello_vely += 1
        uccelloy += uccello_vely
        
        # Aggiorna il punteggio
        aggiorna_punteggio()
        
        # Rimuovi le coppie uscite e aggiungine di nuove
        if len(tubi) > 0 and tubi[0]['x'] < -60:
            # Rimuovi la coppia (2 tubi: superiore e inferiore)
            tubi.pop(0)
            tubi.pop(0)
            
            # Trova la x dell'ultimo tubo e aggiungi una nuova coppia
            if len(tubi) >= 2:
                ultima_x = tubi[-1]['x']
            else:
                ultima_x = 500
                
            nuova_coppia = crea_coppia_tubi(ultima_x + 250)
            tubi.extend(nuova_coppia)

        # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                uccello_vely = -10
                
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        # Dimensioni dell'uccello
        uccello_largh = uccello.get_width()
        uccello_alt = uccello.get_height()
        
<<<<<<< HEAD
        # Verifica collisione con base o soffitto
        if uccelloy >= 390 or uccelloy <= 10:
            hai_perso()
        
        # Verifica collisione con i tubi
        for tubo in tubi:
            if controlla_collisione(60, uccelloy, uccello_largh, uccello_alt, tubo):
                hai_perso()
                break
        
        if punteggio >= 10:  # Condizione per vincere 
            hai_vinto()
            return
        
        disegna()
        aggiorna()
=======

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
>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7


def livello2():
    livello = 2
    global uccelloy, uccello_vely, basex   
    inizializza()
    running = True  
    while running: 
        # Muovi i tubi
        for tubo in tubi:
            muovi_tubo(tubo)
        
        basex -= VEL_AVANZ + livello  # La base si muove più velocemente con l'aumentare del livello
        if basex < -45:
            basex = 0
            
        uccello_vely += 1
        uccelloy += uccello_vely
        
        # Aggiorna il punteggio
        aggiorna_punteggio()
        
<<<<<<< HEAD
        # Rimuovi le coppie uscite e aggiungine di nuove
        if len(tubi) > 0 and tubi[0]['x'] < -60:
            # Rimuovi la coppia (2 tubi: superiore e inferiore)
            tubi.pop(0)
            tubi.pop(0)
            
            # Trova la x dell'ultimo tubo e aggiungi una nuova coppia
            if len(tubi) >= 2:
                ultima_x = tubi[-1]['x']
            else:
                ultima_x = 500
                
            nuova_coppia = crea_coppia_tubi(ultima_x + 250)
            tubi.extend(nuova_coppia)
=======
    if uccelloy >= 390 or uccelloy <= 10: #verifica se l'uccello va a contatto con la base2 o con il "soffito"
        hai_perso()
        
>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7

        # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                uccello_vely = -10
                
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        # Dimensioni dell'uccello
        uccello_largh = uccello.get_width()
        uccello_alt = uccello.get_height()
        
        # Verifica collisione con base o soffitto
        if uccelloy >= 390 or uccelloy <= 10:
            hai_perso()
        
        # Verifica collisione con i tubi
        for tubo in tubi:
            if controlla_collisione(60, uccelloy, uccello_largh, uccello_alt, tubo):
                hai_perso()
                break
        
        if punteggio >= 50:  # Condizione per vincere
            hai_vinto()
            return
        disegna()
        aggiorna() 

<<<<<<< HEAD
def menu():
    schermo.blit(sfondo, (0, 0))
    testo_menu = font.render("Premi SPAZIO per iniziare", True, (255, 255, 255))
    schermo.blit(testo_menu, (55, 200))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                livello1()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                livello2()
                return

menu()
#main()
=======
#main()

>>>>>>> 2055c010089acf3b9e80c4554890e161faf5eba7
