import pygame
import os

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.assets = []
        for i in range(0,6):
            base_path = os.path.dirname(__file__)
            img = pygame.image.load(os.path.join(base_path, '..', 'assets', 'hero' + str(i) + '.png')).convert_alpha()
            img = pygame.transform.scale_by(img, 2)
            self.assets.append(img)
            self.current_sprite = 0
            self.image = self.assets[self.current_sprite]
            self.rect = self.image.get_rect()
            
        self.velocity = 3
        self.rect.x = 500
        self.rect.y = 750

#permet de changer de sprite pour animer le personnage
    def update(self):
        self.current_sprite+= 0.2  #ralentir l'animation pour la rendre plus naturel
        if self.current_sprite>=len(self.assets):
            self.current_sprite=0

        self.image= self.assets[int(self.current_sprite)] 

#animation + avancé le personnage avec un rotation vers la gauche         
    def move_left(self):
        self.rect.x -= self.velocity
        self.update()
        self.image = pygame.transform.flip(self.image, True, False) 

#animation + avancé le personnage
    def move_right(self):
        self.rect.x += self.velocity
        self.update()