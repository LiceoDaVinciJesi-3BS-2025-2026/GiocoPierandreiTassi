import pygame
import random
import json
import os

# ──────────────────────────────────────────────────────────────────────────────
# INIZIALIZZAZIONE PYGAME
# ──────────────────────────────────────────────────────────────────────────────
pygame.init()

# ──────────────────────────────────────────────────────────────────────────────
# CARICAMENTO IMMAGINI
# Ogni immagine viene caricata dal file e ridimensionata se necessario.
# Le skin sono tutte scalate alla stessa dimensione della skin1 (quella base).
# ──────────────────────────────────────────────────────────────────────────────
sfondo               = pygame.transform.scale(pygame.image.load("sfondo.png"), (400, 600))
skin1                = pygame.image.load("skin1.png")
skin2                = pygame.transform.scale(pygame.image.load("skin2.png"),  (skin1.get_width(), skin1.get_height()))
skin3                = pygame.transform.scale(pygame.image.load("skin3.png"),  (skin1.get_width(), skin1.get_height()))
skin4                = pygame.transform.scale(pygame.image.load("skin4.png"),  (skin1.get_width(), skin1.get_height()))
skin5                = pygame.transform.scale(pygame.image.load("skin5.png"),  (skin1.get_width(), skin1.get_height()))
skin6                = pygame.transform.scale(pygame.image.load("skin6.png"),  (skin1.get_width(), skin1.get_height()))
rotella_impostazioni = pygame.transform.scale(pygame.image.load("rotella.png"), (50, 50))
base                 = pygame.transform.scale(pygame.image.load("base.png"),    (400, 100))
gameover_img         = pygame.image.load("gameover.png")
tubo_giu             = pygame.image.load("tubo.png")
tubo_su              = pygame.transform.flip(tubo_giu, False, True)  # tubo capovolto per quello in alto

# ──────────────────────────────────────────────────────────────────────────────
# COSTANTI DI GIOCO
# ──────────────────────────────────────────────────────────────────────────────
schermo        = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")
FPS            = 60          # fotogrammi al secondo
VEL_AVANZAMENTO = 4          # velocità di avanzamento tubi e base
VEL_SFONDO     = 0.5         # velocità dello sfondo (più lenta per effetto parallasse)
clock          = pygame.time.Clock()

# ──────────────────────────────────────────────────────────────────────────────
# FILE JSON PER LA CLASSIFICA
# Tutti i punteggi vengono salvati in questo file nella stessa cartella del gioco.
# Struttura: { "nomeutente": punteggio_massimo, ... }
# ──────────────────────────────────────────────────────────────────────────────
FILE_CLASSIFICA = "classifica.json"

# ──────────────────────────────────────────────────────────────────────────────
# VARIABILI GLOBALI DI GIOCO
# Vengono inizializzate qui e reimpostate ogni volta che si ricomincia una partita.
# ──────────────────────────────────────────────────────────────────────────────
uccello    = skin1     # immagine dell'uccello corrente (cambia in base alla skin scelta)
uccello_x  = 50        # posizione orizzontale dell'uccello (fissa)
uccello_y  = 300       # posizione verticale dell'uccello (varia con la fisica)
velocitay  = 0         # velocità verticale dell'uccello (positiva = scende, negativa = sale)
basex      = 0         # offset orizzontale della base (per animazione scorrimento)
sfondox    = 0.0       # offset orizzontale dello sfondo (float per velocità decimale)
tubi       = []        # lista di dizionari, uno per ogni tubo presente a schermo
punteggio  = 0         # punteggio della partita corrente
fra_i_tubi = False     # True se l'uccello è orizzontalmente dentro un varco di tubi
giocatore  = ""        # nome del giocatore attualmente connesso


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 1 – GESTIONE CLASSIFICA (JSON)
# ══════════════════════════════════════════════════════════════════════════════

