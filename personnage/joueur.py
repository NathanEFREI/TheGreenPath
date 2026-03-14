import pygame
import os

#CONSTANTE RÉAJUSTABLE
VELOCITY = 3
PLAYER_SCALE = 2.5
HEIGHT = 735
WIDTH = 200

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.assets = []
        info = pygame.display.Info()
        # Récupérer la résolution de l'écran 
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        for i in range(0,6):
            base_path = os.path.dirname(__file__)
            img = pygame.image.load(os.path.join(base_path, '..', 'assets', 'hero' + str(i) + '.png')).convert_alpha()
            img = pygame.transform.scale_by(img, PLAYER_SCALE)
            self.assets.append(img)
            self.current_sprite = 0
            self.image = self.assets[self.current_sprite]
            self.rect = self.image.get_rect()
        #adapter la position du joueur
        self.velocity = VELOCITY
        x_ratio = WIDTH / self.WIDTH
        y_ratio = HEIGHT / self.HEIGHT
        self.rect.x = self.WIDTH* x_ratio
        self.rect.y = self.HEIGHT * y_ratio
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