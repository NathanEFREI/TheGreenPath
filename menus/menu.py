import json
import os

from menus.creer_partie import creer_party
from constante import FPS
from game.cinematique import SceneCinematique
from game.game import Game
from game.utils import draw_hover_button, confirm_quit
from game.parametre import afficher_parametres
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
DEFAULT_VOLUME = 0.4


def load_volume():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, dict):
            return float(data.get("volume", DEFAULT_VOLUME))
    except Exception:
        pass
    return DEFAULT_VOLUME


def save_volume(volume):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
            json.dump({"volume": float(volume)}, file, indent=4)
    except Exception:
        pass


def main_menu():
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    running = True
    clock = pygame.time.Clock()

    pos_x = (WIDTH // 2) - ((WIDTH / 2.5) / 2)
    fonttitle  = pygame.font.SysFont("comicsansms", 80)
    font_bouton = pygame.font.SysFont("calibri", 35, bold=True)
    texttitle  = fonttitle.render("The Green Path", True, "black")

    # États du popup
    active1      = False
    active2      = False
    fenetre      = False
    darken_overlay = False
    nom_partie   = ""
    nom_joueur   = ""
    fenetre_param = False
    volume = load_volume()

    while running:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
                    running = False
                    cine.terminee = True  # Assure que la cinématique se ferme aussi

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if fenetre:
                        # Ferme le popup avec Échap
                        fenetre        = False
                        darken_overlay = False
                        active1        = False
                        active2        = False
                    else:
                        if confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
                            running = False
                            cine.terminee = True
                            

                elif fenetre:
                    # --- Saisie clavier dans les boîtes ---
                    if event.key == pygame.K_BACKSPACE:
                        if active1:
                            nom_partie = nom_partie[:-1]
                        elif active2:
                            nom_joueur = nom_joueur[:-1]
                    elif event.key == pygame.K_TAB:
                        # Tab bascule entre les deux boîtes
                        active1, active2 = active2, active1
                    else:
                        if active1 and len(nom_partie) < 20:
                            nom_partie += event.unicode
                        elif active2 and len(nom_joueur) < 20:
                            nom_joueur += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fenetre:
                    if input_box1.collidepoint(mouse_x, mouse_y):
                        active1, active2 = True, False
                    elif input_box2.collidepoint(mouse_x, mouse_y):
                        active1, active2 = False, True
                    elif bouton_jouer.collidepoint(mouse_x, mouse_y):
                        # Validation : on lance la cinématique
                        if nom_partie.strip() and nom_joueur.strip():
                            running = False   # sort du menu
                    elif not rect_popup.collidepoint(mouse_x, mouse_y):
                        fenetre        = False
                        darken_overlay = False
                        active1        = False
                        active2        = False
                elif fenetre_param:
                    if barre_fond.collidepoint(mouse_x, mouse_y):
                        relative_x = mouse_x - barre_fond.x
                        volume = max(0.0, min(1.0, relative_x / barre_fond.width))
                        pygame.mixer.music.set_volume(volume)
                        save_volume(volume)
                    elif btn_retour.collidepoint(mouse_x, mouse_y):
                        fenetre_param = False
                        darken_overlay = False
                    elif not rect_popup.collidepoint(mouse_x, mouse_y):
                        fenetre_param = False
                        darken_overlay = False
                else:
                    if rect1.collidepoint(mouse_x, mouse_y):
                        fenetre = True
                        darken_overlay = True
                    elif rect3.collidepoint(mouse_x, mouse_y):
                        fenetre_param = True
                        darken_overlay = True
                    elif rect4.collidepoint(mouse_x, mouse_y):
                        if confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
                            running = False
                            cine.terminee = True

        # --- Dessin ---
        screen.fill("green")
        rect1 = draw_hover_button(pos_x, HEIGHT * 0.2, WIDTH / 2.5, HEIGHT / 6,
                                  "orange", "Créer une partie", font_bouton, screen, "darkorchid1")
        rect2 = draw_hover_button(pos_x, HEIGHT * 0.4, WIDTH / 2.5, HEIGHT / 6,
                                  "orange", "Charger une partie", font_bouton, screen, "darkorchid1")
        rect3 = draw_hover_button(pos_x, HEIGHT * 0.6, WIDTH / 2.5, HEIGHT / 6,
                                  "orange", "Paramètre", font_bouton, screen, "darkorchid1")
        rect4 = draw_hover_button(pos_x, HEIGHT * 0.8, WIDTH / 2.5, HEIGHT / 6,
                                  "orange", "Quittez", font_bouton, screen, "darkorchid1")

        if darken_overlay:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            screen.blit(overlay, (0, 0))

        rect_titre = texttitle.get_rect(center=(WIDTH // 2, HEIGHT * 0.1))
        screen.blit(texttitle, rect_titre)

        if fenetre:
            rect_popup, input_box2, input_box1, bouton_jouer = creer_party(
                screen, WIDTH, HEIGHT, active1, active2, nom_partie, nom_joueur
            )
        
        if fenetre_param:
            rect_popup, barre_fond, btn_retour = afficher_parametres(
                screen, WIDTH, HEIGHT, volume
            )

        pygame.display.flip()
        clock.tick(FPS)

    # --- Lancement de la cinématique ---
    game = Game(volume=volume)

    def lancer_jeu():
        game.run()

    cine = SceneCinematique(game.screen, volume = volume, callback_fin=lancer_jeu)
    clock_cine = pygame.time.Clock()

    while not cine.terminee:
        dt = clock_cine.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass  #On veut pas que l'on puisse femer la cinématique.
            cine.handle_event(event)
        cine.update(dt)
        cine.draw()
        pygame.display.flip()
    lancer_jeu()

    pygame.quit()

