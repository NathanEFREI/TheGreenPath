import pygame

class MenuTri:
    def __init__(self, poubelle_rect, option1_img, option2_img, type1, type2):
        self.active = True
        #bulles à gauche et à droite au-dessus de la poubelle
        self.rect1 = option1_img.get_rect(midbottom=(poubelle_rect.left - 20, poubelle_rect.top - 20))
        self.rect2 = option2_img.get_rect(midbottom=(poubelle_rect.right + 20, poubelle_rect.top - 20))
        
        self.img1 = option1_img
        self.img2 = option2_img
        self.type1 = type1 
        self.type2 = type2 

    def draw(self, screen):
        #cercles de fond pour faire ressortir les icônes
        pygame.draw.circle(screen, (240, 240, 240), self.rect1.center, 35)
        pygame.draw.circle(screen, (240, 240, 240), self.rect2.center, 35)
        #Dessiner les images
        screen.blit(self.img1, self.rect1)
        screen.blit(self.img2, self.rect2)

    def check_click(self, mouse_pos):
        if self.rect1.collidepoint(mouse_pos):
            return self.type1
        if self.rect2.collidepoint(mouse_pos):
            return self.type2
        return None