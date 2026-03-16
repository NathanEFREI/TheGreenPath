import pygame
from menus.creer_partie import *

FPS = 120

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
fonttitle = pygame.font.SysFont("comicsansms", 80) #police et taille pour le titre
font_bouton = pygame.font.SysFont("calibri", 35, bold=True) #police et taille pour les boutons
#couleurs et texte :
texttitle = fonttitle.render("The Green Path", True, "black")
text_button1 = font_bouton.render("Créer une partie ", True, "black")
text_button2 = font_bouton.render("Charger une partie ", True, "black")
text_button3 = font_bouton.render("Paramètre", True, "black")
fenetre = False
rect_popup = creer_party(screen, WIDTH, HEIGHT)
while running:
    keys = pygame.key.get_pressed() #prend les touches du clavier
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]: #permet de quitter
            running = False
    screen.fill("green") #couleur de l'écran
    #centrer les rectangles sur l'axe des abscisses
    rect1.centerx = WIDTH//2
    rect2.centerx = WIDTH//2
    rect3.centerx = WIDTH//2
    #afficher les rectangles
    pygame.draw.rect(screen,pygame.Color("orange"),rect2,border_radius=15)
    pygame.draw.rect(screen, pygame.Color("orange"), rect1, border_radius=15)
    pygame.draw.rect(screen, pygame.Color("orange"), rect3, border_radius=15)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #change la couleur des rectangles au survol
    if rect1.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, pygame.Color("darkorchid1"), rect1, border_radius=15)
    if rect2.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, pygame.Color("darkorchid1"), rect2, border_radius=15)
    if rect3.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, pygame.Color("darkorchid1"), rect3, border_radius=15)
    #permet de centrer les textes
    rect_titre = texttitle.get_rect()
    rect_titre.center = (WIDTH//2,HEIGHT*0.1)
    rect_text1 = text_button1.get_rect()
    rect_text2 = text_button2.get_rect()
    rect_text3 = text_button3.get_rect()
    rect_text1.center = rect1.center
    rect_text2.center = rect2.center
    rect_text3.center = rect3.center
    #affichage des textes
    screen.blit(texttitle, rect_titre)
    screen.blit(text_button1, rect_text1)
    screen.blit(text_button2, rect_text2)
    screen.blit(text_button3, rect_text3)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if not fenetre and rect1.collidepoint(mouse_x, mouse_y):
                fenetre = True
        if not rect_popup.collidepoint(mouse_x, mouse_y):
            fenetre = False
    if fenetre :
        creer_party(screen, WIDTH, HEIGHT)

    pygame.display.flip()
    clock.tick(FPS) #limite de fps
pygame.quit()