def carica_classifica():
    """
    Legge il file JSON della classifica e restituisce un dizionario
    { nome: punteggio_massimo }.
    Se il file non esiste o è corrotto, restituisce un dizionario vuoto.
    """
    if not os.path.exists(FILE_CLASSIFICA):
        return {}                                   # prima volta: file ancora assente
    try:
        with open(FILE_CLASSIFICA, "r") as f:
            return json.load(f)                    # deserializza il JSON in un dict Python
    except (json.JSONDecodeError, IOError):
        return {}                                  # file corrotto → partiamo da zero


def salva_classifica(classifica):
    """
    Scrive il dizionario della classifica nel file JSON.
    indent=2 rende il file leggibile anche aprendo con un editor di testo.
    """
    with open(FILE_CLASSIFICA, "w") as f:
        json.dump(classifica, f, indent=2)         # serializza il dict in JSON formattato


def aggiorna_punteggio(nome, nuovo_punteggio):
    """
    Aggiorna il record personale del giocatore se il nuovo punteggio
    supera quello già salvato (o se è la prima partita).
    Ritorna True se è stato stabilito un nuovo record, False altrimenti.
    """
    classifica = carica_classifica()
    record_precedente = classifica.get(nome, 0)    # 0 se il giocatore non ha mai giocato

    if nuovo_punteggio > record_precedente:
        classifica[nome] = nuovo_punteggio         # aggiorna solo se è un nuovo massimo
        salva_classifica(classifica)
        return True                                # segnala nuovo record al chiamante

    return False                                   # nessun aggiornamento necessario


def top_classifica(quanti=10):
    """
    Restituisce una lista di tuple (nome, punteggio) ordinata dal punteggio
    più alto al più basso, limitata ai primi 'quanti' giocatori.
    """
    classifica = carica_classifica()
    # sorted() con key=lambda ordina per il secondo elemento della tupla (il punteggio)
    # reverse=True → ordine decrescente (dal più alto)
    ordinata = sorted(classifica.items(), key=lambda x: x[1], reverse=True)
    return ordinata[:quanti]                       # ritorna solo i primi N


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 2 – FUNZIONI UI (pannelli, tasti, sfondo)
# ══════════════════════════════════════════════════════════════════════════════

def disegna_sfondo_animato(sx):
    """
    Disegna lo sfondo scorrevole usando due copie affiancate.
    Quando la prima copia esce a sinistra, la seconda è già visibile a destra,
    creando un ciclo infinito senza salti.
    sx: offset corrente (float o int)
    """
    schermo.blit(sfondo, (int(sx), 0))
    schermo.blit(sfondo, (int(sx) + 400, 0))


def disegna_tasto(testo_str, cx, cy, w, h, col_sfondo, col_testo, font):
    """
    Disegna un pulsante rettangolare con angoli arrotondati, centrato in (cx, cy).
    Restituisce il pygame.Rect del pulsante per la rilevazione del click.

    testo_str  : etichetta del pulsante
    cx, cy     : centro del pulsante
    w, h       : larghezza e altezza
    col_sfondo : colore di riempimento (R, G, B)
    col_testo  : colore del testo e del bordo
    font       : oggetto pygame.font
    """
    rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
    pygame.draw.rect(schermo, col_sfondo, rect, border_radius=12)          # riempimento
    pygame.draw.rect(schermo, col_testo,  rect, 2, border_radius=12)       # bordo sottile
    txt = font.render(testo_str, True, col_testo)
    schermo.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))
    return rect


def disegna_pannello(x, y, w, h, alpha=160):
    """
    Disegna un rettangolo nero semi-trasparente come pannello di sfondo
    per testi o elementi UI, in modo che siano leggibili sullo sfondo animato.

    alpha: opacità 0 (invisibile) – 255 (opaco)
    """
    pannello = pygame.Surface((w, h), pygame.SRCALPHA)   # superficie con canale alpha
    pannello.fill((0, 0, 0, alpha))
    schermo.blit(pannello, (x, y))


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 3 – SCHERMATE (login, menu, skin, classifica, game over)
# ══════════════════════════════════════════════════════════════════════════════

