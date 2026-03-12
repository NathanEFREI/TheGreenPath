import pygame
import os

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.assets = []
        for i in range(0,6):
            img = pygame.image.load(os.path.join('assets', 'hero' + str(i) + '.png')).convert()
            self.assets.append(img)
            self.image = self.assets[0]
            self.rect = self.image.get_rect()
        