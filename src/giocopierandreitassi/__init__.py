# CLAUDIA = ho già messo le righe di codice per 6 skin ma ancora non ci sono le immagini nella cartella quindi per adesso il gioco non funzionA

import pygame
import random
import sys
import os
import json

pygame.init()

# ───────────── SCHERMO ─────────────
schermo = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flappy Game")

# ───────────── RISORSE ─────────────
sfondogiorno = pygame.transform.scale(pygame.image.load("sfondo.png").convert(), (500, 500))
sfondonotte = pygame.transform.scale(pygame.image.load("sfondonotte.png").convert(), (500, 500))
sfondoApocalittico = pygame.transform.scale(pygame.image.load("SfondoApocalittico.png").convert(), (500, 500))

base2 = pygame.transform.scale(pygame.image.load("base2.png").convert(), (600, 100))

skin1 = pygame.image.load("uccello.png").convert_alpha()
skin2 = pygame.transform.scale(pygame.image.load("rainbowdash.png").convert_alpha(), (70, 70))
skin3 = pygame.transform.scale(pygame.image.load("skin3.png").convert_alpha(), (70, 70))
skin4 = pygame.transform.scale(pygame.image.load("skin4.png").convert_alpha(), (70, 70))
skin5 = pygame.transform.scale(pygame.image.load("skin5.png").convert_alpha(), (70, 70))
skin6 = pygame.transform.scale(pygame.image.load("skin6.png").convert_alpha(), (70, 70))

uccello_img = skin1

tuboGiu = pygame.image.load("tubo.png")
tuboSu = pygame.transform.flip(tuboGiu, False, True)
gameover = pygame.image.load("gameover.png")

font = pygame.font.SysFont("Comic Sans MS", 28)
titolo_font = pygame.font.SysFont("Comic Sans MS", 46)

# ───────────── COSTANTI ─────────────
VEL_AVANZ = 3
FPS = 60
clock = pygame.time.Clock()

UTENTI_FILE = "utenti.json"
utente_corrente = None

# ───────────── VARIABILI GLOBALI ─────────────
gravita_invertita = False
livello_corrente = 1
punteggio_massimo_livello = 30

punteggio = 0
uccelloy = 200
uccello_vely = 0
base2x = 0
tubi = []
sfondo_corrente = sfondogiorno

# ═══════════════════════════════════
# GESTIONE UTENTI
# ═══════════════════════════════════

def carica_utenti():
    if os.path.exists(UTENTI_FILE):
        with open(UTENTI_FILE, "r") as f:
            return json.load(f)
    return {}

def salva_utenti(dati):
    with open(UTENTI_FILE, "w") as f:
        json.dump(dati, f, indent=4)

