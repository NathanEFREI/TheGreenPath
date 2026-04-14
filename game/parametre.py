import pygame
from game.utils import draw_hover_button


def afficher_parametres(screen, WIDTH, HEIGHT, volume_actuel):
    """Affiche le menu des paramètres au-dessus de l'écran de jeu."""

    # Le popup de paramètres occupe 60% de la largeur et de la hauteur de l'écran.
    rect_popup = pygame.Rect(0, 0, WIDTH * 0.6, HEIGHT * 0.6)
    rect_popup.center = (WIDTH // 2, HEIGHT // 2)

    # Dessin du rectangle de fond du popup et de la bordure.
    pygame.draw.rect(screen, (50, 50, 50), rect_popup, border_radius=15)
    pygame.draw.rect(screen, "white", rect_popup, 3, border_radius=15)

    font = pygame.font.SysFont("calibri", 30, bold=True)

    # Titre principal du menu de paramètres.
    titre = font.render("PARAMÈTRES", True, "white")
    screen.blit(titre, (rect_popup.x + 20, rect_popup.y + 20))

    # Affichage du pourcentage de volume actuel.
    txt_vol = font.render(f"Volume : {int(volume_actuel * 100)}%", True, "white")
    screen.blit(txt_vol, (rect_popup.x + 50, rect_popup.y + 100))

    # Dessine la barre de fond du réglage du volume.
    barre_fond = pygame.Rect(rect_popup.x + 50, rect_popup.y + 140, rect_popup.width - 100, 20)
    pygame.draw.rect(screen, (100, 100, 100), barre_fond)

    # Dessine le niveau de volume actuel comme une barre colorée.
    barre_volume = pygame.Rect(rect_popup.x + 50, rect_popup.y + 140, (rect_popup.width - 100) * volume_actuel, 20)
    pygame.draw.rect(screen, "orange", barre_volume)

    # Bouton de retour pour fermer le menu des paramètres.
    btn_retour = draw_hover_button(
        rect_popup.centerx - 100,
        rect_popup.bottom - 80,
        200,
        50,
        "gray",
        "Retour",
        font,
        screen,
        "red",
        "white"
    )

    return rect_popup, barre_fond, btn_retour