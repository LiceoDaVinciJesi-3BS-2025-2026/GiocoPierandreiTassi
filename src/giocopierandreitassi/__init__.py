#def main():
import pygame
import random
import sys

pygame.init()

# importazione delle immagini
schermo = pygame.display.set_mode((500,500))
sfondo = pygame.image.load("sfondo.png").convert()
sfondo = pygame.transform.scale(sfondo, (500, 500))
sfondoApocalittico = pygame.image.load("SfondoApocalittico.png").convert()
sfondoApocalittico = pygame.transform.scale(sfondoApocalittico, (500, 500))
base = pygame.image.load("base.png").convert()
base = pygame.transform.scale(base, (600,100))
uccello = pygame.image.load("uccello.png")
tuboGiu = pygame.image.load("tubo.png")
tuboSu = pygame.transform.flip(tuboGiu, False, True)
gameover = pygame.image.load("gameover.png")
font = pygame.font.SysFont('Comic Sans MS', 32)
livello = 0 # 0 = menu, 1 = livello 1, 2 = livello 2 etc...
VEL_AVANZ = 3 # Velocità di avanzamento dei tubi base
FPS = 60 # Frames per secondo
gravita_invertita = False

def disegna_barra_progresso(x, y, larghezza, altezza, percentuale):
    pygame.draw.rect(schermo, (100, 100, 100), (x, y, larghezza, altezza), border_radius=8)
    pygame.draw.rect(schermo, (0, 200, 0), (x, y, larghezza * percentuale // 100, altezza), border_radius=8)


def invertiGravita():
    global gravita_invertita
    gravita_invertita = not gravita_invertita


def crea_coppia_tubi(x): # Crea una coppia di tubi (superiore e inferiore) con una posizione casuale per lo spazio tra i due tubi
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

def muovi_tubo(tubo): # Sposta il tubo verso sinistra
    
    tubo['x'] -= VEL_AVANZ # La velocità di avanzamento è costante, ma aumenta con il livello

def disegna_tubo(tubo): #   Disegna il tubo sullo schermo in base al suo tipo (superiore o inferiore)
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

def aggiorna_punteggio(): # Aggiorna il punteggio quando l'uccello supera un tubo
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
    if gravita_invertita:
        schermo.blit(sfondoApocalittico, (0, 0))
    else:
        schermo.blit(sfondo, (0, 0))
    
    for tubo in tubi:
        disegna_tubo(tubo)
    
    schermo.blit(base, (basex, 400))
    schermo.blit(uccello, (60, uccelloy))
    
    testo_punteggio = font.render(f"Punteggio: {int(punteggio)}", True, (255, 255, 255))
    schermo.blit(testo_punteggio, (180, 10))  
    pygame.display.flip()


def hai_perso():
    schermo.blit(gameover, (160, 200))
    aggiorna()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                return
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu()
                return


def inizializza():
    global uccelloy, uccello_vely, basex, tubi, punteggio, gravita_invertita 
    basex = 0
    uccelloy = 200
    uccello_vely = 3
    punteggio = 0
    gravita_invertita = False
    # Crea le coppie di tubi
    tubi = []
    coppia1 = crea_coppia_tubi(500)
    coppia2 = crea_coppia_tubi(750)
    
    tubi.extend(coppia1)
    tubi.extend(coppia2)

def hai_vinto(): # Mostra la schermata di vittoria e torna al menu
    schermo.blit(sfondo, (0, 0))  # Schermo nero per indicare la vittoria
    testo_vittoria = font.render("Hai vinto!", True, (255, 255, 255))
    schermo.blit(testo_vittoria, (200, 10))
    testo_menu = font.render("TORNA AL MENU", True, (255, 255, 255))
    
    
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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 150 <= mouse_x <= 350 and 50 <= mouse_y <= 100:  # Controlla se il click è sul testo "TORNA AL MENU"
                    menu()
                    return

#----------------------------------------------------------------------------------------------------------------
#------------------------------------------------ LIVELLO 1 -----------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
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
        
        # Verifica collisione con base o soffitto
        if uccelloy >= 390 or uccelloy <= 10:
            hai_perso()
        
        # Verifica collisione con i tubi
        for tubo in tubi:
            if controlla_collisione(60, uccelloy, uccello_largh, uccello_alt, tubo):
                hai_perso()
                break
        
        if punteggio >= 30:  # Condizione per vincere 
            hai_vinto()
            return
        
        disegna()
        aggiorna()

#----------------------------------------------------------------------------------------------------------------
#------------------------------------------------ LIVELLO 2 -----------------------------------------------------
#----------------------------------------------------------------------------------------------------------------
def livello2():
    livello = 2
    global uccelloy, uccello_vely, basex, gravita_invertita
    
    inizializza()
    running = True  
    
    while running: 
        # Muovi i tubi
        for tubo in tubi:
            muovi_tubo(tubo)
        
        basex -= VEL_AVANZ + livello
        if basex < -45:
            basex = 0
        
        if gravita_invertita:
            uccello_vely -= 1
        else:
            uccello_vely += 1

        uccelloy += uccello_vely

        # Aggiorna il punteggio
        aggiorna_punteggio()


        
        # Rimuovi le coppie uscite e aggiungine di nuove
        if len(tubi) > 0 and tubi[0]['x'] < -60:
            tubi.pop(0)
            tubi.pop(0)
            
            if len(tubi) >= 2:
                ultima_x = tubi[-1]['x']
            else:
                ultima_x = 500
                
            nuova_coppia = crea_coppia_tubi(ultima_x + 250)
            tubi.extend(nuova_coppia)

        # Gestione eventi
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if gravita_invertita:
                    uccello_vely = 10  # Spinta verso il basso quando la gravità è invertita
                else:
                    uccello_vely = -10  # Spinta verso l'alto (normale)
                
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
        
        if punteggio >= 20 and not gravita_invertita:
            invertiGravita()


        if punteggio >= 70:  # Condizione per vincere
            hai_vinto()
            return
            
        disegna()
        aggiorna()

def menu():
    clock = pygame.time.Clock()

    # Percentuali di completamento (modifica in futuro se salvi i progressi)
    progresso_livello1 = min(int((punteggio / 30) * 100), 100) if 'punteggio' in globals() else 0
    progresso_livello2 = min(int((punteggio / 70) * 100), 100) if 'punteggio' in globals() else 0

    while True:
        schermo.blit(sfondo, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Titolo
        titolo_font = pygame.font.SysFont('Comic Sans MS', 48)
        titolo = titolo_font.render("FLAPPY GAME", True, (255, 255, 255))
        schermo.blit(titolo, (120, 40))

        # ---------- LIVELLO 1 ----------
        r1 = pygame.Rect(110, 150, 280, 90)
        colore1 = (70, 150, 255) if r1.collidepoint(mouse_x, mouse_y) else (40, 90, 200)
        pygame.draw.rect(schermo, colore1, r1, border_radius=15)

        testo1 = font.render("Livello 1", True, (255, 255, 255))
        schermo.blit(testo1, (r1.x + 20, r1.y + 10))

        # Barra progresso livello 1
        barra_x = r1.x + 20
        barra_y = r1.y + 50
        barra_larg = 200
        barra_alt = 14

        pygame.draw.rect(schermo, (120, 120, 120), (barra_x, barra_y, barra_larg, barra_alt), border_radius=7)
        pygame.draw.rect(schermo, (0, 220, 0),
                         (barra_x, barra_y, barra_larg * progresso_livello1 // 100, barra_alt),
                         border_radius=7)

        perc1 = font.render(f"{progresso_livello1}%", True, (255, 255, 255))
        schermo.blit(perc1, (barra_x + barra_larg + 10, barra_y - 5))

        # ---------- LIVELLO 2 ----------
        r2 = pygame.Rect(110, 280, 280, 90)
        colore2 = (255, 140, 80) if r2.collidepoint(mouse_x, mouse_y) else (200, 90, 40)
        pygame.draw.rect(schermo, colore2, r2, border_radius=15)

        testo2 = font.render("Livello 2", True, (255, 255, 255))
        schermo.blit(testo2, (r2.x + 20, r2.y + 10))

        # Barra progresso livello 2
        barra_x2 = r2.x + 20
        barra_y2 = r2.y + 50

        pygame.draw.rect(schermo, (120, 120, 120), (barra_x2, barra_y2, barra_larg, barra_alt), border_radius=7)
        pygame.draw.rect(schermo, (0, 220, 0),
                         (barra_x2, barra_y2, barra_larg * progresso_livello2 // 100, barra_alt),
                         border_radius=7)

        perc2 = font.render(f"{progresso_livello2}%", True, (255, 255, 255))
        schermo.blit(perc2, (barra_x2 + barra_larg + 10, barra_y2 - 5))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if r1.collidepoint(event.pos):
                    livello1()
                    return
                if r2.collidepoint(event.pos):
                    livello2()
                    return


                
menu()
#main()
