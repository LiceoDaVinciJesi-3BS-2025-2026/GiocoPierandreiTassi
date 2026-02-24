import pygame
import random
import sys

pygame.init()

# ── Schermo ─────────────────────────────────────────────
schermo = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flappy Game")

# ── Risorse ─────────────────────────────────────────────
sfondogiorno = pygame.transform.scale(pygame.image.load("sfondo.png").convert(), (500, 500))
sfondonotte = pygame.transform.scale(pygame.image.load("sfondonotte.png").convert(), (500, 500))
sfondoApocalittico = pygame.transform.scale(pygame.image.load("SfondoApocalittico.png").convert(), (500, 500))

base2 = pygame.transform.scale(pygame.image.load("base2.png").convert(), (600, 100))

uccello_base = pygame.image.load("uccello.png").convert_alpha()
rainbow_skin = pygame.image.load("rainbowdash.png").convert_alpha()

rainbow_skin = pygame.transform.scale(rainbow_skin, (70, 70))

tuboGiu = pygame.image.load("tubo.png")
tuboSu = pygame.transform.flip(tuboGiu, False, True)
gameover = pygame.image.load("gameover.png")

font = pygame.font.SysFont("Comic Sans MS", 32)
titolo_font = pygame.font.SysFont("Comic Sans MS", 48)

# ── Costanti ─────────────────────────────────────────────
VEL_AVANZ = 3
FPS = 60
clock = pygame.time.Clock()

SALVATAGGIO_FILE = "progressioneLivello.txt"

# ── Variabili globali ────────────────────────────────────
gravita_invertita = False
livello_corrente = 1
punteggio_massimo_livello = 30

punteggio = 0
uccelloy = 200
uccello_vely = 0
base2x = 0
tubi = []
sfondo_corrente = sfondogiorno

# ── Salvataggio ──────────────────────────────────────────
def carica_progressi():
    try:
        with open(SALVATAGGIO_FILE, "r") as f:
            righe = f.readlines()
        progressi = [int(r.strip()) if r.strip().isdigit() else 0 for r in righe]
        while len(progressi) < 2:
            progressi.append(0)
        return progressi
    except FileNotFoundError:
        salva_progressi([0, 0])
        return [0, 0]

def salva_progressi(progressi):
    with open(SALVATAGGIO_FILE, "w") as f:
        for p in progressi:
            f.write(f"{p}\n")

def aggiorna_progresso_livello(numero_livello, punteggio_attuale, punteggio_massimo):
    progressi = carica_progressi()
    nuova_percentuale = min(int((punteggio_attuale / punteggio_massimo) * 100), 100)
    indice = numero_livello - 1
    if nuova_percentuale > progressi[indice]:
        progressi[indice] = nuova_percentuale
        salva_progressi(progressi)

# ── Utility ──────────────────────────────────────────────
def inizializza():
    global uccelloy, uccello_vely, base2x, tubi, punteggio, gravita_invertita

    base2x = 0
    uccelloy = 200
    uccello_vely = 0
    punteggio = 0
    gravita_invertita = False

    tubi = []
    tubi.extend(crea_coppia_tubi(500))
    tubi.extend(crea_coppia_tubi(750))

