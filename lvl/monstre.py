import pygame
import os


# Tu peux importer tes constantes de redimensionnement ici si besoin

class Monstre(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type_monstre=1):
        super().__init__()
        self.WIDTH, self.HEIGHT = width, height
        self.type_monstre = type_monstre

        # --- 1. CHARGEMENT DES SPRITES (Selon le type) ---
        self.sprites_walk = []
        base_path = os.path.dirname(__file__)

        if self.type_monstre == 1:
            # Charger les images du monstre 1 (ex: les 8 frames de monstre1_walk)
            for i in range(1, 9):
                chemin = os.path.join(base_path, "..", "assets", "monstre1", f"monstre1_walk{i}.png")
                # Pense à redimensionner (scale) comme pour le joueur si nécessaire
                image = pygame.image.load(chemin).convert_alpha()
                image = pygame.transform.scale(image, (60, 60))  # Exemple de taille
                self.sprites_walk.append(image)
            self.vitesse = 1.5
            self.pv_max = 100

        elif self.type_monstre == 2:
            for i in range(1, 7):
                chemin2 = os.path.join(base_path, "..", "assets", "monstre2", f"monstre2_walk{i}.png")
                image2 = pygame.image.load(chemin2).convert_alpha()
                image2 = pygame.transform.scale(image2, (60, 60))
                self.sprites_walk.append(image2)
            self.vitesse = 3
            self.pv_max = 40

        self.current_sprite = 0
        self.image = self.sprites_walk[self.current_sprite]
        self.rect = self.image.get_rect()

        # Placer le monstre aux coordonnées voulues
        self.rect.x = x
        self.rect.y = y

        # --- 2. VARIABLES DE DÉPLACEMENT AUTO ---
        self.direction = -1  # 1 = va à droite, -1 = va à gauche
        self.compteur_pas = 0
        #self.limite_pas = 150  # Le monstre fait 150 pixels puis fait demi-tour
        self.pv = self.pv_max
        self.invulnerable = False

    def subir_degats(self, montant):
        """Réduit la vie du monstre, le tue si PV <= 0. Retourne True si le monstre meurt."""
        self.pv -= montant
        if self.pv <= 0:
            self.kill()
            return True
        return False

    def afficher_barre_vie(self, surface):
        """Dessine une barre de vie au-dessus du monstre"""
        couleur_fond = (200, 0, 0)  # Rouge foncé (vie perdue)
        couleur_vie = (0, 200, 0)  # Vert (vie restante)

        largeur_barre = 40
        hauteur_barre = 5

        # On centre la barre juste au-dessus du rect du monstre
        x_barre = self.rect.centerx - (largeur_barre // 2)
        y_barre = self.rect.top - 10

        # Calcul de la proportion de la barre verte
        ratio_vie = self.pv / self.pv_max
        largeur_actuelle = int(largeur_barre * ratio_vie)

        # Dessin de l'arrière plan rouge
        pygame.draw.rect(surface, couleur_fond, (x_barre, y_barre, largeur_barre, hauteur_barre))
        # Dessin de la vie restante verte (si supérieure à 0)
        if largeur_actuelle > 0:
            pygame.draw.rect(surface, couleur_vie, (x_barre, y_barre, largeur_actuelle, hauteur_barre))
    def update(self):
        """Cette fonction sera appelée à chaque image dans la boucle run()"""
        # A. ANIMATION
        self.current_sprite += 0.15  # Vitesse de l'animation
        if self.current_sprite >= len(self.sprites_walk):
            self.current_sprite = 0

        self.image = self.sprites_walk[int(self.current_sprite)]

        # Si le monstre va à gauche, on retourne l'image (flip)
        if self.type_monstre == 2:
            self.image = pygame.transform.flip(self.image, True, False)

        # B. DÉPLACEMENT
        self.rect.x += self.vitesse * self.direction
        self.compteur_pas += abs(self.vitesse)