def schermata_login():
    """
    Prima schermata mostrata all'avvio.
    L'utente digita il proprio nome (massimo 16 caratteri).
    Il nome viene usato come chiave nella classifica JSON.
    Premi INVIO per confermare, BACKSPACE per cancellare l'ultimo carattere.
    """
    global giocatore

    sx      = 0.0                                          # offset sfondo per animazione
    nome    = ""                                           # stringa digitata dall'utente
    errore  = ""                                           # messaggio di errore eventuale

    font_tit   = pygame.font.SysFont("Arial", 32, bold=True)
    font_input = pygame.font.SysFont("Arial", 26)
    font_err   = pygame.font.SysFont("Arial", 18)
    font_hint  = pygame.font.SysFont("Arial", 16)

    while True:
        # ── aggiorna animazione sfondo ──
        sx -= VEL_SFONDO
        if sx <= -400:
            sx = 0.0
        disegna_sfondo_animato(sx)
        schermo.blit(base, (0, 500))

        # ── pannello centrale ──
        disegna_pannello(30, 150, 340, 260, alpha=170)

        # ── titolo ──
        tit = font_tit.render("FLAPPY BIRD", True, (255, 220, 50))
        schermo.blit(tit, (200 - tit.get_width() // 2, 165))

        sub = font_input.render("Inserisci il tuo nome:", True, (255, 255, 255))
        schermo.blit(sub, (200 - sub.get_width() // 2, 215))

        # ── campo di testo (rettangolo bianco con nome digitato) ──
        campo = pygame.Rect(60, 255, 280, 40)
        pygame.draw.rect(schermo, (255, 255, 255), campo, border_radius=8)
        pygame.draw.rect(schermo, (100, 180, 255), campo, 2, border_radius=8)
        nome_txt = font_input.render(nome + "|", True, (0, 0, 0))  # "|" simula cursore
        schermo.blit(nome_txt, (70, 262))

        # ── tasto ENTRA ──
        col_btn = (50, 180, 80) if nome.strip() else (100, 100, 100)  # grigio se vuoto
        rect_entra = disegna_tasto("ENTRA", 200, 330, 160, 44, col_btn, (255, 255, 255), font_input)

        # ── eventuale messaggio di errore ──
        if errore:
            err_txt = font_err.render(errore, True, (255, 80, 80))
            schermo.blit(err_txt, (200 - err_txt.get_width() // 2, 375))

        # ── suggerimento ──
        hint = font_hint.render("Max 16 caratteri, solo lettere e numeri", True, (200, 200, 200))
        schermo.blit(hint, (200 - hint.get_width() // 2, 400))

        pygame.display.update()
        clock.tick(FPS)

        # ── gestione eventi ──
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]                           # cancella ultimo carattere
                    errore = ""
                elif evento.key == pygame.K_RETURN:
                    # validazione: nome non vuoto e alfanumerico
                    if nome.strip() == "":
                        errore = "Il nome non può essere vuoto!"
                    elif not nome.replace("_", "").replace(" ", "").isalnum():
                        errore = "Usa solo lettere, numeri o _"
                    else:
                        giocatore = nome.strip()               # salva il nome globalmente
                        return                                 # esci dal login
                else:
                    # aggiunge il carattere digitato se sotto il limite
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
    """
    Mostra la top-10 dei punteggi salvati nel file JSON.
    Il giocatore corrente viene evidenziato in giallo.
    Tasto INDIETRO o ESC per tornare al menu.
    """
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

        # ── pannello ──
        disegna_pannello(20, 30, 360, 450, alpha=180)

        # ── titolo ──
        tit = font_tit.render("🏆  CLASSIFICA  🏆", True, (255, 220, 50))
        schermo.blit(tit, (200 - tit.get_width() // 2, 45))

        # ── intestazione colonne ──
        pygame.draw.line(schermo, (200, 200, 200), (30, 90), (370, 90), 1)
        col_h = font_rig.render("#    Nome                 Punti", True, (180, 220, 255))
        schermo.blit(col_h, (38, 95))
        pygame.draw.line(schermo, (200, 200, 200), (30, 118), (370, 118), 1)

        # ── righe classifica ──
        top = top_classifica(10)

        if not top:
            # nessun punteggio ancora registrato
            vuoto = font_rig.render("Nessun punteggio ancora!", True, (200, 200, 200))
            schermo.blit(vuoto, (200 - vuoto.get_width() // 2, 220))
        else:
            for i, (nome, punti) in enumerate(top):
                y_riga = 128 + i * 30

                # colore diverso per i primi tre posti
                if i == 0:
                    col = (255, 215, 0)      # oro
                elif i == 1:
                    col = (192, 192, 192)    # argento
                elif i == 2:
                    col = (205, 127, 50)     # bronzo
                else:
                    col = (230, 230, 230)    # bianco normale

                # evidenzia il giocatore corrente in ciano
                if nome == giocatore:
                    col = (80, 255, 200)

                # tronca nomi lunghi per non uscire dal pannello
                nome_troncato = nome[:14] + ".." if len(nome) > 14 else nome
                riga = f"{i+1:<4} {nome_troncato:<18} {punti}"
                txt  = font_rig.render(riga, True, col)
                schermo.blit(txt, (38, y_riga))

        # ── punteggio personale dell'utente loggato (in fondo al pannello) ──
        classifica_completa = carica_classifica()
        mio_record = classifica_completa.get(giocatore, 0)
        mio_txt = font_btn.render(f"Il tuo record: {mio_record}  ({giocatore})", True, (80, 255, 200))
        schermo.blit(mio_txt, (200 - mio_txt.get_width() // 2, 440))

        # ── tasto indietro ──
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
                    return                                 # torna al menu
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return


def seleziona_skin():
    """
    Schermata per scegliere la skin dell'uccello.
    Usa lo stesso sfondo scorrevole del gioco per coerenza visiva.
    La skin attualmente scelta è evidenziata con un bordo giallo.
    Si conferma cliccando sulla skin desiderata; ESC o "Indietro" torna al menu.
    """
    global uccello

    sx       = 0.0
    font_tit = pygame.font.SysFont("Arial", 24, bold=True)
    font_btn = pygame.font.SysFont("Arial", 20)
    opzioni  = [skin1, skin2, skin3, skin4, skin5, skin6]

    # calcola posizione centrata delle skin nella riga
    n         = len(opzioni)
    padding   = 10
    larg_tot  = n * skin1.get_width() + (n - 1) * padding
    start_x   = (400 - larg_tot) // 2
    skin_y    = 230

    while True:
        sx -= VEL_SFONDO
        if sx <= -400:
            sx = 0.0
        disegna_sfondo_animato(sx)
        schermo.blit(base, (0, 500))

        disegna_pannello(20, 130, 360, 310, alpha=160)

        # ── titolo ──
        tit = font_tit.render("Scegli la tua skin", True, (255, 255, 255))
        schermo.blit(tit, (200 - tit.get_width() // 2, 148))

        # ── disegna le skin con bordo di selezione ──
        skin_rects = []
        for i, op in enumerate(opzioni):
            x = start_x + i * (op.get_width() + padding)
            r = pygame.Rect(x - 4, skin_y - 4, op.get_width() + 8, op.get_height() + 8)

            if op is uccello:
                # bordo giallo spesso = skin attualmente selezionata
                pygame.draw.rect(schermo, (255, 220, 0), r, border_radius=6)
            else:
                # bordo bianco sottile = skin non selezionata
                pygame.draw.rect(schermo, (220, 220, 220), r, 1, border_radius=6)

            schermo.blit(op, (x, skin_y))
            skin_rects.append((r, op))

        # ── anteprima ingrandita della skin selezionata ──
        anteprima = pygame.transform.scale(uccello, (60, 60))
        schermo.blit(anteprima, (200 - 30, 310))
        sel_lbl = font_btn.render("Selezionata", True, (255, 220, 0))
        schermo.blit(sel_lbl, (200 - sel_lbl.get_width() // 2, 378))

        # ── tasto indietro ──
        rect_back = disegna_tasto("← Indietro", 200, 430, 150, 38,
                                  (180, 60, 60), (255, 255, 255), font_btn)

        pygame.display.update()
        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # controlla se ha cliccato su una skin
                for r, op in skin_rects:
                    if r.collidepoint(evento.pos):
                        uccello = op               # cambia la skin globale
                if rect_back.collidepoint(evento.pos):
                    return                         # torna al menu
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return


def menu():
    """
    Menu principale. Mostra:
      - Titolo del gioco
      - Uccello decorativo (con la skin scelta)
      - Tasto GIOCA (al centro)
      - Tasto CLASSIFICA (sotto)
      - Rotella in alto a destra per accedere alle impostazioni skin
      - Nome del giocatore loggato in alto a sinistra
    Sfondo animato con effetto parallasse.
    """
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

        # ── nome giocatore in alto a sinistra ──
        nome_lbl = font_xs.render(f"👤 {giocatore}", True, (255, 255, 255))
        schermo.blit(nome_lbl, (10, 14))

        # ── rotella impostazioni in alto a destra (apre selezione skin) ──
        schermo.blit(rotella_impostazioni, (340, 10))

        # ── titolo con ombra ──
        ombra  = font_tit.render("FLAPPY BIRD", True, (0, 0, 0))
        titolo = font_tit.render("FLAPPY BIRD", True, (255, 255, 255))
        schermo.blit(ombra,  (200 - titolo.get_width() // 2 + 2, 122))
        schermo.blit(titolo, (200 - titolo.get_width() // 2,     120))

        # ── uccello decorativo (usa la skin scelta) ──
        schermo.blit(uccello, (200 - uccello.get_width() // 2, 200))

        # ── tasto GIOCA ──
        rect_gioca = disegna_tasto("GIOCA", 200, 340, 180, 52,
                                   (50, 200, 80), (255, 255, 255), font_btn)

        # ── tasto CLASSIFICA ──
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
                    inizializza()                          # prepara la partita
                    return                                 # esce dal menu → entra nel game loop

                if rect_class.collidepoint(evento.pos):
                    schermata_classifica()                 # mostra la classifica, poi torna qui

                # click sulla rotella → selezione skin
                if 340 <= evento.pos[0] <= 390 and 10 <= evento.pos[1] <= 60:
                    seleziona_skin()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                inizializza()
                return


def hai_perso():
    """
    Schermata game over. Mostra l'immagine gameover, il punteggio ottenuto,
    il record personale aggiornato e le istruzioni per continuare.
    Aggiorna automaticamente il record nel file JSON se il punteggio è nuovo massimo.
    SPAZIO → rigioca con la stessa skin
    ESC    → torna al menu principale
    """
    # ── aggiorna il record nel JSON ──
    nuovo_record = aggiorna_punteggio(giocatore, punteggio)

    font_big = pygame.font.SysFont("Arial", 28, bold=True)
    font_med = pygame.font.SysFont("Arial", 22)
    font_sm  = pygame.font.SysFont("Arial", 18)

    # mostra l'immagine gameover centrata
    schermo.blit(gameover_img, (200 - gameover_img.get_width() // 2, 160))

    # ── punteggio partita ──
    pt_txt = font_big.render(f"Punteggio: {punteggio}", True, (0, 0, 0))
    schermo.blit(pt_txt, (200 - pt_txt.get_width() // 2, 270))

    # ── record personale (con "NUOVO RECORD!" se battuto) ──
    classifica = carica_classifica()
    record     = classifica.get(giocatore, 0)
    rec_col    = (0, 0, 0) if nuovo_record else (200, 200, 200)
    rec_str    = f"Record: {record}  {'NUOVO!' if nuovo_record else ''}"
    rec_txt    = font_med.render(rec_str, True, rec_col)
    schermo.blit(rec_txt, (200 - rec_txt.get_width() // 2, 308))

    # ── istruzioni ──
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
                    inizializza()      # riavvia la partita (stessa skin, stesso utente)
                    return
                if evento.key == pygame.K_ESCAPE:
                    menu()             # torna al menu principale
                    return


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 4 – FUNZIONI TUBI
# I tubi sono rappresentati come dizionari { "x": int, "y": int }.
# Questo evita l'uso di una classe e mantiene il codice più semplice.
# ══════════════════════════════════════════════════════════════════════════════

def crea_tubo():
    """
    Crea un nuovo tubo con posizione x fuori dallo schermo (destra)
    e altezza casuale. Restituisce un dizionario con le chiavi "x" e "y".
    """
    return {
        "x": 500,                             # parte fuori dallo schermo a destra
        "y": random.randint(-100, 200)        # altezza casuale del varco
    }


def avanza_e_disegna_tubo(t):
    """
    Sposta il tubo verso sinistra di VEL_AVANZAMENTO pixel e lo disegna.
    Il tubo superiore viene posizionato sopra il varco, quello inferiore sotto.
    Il valore +230 / -230 determina l'ampiezza del varco tra i tubi.
    """
    t["x"] -= VEL_AVANZAMENTO
    schermo.blit(tubo_giu, (t["x"], t["y"] + 230))    # tubo che scende dall'alto
    schermo.blit(tubo_su,  (t["x"], t["y"] - 230))    # tubo che sale dal basso


def collisione_tubo(t, ux, uy, ucc):
    """
    Controlla se l'uccello (posizione ux, uy, immagine ucc) tocca il tubo t.
    Usa una tolleranza di 2px per rendere la hitbox leggermente più piccola
    dell'immagine, così il gioco risulta più giusto.
    Restituisce True se c'è collisione, False altrimenti.
    """
    tol    = 2
    ux_dx  = ux + ucc.get_width()  - tol    # bordo destro uccello
    ux_sx  = ux + tol                        # bordo sinistro uccello
    uy_su  = uy + tol                        # bordo superiore uccello
    uy_giu = uy + ucc.get_height() - tol    # bordo inferiore uccello

    tx_dx  = t["x"] + tubo_giu.get_width()  # bordo destro tubo
    tx_sx  = t["x"]                          # bordo sinistro tubo
    ty_su  = t["y"] - 230 + tubo_su.get_height()  # bordo inferiore tubo superiore
    ty_giu = t["y"] + 230                          # bordo superiore tubo inferiore

    # prima controlla l'allineamento orizzontale, poi quello verticale
    if ux_dx > tx_sx and ux_sx < tx_dx:
        if uy_su < ty_su or uy_giu > ty_giu:
            return True
    return False


def tubo_fra_i_tubi(t, ux, ucc):
    """
    Controlla se l'uccello si trova orizzontalmente dentro il varco del tubo.
    Usato per il sistema di punteggio: quando l'uccello entra e poi esce
    dal varco, viene assegnato un punto.
    Restituisce True se l'uccello è allineato con il tubo.
    """
    tol   = 2
    ux_dx = ux + ucc.get_width() - tol
    ux_sx = ux + tol
    return ux_dx > t["x"] and ux_sx < t["x"] + tubo_giu.get_width()


# ══════════════════════════════════════════════════════════════════════════════
# SEZIONE 5 – INIZIALIZZAZIONE E DISEGNO
# ══════════════════════════════════════════════════════════════════════════════

def inizializza():
    """
    Reimposta tutte le variabili di gioco ai valori iniziali.
    Viene chiamata all'inizio di ogni nuova partita (dal menu o da game over).
    Non cambia la skin né il nome del giocatore.
    """
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
    tubi       = [crea_tubo()]    # parte con un solo tubo


def disegna():
    """
    Disegna tutti gli elementi del frame corrente nell'ordine corretto:
    sfondo → tubi → uccello → base → punteggio.
    L'ordine è importante: gli elementi disegnati dopo appaiono sopra.
    """
    # ── sfondo scorrevole (due copie affiancate) ──
    schermo.blit(sfondo, (int(sfondox), 0))
    schermo.blit(sfondo, (int(sfondox) + 400, 0))

    # ── tubi (avanzano e vengono disegnati insieme) ──
    for t in tubi:
        avanza_e_disegna_tubo(t)

    # ── uccello ──
    schermo.blit(uccello, (uccello_x, uccello_y))

    # ── base (due copie per scorrimento continuo) ──
    schermo.blit(base, (basex, 500))
    schermo.blit(base, (basex + 400, 500))

    # ── punteggio centrato in alto ──
    font = pygame.font.SysFont("Arial", 36, bold=True)
    tp   = font.render(str(punteggio), True, (255, 255, 255))
    schermo.blit(tp, (200 - tp.get_width() // 2, 40))

    pygame.display.update()


# SEZIONE 6 – AVVIO DEL GIOCO


# 1. Mostra prima il login per registrare il nome del giocatore
schermata_login()

# 2. Inizializza le variabili di gioco (senza entrare ancora nel game loop)
inizializza()

# 3. Mostra il menu principale
menu()


# GAME LOOP PRINCIPALE
# Questo ciclo gira a 60 FPS e gestisce tutta la logica del gioco:
# fisica, input, collisioni, punteggio e disegno.

while True:
    clock.tick(FPS)    # limita il loop a FPS fotogrammi al secondo

    # scorrimento base (terreno)
    basex -= VEL_AVANZAMENTO
    if basex <= -400:
        basex = 0       # reset ciclico

    # ── scorrimento sfondo (più lento = effetto parallasse) ──
    sfondox -= VEL_SFONDO
    if sfondox <= -400:
        sfondox = 0.0

    # ── fisica: gravità ──
    velocitay += 0.5          # incremento costante verso il basso
    uccello_y += velocitay    # aggiorna la posizione verticale

    # ── gestione input ──
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            velocitay = -8     # click sinistro → salto

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                velocitay = -8  # spazio → salto
            if evento.key == pygame.K_ESCAPE:
                menu()          # ESC → torna al menu (il game loop riprende dopo)

    # ── gestione tubi: rimozione di quelli usciti a sinistra ──
    tubi = [t for t in tubi if t["x"] > -tubo_giu.get_width()]

    # ── spawn nuovo tubo quando l'ultimo ha superato metà schermo ──
    if tubi[-1]["x"] < 200:
        tubi.append(crea_tubo())

    # ── rilevamento collisioni con i tubi ──
    for t in tubi:
        if collisione_tubo(t, uccello_x, uccello_y, uccello):
            hai_perso()    # mostra game over e aggiorna JSON
            break

    # ── sistema di punteggio ──
    # Salva lo stato precedente, poi ricalcola.
    # Se prima l'uccello era nel varco e ora non lo è più → ha superato il tubo → +1 punto.
    era_tra_i_tubi = fra_i_tubi
    fra_i_tubi     = any(tubo_fra_i_tubi(t, uccello_x, uccello) for t in tubi)
    if era_tra_i_tubi and not fra_i_tubi:
        punteggio += 1

    # ── collisione con il suolo o uscita dall'alto ──
    if uccello_y > 480 or uccello_y < 0:
        hai_perso()

    # ── disegna il frame ──
    disegna()