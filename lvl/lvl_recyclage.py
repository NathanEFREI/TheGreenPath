import os
import pygame
from game.game import Fenetre
from personnage.joueur import Player
from lvl.projectile import Projectile
from constante import FPS
from lvl.monstre import Monstre
from ui.dialogue import afficher_dialogue
from lvl.mini_jeu_depot import MiniJeuDepot
import random


class LvlRecyclage(Fenetre):
    """
    Niveau de recyclage où le joueur affronte des monstres et trie les déchets.
    """

    def __init__(self):
        super().__init__("The Green Path - Niveau Recyclage")

        # --- CHARGEMENT DU BACKGROUND ---
        base_path = os.path.dirname(__file__)
        self.ratio_w = self.WIDTH / 1536
        self.ratio_h = self.HEIGHT / 864
        # Remplace "ville1.png" par l'image de fond spécifique au niveau recyclage si tu en as une
        image_path = os.path.join(base_path, "..", "assets", "villereparer.webp")
        icone_path = os.path.join(base_path, "..", "assets", "icones", "icone_dechets.png")
        self.background_base = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))
        self.etat = "EXPLICATION"
        self.temps_fin_dialogue = 0
        self.textes_gardien = [
            "Je suis le gardien du tri, celui qui veille à ce que les déchets trouvent le bon chemin. Chaque jour, je m’assure que rien ne soit gaspillé et que la nature reste propre et protégée.",
            "Quand tu jettes quelque chose, il ne disparaît pas vraiment. Les déchets peuvent polluer la terre, l’eau et mettre en danger les animaux. C’est pour cela qu’il est très important de bien trier ses déchets.",
            "En séparant le plastique, le papier, le verre et les restes de nourriture, on peut recycler et donner une seconde vie à beaucoup de choses. Cela permet de fabriquer de nouveaux objets sans abîmer encore plus la planète.",
            "Si on ne trie pas, les déchets s’accumulent et la nature souffre. Mais si chacun fait un petit effort, ensemble, on peut garder la Terre propre et en bonne santé.",
            "Pour ton épreuve, des créatures faites de déchets vont apparaître. Tu devras les vaincre en appuyant sur F, puis récupérer les déchets afin de les envoyer dans la poubelle de tri en appuyant sur espace ! Chaque déchet bien trié est une aide précieuse pour la planète. À toi de jouer, jeune aventurier"
        ]
        # --- CHARGEMENT DU GARDIEN ---
        path_gardien = os.path.join(os.path.dirname(__file__), "..", "assets", "gardien", "gardien-reparer.png")
        self.gardien_img = pygame.image.load(path_gardien).convert_alpha()
        taille_g = int(150 * self.ratio_w)
        self.gardien_img = pygame.transform.flip(self.gardien_img, True, False)
        self.gardien_img = pygame.transform.scale(self.gardien_img, (taille_g, taille_g))
        # On le place à gauche du sol
        pos_x_gardien = int(50 * self.ratio_w)
        pos_y_gardien = self.HEIGHT - int(200 * self.ratio_h)
        self.gardien_rect = self.gardien_img.get_rect(bottomleft=(pos_x_gardien, pos_y_gardien))
        self.index_dialogue = 0
        self.dialogue_actuel = (self.textes_gardien[self.index_dialogue], "green")
        self.player = Player(self.WIDTH, self.HEIGHT)
        self.player.actu(self.WIDTH, self.HEIGHT)
        self.compteur = 0

        self.icone_base = pygame.image.load(icone_path).convert_alpha()
        self.icone = pygame.transform.scale(self.icone_base, (100, 100))

        pygame.font.init()
        self.police = pygame.font.SysFont("arial", 40)
        # --- VARIABLES DE GESTION ---
        self.pressed = {}
        self.move = False

        self.elems = ["background"]
        self.groupe_monstres = pygame.sprite.Group()

        # 1. Définir les "points de spawn" possibles (les mêmes endroits)
        # Remplace self.HEIGHT - 100 par la hauteur de ton sol (self.player.GROUND)
        sol_y = self.HEIGHT - int(100 * self.ratio_h)
        nb_monstres = random.randint(3, 6)


        for i in range(nb_monstres):
            # Position X aléatoire EN DEHORS de l'écran à droite
            # Par exemple : entre le bord droit + 50 pixels, et le bord droit + 1000 pixels
            pos_x = random.randint(self.WIDTH + 50, self.WIDTH + 1000)

            # Choisir aléatoirement le type de monstre (1 ou 2)
            type_choisi = random.choice([1, 2])

            # Créer le monstre avec la position et le type choisis
            nouveau_monstre = Monstre(pos_x, sol_y, self.WIDTH, self.HEIGHT, type_monstre=type_choisi)

            # L'ajouter au groupe
            self.groupe_monstres.add(nouveau_monstre)

        self.temps_debut = pygame.time.get_ticks()
        self.duree_niveau = 60  # 60 secondes (1 minute)

        # --- GESTION DU SPAWN CONTINU ---
        self.dernier_spawn = pygame.time.get_ticks()
        self.intervalle_spawn = 2000  # Apparition toutes les 2000ms (2 secondes)
        self.groupe_monstres = pygame.sprite.Group()
        # Ajoute le groupe pour les projectiles en dessous de celui des monstres
        self.groupe_projectiles = pygame.sprite.Group()
        # --- GESTION DES MUNITIONS ---
        self.munitions = 20
        self.munitions_max = 20
        self.dernier_recharge = pygame.time.get_ticks()
        self.temps_recharge = 2000  # 2 secondes en millisecondes
        self.police_geante = pygame.font.SysFont("arial", 200, bold=True)

    def afficher_munitions(self):
        """
        Affiche le compteur de munitions à l'écran.
        """

        texte_munitions = f"Munitions: {self.munitions}/{self.munitions_max}"
        couleur = (255, 255, 255) if self.munitions > 5 else (255, 165, 0)

        surface_mun = self.police.render(texte_munitions, True, couleur)
        # On le place sous le compteur de déchets (ajusté selon ton affichage existant)
        rect_mun = surface_mun.get_rect(topright=(self.WIDTH - 20, 80))
        self.screen.blit(surface_mun, rect_mun)

    def afficher_minuteur(self):
        # Calcul du temps écoulé en secondes
        secondes_ecoulees = (pygame.time.get_ticks() - self.temps_debut) // 1000
        temps_restant = max(0, self.duree_niveau - secondes_ecoulees)

        # Formatage en MM:SS (facultatif, tu peux juste mettre le chiffre)
        minutes = temps_restant // 60
        secondes = temps_restant % 60
        texte_timer = f"{minutes:02d}:{secondes:02d}"

        # Rendu du texte
        surface_timer = self.police.render(texte_timer, True, (255, 255, 255))
        # On utilise midtop pour centrer parfaitement par rapport à la largeur (self.WIDTH // 2)
        rect_timer = surface_timer.get_rect(midtop=(self.WIDTH // 2, 20))

        self.screen.blit(surface_timer, rect_timer)

    def afficher_compteur(self):
        """
        Affiche l'icône et le chiffre en haut à droite de l'écran
        """

        # --- L'IMAGE ---
        icone_rect = self.icone.get_rect()
        # On place le bord haut-droit de l'image à 100 pixels du bord droit de l'écran et 20 du haut
        icone_rect.topleft = (self.WIDTH- self.WIDTH+10, 20)
        self.screen.blit(self.icone, icone_rect)

        # --- LE TEXTE (CHIFFRE) ---
        # Rendu du texte (le texte doit être un string, True pour lisser les bords, (Couleur RGB))
        texte_surface = self.police.render(str(self.compteur), True, (255, 255, 255))  # Texte blanc
        texte_rect = texte_surface.get_rect()

        # On place le texte juste à droite de l'image, centré sur la hauteur de l'image
        texte_rect.midleft = (icone_rect.right + 15, icone_rect.centery)

        self.screen.blit(texte_surface, texte_rect)

    def run(self):
        """
        Boucle principale du niveau de recyclage.
        """
        
        clock = pygame.time.Clock()

        while self.running:
            maintenant = pygame.time.get_ticks()

            # --- 1. GESTION DES ÉVÉNEMENTS ---
            for event in pygame.event.get():
                self.event(event)

                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True

                    # A. GESTION DU DIALOGUE (Touche E ou ESPACE)
                    if self.etat == "EXPLICATION" and (event.key == pygame.K_e or event.key == pygame.K_SPACE):
                        # Passage à la phrase suivante du gardien durant l'explication.
                        self.index_dialogue += 1

                        if self.index_dialogue < len(self.textes_gardien):
                            self.dialogue_actuel = (self.textes_gardien[self.index_dialogue], "green")
                        else:
                            self.dialogue_actuel = None
                            self.etat = "ATTENTE"
                            self.temps_fin_dialogue = maintenant

                    # B. TIRER UN PROJECTILE (Touche F)
                    elif event.key == pygame.K_f and self.munitions > 0 and self.etat == "JEU":
                        # Le joueur tire un projectile s'il a des munitions.
                        type_p = random.choice([1, 2, 3])
                        nouveau_proj = Projectile(self.player.rect.right, self.player.rect.centery, self.WIDTH, type_p)
                        self.groupe_projectiles.add(nouveau_proj)
                        self.munitions -= 1

                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            # --- 2. LOGIQUE DES ÉTATS ET DU JEU ---
            if self.etat == "ATTENTE":
                # On attend 5 secondes (5000 ms) avant de lancer l'épreuve
                if maintenant - self.temps_fin_dialogue >= 5000:
                    self.etat = "JEU"
                    self.temps_debut = maintenant  # Le vrai chrono (1 min) commence ICI !
                    self.dernier_spawn = maintenant
                    self.dernier_recharge = maintenant

            elif self.etat == "JEU":
                # Calcul du temps restant (pour stopper le spawn à 0)
                secondes_ecoulees = (maintenant - self.temps_debut) // 1000
                temps_restant = max(0, self.duree_niveau - secondes_ecoulees)

                # A. RECHARGE DES MUNITIONS
                if self.munitions < self.munitions_max:
                    if maintenant - self.dernier_recharge > self.temps_recharge:
                        self.munitions += 1
                        self.dernier_recharge = maintenant

                # B. SPAWN ET NETTOYAGE DES MONSTRES
                # B. SPAWN ET NETTOYAGE DES MONSTRES
                if temps_restant > 0:
                    if maintenant - self.dernier_spawn > self.intervalle_spawn:
                        # Position X au-delà de l'écran adaptative (+50 à +300)
                        spawn_min = self.WIDTH + int(50 * self.ratio_w)
                        spawn_max = self.WIDTH + int(300 * self.ratio_w)
                        pos_x = random.randint(spawn_min, spawn_max)

                        # La hauteur du sol adaptative (le fameux 250 de base)
                        sol_y = self.HEIGHT - int(250 * self.ratio_h)

                        type_choisi = random.choice([1, 2])

                        nouveau_monstre = Monstre(pos_x, sol_y, self.WIDTH, self.HEIGHT,
                                                  type_monstre=type_choisi)
                        self.groupe_monstres.add(nouveau_monstre)
                        self.dernier_spawn = maintenant
                else:
                    # Le temps est fini : on fait disparaître tous les monstres
                    self.groupe_monstres.empty()
                    mini_jeu = MiniJeuDepot(self.compteur)
                    mini_jeu.run()

                    # 2. Le mini-jeu est terminé, on vérifie le score
                    if mini_jeu.dechets_reussis >= 5:
                        # --- GAGNÉ ---
                        self.running = False  # On quitte ce niveau définitivement
                        return

                    else:
                        # --- PERDU : ON RÉINITIALISE LE NIVEAU ---
                        # On remet l'état au dialogue du début
                        self.etat = "EXPLICATION"
                        self.index_dialogue = 0
                        self.dialogue_actuel = (self.textes_gardien[self.index_dialogue], "green")

                        # On remet les scores et munitions à zéro
                        self.compteur = 0
                        self.munitions = self.munitions_max

                        # IMPORTANT : On met à jour le temps de fin de dialogue
                        # pour que les 5 secondes d'attente se relancent correctement plus tard
                        self.temps_fin_dialogue = pygame.time.get_ticks()

                        # On vide les groupes (on supprime tous les anciens monstres et tirs)
                        self.groupe_monstres.empty()
                        self.groupe_projectiles.empty()

                        # On replace le joueur à son point de départ
                        self.player.actu(self.WIDTH, self.HEIGHT)

                        # On vide les touches appuyées pour éviter qu'il ne tire ou saute tout seul
                        self.pressed.clear()

                # C. MISE À JOUR DES SPRITES (Animations, Déplacements)
                self.groupe_monstres.update()
                self.groupe_projectiles.update()

                # D. VÉRIFICATION DE L'INVULNÉRABILITÉ (Monstres qui ont dépassé le joueur)
                for monstre in self.groupe_monstres:
                    if monstre.rect.right < self.player.rect.left:
                        monstre.invulnerable = True

                # E. COLLISIONS ET SCORE
                collisions = pygame.sprite.groupcollide(self.groupe_projectiles, self.groupe_monstres, True, False)
                for projectile, liste_monstres in collisions.items():
                    for monstre in liste_monstres:
                        if not monstre.invulnerable:  # On vérifie sa mémoire d'invulnérabilité
                            if monstre.subir_degats(projectile.degats):
                                self.compteur += 1  # On augmente le score s'il meurt
                                self.munitions += 4

            # --- 3. PHYSIQUE ET DÉPLACEMENTS DU JOUEUR ---
            self.move = True
            self.player.apply_gravity()

            if self.pressed.get(pygame.K_q) and self.player.rect.left > 0:
                self.player.move_left()
                self.move = False

            if self.pressed.get(pygame.K_d) and self.player.rect.right < self.WIDTH:
                self.player.move_right()
                self.move = False

            if (self.pressed.get(pygame.K_SPACE) or self.pressed.get(pygame.K_z)) and not self.player.jumping:
                # On l'empêche de sauter s'il lit le dialogue pour éviter les bugs visuels
                if self.etat != "EXPLICATION":
                    self.player.jump()
                    self.move = False

            if self.move:
                self.player.idle()

            # --- 4. AFFICHAGE (RENDU GRAPHIQUE) ---
            # Le fond et le joueur sont toujours affichés
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image, self.player.rect)

            # Affichage différent selon l'état de la partie
            if self.etat == "EXPLICATION" or self.etat == "ATTENTE":
                # Afficher le gardien
                self.screen.blit(self.gardien_img, self.gardien_rect)
                # Afficher le texte (uniquement pendant l'explication)
                if self.dialogue_actuel:
                    texte, couleur = self.dialogue_actuel
                    afficher_dialogue(self.screen, texte, couleur)
                if self.etat == "EXPLICATION" and self.dialogue_actuel:
                    texte, couleur = self.dialogue_actuel
                    afficher_dialogue(self.screen, texte, couleur)

                    # --- AFFICHAGE DU COMPTE À REBOURS ---
                if self.etat == "ATTENTE":
                    # On calcule combien de secondes il reste (5, 4, 3, 2, 1)
                    temps_passe = maintenant - self.temps_fin_dialogue
                    compte_a_rebours = 5 - (temps_passe // 1000)

                    if compte_a_rebours > 0:
                        # On crée le texte en jaune pour qu'il soit bien visible
                        surface_compte = self.police_geante.render(str(compte_a_rebours), True, (255, 255, 0))
                        # On récupère le rectangle et on le place au centre de l'écran
                        rect_compte = surface_compte.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                        self.screen.blit(surface_compte, rect_compte)

            elif self.etat == "JEU":
                # Afficher l'interface utilisateur
                self.afficher_compteur()
                self.afficher_munitions()
                self.afficher_minuteur()

                # Afficher les entités
                self.groupe_monstres.draw(self.screen)
                for monstre in self.groupe_monstres:
                    monstre.afficher_barre_vie(self.screen)
                self.groupe_projectiles.draw(self.screen)

            # --- 5. RAFRAÎCHISSEMENT ---
            clock.tick(FPS)
            pygame.display.flip()



if __name__ == "__main__":
    niveau = LvlRecyclage()
    niveau.run()