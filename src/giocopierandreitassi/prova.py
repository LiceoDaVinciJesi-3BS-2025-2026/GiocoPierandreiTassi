import pygame
import random
import sys
import os
import json

pygame.init()

# ───────────────── SCHERMO ─────────────────
schermo = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flappy Game")

# ───────────────── RISORSE ─────────────────
sfondogiorno = pygame.transform.scale(pygame.image.load("sfondo.png").convert(), (500, 500))
sfondonotte = pygame.transform.scale(pygame.image.load("sfondonotte.png").convert(), (500, 500))
sfondoApocalittico = pygame.transform.scale(pygame.image.load("SfondoApocalittico.png").convert(), (500, 500))

base2 = pygame.transform.scale(pygame.image.load("base2.png").convert(), (600, 100))
uccello_img_originale = pygame.image.load("uccello.png")
uccello_img = uccello_img_originale.copy()

tuboGiu = pygame.image.load("tubo.png")
tuboSu = pygame.transform.flip(tuboGiu, False, True)
gameover = pygame.image.load("gameover.png")

font = pygame.font.SysFont("Comic Sans MS", 28)
titolo_font = pygame.font.SysFont("Comic Sans MS", 46)

# ───────────────── FILE UTENTI ─────────────────
UTENTI_FILE = "utenti.json"
utente_corrente = None

# ───────────────── COSTANTI ─────────────────
VEL_AVANZ = 3
FPS = 60
clock = pygame.time.Clock()

# ───────────────── VARIABILI GLOBALI ─────────────────
gravita_invertita = False
livello_corrente = 1
punteggio_massimo_livello = 30

punteggio = 0
uccelloy = 200
uccello_vely = 0
base2x = 0
tubi = []
sfondo_corrente = sfondogiorno


# ═════════════════════════════════════════════
# ───────────── GESTIONE UTENTI ──────────────
# ═════════════════════════════════════════════

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


# ═════════════════════════════════════════════
# ───────────── CLASSIFICA GLOBALE ───────────
# ═════════════════════════════════════════════

def mostra_classifica():
    utenti = carica_utenti()

    classifica = sorted(
        utenti.items(),
        key=lambda x: x[1]["record_competitive"],
        reverse=True
    )

    while True:
        schermo.fill((20,20,20))

        schermo.blit(titolo_font.render("CLASSIFICA GLOBALE", True, (255,255,0)), (60, 60))

        y = 150
        posizione = 1

        for nome, dati in classifica[:5]:
            testo = f"{posizione}. {nome} - {dati['record_competitive']}"
            schermo.blit(font.render(testo, True, (255,255,255)), (120, y))
            y += 40
            posizione += 1

        schermo.blit(font.render("ESC per tornare", True, (200,200,200)), (150, 430))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


# ═════════════════════════════════════════════
# ───────────── MENU PRINCIPALE ──────────────
# ═════════════════════════════════════════════

def menu():
    global utente_corrente

    while True:
        utenti = carica_utenti()

        if utente_corrente is None:
            login()
            continue

        record_comp = utenti[utente_corrente]["record_competitive"]

        schermo.blit(sfondogiorno, (0, 0))

        schermo.blit(titolo_font.render("FLAPPY GAME", True, (255,255,255)), (120, 40))
        schermo.blit(font.render(f"Utente: {utente_corrente}", True, (255,255,0)), (10, 10))

        r1 = pygame.Rect(120, 150, 260, 60)
        r2 = pygame.Rect(120, 230, 260, 60)
        r3 = pygame.Rect(120, 310, 260, 60)
        r4 = pygame.Rect(120, 390, 260, 60)

        pygame.draw.rect(schermo, (40,90,200), r1, border_radius=12)
        pygame.draw.rect(schermo, (200,90,40), r2, border_radius=12)
        pygame.draw.rect(schermo, (150,0,150), r3, border_radius=12)
        pygame.draw.rect(schermo, (0,120,0), r4, border_radius=12)

        schermo.blit(font.render("Livello 1", True, (255,255,255)), (180,165))
        schermo.blit(font.render("Livello 2", True, (255,255,255)), (180,245))
        schermo.blit(font.render("Competitive", True, (255,255,255)), (165,325))
        schermo.blit(font.render("Classifica", True, (255,255,255)), (175,405))

        schermo.blit(font.render(f"Record: {record_comp}", True, (255,255,255)), (170,355))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if r1.collidepoint(event.pos):
                    livello1()
                if r2.collidepoint(event.pos):
                    livello2()
                if r3.collidepoint(event.pos):
                    competitive()
                if r4.collidepoint(event.pos):
                    mostra_classifica()


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
                uccello_vely = -5

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
#--------------------------------------------------------------------------------------------------------ù

def livello2():
    global gravita_invertita, livello_corrente, punteggio_massimo_livello
    global uccelloy, uccello_vely, base2x, sfondo_corrente, uccello

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
                    uccello = pygame.transform.flip(uccello, False, True)
                    uccello_vely = 6
                else:
                    uccello_vely = -6

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

#-----------------------------------------------------------------------------------------------------------
#--------------------------------------------- competitive -------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

def competitive():
    global gravita_invertita, livello_corrente
    global uccelloy, uccello_vely, base2x, sfondo_corrente

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

# avvio
if __name__ == "__main__":
    login()
    menu()