import pygame
import os
import math
import random
from game.game import Fenetre
from personnage.joueur import Player
from constante import FPS


class MiniJeuDepot(Fenetre):
    def __init__(self, score_joueur):
        super().__init__("Mini-Jeu : Dépôt des déchets")

        # --- CALCUL DES RATIOS D'ÉCRAN ---
        self.ratio_w = self.WIDTH / 1536
        self.ratio_h = self.HEIGHT / 864

        # --- VARIABLES DE BASE ---
        self.tentatives = score_joueur
        self.dechets_reussis = 0
        self.pressed = {}

        # --- CHARGEMENT DU FOND ET DU JOUEUR ---
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "..", "assets", "villereparer.webp")
        self.background_base = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))

        self.player = Player(self.WIDTH, self.HEIGHT)
        self.player.actu(self.WIDTH, self.HEIGHT)

        # --- CHARGEMENT DES ASSETS VISUELS (Adaptatifs) ---
        # 1. La Poubelle
        path_poubelle = os.path.join(base_path, "..", "assets", "poubelles", "poubelle_ou_jeter.png")
        self.poubelle_img = pygame.image.load(path_poubelle).convert_alpha()
        taille_p_w = int(100 * self.ratio_w)
        taille_p_h = int(120 * self.ratio_h)
        self.poubelle_img = pygame.transform.scale(self.poubelle_img, (taille_p_w, taille_p_h))
        self.poubelle_rect = self.poubelle_img.get_rect()

        # 2. Le Déchet
        path_icone = os.path.join(base_path, "..", "assets", "icones", "icone_dechets.png")
        self.dechet_img = pygame.image.load(path_icone).convert_alpha()
        taille_d = int(40 * self.ratio_w)
        self.dechet_img = pygame.transform.scale(self.dechet_img, (taille_d, taille_d))

        # --- VARIABLES DE PHYSIQUE (Adaptatives) ---
        self.phase = "VISEE"
        self.angle_fleche = 0
        self.vitesse_fleche = 2.5
        # On multiplie la puissance et la gravité par les ratios !
        self.puissance_lancer = 18 * self.ratio_w
        self.gravite_mini_jeu = 0.6 * self.ratio_h

        self.pos_dechet = [0, 0]
        self.vel_dechet = [0, 0]

        pygame.font.init()
        # Police adaptative
        taille_police = int(40 * self.ratio_w)
        self.police = pygame.font.SysFont("arial", taille_police, bold=True)

        self.chrono_fin = 0
        self.teleporter_joueur()

        if self.tentatives <= 0:
            self.phase = "FIN"
            self.chrono_fin = pygame.time.get_ticks()

    def teleporter_joueur(self):
        """Téléporte le joueur et place la poubelle de manière adaptative"""
        zone_debut = self.WIDTH // 2
        zone_fin = (self.WIDTH * 3) // 4
        self.player.rect.left = random.randint(zone_debut, zone_fin)

        # Le sol adaptatif (ici on a gardé ton 250 de base, modifie-le si ton image a changé !)
        sol_y = self.HEIGHT - int(200 * self.ratio_h)

        self.player.rect.bottom = sol_y
        # TRÈS IMPORTANT : On dit au joueur où est son nouveau sol pour la phase de transition
        self.player.limite_sol = sol_y

        # On place la poubelle avec une marge adaptative
        marge_droite = int(120 * self.ratio_w)
        self.poubelle_rect.midbottom = (self.WIDTH - marge_droite, sol_y)

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            maintenant = pygame.time.get_ticks()

            # --- 1. GESTION DES ÉVÉNEMENTS ---
            for event in pygame.event.get():
                self.event(event)
                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True

                    if event.key == pygame.K_SPACE:
                        if self.phase == "VISEE" and self.tentatives > 0:
                            self.phase = "VOL"
                            rad = math.radians(self.angle_fleche)

                            # Point de départ adaptatif (la main du joueur)
                            decalage_main = int(20 * self.ratio_h)
                            self.pos_dechet = [float(self.player.rect.centerx),
                                               float(self.player.rect.top + decalage_main)]

                            self.vel_dechet = [
                                self.puissance_lancer * math.cos(rad),
                                -self.puissance_lancer * math.sin(rad)
                            ]
                            self.tentatives -= 1

                        elif self.phase == "FIN" and self.dechets_reussis < 5:
                            self.running = False

                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            # --- 2. LOGIQUE DES ÉTATS ---
            if self.phase == "VISEE":
                self.angle_fleche += self.vitesse_fleche
                if self.angle_fleche > 90 or self.angle_fleche < 0:
                    self.vitesse_fleche *= -1

            elif self.phase == "VOL":
                self.pos_dechet[0] += self.vel_dechet[0]
                self.vel_dechet[1] += self.gravite_mini_jeu
                self.pos_dechet[1] += self.vel_dechet[1]

                dechet_rect = self.dechet_img.get_rect(topleft=(self.pos_dechet[0], self.pos_dechet[1]))

                if dechet_rect.colliderect(self.poubelle_rect):
                    self.dechets_reussis += 1
                    self.phase = "RESULTAT"
                elif self.pos_dechet[1] > self.HEIGHT - int(150 * self.ratio_h) or self.pos_dechet[0] > self.WIDTH:
                    self.phase = "RESULTAT"

            elif self.phase == "RESULTAT":
                if self.tentatives > 0:
                    self.teleporter_joueur()
                    self.phase = "VISEE"
                else:
                    self.phase = "FIN"
                    self.chrono_fin = maintenant

                    # --- PHASE DE TRANSITION ---
            elif self.phase == "TRANSITION_SUITE":
                self.move = True
                self.player.apply_gravity()

                if self.pressed.get(pygame.K_q) and self.player.rect.left > 0:
                    self.player.move_left()
                    self.move = False

                if self.pressed.get(pygame.K_d):
                    self.player.move_right()
                    self.move = False
                    if self.player.rect.left > self.WIDTH:
                        self.running = False

                if (self.pressed.get(pygame.K_SPACE) or self.pressed.get(pygame.K_z)) and not self.player.jumping:
                    self.player.jump()
                    self.move = False

                if self.move:
                    self.player.idle()

            # --- 3. AFFICHAGE ---
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image, self.player.rect)

            if self.phase != "TRANSITION_SUITE":
                self.screen.blit(self.poubelle_img, self.poubelle_rect)
                surface_essais = self.police.render(f"Déchets : {self.tentatives}", True, (255, 255, 255))
                surface_score = self.police.render(f"Triés : {self.dechets_reussis} / 5", True, (50, 255, 50))

                marge_texte = int(30 * self.ratio_w)
                self.screen.blit(surface_essais, (marge_texte, marge_texte))
                self.screen.blit(surface_score, (marge_texte, marge_texte + int(50 * self.ratio_h)))

            if self.phase == "VISEE":
                rad = math.radians(self.angle_fleche)
                decalage_main = int(20 * self.ratio_h)
                longueur_ligne = int(60 * self.ratio_w)

                depart = (self.player.rect.centerx, self.player.rect.top + decalage_main)
                fin = (depart[0] + longueur_ligne * math.cos(rad), depart[1] - longueur_ligne * math.sin(rad))
                epaisseur = max(1, int(4 * self.ratio_w))
                pygame.draw.line(self.screen, (255, 255, 0), depart, fin, epaisseur)

            elif self.phase == "VOL":
                self.screen.blit(self.dechet_img, (self.pos_dechet[0], self.pos_dechet[1]))

            elif self.phase == "FIN":
                voile = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                voile.fill((0, 0, 0, 150))
                self.screen.blit(voile, (0, 0))

                if self.dechets_reussis >= 5:
                    msg = "GAGNÉ ! Bien joué !"
                    couleur = (50, 255, 50)

                    temps_ecoule = maintenant - self.chrono_fin
                    if temps_ecoule >= 5000:
                        self.phase = "TRANSITION_SUITE"
                        self.pressed.clear()
                else:
                    msg = "ECHEC... Pas assez de déchets (ESPACE pour recommencer)"
                    couleur = (255, 50, 50)

                txt_fin = self.police.render(msg, True, couleur)
                rect_fin = txt_fin.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                self.screen.blit(txt_fin, rect_fin)

            clock.tick(FPS)
            pygame.display.flip()