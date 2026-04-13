import pygame
import assets.asset as aa
from constante import (PLAYER_SCALE_W, PLAYER_SCALE_H,
                        X_RATIO, Y_RATIO, INIT_SPRITE, 
                        VELOCITY)


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        # Récupérer la résolution de la fenêtre de jeu
        self.WIDTH, self.HEIGHT = width, height
        self.resize_img(self.WIDTH, self.HEIGHT)

        self.current_sprite = 0
        self.image = self.walk_assets[self.current_sprite]
        self.state = "walk"
        self.rect = self.image.get_rect()

        #adapter la position du joueur
        self.velocity = VELOCITY
        self.scale_pos()
        
        #constante du jump
        self.jumping = False
        self.GRAVITY = 40
        self.JUMP_HEIGHT = 20
        self.JUMP_VELOCITY = self.JUMP_HEIGHT
        
        ### plateforme
        self.GROUND = self.rect.y


    def scale_pos(self):
        """
        Calcule la nouvelle position en fonction de la taille de la fenêtre
        """
        self.rect.x = int(X_RATIO * self.WIDTH)
        self.rect.y = int(Y_RATIO * self.HEIGHT)
        # GROUND correspond à la ligne de sol où le joueur revient après un saut
        # Placer sur le sol logique, pas au-dessus du bas de la fenêtre
        self.GROUND = min(int(Y_RATIO * self.HEIGHT), self.HEIGHT - self.rect.height)

    def max_jump_height(self):
        """Retourne la hauteur approximative du saut en pixels."""
        gravity_step = self.GRAVITY * 0.05
        velocity = self.JUMP_HEIGHT
        height = 0.0
        while velocity > 0:
            height += velocity
            velocity -= gravity_step
        return int(height)

    def resize_img(self, w, h):
        """
        Redimensionne les images du player en fonction de la taille de la fenetre
        """
        self.WIDTH, self.HEIGHT = w, h

        def scale_sprite(load, scale):
            return lambda x: scale(load(x).convert_alpha(), (PLAYER_SCALE_W * self.WIDTH, PLAYER_SCALE_H * self.HEIGHT))

        self.fonction = scale_sprite(pygame.image.load, pygame.transform.scale)

        for nom_asset in INIT_SPRITE:
            setattr(self, nom_asset + "_assets", aa.recup_sprite(nom_asset, self.fonction))
    

    def actu(self, w, h):
        """
        Reactualise les infos lors d'un redimensionnement
        conserve la position actuelle du player.
        """
        # On conserve la position relative (si l'ancien width/height était non nul)
        old_w, old_h = self.WIDTH, self.HEIGHT
        rel_x = self.rect.x / old_w if old_w > 0 else X_RATIO
        rel_y = self.rect.y / old_h if old_h > 0 else Y_RATIO

        self.resize_img(w, h)
        # recalculer le positionnement proportionnel (au lieu de réinitialiser le ratio fixe)
        self.rect = self.image.get_rect()
        self.rect.x = int(rel_x * self.WIDTH)
        self.rect.y = int(rel_y * self.HEIGHT)

        setattr(self, "image", getattr(self, self.state + "_assets")[int(self.current_sprite)])
        self.GROUND = min(self.rect.y, self.HEIGHT - self.rect.height)
        

    #permet de changer de sprite pour animer le personnage
    def update(self, assets):
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
            self.state = "walk"
        self.image = pygame.transform.flip(self.image, True, False) 


    #animation + avancé le personnage
    def move_right(self):
        self.rect.x += self.velocity
        if not self.jumping:
            self.state = "walk"
            self.update(self.walk_assets)


    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.state = "jump"
            # On réinitialise la vitesse de saut à sa hauteur maximale
            self.JUMP_VELOCITY = self.JUMP_HEIGHT 
            self.current_sprite = 0 


    def idle(self):
        self.update(self.idle_assets)
        self.state = "idle"


    def apply_gravity(self):
        if self.jumping:
            # On monte : on soustrait la vitesse actuelle à Y 
            self.rect.y -= self.JUMP_VELOCITY 
            # On réduit la puissance du saut avec la constante GRAVITY
            self.JUMP_VELOCITY -= (self.GRAVITY * 0.05)
            #on applique l'animation
            self.update(self.jump_assets)

            # Vérifier si on touche le sol
            if self.rect.y >= self.GROUND: ### a changer pour les trucs de plateforme
                self.rect.y = self.GROUND
                self.jumping = False
                # On remet la puissance de saut prête pour le prochain coup
                self.JUMP_VELOCITY = self.JUMP_HEIGHT
                self.image = self.walk_assets[0]

    
