import os
import pygame
from pygame.surface import Surface
import assets.asset as aa


#CONSTANTE RÉAJUSTABLE
VELOCITY = 5
PLAYER_SCALE_W = 80 / 2560
PLAYER_SCALE_H = 80 / 1600
X_RATIO = 200 / 2560
Y_RATIO = 1024 / 1440



class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        info = pygame.display.Info()
        # Récupérer la résolution de l'écran 
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        # wahou ! (NEW pour moi aussi jai voulu teste deso)
        def scale_sprite(load, scale):
            return lambda x: scale(load(x).convert_alpha() ,(PLAYER_SCALE_W * self.WIDTH, PLAYER_SCALE_H* self.HEIGHT))

        fonction = scale_sprite(pygame.image.load, pygame.transform.scale)

        self.walk_assets = aa.recup_sprite("walk", fonction)
        self.jump_assets = aa.recup_sprite("jump", fonction)
        self.idle_assets = aa.recup_sprite("idle", fonction)


        self.current_sprite = 0
        self.image = self.walk_assets[self.current_sprite]
        self.rect = self.image.get_rect()


        #adapter la position du joueur
        self.velocity = VELOCITY
        self.rect.x = X_RATIO * self.WIDTH
        self.rect.y = Y_RATIO * self.HEIGHT

        
        #constante du jump
        self.jumping = False
        self.GRAVITY = 40
        self.JUMP_HEIGHT = 20
        self.JUMP_VELOCITY = self.JUMP_HEIGHT

        #####
        self.GROUND = self.rect.y

        
        
    #permet de changer de sprite pour animer le personnage
    def update(self,assets):
        self.current_sprite+= 0.2  #ralentir l'animation pour la rendre plus naturel
        LONGUEUR = len(assets)
        if self.jumping:
            # --- LOGIQUE DE SAUT (8 frames) ---
            if self.current_sprite >= LONGUEUR :
                # On reste sur la dernière frame de chute à la fin de l'anim
                self.current_sprite = LONGUEUR - 1
            
            self.image = assets[int(self.current_sprite)]

        else:
            # --- LOGIQUE DE MARCHE (6 frames) ---
            if self.current_sprite >= LONGUEUR- 1:
                self.current_sprite = 0 # On boucle la marche
            
            self.image = assets[int(self.current_sprite)]


            
    #animation + avancé le personnage avec un rotation vers la gauche         
    def move_left(self):
        self.rect.x -= self.velocity
        if not self.jumping:
            self.update(self.walk_assets)
        self.image = pygame.transform.flip(self.image, True, False) 

    #animation + avancé le personnage
    def move_right(self):
        self.rect.x += self.velocity
        if not self.jumping:
            self.update(self.walk_assets)

    def jump(self):
        if not self.jumping:
            self.jumping = True
            # On réinitialise la vitesse de saut à sa hauteur maximale
            self.JUMP_VELOCITY = self.JUMP_HEIGHT 
            self.current_sprite = 0 

    def idle(self):
        self.update(self.idle_assets)

    def apply_gravity(self):
        if self.jumping:
            # On monte : on soustrait la vitesse actuelle à Y 
            self.rect.y -= self.JUMP_VELOCITY 
            # On réduit la puissance du saut avec la constante GRAVITY
            self.JUMP_VELOCITY -= (self.GRAVITY * 0.05)
            #on applique l'animation
            self.update(self.jump_assets)
            # Vérifier si on touche le sol
            if self.rect.y >= self.GROUND:
                self.rect.y = self.GROUND
                self.jumping = False
                # On remet la puissance de saut prête pour le prochain coup
                self.JUMP_VELOCITY = self.JUMP_HEIGHT
                self.image = self.walk_assets[0]

    
