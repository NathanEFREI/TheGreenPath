import pygame

class Poubelle:
    def __init__(self, x, y, image, couleur_nom, dechet_attendu):
        self.image = image 
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.type = couleur_nom
        self.dechet_attendu = dechet_attendu 
        self.reussie = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)