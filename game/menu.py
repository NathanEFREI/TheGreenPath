import pygame

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()
rect1 = pygame.rect.Rect(0,HEIGHT*0.25,WIDTH/2.5, HEIGHT/6)
rect2 = pygame.rect.Rect(0,HEIGHT*0.45,WIDTH/2.5, HEIGHT/6)
rect3 = pygame.rect.Rect(0,HEIGHT*0.65,WIDTH/2.5, HEIGHT/6)
fonttitle = pygame.font.SysFont("comicsansms", 80)
font_bouton = pygame.font.SysFont("calibri", 35, bold=True)
texttitle = fonttitle.render("The Green Path", True, "black")
text_button1 = font_bouton.render("Créer une partie ", True, "black")
text_button2 = font_bouton.render("Charger une partie ", True, "black")
text_button3 = font_bouton.render("Paramètre", True, "black")
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False
    screen.fill("green")
    rect1.centerx = WIDTH//2
    rect2.centerx = WIDTH//2
    rect3.centerx = WIDTH//2
    pygame.draw.rect(screen,pygame.Color("orange"),rect2,border_radius=15)
    pygame.draw.rect(screen, pygame.Color("orange"), rect1, border_radius=15)
    pygame.draw.rect(screen, pygame.Color("orange"), rect3, border_radius=15)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if rect1.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, pygame.Color("darkorchid1"), rect1, border_radius=15)
    if rect2.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, pygame.Color("darkorchid1"), rect2, border_radius=15)
    if rect3.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, pygame.Color("darkorchid1"), rect3, border_radius=15)
    rect_titre = texttitle.get_rect()
    rect_titre.center = (WIDTH//2,HEIGHT*0.1)
    rect_text1 = text_button1.get_rect()
    rect_text2 = text_button2.get_rect()
    rect_text3 = text_button3.get_rect()
    rect_text1.center = rect1.center
    rect_text2.center = rect2.center
    rect_text3.center = rect3.center
    screen.blit(texttitle, rect_titre)
    screen.blit(text_button1, rect_text1)
    screen.blit(text_button2, rect_text2)
    screen.blit(text_button3, rect_text3)
    pygame.display.flip()
    clock.tick(120)
pygame.quit()
