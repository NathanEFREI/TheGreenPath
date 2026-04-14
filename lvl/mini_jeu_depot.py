import pygame
import os
import math
import random
from game.game import Fenetre
from personnage.joueur import Player
from constante import FPS


class MiniJeuDepot(Fenetre):
    """
    Mini-jeu où le joueur doit lancer des déchets dans une poubelle.
    """

    def __init__(self, score_joueur):
        super().__init__("Mini-Jeu : Dépôt des déchets")

        # Nombre de lancers autorisés, basé sur le score précédent.
        self.tentatives = score_joueur
        self.dechets_reussis = 0
        self.pressed = {}

        # Chargement du fond et du joueur.
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "..", "assets", "ville1.png")
        self.background_base = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))

        self.player = Player(self.WIDTH, self.HEIGHT)
        self.player.actu(self.WIDTH, self.HEIGHT)

        # --- CHARGEMENT DES ASSETS VISUELS ---
        # 1. La Poubelle
        path_poubelle = os.path.join(base_path, "..", "assets", "poubelles", "poubelle_ou_jeter.png")
        self.poubelle_img = pygame.image.load(path_poubelle).convert_alpha()
        self.poubelle_img = pygame.transform.scale(self.poubelle_img, (100, 120))
        self.poubelle_rect = self.poubelle_img.get_rect()

        # 2. Le Déchet (l'icône du compteur)
        path_icone = os.path.join(base_path, "..", "assets", "icones", "icone_dechets.png")
        self.dechet_img = pygame.image.load(path_icone).convert_alpha()
        self.dechet_img = pygame.transform.scale(self.dechet_img, (40, 40))  # Taille adaptée au tir

        # --- VARIABLES DE PHYSIQUE ---
        self.phase = "VISEE"
        self.angle_fleche = 0
        self.vitesse_fleche = 2.5  # Un peu plus rapide car on est plus près
        self.puissance_lancer = 18
        self.gravite_mini_jeu = 0.6

        self.pos_dechet = [0, 0]
        self.vel_dechet = [0, 0]

        pygame.font.init()
        self.police = pygame.font.SysFont("arial", 40, bold=True)

        self.teleporter_joueur()

    def teleporter_joueur(self):
        """
        Place le joueur dans une zone de lancement aléatoire et fixe la poubelle.
        """

        zone_debut = self.WIDTH // 2
        zone_fin = (self.WIDTH * 3) // 4

        self.player.rect.left = random.randint(zone_debut, zone_fin)
        self.player.rect.bottom = self.HEIGHT - 250

        self.poubelle_rect.midbottom = (self.WIDTH - 120, self.HEIGHT - 250)

    def run(self):
        """
        Boucle principale du mini-jeu de dépôt de déchets.
        """
        
        clock = pygame.time.Clock()

        while self.running:
            maintenant = pygame.time.get_ticks()

            for event in pygame.event.get():
                self.event(event)
                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                    if event.key == pygame.K_SPACE and self.phase == "VISEE":
                        if self.tentatives > 0:
                            self.phase = "VOL"
                            rad = math.radians(self.angle_fleche)
                            self.pos_dechet = [float(self.player.rect.centerx), float(self.player.rect.top + 20)]
                            self.vel_dechet = [
                                self.puissance_lancer * math.cos(rad),
                                -self.puissance_lancer * math.sin(rad)
                            ]
                            self.tentatives -= 1
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            # --- LOGIQUE ---
            if self.phase == "VISEE":
                # Le curseur d'angle oscille entre 0 et 90 degrés.
                self.angle_fleche += self.vitesse_fleche
                if self.angle_fleche > 90 or self.angle_fleche < 0:
                    self.vitesse_fleche *= -1

            elif self.phase == "VOL":
                # Applique la physique du lancer sur le déchet.
                self.pos_dechet[0] += self.vel_dechet[0]
                self.vel_dechet[1] += self.gravite_mini_jeu
                self.pos_dechet[1] += self.vel_dechet[1]

                dechet_rect = self.dechet_img.get_rect(topleft=(self.pos_dechet[0], self.pos_dechet[1]))

                if dechet_rect.colliderect(self.poubelle_rect):
                    self.dechets_reussis += 1
                    self.phase = "RESULTAT"
                elif self.pos_dechet[1] > self.HEIGHT - 150 or self.pos_dechet[0] > self.WIDTH:
                    self.phase = "RESULTAT"

            elif self.phase == "RESULTAT":
                # Après un lancer, on réinitialise ou on termine le mini-jeu.
                if self.tentatives > 0:
                    self.teleporter_joueur()
                    self.phase = "VISEE"
                else:
                    self.running = False

            # --- AFFICHAGE ---
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.poubelle_img, self.poubelle_rect)

            surface_essais = self.police.render(f"Déchets : {self.tentatives}", True, (255, 255, 255))
            surface_score = self.police.render(f"Triés : {self.dechets_reussis}", True, (50, 255, 50))
            self.screen.blit(surface_essais, (30, 30))
            self.screen.blit(surface_score, (30, 80))

            if self.phase == "VISEE":
                rad = math.radians(self.angle_fleche)
                # On dessine la flèche depuis le joueur
                depart = (self.player.rect.centerx, self.player.rect.top + 20)
                fin = (depart[0] + 60 * math.cos(rad), depart[1] - 60 * math.sin(rad))
                pygame.draw.line(self.screen, (255, 255, 0), depart, fin, 4)

            elif self.phase == "VOL":
                # On affiche l'icône de déchet au lieu du rectangle gris
                self.screen.blit(self.dechet_img, (self.pos_dechet[0], self.pos_dechet[1]))

            clock.tick(FPS)
            pygame.display.flip()