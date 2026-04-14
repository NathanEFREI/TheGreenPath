import pygame
import os


class Monstre(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type_monstre=1):
        super().__init__()
        self.WIDTH, self.HEIGHT = width, height

        # --- CALCUL DES RATIOS D'ÉCRAN ---
        # Basé sur ta résolution d'origine (1536x864)
        self.ratio_w = self.WIDTH / 1536
        self.ratio_h = self.HEIGHT / 864

        self.type_monstre = type_monstre

        # --- 1. CHARGEMENT DES SPRITES ---
        self.sprites_walk = []
        base_path = os.path.dirname(__file__)

        # Taille adaptative (60 pixels sur ton écran devient proportionnel ailleurs)
        # On utilise ratio_w pour les deux afin de garder le monstre bien carré
        taille_m = int(60 * self.ratio_w)

        if self.type_monstre == 1:
            for i in range(1, 9):
                chemin = os.path.join(base_path, "..", "assets", "monstre1", f"monstre1_walk{i}.png")
                image = pygame.image.load(chemin).convert_alpha()
                image = pygame.transform.scale(image, (taille_m, taille_m))
                self.sprites_walk.append(image)

            # Vitesse adaptée à la largeur de l'écran
            self.vitesse = 2 * self.ratio_w
            self.pv_max = 100

        elif self.type_monstre == 2:
            for i in range(1, 7):
                chemin2 = os.path.join(base_path, "..", "assets", "monstre2", f"monstre2_walk{i}.png")
                image2 = pygame.image.load(chemin2).convert_alpha()
                image2 = pygame.transform.scale(image2, (taille_m, taille_m))
                self.sprites_walk.append(image2)

            self.vitesse = 4 * self.ratio_w
            self.pv_max = 40

        self.current_sprite = 0
        self.image = self.sprites_walk[self.current_sprite]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.direction = -1
        self.pv = self.pv_max
        self.invulnerable = False

    def subir_degats(self, montant):
        self.pv -= montant
        if self.pv <= 0:
            self.kill()
            return True
        return False

    def afficher_barre_vie(self, surface):
        couleur_fond = (200, 0, 0)
        couleur_vie = (0, 200, 0)

        # Barres de vie adaptatives (40 et 5 étaient tes valeurs de base)
        largeur_barre = int(40 * self.ratio_w)
        hauteur_barre = int(5 * self.ratio_h)

        x_barre = self.rect.centerx - (largeur_barre // 2)
        y_barre = self.rect.top - int(10 * self.ratio_h)

        ratio_vie = self.pv / self.pv_max
        largeur_actuelle = int(largeur_barre * ratio_vie)

        pygame.draw.rect(surface, couleur_fond, (x_barre, y_barre, largeur_barre, hauteur_barre))
        if largeur_actuelle > 0:
            pygame.draw.rect(surface, couleur_vie, (x_barre, y_barre, largeur_actuelle, hauteur_barre))

    def update(self):
        self.current_sprite += 0.15
        if self.current_sprite >= len(self.sprites_walk):
            self.current_sprite = 0

        self.image = self.sprites_walk[int(self.current_sprite)]

        if self.type_monstre == 2:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.vitesse * self.direction

        if self.rect.right < 0:
            self.kill()