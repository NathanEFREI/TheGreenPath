import pygame

#from game.menu import mouse_x


def creer_party(screen, width, height):

        popup_w = width * 0.8
        popup_h = height * 0.7
        rect_popup = pygame.Rect(0, 0, popup_w, popup_h)
        rect_popup.center = (width // 2, height // 2)
        input_box1 = pygame.Rect(popup_w * 0.23, popup_h * 0.55, popup_w * 0.35, popup_h * 0.07)#1 (largeur de l'écran), 2(hauteur de l'écran), 3 largeur de la vairable, 4 hauteur de la variable
        input_box2 = pygame.Rect(popup_w * 0.23, popup_h * 0.85, popup_w * 0.35, popup_h * 0.07)#1 (largeur de l'écran), 2(hauteur de l'écran), 3 largeur de la vairable, 4 hauteur de la variable
        active = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, pygame.Color("lightgrey"), rect_popup, border_radius=20)

        pygame.draw.rect(screen, pygame.Color("dimgrey"), rect_popup, width=5, border_radius=20)
        font_bouton = pygame.font.SysFont("calibri", 35, bold=True)
        text1 = font_bouton.render("Choisir le nom de votre partie ", True, "black")
        text2 = font_bouton.render("Choisir le nom de votre joueur ", True, "black")
        marge_gauche = rect_popup.width * 0.10
        pos_x = rect_popup.left + marge_gauche

        # 2. On calcule les positions Y (ex: 25% de la hauteur pour le 1er, 55% pour le 2ème)
        pos_y1 = rect_popup.top + (rect_popup.height * 0.25)
        pos_y2 = rect_popup.top + (rect_popup.height * 0.55)

        # 3. On place les rectangles de texte en alignant leur "milieu-gauche" (midleft)
        rect_text1 = text1.get_rect(midleft=(pos_x, pos_y1))
        rect_text2 = text2.get_rect(midleft=(pos_x, pos_y2))

        # 4. On les affiche
        screen.blit(text1, rect_text1)
        screen.blit(text2, rect_text2)
        pygame.draw.rect(screen, pygame.Color("white"), input_box1, 2)
        pygame.draw.rect(screen, pygame.Color("white"), input_box2, 2)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box1.collidepoint(mouse_x, mouse_y):
                active = True
        if active :
            print("joueur")
        else :
            print("joueurfaux")
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