def crea_coppia_tubi(x):
    spazio = 200
    y_apertura = random.randint(120, 300)

    tubo_superiore = {
        "x": x,
        "y": 0,
        "altezza": y_apertura - spazio // 2,
        "tipo": "superiore",
        "larghezza": tuboSu.get_width(),
        "punteggiato": False
    }

    tubo_inferiore = {
        "x": x,
        "y": y_apertura + spazio // 2,
        "altezza": 500 - (y_apertura + spazio // 2),
        "tipo": "inferiore",
        "larghezza": tuboGiu.get_width(),
        "punteggiato": False
    }

    return [tubo_superiore, tubo_inferiore]

def muovi_tubi():
    for tubo in tubi:
        tubo["x"] -= VEL_AVANZ

def controlla_collisione(rect_uccello, tubo):
    rect_tubo = pygame.Rect(tubo["x"], tubo["y"], tubo["larghezza"], tubo["altezza"])
    return rect_uccello.colliderect(rect_tubo)

def aggiorna_punteggio():
    global punteggio
    for tubo in tubi:
        if tubo["tipo"] == "inferiore":
            if tubo["x"] + tubo["larghezza"] < 60 and not tubo["punteggiato"]:
                punteggio += 1
                tubo["punteggiato"] = True
                aggiorna_progresso_livello(livello_corrente, punteggio, punteggio_massimo_livello)

def disegna():
    schermo.blit(sfondo_corrente, (0, 0))

    for tubo in tubi:
        img = tuboSu if tubo["tipo"] == "superiore" else tuboGiu
        img_scalata = pygame.transform.scale(img, (tubo["larghezza"], tubo["altezza"]))
        schermo.blit(img_scalata, (tubo["x"], tubo["y"]))

    schermo.blit(base2, (base2x, 400))
    schermo.blit(uccello_img, (60, uccelloy))
    schermo.blit(font.render(f"Punteggio: {punteggio}", True, (255,255,255)), (170, 10))

    pygame.display.flip()

def hai_perso():
    schermo.blit(gameover, (150, 200))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    menu(); return

def hai_vinto():
    schermo.blit(sfondogiorno, (0,0))
    testo = font.render("HAI VINTO!", True, (255,255,255))
    schermo.blit(testo, (150, 200))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                return
#-----------------------------------------------------------------------------------------------------------
#------------------------------------------ Livello 1 ------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

def livello1():
    global uccelloy, uccello_vely, base2x
    global livello_corrente, punteggio_massimo_livello, sfondo_corrente

    livello_corrente = 1
    punteggio_massimo_livello = 30
    sfondo_corrente = sfondogiorno

    inizializza()

    while True:
        clock.tick(FPS)

        muovi_tubi()

        base2x -= VEL_AVANZ
        if base2x < -45:
            base2x = 0

        uccello_vely += 0.5
        uccelloy += uccello_vely

        if punteggio >= 20:
            sfondo_corrente = sfondonotte

        aggiorna_punteggio()

        if tubi[0]["x"] < -60:
            tubi.pop(0); tubi.pop(0)
            ultima_x = tubi[-1]["x"]
            tubi.extend(crea_coppia_tubi(ultima_x + 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                uccello_vely = -10

        rect_uccello = pygame.Rect(60, uccelloy, uccello_img.get_width(), uccello_img.get_height())

        if uccelloy >= 390 or uccelloy <= 0:
            hai_perso(); inizializza()

        for tubo in tubi:
            if controlla_collisione(rect_uccello, tubo):
                hai_perso(); inizializza()
                break

        if punteggio >= 30:
            hai_vinto(); return

        disegna()
#--------------------------------------------------------------------------------------------------------
# ─--------------------------------------------- Livello 2 ----------------------------------------------
#--------------------------------------------------------------------------------------------------------

def livello2():
    global gravita_invertita, livello_corrente, punteggio_massimo_livello
    global uccelloy, uccello_vely, base2x, sfondo_corrente

    livello_corrente = 2
    punteggio_massimo_livello = 70
    sfondo_corrente = sfondoApocalittico

    inizializza()

    while True:
        clock.tick(FPS)

        muovi_tubi()

        base2x -= VEL_AVANZ + 1
        if base2x < -45:
            base2x = 0

        if gravita_invertita:
            uccello_vely -= 0.5
        else:
            uccello_vely += 0.5

        uccelloy += uccello_vely

        aggiorna_punteggio()

        if punteggio >= 20 and not gravita_invertita:
            gravita_invertita = True

        if tubi[0]["x"] < -60:
            tubi.pop(0); tubi.pop(0)
            ultima_x = tubi[-1]["x"]
            tubi.extend(crea_coppia_tubi(ultima_x + 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if gravita_invertita:
                    uccello_vely = 10
                else:
                    uccello_vely = -10

        rect_uccello = pygame.Rect(60, uccelloy, uccello_img.get_width(), uccello_img.get_height())

        if uccelloy >= 390 or uccelloy <= 0:
            hai_perso(); inizializza()

        for tubo in tubi:
            if controlla_collisione(rect_uccello, tubo):
                hai_perso(); inizializza()
                break

        if punteggio >= 70:
            hai_vinto(); return

        disegna()

def menu():
    global uccello_img
    schermata = "menu"

    # Rettangoli menu e skin
    r1 = pygame.Rect(110,150,280,90)
    r2 = pygame.Rect(110,280,280,90)
    r_skin = pygame.Rect(110,400,280,60)

    while True:
        schermo.blit(sfondogiorno, (0,0))

        mouse = pygame.mouse.get_pos()

        if schermata == "menu":

            # Pulsanti
            pygame.draw.rect(schermo,(40,90,200),r1,border_radius=15)
            pygame.draw.rect(schermo,(200,90,40),r2,border_radius=15)
            pygame.draw.rect(schermo,(90,40,200),r_skin,border_radius=15)

            schermo.blit(font.render("Livello 1",True,(255,255,255)),(r1.x+20,r1.y+10))
            schermo.blit(font.render("Livello 2",True,(255,255,255)),(r2.x+20,r2.y+10))
            schermo.blit(font.render("Skin",True,(255,255,255)),(r_skin.x+90,r_skin.y+15))

        elif schermata == "skin":
            schermo.blit(titolo_font.render("Scegli Skin", True, (255,255,255)), (130,40))

            # Posizioni immagini skin
            rect1 = uccello_base.get_rect(center=(200,250))
            rect2 = rainbow_skin.get_rect(center=(350,250))

            # Mostra le skin
            schermo.blit(uccello_base, rect1)
            schermo.blit(rainbow_skin, rect2)

        pygame.display.flip()
        clock.tick(FPS)

        # Eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if schermata == "menu":
                    if r1.collidepoint(event.pos):
                        livello1()
                    elif r2.collidepoint(event.pos):
                        livello2()
                    elif r_skin.collidepoint(event.pos):
                        schermata = "skin"

                elif schermata == "skin":
                    if rect1.collidepoint(event.pos):
                        uccello_img = uccello_base
                        schermata = "menu"
                    elif rect2.collidepoint(event.pos):
                        uccello_img = rainbow_skin
                        schermata = "menu"

# ── Avvio ────────────────────────────────────────────────
menu()