def login():
    global utente_corrente
    utenti = carica_utenti()

    input_user = pygame.Rect(150, 200, 200, 40)
    input_pass = pygame.Rect(150, 260, 200, 40)

    username = ""
    password = ""
    active_user = False
    active_pass = False

    while True:
        schermo.fill((30, 30, 30))
        schermo.blit(font.render("LOGIN / REGISTRAZIONE", True, (255,255,255)), (110, 140))

        pygame.draw.rect(schermo, (255,255,255), input_user, 2)
        pygame.draw.rect(schermo, (255,255,255), input_pass, 2)

        schermo.blit(font.render(username, True, (255,255,255)), (input_user.x+5, input_user.y+5))
        schermo.blit(font.render("*"*len(password), True, (255,255,255)), (input_pass.x+5, input_pass.y+5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                active_user = input_user.collidepoint(event.pos)
                active_pass = input_pass.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username == "" or password == "":
                        continue

                    if username in utenti:
                        if utenti[username]["password"] == password:
                            utente_corrente = username
                            return
                        else:
                            username = ""
                            password = ""
                    else:
                        utenti[username] = {
                            "password": password,
                            "livello1": 0,
                            "livello2": 0,
                            "record_competitive": 0
                        }
                        salva_utenti(utenti)
                        utente_corrente = username
                        return

                if active_user:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.unicode.isprintable():
                        username += event.unicode

                if active_pass:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.unicode.isprintable():
                        password += event.unicode


# ═══════════════════════════════════
# CLASSIFICA GLOBALE
# ═══════════════════════════════════

def mostra_classifica():
    utenti = carica_utenti()

    classifica = sorted(
        utenti.items(),
        key=lambda x: x[1]["record_competitive"],
        reverse=True
    )

    while True:
        schermo.fill((20,20,20))
        schermo.blit(titolo_font.render("CLASSIFICA", True, (255,255,0)), (140, 60))

        y = 150
        pos = 1

        for nome, dati in classifica[:5]:
            testo = f"{pos}. {nome} - {dati['record_competitive']}"
            schermo.blit(font.render(testo, True, (255,255,255)), (120, y))
            y += 40
            pos += 1

        schermo.blit(font.render("ESC per tornare", True, (200,200,200)), (150, 430))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


# ═══════════════════════════════════
# LOGICA GIOCO
# ═══════════════════════════════════

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

def salva_record():
    utenti = carica_utenti()
    if utente_corrente is None:
        return
    if punteggio > utenti[utente_corrente]["record_competitive"]:
        utenti[utente_corrente]["record_competitive"] = punteggio
        salva_utenti(utenti)

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

# ═══════════════════════════════════
# LIVELLI + COMPETITIVE
# ═══════════════════════════════════

def livello_base(target_score):
    global uccelloy, uccello_vely, base2x, punteggio

    inizializza()

    while True:
        clock.tick(FPS)
        muovi_tubi()

        base2x -= VEL_AVANZ
        if base2x < -45:
            base2x = 0

        uccello_vely += 0.5
        uccelloy += uccello_vely

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

        rect = pygame.Rect(60, uccelloy, uccello_img.get_width(), uccello_img.get_height())

        if uccelloy >= 390 or uccelloy <= 0:
            salva_record()
            return

        for tubo in tubi:
            if controlla_collisione(rect, tubo):
                salva_record()
                return

        if target_score and punteggio >= target_score:
            return

        disegna()

# ═══════════════════════════════════
# MENU CON SKIN + CLASSIFICA
# ═══════════════════════════════════

def menu():
    global uccello_img, titolo_font, titolo, r1, r2, r3, r4, r_skin 

    schermata = "menu"

    titolo_font = pygame.font.SysFont("Comic Sans MS", 46)


    r1 = pygame.Rect(110,130,280,60)
    r2 = pygame.Rect(110,200,280,60)
    r3 = pygame.Rect(110,270,280,60)
    r4 = pygame.Rect(110,340,280,60)
    r_skin = pygame.Rect(110,410,280,50)

    while True:
        # limita la velocità del cambio di colore del testo
        clock.tick(FPS)
        
        # Sfondo
        schermo.blit(sfondogiorno, (0,0))

        # Colore casuale
        colore = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        # Ricrea il titolo con il nuovo colore
        titolo = titolo_font.render("Flappy Game", True, colore)

        # Disegna il titolo
        schermo.blit(titolo, (130, 40))
        
        if schermata == "menu":
            pygame.draw.rect(schermo,(40,90,200),r1, border_radius=12)
            pygame.draw.rect(schermo,(200,90,40),r2, border_radius=12)
            pygame.draw.rect(schermo,(150,0,150),r3, border_radius=12)
            pygame.draw.rect(schermo,(0,120,0),r4, border_radius=12)
            pygame.draw.rect(schermo,(90,40,200),r_skin, border_radius=12)

            schermo.blit(font.render("Livello 1",True,(255,255,255)),(180,145))
            schermo.blit(font.render("Livello 2",True,(255,255,255)),(180,215))
            schermo.blit(font.render("Competitive",True,(255,255,255)),(165,285))
            schermo.blit(font.render("Classifica",True,(255,255,255)),(175,355))
            schermo.blit(font.render("Skin",True,(255,255,255)),(210,420))

        elif schermata == "skin":
            schermo.blit(titolo_font.render("Scegli Skin", True, (255,255,255)), (130,40))
            
            rect1 = skin1.get_rect(center=(130,200))
            rect2 = skin2.get_rect(center=(250,200))
            rect3 = skin3.get_rect(center=(370,200))
            rect4 = skin4.get_rect(center=(130,300))
            rect5 = skin5.get_rect(center=(250,300))
            rect6 = skin6.get_rect(center=(370,300))

            schermo.blit(skin1, rect1)
            schermo.blit(skin2, rect2)
            schermo.blit(skin3, rect3)
            schermo.blit(skin4, rect4)
            schermo.blit(skin5, rect5)
            schermo.blit(skin6, rect6)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if schermata == "menu":
                    if r1.collidepoint(event.pos):
                        livello_base(30)
                    elif r2.collidepoint(event.pos):
                        livello_base(70)
                    elif r3.collidepoint(event.pos):
                        livello_base(None)
                    elif r4.collidepoint(event.pos):
                        mostra_classifica()
                    elif r_skin.collidepoint(event.pos):
                        schermata = "skin"
                        selezionata = uccello_img
                        
                        # la skin selezionata ha un bordo giallo
                        for i, skin in enumerate([skin1, skin2, skin3, skin4, skin5, skin6]):
                            rect = [rect1, rect2, rect3, rect4, rect5, rect6][i]
                            if skin == selezionata:
                                pygame.draw.rect(schermo, (255,255,0), rect.inflate(10,10), 3) 

                elif schermata == "skin":
                    if rect1.collidepoint(event.pos):
                        uccello_img = skin1
                        schermata = "menu"
                        
                    elif rect2.collidepoint(event.pos):
                        uccello_img = skin2
                        schermata = "menu"
                        
                    elif rect3.collidepoint(event.pos):
                        uccello_img = skin3
                        schermata = "menu"

                    elif rect4.collidepoint(event.pos):
                        uccello_img = skin4
                        schermata = "menu"

                    elif rect5.collidepoint(event.pos):
                        uccello_img = skin5
                        schermata = "menu"

                    elif rect6.collidepoint(event.pos):
                        uccello_img = skin6
                        schermata = "menu"


# ───────────── AVVIO ─────────────
login()
menu()