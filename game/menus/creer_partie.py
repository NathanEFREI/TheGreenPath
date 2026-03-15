import pygame

def creer_party(screen, width, height):
        # 1. On crée le rectangle du "Popup" (ex: 80% de la largeur, 70% de la hauteur)
        popup_w = width * 0.8
        popup_h = height * 0.7
        rect_popup = pygame.Rect(0, 0, popup_w, popup_h)
        rect_popup.center = (width // 2, height // 2)

        # 2. On dessine le fond du popup (ex: gris clair) avec des bords arrondis
        pygame.draw.rect(screen, pygame.Color("lightgrey"), rect_popup, border_radius=20)

        # 3. On ajoute une bordure plus foncée pour faire joli
        pygame.draw.rect(screen, pygame.Color("dimgrey"), rect_popup, width=5, border_radius=20)
        return rect_popup

if __name__ == "__main__":
    pygame.init()
    # On simule la fenêtre de ton jeu principal
    test_screen = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        test_screen.fill("white")  # On met un fond blanc pour le test

        # On simule la taille actuelle
        w, h = test_screen.get_width(), test_screen.get_height()

        # ON APPELLE TA FONCTION POUR VOIR LE RÉSULTAT
        creer_party(test_screen, w, h)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()