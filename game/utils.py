import pygame


# Ta fonction pour le texte libre (très bien pour les titres !)
def draw_centered_text(text, y, color, font, screen):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(rendered_text, text_rect)
    return text_rect

# Ta nouvelle fonction de bouton tout-en-un
# Remarque : j'ai ajouté 'font' et un 'text_color' qui est noir par défaut
def draw_button(x, y, width, height, color, text, font, screen, text_color="black"):
    border_radius = 20

    button_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)

    rendered_text = font.render(text, True, text_color)

    text_rect = rendered_text.get_rect(center=button_rect.center)
    screen.blit(rendered_text, text_rect)
    return button_rect

def draw_hover_button(x, y, width, height, color, text, font, screen,over_color, text_color="black"):
    border_radius = 20
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)

    rendered_text = font.render(text, True, text_color)

    text_rect = rendered_text.get_rect(center=button_rect.center)
    if button_rect.collidepoint(mouse_x,mouse_y):
        pygame.draw.rect(screen,over_color,button_rect, border_radius=15)
    screen.blit(rendered_text, text_rect)
    return button_rect


# On ajoute les paramètres dont la fonction a besoin pour travailler !
def confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
    """ Affiche une fenêtre de confirmation """

    # 1. On crée une horloge locale pour ne pas faire exploser le processeur
    clock = pygame.time.Clock()

    # 2. LA MAGIE : On prend une "photo" de l'écran de jeu actuel
    fond_ecran = screen.copy()

    # 3. On prépare le voile noir UNE SEULE FOIS
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))

    while True:  # Pas besoin de variable 'confirming', le 'return' arrête la boucle

        # --- DESSIN ---
        # A. On colle la "photo" de base pour effacer l'image précédente
        screen.blit(fond_ecran, (0, 0))

        # B. On applique le voile noir par-dessus
        screen.blit(overlay, (0, 0))

        # C. Dessin de la boîte de dialogue
        dialog_rect = pygame.Rect(0, 0, 400, 200)
        dialog_rect.center = (WIDTH // 2, HEIGHT // 2)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, border_radius=15)

        # D. Texte de confirmation
        msg = font_bouton.render("Voulez-vous quitter ?", True, "black")
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        screen.blit(msg, msg_rect)


        oui = draw_hover_button(WIDTH//2-110,HEIGHT//2+20,100,50,"gray","Oui",font_bouton,screen,"red","white")
        non = draw_hover_button(WIDTH//2+10,HEIGHT//2+20,100,50,"gray","Non",font_bouton,screen,"green","white")


        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if oui.collidepoint(event.pos):
                    return True  # On quitte
                if non.collidepoint(event.pos):
                    return False  # On revient au jeu

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # On annule avec Echap

        # On limite à 60 images par seconde
        clock.tick(60)