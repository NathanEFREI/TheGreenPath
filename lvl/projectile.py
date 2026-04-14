import os
import random
import pygame


class Projectile(pygame.sprite.Sprite):
    """
    Projectile tiré par le joueur pendant le niveau de recyclage.
    """

    def __init__(self, x, y, width, type_proj):
        super().__init__()
        self.WIDTH = width
        self.vitesse = 8
        base_path = os.path.dirname(__file__)
        if type_proj == 1:
            self.degats = 5
        elif type_proj == 2:
            self.degats = 10
        else:
            self.degats = 20

        # --- GESTION DES SPRITES ---
        self.sprites = []

        # ASTUCE : Pour le moment, je mets des rectangles de couleur pour que tu puisses tester.
        # Quand tu auras tes images, remplace les 3 lignes img = pygame.Surface... par :
        # img = pygame.image.load("ton_chemin.png").convert_alpha()

        for i in range(3):
            # On donne une couleur différente selon la puissance pour bien les différencier
            if self.degats == 5:
                image = pygame.image.load(os.path.join(base_path, "..","assets","poubelles","poubelle_grise.png"))
                image = pygame.transform.scale(image, (60, 60))
            elif self.degats == 10:
                image = pygame.image.load(os.path.join(base_path, "..", "assets", "poubelles", "poubelle_bleu.png"))
                image = pygame.transform.scale(image, (60, 60))
            else:
                image = pygame.image.load(os.path.join(base_path, "..", "assets", "poubelles", "poubelle_jaune.png"))
                image = pygame.transform.scale(image, (60, 60))

            # Petit point blanc aléatoire pour voir l'alternance (à retirer avec tes images)

            self.sprites.append(image)

        # On choisit une image de départ au hasard
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect()

        # On place le projectile à la position (x, y) donnée au tir
        self.rect.left = x
        self.rect.centery = y

        self.compteur_anim = 0

    def update(self):
        """
        Déplace le projectile et anime son sprite.
        """
        
        self.rect.x += self.vitesse
        self.compteur_anim += 1
        if self.compteur_anim >= 4:
            self.image = random.choice(self.sprites)
            self.compteur_anim = 0

        if self.rect.left > self.WIDTH:
            self.kill()