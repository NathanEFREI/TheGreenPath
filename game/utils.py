import pygame


import pygame

# Dessine un texte centré horizontalement sur l'écran.
def draw_centered_text(text, y, color, font, screen):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(rendered_text, text_rect)
    return text_rect


# Dessine un bouton simple avec texte centré.
# Retourne le rectangle du bouton pour détecter les clics.
def draw_button(x, y, width, height, color, text, font, screen, text_color="black"):
    border_radius = 20
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)
    rendered_text = font.render(text, True, text_color)
    text_rect = rendered_text.get_rect(center=button_rect.center)
    screen.blit(rendered_text, text_rect)
    return button_rect


def draw_hover_button(x, y, width, height, color, text, font, screen, over_color, text_color="black"):
    border_radius = 20
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)
    rendered_text = font.render(text, True, text_color)
    text_rect = rendered_text.get_rect(center=button_rect.center)
    # Change visuellement la couleur du bouton lorsque la souris passe dessus.
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, over_color, button_rect, border_radius=15)
    screen.blit(rendered_text, text_rect)
    return button_rect


def confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
    """Affiche une boîte de confirmation avant de quitter le jeu."""

    # Crée une horloge locale pour limiter la boucle d'affichage.
    clock = pygame.time.Clock()

    # On conserve une capture de l'écran actuel pour pouvoir dessiner le menu sans le
    # redessiner depuis zéro à chaque frame.
    fond_ecran = screen.copy()

    # Prépare un voile semi-transparent pour assombrir l'arrière-plan.
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))

    while True:
        screen.blit(fond_ecran, (0, 0))
        screen.blit(overlay, (0, 0))

        dialog_rect = pygame.Rect(0, 0, 400, 200)
        dialog_rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, border_radius=15)

        msg = font_bouton.render("Voulez-vous quitter ?", True, "black")
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(msg, msg_rect)

        oui = draw_hover_button(WIDTH // 2 - 110, HEIGHT // 2 + 20, 100, 50, "gray", "Oui", font_bouton, screen, "red", "white")
        non = draw_hover_button(WIDTH // 2 + 10, HEIGHT // 2 + 20, 100, 50, "gray", "Non", font_bouton, screen, "green", "white")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if oui.collidepoint(event.pos):
                    return True
                if non.collidepoint(event.pos):
                    return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        clock.tick(60)