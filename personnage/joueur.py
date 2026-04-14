import pygame
import assets.asset as aa
from constante import (
    PLAYER_SCALE_W,
    PLAYER_SCALE_H,
    X_RATIO,
    Y_RATIO,
    INIT_SPRITE,
    VELOCITY,
)


class Player(pygame.sprite.Sprite):
    """
    Représente le joueur et gère son animation, son déplacement et son saut.
    """

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

        # Indique si le joueur est en train de sauter.
        self.jumping = False
        # Constantes du saut et de la gravité appliquées à chaque frame.
        self.GRAVITY = 40
        self.JUMP_HEIGHT = 20
        self.JUMP_VELOCITY = self.JUMP_HEIGHT

        # Ligne de sol, c'est la position Y à laquelle le joueur revient après un saut.
        self.GROUND = self.rect.y


    def scale_pos(self):
        """
        Positionne le joueur en fonction de la résolution de l'écran.
        """

        self.rect.x = int(X_RATIO * self.WIDTH)
        self.rect.y = int(Y_RATIO * self.HEIGHT)
        # GROUND est la position du sol logique, en évitant que le joueur dépasse du bas de l'écran.
        self.GROUND = min(int(Y_RATIO * self.HEIGHT), self.HEIGHT - self.rect.height)

    def max_jump_height(self):
        """
        Calcule la hauteur maximale atteinte par le saut actuel.
        """

        gravity_step = self.GRAVITY * 0.05
        velocity = self.JUMP_HEIGHT
        height = 0.0
        while velocity > 0:
            height += velocity
            velocity -= gravity_step
        return int(height)

    def resize_img(self, w, h):
        """
        Redimensionne les textures du joueur selon la taille de la fenêtre.
        """

        self.WIDTH, self.HEIGHT = w, h

        def scale_sprite(load, scale):
            return lambda x: scale(load(x).convert_alpha(), (PLAYER_SCALE_W * self.WIDTH, PLAYER_SCALE_H * self.HEIGHT))

        self.fonction = scale_sprite(pygame.image.load, pygame.transform.scale)

        for nom_asset in INIT_SPRITE:
            setattr(self, nom_asset + "_assets", aa.recup_sprite(nom_asset, self.fonction))
    

    def actu(self, w, h):
        """
        Met à jour les sprites et la position du joueur lors du redimensionnement de la fenêtre.
        """

        old_w, old_h = self.WIDTH, self.HEIGHT
        rel_x = self.rect.x / old_w if old_w > 0 else X_RATIO
        rel_y = self.rect.y / old_h if old_h > 0 else Y_RATIO

        self.resize_img(w, h)
        self.rect = self.image.get_rect()
        self.rect.x = int(rel_x * self.WIDTH)
        self.rect.y = int(rel_y * self.HEIGHT)

        setattr(self, "image", getattr(self, self.state + "_assets")[int(self.current_sprite)])
        self.GROUND = min(self.rect.y, self.HEIGHT - self.rect.height)
        

    #permet de changer de sprite pour animer le personnage
    def update(self, assets):
        """
        Fait avancer l'animation du joueur en fonction de son état.
        """

        self.current_sprite += 0.2
        LONGUEUR = len(assets)
        if self.jumping:
            if self.current_sprite >= LONGUEUR:
                self.current_sprite = LONGUEUR - 1
            self.image = assets[int(self.current_sprite)]
        else:
            if self.current_sprite >= LONGUEUR - 1:
                self.current_sprite = 0
            self.image = assets[int(self.current_sprite)]


    def move_left(self):
        """
        Déplace le joueur vers la gauche et met à jour l'animation de marche.
        """

        self.rect.x -= self.velocity
        if not self.jumping:
            self.update(self.walk_assets)
            self.state = "walk"
        self.image = pygame.transform.flip(self.image, True, False)

    def move_right(self):
        """
        Déplace le joueur vers la droite et met à jour l'animation de marche.
        """

        self.rect.x += self.velocity
        if not self.jumping:
            self.state = "walk"
            self.update(self.walk_assets)


    def jump(self):
        """
        Lance l'animation de saut et initialise la vitesse verticale.
        """

        if not self.jumping:
            self.jumping = True
            self.state = "jump"
            self.JUMP_VELOCITY = self.JUMP_HEIGHT
            self.current_sprite = 0

    def idle(self):
        """
        Met le joueur en état d'attente (idle).
        """

        self.update(self.idle_assets)
        self.state = "idle"


    def apply_gravity(self):
        """
        Applique la gravité lorsque le joueur est en saut et gère la retombée.
        """
        
        if self.jumping:
            self.rect.y -= self.JUMP_VELOCITY
            self.JUMP_VELOCITY -= (self.GRAVITY * 0.05)
            self.update(self.jump_assets)

            # Si le joueur redescend jusqu'au sol, arrêter le saut.
            if self.rect.y >= self.GROUND:
                self.rect.y = self.GROUND
                self.jumping = False
                self.JUMP_VELOCITY = self.JUMP_HEIGHT
                self.image = self.walk_assets[0]

    
