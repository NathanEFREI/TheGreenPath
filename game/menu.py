import pygame

#CONSTANTES RÉAJUSTABLE
FPS = 60

pygame.init()   #initialiser pygame
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h #prend la taille de l'écran au max
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()
#création des rectangles
rect1 = pygame.rect.Rect(0,HEIGHT*0.25,WIDTH/2.5, HEIGHT/6)
rect2 = pygame.rect.Rect(0,HEIGHT*0.45,WIDTH/2.5, HEIGHT/6)
rect3 = pygame.rect.Rect(0,HEIGHT*0.65,WIDTH/2.5, HEIGHT/6)
rect_quit = pygame.rect.Rect(0, HEIGHT*0.85, WIDTH/2.5, HEIGHT/6) 
fonttitle = pygame.font.SysFont("comicsansms", 80) #police et taille pour le titre
font_bouton = pygame.font.SysFont("calibri", 35, bold=True) #police et taille pour les boutons
#couleurs et texte :
texttitle = fonttitle.render("The Green Path", True, "black")
text_button1 = font_bouton.render("Créer une partie ", True, "black")
text_button2 = font_bouton.render("Charger une partie ", True, "black")
text_button3 = font_bouton.render("Paramètre", True, "black")
text_buttonquit = font_bouton.render("Quitter le jeu", True, "black")
def confirm_quit():
    """ Affiche une fenêtre de confirmation """
    confirming = True
    while confirming:
        # Création d'un overlay semi-transparent
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0,0))
        # Dessin de la boîte de dialogue
        dialog_rect = pygame.Rect(0, 0, 400, 200)
        dialog_rect.center = (WIDTH//2, HEIGHT//2)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, border_radius=15)
        
        # Texte de confirmation
        msg = font_bouton.render("Voulez vous quitter ?", True, "black")
        msg_rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        screen.blit(msg, msg_rect)

        # Boutons Oui / Non
        btn_yes = pygame.Rect(WIDTH//2 - 110, HEIGHT//2 + 20, 100, 50)
        btn_no = pygame.Rect(WIDTH//2 + 10, HEIGHT//2 + 20, 100, 50)
        
        pygame.draw.rect(screen, "red", btn_yes, border_radius=10)
        pygame.draw.rect(screen, "gray", btn_no, border_radius=10)

        screen.blit(font_bouton.render("OUI", True, "white"), (btn_yes.centerx-25, btn_yes.centery-15))
        screen.blit(font_bouton.render("NON", True, "white"), (btn_no.centerx-25, btn_no.centery-15))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_yes.collidepoint(event.pos):
                    return True # On quitte
                if btn_no.collidepoint(event.pos):
                    return False # On revient au menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False


while running:
    keys = pygame.key.get_pressed() #prend les touches du clavier
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]: #permet de quitter
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if confirm_quit():
                    running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 1 = Clic gauche
                # On vérifie si la souris est sur le bouton Quitter au moment du clic
                if rect_quit.collidepoint(event.pos):
                    if confirm_quit(): # Appel de la confirmation sur le bouton
                        running = False
    

    screen.fill("green") #couleur de l'écran

    for r in [rect1, rect2, rect3, rect_quit]:
        r.centerx = WIDTH // 2

    # Affichage et gestion du survol
    buttons = [(rect1, text_button1), (rect2, text_button2), (rect3, text_button3), (rect_quit, text_buttonquit)]
    
    for rect, text in buttons:
        color = "darkorchid1" if rect.collidepoint(mouse_pos) else "orange"
        pygame.draw.rect(screen, pygame.Color(color), rect, border_radius=15)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Titre
    rect_titre = texttitle.get_rect(center=(WIDTH//2, HEIGHT*0.1))
    screen.blit(texttitle, rect_titre)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
