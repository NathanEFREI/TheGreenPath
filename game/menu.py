from menus.creer_partie import *
from utils import *
FPS = 120


pygame.init()   #initialiser pygame
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h #prend la taille de l'écran au max
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()
# Création des rectangles
pos_x = (WIDTH // 2) - ((WIDTH / 2.5)/2)
fonttitle = pygame.font.SysFont("comicsansms", 80) #police et taille pour le titre
font_bouton = pygame.font.SysFont("calibri", 35, bold=True) #police et taille pour les boutons
#couleurs et texte :
texttitle = fonttitle.render("The Green Path", True, "black")
active1,active2 = False,False
fenetre = False
darken_overlay = False
rect_popup,inputbox2,inputbox1 = creer_party(screen, WIDTH, HEIGHT,active1,active2)
while running:
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed() #prend les touches du clavier
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
                running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            if fenetre:
                if inputbox1.collidepoint(mouse_x, mouse_y):
                    active1 = True
                    active2 = False
                    print("j1")
                elif inputbox2.collidepoint(mouse_x, mouse_y):
                    active2 = True
                    active1 = False
                    print("j2")

                elif not rect_popup.collidepoint(mouse_x, mouse_y):
                    fenetre = False
                    darken_overlay = False
                    active1 = False
                    active2 = False

            # CAS 2 : Le popup est FERMÉ (On est sur le menu principal)
            else:
                if rect1.collidepoint(mouse_x, mouse_y):
                    fenetre = True
                    darken_overlay = True
                elif rect4.collidepoint(mouse_x, mouse_y):
                    if confirm_quit(screen, WIDTH, HEIGHT, font_bouton):
                        running = False
    screen.fill("green") #couleur de l'écran

    #afficher les rectangles

    rect1 = draw_hover_button(pos_x, HEIGHT * 0.2, WIDTH / 2.5, HEIGHT / 6, "orange", "Créer une partie", font_bouton,
                        screen,"darkorchid1")
    rect2 = draw_hover_button(pos_x, HEIGHT * 0.4, WIDTH / 2.5, HEIGHT / 6, "orange", "Charger une partie", font_bouton,
                        screen,"darkorchid1")
    rect3 = draw_hover_button(pos_x, HEIGHT * 0.6, WIDTH / 2.5, HEIGHT / 6, "orange", "Paramètre", font_bouton,
                        screen,"darkorchid1")
    rect4 = draw_hover_button(pos_x, HEIGHT*0.8, WIDTH/2.5, HEIGHT/6, "orange", "Quittez", font_bouton,
                              screen,"darkorchid1")

    #permet de centrer les textes
    if darken_overlay:
        # Dessiner un overlay sombre
        overlay = pygame.Surface((WIDTH,HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # Opacité de l'overlay
        screen.blit(overlay, (0, 0))
    rect_titre = texttitle.get_rect()
    rect_titre.center = (WIDTH//2,HEIGHT*0.1)

    #affichage des textes
    screen.blit(texttitle, rect_titre)


    if fenetre :
        creer_party(screen, WIDTH, HEIGHT,active1,active2)

    pygame.display.flip()
    clock.tick(FPS) #limite de fps
pygame.quit()
