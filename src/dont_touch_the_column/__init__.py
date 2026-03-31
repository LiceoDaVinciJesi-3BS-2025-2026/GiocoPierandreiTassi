import pygame
import random
import json
import os
from dont_touch_the_column.resources import get_image

# ──────────────────────────────────────────────────────────────────────────────
# VARIABILI GLOBALI – dichiarate a livello modulo, inizializzate in main()
# ──────────────────────────────────────────────────────────────────────────────
schermo              = None
clock                = None
sfondo               = None
skin1 = skin2 = skin3 = skin4 = skin5 = skin6 = None
rotella_impostazioni = None
base                 = None
gameover_img         = None
tubo_giu             = None
tubo_su              = None
uccello              = None

FPS              = 60
VEL_AVANZAMENTO  = 4
VEL_SFONDO       = 0.5
from pathlib import Path
FILE_CLASSIFICA = str(Path(__file__).parent / "classifica.json")

uccello_x  = 50
uccello_y  = 300
velocitay  = 0
basex      = 0
sfondox    = 0.0
tubi       = []
punteggio  = 0
fra_i_tubi = False
giocatore  = ""


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1 – GESTIONE CLASSIFICA (JSON)
# ══════════════════════════════════════════════════════════════════════════════

def carica_classifica():
    if not os.path.exists(FILE_CLASSIFICA):
        return {}
    try:
        with open(FILE_CLASSIFICA, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def salva_classifica(classifica):
    with open(FILE_CLASSIFICA, "w") as f:
        json.dump(classifica, f, indent=2)


def aggiorna_punteggio(nome, nuovo_punteggio):
    classifica = carica_classifica()
    record_precedente = classifica.get(nome, 0)
    if nuovo_punteggio > record_precedente:
        classifica[nome] = nuovo_punteggio
        salva_classifica(classifica)
        return True
    return False


def top_classifica(quanti=10):
    classifica = carica_classifica()
    ordinata = sorted(classifica.items(), key=lambda x: x[1], reverse=True)
    return ordinata[:quanti]


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2 – FUNZIONI UI
# ══════════════════════════════════════════════════════════════════════════════

def disegna_sfondo_animato(sx):
    schermo.blit(sfondo, (int(sx), 0))
    schermo.blit(sfondo, (int(sx) + 400, 0))


def disegna_tasto(testo_str, cx, cy, w, h, col_sfondo, col_testo, font):
    rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
    pygame.draw.rect(schermo, col_sfondo, rect, border_radius=12)
    pygame.draw.rect(schermo, col_testo,  rect, 2, border_radius=12)
    txt = font.render(testo_str, True, col_testo)
    schermo.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))
    return rect


def disegna_pannello(x, y, w, h, alpha=160):
    pannello = pygame.Surface((w, h), pygame.SRCALPHA)
    pannello.fill((0, 0, 0, alpha))
    schermo.blit(pannello, (x, y))


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3 – SCHERMATE
# ══════════════════════════════════════════════════════════════════════════════

