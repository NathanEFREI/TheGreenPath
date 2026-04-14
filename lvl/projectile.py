import os

import pygame
import random


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, width, type_proj):
        super().__init__()
        self.WIDTH = width
        self.vitesse = 8
        base_path = os.path.dirname(__file__)
        # On définit les dégâts selon le type de projectile (1, 2 ou 3)
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
        # 1. Déplacement vers la droite
        self.rect.x += self.vitesse

        # 2. Alternance aléatoire de l'image (toutes les 4 frames environ pour ne pas clignoter trop vite)
        self.compteur_anim += 1
        if self.compteur_anim >= 4:
            self.image = random.choice(self.sprites)
            self.compteur_anim = 0

        # 3. Disparaître si le projectile sort de l'écran à droite
        if self.rect.left > self.WIDTH:
            self.kill()