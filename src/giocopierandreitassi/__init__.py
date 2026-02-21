import pygame
import random
import sys

pygame.init()

# ── Risorse ──────────────────────────────────────────────────────────────────
schermo = pygame.display.set_mode((500, 500))
sfondo             = pygame.transform.scale(pygame.image.load("sfondo.png").convert(),            (500, 500))
sfondoApocalittico = pygame.transform.scale(pygame.image.load("SfondoApocalittico.png").convert(),(500, 500))
base               = pygame.transform.scale(pygame.image.load("base.png").convert(),              (600, 100))
uccello  = pygame.image.load("uccello.png")
tuboGiu  = pygame.image.load("tubo.png")
tuboSu   = pygame.transform.flip(tuboGiu, False, True)
gameover = pygame.image.load("gameover.png")
font     = pygame.font.SysFont('Comic Sans MS', 32)

# ── Costanti / Globali ────────────────────────────────────────────────────────
VEL_AVANZ    = 3
FPS          = 60
clock_globale = pygame.time.Clock()          # UN solo Clock riusato ovunque

SALVATAGGIO_FILE = "progressioneLivello.txt"

# Stato di gioco
gravita_invertita       = False
livello_corrente        = 1
punteggio_massimo_livello = 30
punteggio = 0
uccelloy = 200
uccello_vely = 3
basex = 0
tubi: list = []

# ── Salvataggio progressi ─────────────────────────────────────────────────────

def carica_progressi():
    """Legge le percentuali dal file. Restituisce [perc_liv1, perc_liv2]."""
    try:
        with open(SALVATAGGIO_FILE, "r") as f:
            righe = f.readlines()
        progressi = []
        for riga in righe:
            riga = riga.strip()
            progressi.append(int(riga) if riga.isdigit() else 0)
        while len(progressi) < 2:
            progressi.append(0)
        return progressi
    except FileNotFoundError:
        salva_progressi([0, 0])
        return [0, 0]


def salva_progressi(progressi):
    """Scrive le percentuali nel file, una per riga."""
    with open(SALVATAGGIO_FILE, "w") as f:
        for p in progressi:
            f.write(f"{p}\n")


def aggiorna_progresso_livello(numero_livello, punteggio_attuale, punteggio_massimo):
    """Aggiorna la percentuale solo se migliorativa."""
    progressi = carica_progressi()
    nuova_percentuale = min(int((punteggio_attuale / punteggio_massimo) * 100), 100)
    indice = numero_livello - 1
    if nuova_percentuale > progressi[indice]:
        progressi[indice] = nuova_percentuale
        salva_progressi(progressi)

# ── Utilità ───────────────────────────────────────────────────────────────────

def invertiGravita():
    global gravita_invertita
    gravita_invertita = not gravita_invertita


