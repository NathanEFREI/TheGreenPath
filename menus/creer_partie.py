import pygame


def creer_party(screen, width, height, active1, active2, nom_partie="", nom_joueur=""):
    """
    Affiche le popup pour saisir le nom de la partie et le nom du joueur.
    """
    
    popup_w = width * 0.6
    popup_h = height * 0.5
    rect_popup = pygame.Rect(0, 0, popup_w, popup_h)
    rect_popup.center = (width // 2, height // 2)

    # Prépare les polices de texte pour le titre, les labels, les champs et le bouton.
    font_titre = pygame.font.SysFont("calibri", 40, bold=True)
    font_bouton = pygame.font.SysFont("calibri", 30, bold=True)
    font_label = pygame.font.SysFont("calibri", 28)
    font_input = pygame.font.SysFont("calibri", 26)

    # --- Fond du popup ---
    pygame.draw.rect(screen, pygame.Color("lightgrey"), rect_popup, border_radius=20)
    pygame.draw.rect(screen, pygame.Color("dimgrey"), rect_popup, width=5, border_radius=20)

    # --- Titre ---
    titre = font_titre.render("Nouvelle partie", True, "black")
    rect_titre = titre.get_rect(centerx=rect_popup.centerx, top=rect_popup.top + 18)
    screen.blit(titre, rect_titre)

    # --- Positions des labels et boîtes ---
    marge_gauche = rect_popup.left + popup_w * 0.10
    box_w = popup_w * 0.80
    box_h = popup_h * 0.10

    # Label + champ de saisie pour le nom de la partie
    label1 = font_label.render("Nom de la partie :", True, "black")
    rect_label1 = label1.get_rect(midleft=(marge_gauche, rect_popup.top + popup_h * 0.28))
    screen.blit(label1, rect_label1)
    input_box1 = pygame.Rect(marge_gauche, rect_label1.bottom + 6, box_w, box_h)

    # Label + champ de saisie pour le nom du joueur
    label2 = font_label.render("Nom du joueur :", True, "black")
    rect_label2 = label2.get_rect(midleft=(marge_gauche, rect_popup.top + popup_h * 0.58))
    screen.blit(label2, rect_label2)
    input_box2 = pygame.Rect(marge_gauche, rect_label2.bottom + 6, box_w, box_h)

    # --- Dessin des boîtes de saisie ---
    couleur_box1 = pygame.Color("royalblue") if active1 else pygame.Color("white")
    couleur_box2 = pygame.Color("royalblue") if active2 else pygame.Color("white")

    pygame.draw.rect(screen, pygame.Color("white"), input_box1, border_radius=8)
    pygame.draw.rect(screen, couleur_box1, input_box1, width=3, border_radius=8)
    pygame.draw.rect(screen, pygame.Color("white"), input_box2, border_radius=8)
    pygame.draw.rect(screen, couleur_box2, input_box2, width=3, border_radius=8)

    # --- Texte saisi ---
    if nom_partie:
        surf_nom_partie = font_input.render(nom_partie, True, "black")
        screen.blit(surf_nom_partie, surf_nom_partie.get_rect(
            midleft=(input_box1.left + 10, input_box1.centery)
        ))

    if nom_joueur:
        surf_nom_joueur = font_input.render(nom_joueur, True, "black")
        screen.blit(surf_nom_joueur, surf_nom_joueur.get_rect(
            midleft=(input_box2.left + 10, input_box2.centery)
        ))

    # --- Curseur clignotant dans la boîte active ---
    if (pygame.time.get_ticks() // 500) % 2 == 0:
        if active1:
            largeur_texte = font_input.size(nom_partie)[0]
            cx = input_box1.left + 10 + largeur_texte + 2
            pygame.draw.line(screen, "black",
                             (cx, input_box1.top + 8),
                             (cx, input_box1.bottom - 8), 2)
        if active2:
            largeur_texte = font_input.size(nom_joueur)[0]
            cx = input_box2.left + 10 + largeur_texte + 2
            pygame.draw.line(screen, "black",
                             (cx, input_box2.top + 8),
                             (cx, input_box2.bottom - 8), 2)

    # --- Bouton Jouer ---
    bouton_jouer = pygame.Rect(0, 0, popup_w * 0.35, popup_h * 0.13)
    bouton_jouer.centerx = rect_popup.centerx
    bouton_jouer.top     = input_box2.bottom + 18

    mouse_x, mouse_y = pygame.mouse.get_pos()
    couleur_jouer = pygame.Color("darkorchid1") if bouton_jouer.collidepoint(mouse_x, mouse_y) \
                    else pygame.Color("orange")
    pygame.draw.rect(screen, couleur_jouer, bouton_jouer, border_radius=15)
    txt_jouer = font_bouton.render("Jouer !", True, "black")
    screen.blit(txt_jouer, txt_jouer.get_rect(center=bouton_jouer.center))

    return rect_popup, input_box2, input_box1, bouton_jouer