import pygame
import os

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.assets = []
        for i in range(0,6):
            base_path = os.path.dirname(__file__)
            img = pygame.image.load(os.path.join(base_path, '..', 'assets', 'hero' + str(i) + '.png')).convert_alpha()
            self.assets.append(img)
            self.image = self.assets[0]
            self.rect = self.image.get_rect()
            self.velocity = 1
            self.rect.x = 500
            self.rect.y = 400
         
    def move_left(self):
        self.rect.x -= self.velocity

    def move_right(self):
        self.rect.x += self.velocity