def crea_coppia_tubi(x):
    spazio    = 200
    y_apertura = random.randint(100, 250)
    tubo_superiore = {
        'x': x, 'y': 0,
        'altezza': y_apertura - spazio // 2,
        'tipo': 'superiore',
        'larghezza': tuboSu.get_width(),
        'punteggiato': False,
    }
    tubo_inferiore = {
        'x': x,
        'y': y_apertura + spazio // 2,
        'altezza': 500 - (y_apertura + spazio // 2),
        'tipo': 'inferiore',
        'larghezza': tuboGiu.get_width(),
        'punteggiato': False,
    }
    return [tubo_superiore, tubo_inferiore]


def muovi_tubo(tubo):
    tubo['x'] -= VEL_AVANZ


def disegna_tubo(tubo):
    if tubo['tipo'] == 'superiore':
        schermo.blit(pygame.transform.scale(tuboSu, (tubo['larghezza'], tubo['altezza'])),
                     (tubo['x'], tubo['y']))
    else:
        schermo.blit(pygame.transform.scale(tuboGiu, (tubo['larghezza'], tubo['altezza'])),
                     (tubo['x'], tubo['y']))


def controlla_collisione(ux, uy, ul, ua, tubo):
    return (ux + ul > tubo['x'] and
            ux < tubo['x'] + tubo['larghezza'] and
            uy + ua > tubo['y'] and
            uy < tubo['y'] + tubo['altezza'])


def aggiorna_punteggio():
    global punteggio
    for tubo in tubi:
        if tubo['x'] + tubo['larghezza'] < 60 and not tubo['punteggiato']:
            punteggio += 0.5
            tubo['punteggiato'] = True
            aggiorna_progresso_livello(livello_corrente, punteggio, punteggio_massimo_livello)


def aggiorna():
    """Aggiorna lo schermo e limita gli FPS."""
    pygame.display.update()
    clock_globale.tick(FPS)          # ← Clock riusato, limita davvero gli FPS


def disegna():
    schermo.blit(sfondoApocalittico if gravita_invertita else sfondo, (0, 0))
    for tubo in tubi:
        disegna_tubo(tubo)
    schermo.blit(base, (basex, 400))
    schermo.blit(uccello, (60, uccelloy))
    schermo.blit(font.render(f"Punteggio: {int(punteggio)}", True, (255, 255, 255)), (180, 10))
    pygame.display.flip()


def inizializza():
    global uccelloy, uccello_vely, basex, tubi, punteggio, gravita_invertita
    basex         = 0
    uccelloy      = 200
    uccello_vely  = 3
    punteggio     = 0
    gravita_invertita = False
    tubi = []
    tubi.extend(crea_coppia_tubi(500))
    tubi.extend(crea_coppia_tubi(750))

# ── Schermate ─────────────────────────────────────────────────────────────────

def hai_perso():
    schermo.blit(gameover, (160, 200))
    aggiorna()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return          # il livello chiamerà inizializza() e ripartirà
                if event.key == pygame.K_ESCAPE:
                    menu(); return


def hai_vinto():
    schermo.blit(sfondo, (0, 0))
    schermo.blit(font.render("Hai vinto!", True, (255, 255, 255)), (200, 10))
    aggiorna()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                menu(); return
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu(); return

# ── Livelli ───────────────────────────────────────────────────────────────────

def _vel_livello(n):
    """Velocità base della base per il livello n."""
    return VEL_AVANZ + n      # n = 1 o 2


def livello1():
    global uccelloy, uccello_vely, basex, livello_corrente, punteggio_massimo_livello
    livello_corrente          = 1
    punteggio_massimo_livello = 30
    vel = _vel_livello(1)
    inizializza()

    while True:
        for tubo in tubi:
            muovi_tubo(tubo)

        global basex
        basex -= vel
        if basex < -45:
            basex = 0

        uccello_vely += 1
        uccelloy     += uccello_vely

        aggiorna_punteggio()

        # Ricicla tubi
        if tubi and tubi[0]['x'] < -60:
            tubi.pop(0); tubi.pop(0)
            ultima_x = tubi[-1]['x'] if len(tubi) >= 2 else 500
            tubi.extend(crea_coppia_tubi(ultima_x + 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                uccello_vely = -10

        ul, ua = uccello.get_width(), uccello.get_height()

        if uccelloy >= 390 or uccelloy <= 10:
            hai_perso()
            inizializza()       # ricomincia il livello dopo la schermata game-over

        for tubo in tubi:
            if controlla_collisione(60, uccelloy, ul, ua, tubo):
                hai_perso()
                inizializza()
                break

        if punteggio >= 30:
            hai_vinto()
            return

        disegna()
        aggiorna()


def livello2():
    global uccelloy, uccello_vely, basex, gravita_invertita
    global livello_corrente, punteggio_massimo_livello
    livello_corrente          = 2
    punteggio_massimo_livello = 70
    vel = _vel_livello(2)
    inizializza()

    while True:
        for tubo in tubi:
            muovi_tubo(tubo)

        global basex
        basex -= vel
        if basex < -45:
            basex = 0

        uccello_vely += -1 if gravita_invertita else 1
        uccelloy     += uccello_vely

        aggiorna_punteggio()

        if tubi and tubi[0]['x'] < -60:
            tubi.pop(0); tubi.pop(0)
            ultima_x = tubi[-1]['x'] if len(tubi) >= 2 else 500
            tubi.extend(crea_coppia_tubi(ultima_x + 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                uccello_vely = 10 if gravita_invertita else -10

        ul, ua = uccello.get_width(), uccello.get_height()

        if uccelloy >= 390 or uccelloy <= 10:
            hai_perso()
            inizializza()

        for tubo in tubi:
            if controlla_collisione(60, uccelloy, ul, ua, tubo):
                hai_perso()
                inizializza()
                break

        if punteggio >= 20 and not gravita_invertita:
            invertiGravita()

        if punteggio >= 70:
            hai_vinto()
            return

        disegna()
        aggiorna()

# ── Menu ──────────────────────────────────────────────────────────────────────

def menu():
    titolo_font = pygame.font.SysFont('Comic Sans MS', 48)
    barra_larg, barra_alt = 200, 14

    while True:
        # Rilegge sempre dal file → percentuali aggiornate dopo ogni partita
        progressi          = carica_progressi()
        progresso_livello1 = progressi[0]
        progresso_livello2 = progressi[1]

        schermo.blit(sfondo, (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Titolo
        schermo.blit(titolo_font.render("FLAPPY GAME", True, (255, 255, 255)), (120, 40))

        # ── Livello 1 ──
        r1     = pygame.Rect(110, 150, 280, 90)
        colore1 = (70, 150, 255) if r1.collidepoint(mouse_x, mouse_y) else (40, 90, 200)
        pygame.draw.rect(schermo, colore1, r1, border_radius=15)
        schermo.blit(font.render("Livello 1", True, (255, 255, 255)), (r1.x + 20, r1.y + 10))

        bx1, by1 = r1.x + 20, r1.y + 50
        pygame.draw.rect(schermo, (120, 120, 120), (bx1, by1, barra_larg, barra_alt), border_radius=7)
        pygame.draw.rect(schermo, (0, 220, 0),
                         (bx1, by1, barra_larg * progresso_livello1 // 100, barra_alt),
                         border_radius=7)
        schermo.blit(font.render(f"{progresso_livello1}%", True, (255, 255, 255)),
                     (bx1 + barra_larg + 10, by1 - 5))

        # ── Livello 2 ──
        r2     = pygame.Rect(110, 280, 280, 90)
        colore2 = (255, 140, 80) if r2.collidepoint(mouse_x, mouse_y) else (200, 90, 40)
        pygame.draw.rect(schermo, colore2, r2, border_radius=15)
        schermo.blit(font.render("Livello 2", True, (255, 255, 255)), (r2.x + 20, r2.y + 10))

        bx2, by2 = r2.x + 20, r2.y + 50
        pygame.draw.rect(schermo, (120, 120, 120), (bx2, by2, barra_larg, barra_alt), border_radius=7)
        pygame.draw.rect(schermo, (0, 220, 0),
                         (bx2, by2, barra_larg * progresso_livello2 // 100, barra_alt),
                         border_radius=7)
        schermo.blit(font.render(f"{progresso_livello2}%", True, (255, 255, 255)),
                     (bx2 + barra_larg + 10, by2 - 5))

        pygame.display.flip()
        clock_globale.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if r1.collidepoint(event.pos):
                    livello1(); return
                if r2.collidepoint(event.pos):
                    livello2(); return


# ── Avvio ─────────────────────────────────────────────────────────────────────
menu()