def schermata_login():
    global giocatore

    sx     = 0.0
    nome   = ""
    errore = ""

    font_tit   = pygame.font.SysFont("Arial", 32, bold=True)
    font_input = pygame.font.SysFont("Arial", 26)
    font_err   = pygame.font.SysFont("Arial", 18)

    while True:
        sx -= VEL_SFONDO
        if sx <= -400:
            sx = 0.0
        disegna_sfondo_animato(sx)
        schermo.blit(base, (0, 500))

        disegna_pannello(30, 150, 340, 260, alpha=170)

        tit = font_tit.render("FLAPPY BIRD", True, (255, 220, 50))
        schermo.blit(tit, (200 - tit.get_width() // 2, 165))

        sub = font_input.render("Inserisci il tuo nome:", True, (255, 255, 255))
        schermo.blit(sub, (200 - sub.get_width() // 2, 215))

        campo = pygame.Rect(60, 255, 280, 40)
        pygame.draw.rect(schermo, (255, 255, 255), campo, border_radius=8)
        pygame.draw.rect(schermo, (100, 180, 255), campo, 2, border_radius=8)
        nome_txt = font_input.render(nome + "|", True, (0, 0, 0))
        schermo.blit(nome_txt, (70, 262))

        col_btn = (50, 180, 80) if nome.strip() else (100, 100, 100)
        rect_entra = disegna_tasto("ENTRA", 200, 330, 160, 44, col_btn, (255, 255, 255), font_input)

        if errore:
            err_txt = font_err.render(errore, True, (255, 80, 80))
            schermo.blit(err_txt, (200 - err_txt.get_width() // 2, 375))

        pygame.display.update()
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                    errore = ""
                elif evento.key == pygame.K_RETURN:
                    if nome.strip() == "":
                        errore = "Il nome non può essere vuoto!"
                    elif not nome.replace("_", "").replace(" ", "").isalnum():
                        errore = "Usa solo lettere, numeri o _"
                    else:
                        giocatore = nome.strip()
                        return
                else:
                    if len(nome) < 16:
                        nome += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rect_entra.collidepoint(evento.pos):
                    if nome.strip() == "":
                        errore = "Il nome non può essere vuoto!"
                    elif not nome.replace("_", "").replace(" ", "").isalnum():
                        errore = "Usa solo lettere, numeri o _"
                    else:
                        giocatore = nome.strip()
                        return


def schermata_classifica():
    sx       = 0.0
    font_tit = pygame.font.SysFont("Arial", 30, bold=True)
    font_rig = pygame.font.SysFont("Arial", 22)
    font_btn = pygame.font.SysFont("Arial", 20)

    while True:
        sx -= VEL_SFONDO
        if sx <= -400:
            sx = 0.0
        disegna_sfondo_animato(sx)
        schermo.blit(base, (0, 500))

        disegna_pannello(20, 30, 360, 450, alpha=180)

        tit = font_tit.render("CLASSIFICA", True, (255, 220, 50))
        schermo.blit(tit, (200 - tit.get_width() // 2, 45))

        pygame.draw.line(schermo, (200, 200, 200), (30, 90), (370, 90), 1)
        col_h = font_rig.render("#    Nome                 Punti", True, (180, 220, 255))
        schermo.blit(col_h, (38, 95))
        pygame.draw.line(schermo, (200, 200, 200), (30, 118), (370, 118), 1)

        top = top_classifica(10)
        if not top:
            vuoto = font_rig.render("Nessun punteggio ancora!", True, (200, 200, 200))
            schermo.blit(vuoto, (200 - vuoto.get_width() // 2, 220))
        else:
            for i, (nome, punti) in enumerate(top):
                y_riga = 128 + i * 30
                if i == 0:
                    col = (255, 215, 0)
                elif i == 1:
                    col = (192, 192, 192)
                elif i == 2:
                    col = (205, 127, 50)
                else:
                    col = (230, 230, 230)
                if nome == giocatore:
                    col = (80, 255, 200)
                nome_troncato = nome[:14] + ".." if len(nome) > 14 else nome
                riga = f"{i+1:<4} {nome_troncato:<18} {punti}"
                txt  = font_rig.render(riga, True, col)
                schermo.blit(txt, (38, y_riga))

        classifica_completa = carica_classifica()
        mio_record = classifica_completa.get(giocatore, 0)
        mio_txt = font_btn.render(f"Il tuo record: {mio_record}  ({giocatore})", True, (80, 255, 200))
        schermo.blit(mio_txt, (200 - mio_txt.get_width() // 2, 440))

        rect_back = disegna_tasto("← Indietro", 200, 490, 160, 38,
                                  (180, 60, 60), (255, 255, 255), font_btn)

        pygame.display.update()
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rect_back.collidepoint(evento.pos):
                    return
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return


def seleziona_skin():
    global uccello

    sx       = 0.0
    font_tit = pygame.font.SysFont("Arial", 24, bold=True)
    font_btn = pygame.font.SysFont("Arial", 20)
    opzioni  = [skin1, skin2, skin3, skin4, skin5, skin6]

    n        = len(opzioni)
    padding  = 10
    larg_tot = n * skin1.get_width() + (n - 1) * padding
    start_x  = (400 - larg_tot) // 2
    skin_y   = 230

    while True:
        sx -= VEL_SFONDO
        if sx <= -400:
            sx = 0.0
        disegna_sfondo_animato(sx)
        schermo.blit(base, (0, 500))

        disegna_pannello(20, 130, 360, 310, alpha=160)

        tit = font_tit.render("Scegli la tua skin", True, (255, 255, 255))
        schermo.blit(tit, (200 - tit.get_width() // 2, 148))

        skin_rects = []
        for i, op in enumerate(opzioni):
            x = start_x + i * (op.get_width() + padding)
            r = pygame.Rect(x - 4, skin_y - 4, op.get_width() + 8, op.get_height() + 8)
            if op is uccello:
                pygame.draw.rect(schermo, (255, 220, 0), r, border_radius=6)
            else:
                pygame.draw.rect(schermo, (220, 220, 220), r, 1, border_radius=6)
            schermo.blit(op, (x, skin_y))
            skin_rects.append((r, op))

        anteprima = pygame.transform.scale(uccello, (60, 60))
        schermo.blit(anteprima, (200 - 30, 310))
        sel_lbl = font_btn.render("Selezionata", True, (255, 220, 0))
        schermo.blit(sel_lbl, (200 - sel_lbl.get_width() // 2, 378))

        rect_back = disegna_tasto("← Indietro", 200, 430, 150, 38,
                                  (180, 60, 60), (255, 255, 255), font_btn)

        pygame.display.update()
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for r, op in skin_rects:
                    if r.collidepoint(evento.pos):
                        uccello = op
                if rect_back.collidepoint(evento.pos):
                    return
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return


def menu():
    sx       = 0.0
    font_tit = pygame.font.SysFont("Arial", 44, bold=True)
    font_btn = pygame.font.SysFont("Arial", 28, bold=True)
    font_sm  = pygame.font.SysFont("Arial", 20)
    font_xs  = pygame.font.SysFont("Arial", 16)

    while True:
        sx -= VEL_SFONDO
        if sx <= -400:
            sx = 0.0
        disegna_sfondo_animato(sx)
        schermo.blit(base, (0, 500))

        nome_lbl = font_xs.render(f"{giocatore}", True, (255, 255, 255))
        schermo.blit(nome_lbl, (10, 14))

        schermo.blit(rotella_impostazioni, (340, 10))

        ombra  = font_tit.render("FLAPPY BIRD", True, (0, 0, 0))
        titolo = font_tit.render("FLAPPY BIRD", True, (255, 255, 255))
        schermo.blit(ombra,  (200 - titolo.get_width() // 2 + 2, 122))
        schermo.blit(titolo, (200 - titolo.get_width() // 2,     120))

        schermo.blit(uccello, (200 - uccello.get_width() // 2, 200))

        rect_gioca = disegna_tasto("GIOCA", 200, 340, 180, 52,
                                   (50, 200, 80), (255, 255, 255), font_btn)
        rect_class = disegna_tasto("CLASSIFICA", 200, 415, 180, 40,
                                   (180, 140, 30), (255, 255, 255), font_sm)

        pygame.display.update()
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rect_gioca.collidepoint(evento.pos):
                    inizializza()
                    return
                if rect_class.collidepoint(evento.pos):
                    schermata_classifica()
                if 340 <= evento.pos[0] <= 390 and 10 <= evento.pos[1] <= 60:
                    seleziona_skin()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                inizializza()
                return


def hai_perso():
    nuovo_record = aggiorna_punteggio(giocatore, punteggio)

    font_big = pygame.font.SysFont("Arial", 28, bold=True)
    font_med = pygame.font.SysFont("Arial", 22)
    font_sm  = pygame.font.SysFont("Arial", 18)

    schermo.blit(gameover_img, (200 - gameover_img.get_width() // 2, 160))

    pt_txt = font_big.render(f"Punteggio: {punteggio}", True, (0, 0, 0))
    schermo.blit(pt_txt, (200 - pt_txt.get_width() // 2, 270))

    classifica = carica_classifica()
    record     = classifica.get(giocatore, 0)
    rec_col    = (0, 0, 0) if nuovo_record else (200, 200, 200)
    rec_str    = f"Record: {record}  {'NUOVO!' if nuovo_record else ''}"
    rec_txt    = font_med.render(rec_str, True, rec_col)
    schermo.blit(rec_txt, (200 - rec_txt.get_width() // 2, 308))

    schermo.blit(font_sm.render("SPAZIO  →  rigioca",       True, (0, 0, 0)), (55, 355))
    schermo.blit(font_sm.render("ESC     →  torna al menu", True, (0, 0, 0)), (55, 380))

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    inizializza()
                    return
                if evento.key == pygame.K_ESCAPE:
                    menu()
                    return


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 4 – FUNZIONI TUBI
# ══════════════════════════════════════════════════════════════════════════════

def crea_tubo():
    return {
        "x": 400,
        "y": random.randint(-30, 170)
    }


def avanza_e_disegna_tubo(t):
    t["x"] -= VEL_AVANZAMENTO
    schermo.blit(tubo_giu, (t["x"], t["y"] + 245))
    schermo.blit(tubo_su,  (t["x"], t["y"] - 245))


def collisione_tubo(t, ux, uy, ucc):
    ux_sx  = ux
    ux_dx  = ux + ucc.get_width()
    uy_su  = uy
    uy_giu = uy + ucc.get_height()
    tx_dx  = t["x"] + tubo_giu.get_width()
    tx_sx  = t["x"]
    ty_su  = t["y"] - 245 + tubo_su.get_height()
    ty_giu = t["y"] + 245
    if ux_dx > tx_sx and ux_sx < tx_dx:
        if uy_su < ty_su or uy_giu > ty_giu:
            return True
    return False


def tubo_fra_i_tubi(t, ux, ucc):
    tol   = 2
    ux_dx = ux + ucc.get_width() - tol
    ux_sx = ux + tol
    return ux_dx > t["x"] and ux_sx < t["x"] + tubo_giu.get_width()


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 5 – INIZIALIZZAZIONE E DISEGNO
# ══════════════════════════════════════════════════════════════════════════════

def inizializza():
    global uccello_x, uccello_y, velocitay
    global basex, sfondox
    global tubi, punteggio, fra_i_tubi

    uccello_x  = 50
    uccello_y  = 300
    velocitay  = 0
    basex      = 0
    sfondox    = 0.0
    punteggio  = 0
    fra_i_tubi = False
    tubi       = [crea_tubo()]


def disegna():
    schermo.blit(sfondo, (int(sfondox), 0))
    schermo.blit(sfondo, (int(sfondox) + 400, 0))

    for t in tubi:
        avanza_e_disegna_tubo(t)

    schermo.blit(uccello, (uccello_x, uccello_y))

    schermo.blit(base, (basex, 500))
    schermo.blit(base, (basex + 400, 500))

    font = pygame.font.SysFont("Arial", 36, bold=True)
    tp   = font.render(str(punteggio), True, (0, 0, 0))
    schermo.blit(tp, (200 - tp.get_width() // 2, 40))

    pygame.display.update()


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 6 – MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    global schermo, clock
    global sfondo, skin1, skin2, skin3, skin4, skin5, skin6
    global rotella_impostazioni, base, gameover_img, tubo_giu, tubo_su, uccello
    global basex, sfondox, uccello_y, velocitay, tubi, punteggio, fra_i_tubi

    pygame.init()
    schermo = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    # Caricamento immagini
    sfondo = pygame.transform.scale(
        pygame.image.load(get_image("sfondo.png")), (400, 600)
    )
    skin1 = pygame.image.load(get_image("skin1.png"))
    skin2 = pygame.transform.scale(
        pygame.image.load(get_image("skin2.png")),
        (skin1.get_width(), skin1.get_height()),
    )
    skin3 = pygame.transform.scale(
        pygame.image.load(get_image("skin3.png")),
        (skin1.get_width(), skin1.get_height()),
    )
    skin4 = pygame.transform.scale(
        pygame.image.load(get_image("skin4.png")),
        (skin1.get_width(), skin1.get_height()),
    )
    skin5 = pygame.transform.scale(
        pygame.image.load(get_image("skin5.png")),
        (skin1.get_width(), skin1.get_height()),
    )
    skin6 = pygame.transform.scale(
        pygame.image.load(get_image("skin6.png")),
        (skin1.get_width(), skin1.get_height()),
    )
    rotella_impostazioni = pygame.transform.scale(
        pygame.image.load(get_image("rotella.png")), (70, 50)
    )
    base = pygame.transform.scale(
        pygame.image.load(get_image("base2.png")), (400, 100)
    )
    gameover_img = pygame.image.load(get_image("gameover.png"))
    tubo_giu     = pygame.image.load(get_image("tubo.png"))
    tubo_su      = pygame.transform.flip(tubo_giu, False, True)
    uccello      = skin1

    # Avvio
    schermata_login()
    inizializza()
    menu()

    # Game loop principale
    while True:
        clock.tick(FPS)

        basex -= VEL_AVANZAMENTO
        if basex <= -400:
            basex = 0

        sfondox -= VEL_SFONDO
        if sfondox <= -400:
            sfondox = 0.0

        velocitay += 0.5
        uccello_y += velocitay

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                velocitay = -8
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocitay = -8
                if evento.key == pygame.K_ESCAPE:
                    menu()

        tubi = [t for t in tubi if t["x"] > -tubo_giu.get_width()]

        if tubi[-1]["x"] < 200:
            tubi.append(crea_tubo())

        for t in tubi:
            if collisione_tubo(t, uccello_x, uccello_y, uccello):
                hai_perso()
                break

        era_tra_i_tubi = fra_i_tubi
        fra_i_tubi     = any(tubo_fra_i_tubi(t, uccello_x, uccello) for t in tubi)
        if era_tra_i_tubi and not fra_i_tubi:
            punteggio += 1

        if uccello_y > 480 or uccello_y < 0:
            hai_perso()

        disegna()


if __name__ == "__main__":
    main()
