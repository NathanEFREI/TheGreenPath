import pygame
import os

#CONSTANTE RÉAJUSTABLE
VELOCITY = 5
PLAYER_SCALE = 2.5
HEIGHT_START = 735
WIDTH_START = 200



class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        info = pygame.display.Info()
        # Récupérer la résolution de l'écran 
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        self.walk_assets = []
        self.jump_assets = []
        self.idle_assets = []

        for i in range(0,4):
            base_path = os.path.dirname(__file__)
            img = pygame.image.load(os.path.join(base_path, '..', 'assets/idle', 'hero_idle' + str(i) + '.png')).convert_alpha()
            img = pygame.transform.scale_by(img, PLAYER_SCALE)
            self.walk_assets.append(img)


        for i in range(0,6):
            base_path = os.path.dirname(__file__)
            img = pygame.image.load(os.path.join(base_path, '..', 'assets', 'hero' + str(i) + '.png')).convert_alpha()
            img = pygame.transform.scale_by(img, PLAYER_SCALE)
            self.walk_assets.append(img)
            
        for i in range(0, 8):
            img = pygame.image.load(os.path.join(base_path, '..', 'assets', 'hero_jump' + str(i) + '.png')).convert_alpha()
            self.jump_assets.append(pygame.transform.scale_by(img, PLAYER_SCALE))

        self.current_sprite = 0
        self.image = self.walk_assets[self.current_sprite]
        self.rect = self.image.get_rect()

        
        
        #adapter la position du joueur
        self.velocity = VELOCITY
        x_ratio = WIDTH_START / self.WIDTH
        y_ratio = HEIGHT_START / self.HEIGHT
        self.rect.x = self.WIDTH* x_ratio
        self.rect.y = int(self.HEIGHT * y_ratio)

        #constante du jump
        self.jumping = False
        self.GRAVITY = 40
        self.JUMP_HEIGHT = 20
        self.JUMP_VELOCITY = self.JUMP_HEIGHT
        self.GROUND = int(self.HEIGHT * y_ratio)

        
        
    #permet de changer de sprite pour animer le personnage
    def update(self):
        self.current_sprite+= 0.2  #ralentir l'animation pour la rendre plus naturel
        if self.jumping:
            # --- LOGIQUE DE SAUT (8 frames) ---
            if self.current_sprite >= len(self.jump_assets):
                # On reste sur la dernière frame de chute à la fin de l'anim
                self.current_sprite = len(self.jump_assets) - 1
            
            self.image = self.jump_assets[int(self.current_sprite)]

        else:
            # --- LOGIQUE DE MARCHE (6 frames) ---
            if self.current_sprite >= len(self.walk_assets):
                self.current_sprite = 0 # On boucle la marche
            
            self.image = self.walk_assets[int(self.current_sprite)]

    
            
        

        

            
    #animation + avancé le personnage avec un rotation vers la gauche         
    def move_left(self):
        self.rect.x -= self.velocity
        if not self.jumping:
            self.update()
        self.image = pygame.transform.flip(self.image, True, False) 

    #animation + avancé le personnage
    def move_right(self):
        self.rect.x += self.velocity
        if not self.jumping:
            self.update()

    def jump(self):
        if not self.jumping:
            self.jumping = True
            # On réinitialise la vitesse de saut à sa hauteur maximale
            self.JUMP_VELOCITY = self.JUMP_HEIGHT 
            self.current_sprite = 0 
    
    def apply_gravity(self):
        if self.jumping:
            # On monte : on soustrait la vitesse actuelle à Y 
            self.rect.y -= self.JUMP_VELOCITY 
            # On réduit la puissance du saut avec la constante GRAVITY
            self.JUMP_VELOCITY -= (self.GRAVITY * 0.05)
            #on applique l'animation
            self.update()
            # Vérifier si on touche le sol
            if self.rect.y >= self.GROUND:
                self.rect.y = self.GROUND
                self.jumping = False
                # On remet la puissance de saut prête pour le prochain coup
                self.JUMP_VELOCITY = self.JUMP_HEIGHT
                self.image = self.walk_assets[0]

    
