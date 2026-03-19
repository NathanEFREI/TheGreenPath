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

fenetre = False
darken_overlay = False
rect_popup = creer_party(screen, WIDTH, HEIGHT)
while running:
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    keys = pygame.key.get_pressed() #prend les touches du clavier
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]: #permet de quitter
            running = False
    screen.fill("green") #couleur de l'écran

    #afficher les rectangles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rect1 = draw_hover_button(pos_x, HEIGHT * 0.25, WIDTH / 2.5, HEIGHT / 6, "orange", "Créer une partie", font_bouton,
                        screen,"darkorchid1")
    rect2 = draw_hover_button(pos_x, HEIGHT * 0.45, WIDTH / 2.5, HEIGHT / 6, "orange", "Charger une partie", font_bouton,
                        screen,"darkorchid1")
    rect3 = draw_hover_button(pos_x, HEIGHT * 0.65, WIDTH / 2.5, HEIGHT / 6, "orange", "Paramètre", font_bouton,
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

    if event.type == pygame.MOUSEBUTTONDOWN:
        if not fenetre and rect1.collidepoint(mouse_x, mouse_y):
                fenetre = True
                darken_overlay = True
        if not rect_popup.collidepoint(mouse_x, mouse_y):
            fenetre = False
            darken_overlay = False
    if fenetre :
        creer_party(screen, WIDTH, HEIGHT)

    pygame.display.flip()
    clock.tick(FPS) #limite de fps
pygame.quit()
