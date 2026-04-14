import os
import pygame
from pygame.surface import Surface
from personnage.joueur import Player
from ui.dialogue import afficher_dialogue
from constante import FPS
from levels.epreuve_lumiere import EpreuveLumiere
from levels.epreuve_poubelle import Poubelle
from levels.menu_tri_poubelle import MenuTri
from .utils import draw_button, confirm_quit


# Fenetre est la classe de base qui gère l'écran, la taille et les événements
class Fenetre:
    def __init__(self, caption: str):
        pygame.init()

        # Créer la fenêtre fullscreen d'abord, PUIS lire les vraies dimensions
        # (sur Windows, Info() avant set_mode peut inclure la barre des tâches)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.fullscreen = True
        self.elems = None # Pour éviter d'avoir une erreur quand on appelle resize sans avoir def self.elems dans la sous classe

        pygame.display.set_caption(caption)
        self.running = True


    def event(self, event):
        """Traite les événements de base de la fenêtre.

        Quitter, redimensionner, et basculer en plein écran sont gérés ici.
        """
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.VIDEORESIZE:
            self.WIDTH, self.HEIGHT = event.size
            self.resize()

        elif event.type == pygame.KEYDOWN:
            # Plein écran / fenêtré avec F11.
            if event.key == pygame.K_F11:
                self.fullscreen = not self.fullscreen
                self.resize()

            # Quitter avec Échap.
            elif event.key == pygame.K_ESCAPE:
                self.running = False


    def resize_obj(self):
        """Redimensionne les éléments graphiques enregistrés après un changement de taille."""
        for e in self.elems:
            setattr(self, e, pygame.transform.scale(getattr(self, e + "_base"), (self.WIDTH, self.HEIGHT)))

        # Appelle la méthode de redimensionnement du joueur si elle existe.
        self.player.actu(self.WIDTH, self.HEIGHT)


    def resize(self):
        """Actualise la taille de la fenêtre quand le joueur change de mode ou redimensionne."""
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.WIDTH, self.HEIGHT = self.screen.get_size()
        else:
            dim = (int(self.WIDTH * 0.98), int(self.HEIGHT * 0.98))
            self.screen = pygame.display.set_mode(dim, pygame.RESIZABLE)
        if self.elems is not None:
            self.resize_obj()


class Game(Fenetre):
    def __init__(self, volume: float = 0.4):
        """Configure le jeu, charge les ressources, et initialise l'état global du monde."""
        super().__init__("The Green Path")
        pygame.mixer.init()
        self.volume = volume
        # Chemin absolu vers le dossier du fichier .py
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "..", "assets", "ville1.png")

        # Musique du jeu
        music_path = os.path.join(base_path, "..", "assets", "Sound", "Lobby Time.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

        # Charger l'arrière-plan principal du jeu.
        self.background_base = pygame.image.load(image_path).convert()
        # On garde une copie non redimensionnée afin de pouvoir mettre à l'échelle proprement.
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))

        # Créer le joueur et l'ajuster à la taille de l'écran.
        self.player = Player(self.WIDTH, self.HEIGHT)
        self.player.actu(self.WIDTH, self.HEIGHT)

        # Suivi des touches enfoncées et du compteur de gestes écologiques.
        self.pressed = {}
        self.geste_count = 0
        self.geste_max = 3
        self.geste_icon = None

        # Flag de mouvement du joueur.
        self.move: bool

        # Stocke un dialogue actif sous forme de (texte, couleur), ou None si aucun dialogue.
        self.dialogue_actuel = None

        # État des sections de la scène : spawn, lumiere, tri_dechets, tri_poubelle.
        self.salle_actuelle = "spawn"
        self.epreuve_lumiere_terminee = False

        image_path_epreuve1 = os.path.join(base_path, "..", "assets", "epreuves/epreuve_lumiere_bg.png")
        self.bg_epreuve1_base = pygame.image.load(image_path_epreuve1).convert()
        
        # On agrandit un peu la hauteur pour ne pas avoir de bande noire en bas quand on remonte l'image
        self.bg_epreuve1 = pygame.transform.scale(self.bg_epreuve1_base, (self.WIDTH, self.HEIGHT + 60))

        image_path_epreuve2 = os.path.join(base_path, "..", "assets", "epreuves", "epreuve_recyclage.png")
        self.bg_epreuve2_base = pygame.image.load(image_path_epreuve2).convert()
        self.bg_epreuve2 = pygame.transform.scale(self.bg_epreuve2_base, (self.WIDTH, self.HEIGHT))

        image_path_epreuve3 = os.path.join(base_path, "..", "assets", "ville1.png")
        self.bg_epreuve3_base = pygame.image.load(image_path_epreuve3).convert()
        self.bg_epreuve3 = pygame.transform.scale(self.bg_epreuve3_base, (self.WIDTH, self.HEIGHT))

        self.fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.fade_surface.fill((0,0,0))
        self.fade_opacite = 0
        self.faded_direction = 0

        # Compteur de gestes écologiques
        try:
            path_geste = os.path.join(base_path, "..", "assets", "geste.png")
            self.geste_icon = pygame.image.load(path_geste).convert_alpha()
            icon_size = max(56, min(96, self.HEIGHT // 18))
            w, h = self.geste_icon.get_size()
            ratio = w / h
            new_h = icon_size
            new_w = int(new_h * ratio)
            self.geste_icon = pygame.transform.smoothscale(self.geste_icon, (new_w, new_h))
        except Exception:
            self.geste_icon = None

        self.prochaine_salle_nom = ""
        self.prochain_bg = None
        self.prochaine_pos_x = 50        
        

        self.font_epreuve = pygame.font.SysFont("Arial", 30, bold = True)
        self.epreuve = EpreuveLumiere(self.screen, self.font_epreuve, self.WIDTH, self.HEIGHT)

        #gardien epreuve lumiere
        path_gardien_lumiere = os.path.join(base_path, "..", "assets", "gardien", "gardien-lumiere.png")
        self.gardien_img_base = pygame.image.load(path_gardien_lumiere).convert_alpha()
        self.gardien_tri_img_base = pygame.image.load(os.path.join(base_path, "..", "assets", "gardien", "gardien-recyclager.png")).convert_alpha()
        self.gardien_img = self._scale_gardien(self.gardien_img_base)
        self.gardien_tri_img = self._scale_gardien(self.gardien_tri_img_base)
        self.gardien_rect = self.gardien_img.get_rect()
        self.gardien_tri_rect = self.gardien_tri_img.get_rect()
        self._position_gardiens()

        self.dialogues_gardien_tri = [
            "Je suis le gardien du recyclage, celui qui veille à ce que chaque déchet trouve sa place.",
            "Rien ne doit être perdu, car même ce que l'on jette peut encore servir.",
            "Les déchets mal triés polluent la nature, mais recyclés, ils deviennent de nouvelles ressources.",
            "Voici ton épreuve : ramasse les déchets et place-les dans la bonne poubelle.",
            "Chaque erreur de tri peut nuire à l'équilibre de la nature ! Prêt ?"
        ]
        self.indice_dialogue_tri = -1
        self.tri_autorise = False  

        self.epreuve_tri_terminee = False 
        self.tri_autorise = False



        # Liste des répliques du Gardien
        self.dialogues_gardien = [
            "Je suis le gardien de la lumière, celui qui veille à ce que l’énergie ne soit jamais gaspillée. Je parcours les maisons et les villes pour m’assurer que chaque lumière est utilisée avec sagesse. Mais sais-tu que toi aussi, tu peux m’aider à protéger notre planète ?",
            "Quand tu quittes une pièce, éteindre la lumière peut sembler être un tout petit geste… pourtant, il est très important. Produire de l’électricité demande beaucoup d’énergie, et parfois cela pollue l’air et abîme la nature.",
            "En laissant une lumière allumée pour rien, on gaspille cette énergie. Mais en l’éteignant, tu aides à protéger les animaux, les plantes et même l’air que nous respirons.",
            "Chaque petit geste compte. Alors souviens-toi : quand tu pars d’une pièce, pense à éteindre la lumière. C’est ainsi que, petit à petit, tu deviens toi aussi un véritable gardien de la nature.",
            "Pour prouver que tu es prêt à devenir un protecteur de ton environnement, voici ton épreuve : des lumières vont s’allumer autour de toi. Tu devras toutes les éteindre le plus vite possible, avant que le temps ne soit écoulé. Sois rapide et attentif !"
        ]
        self.indice_dialogue = -1

        # Element a redimensionner
        self.elems = []

        path_poubelles = os.path.join(base_path, "..", "assets")
        self.poubelle_jaune_base = pygame.image.load(os.path.join(path_poubelles, "poubelle_jaune.png")).convert_alpha()
        self.poubelle_marron_base = pygame.image.load(os.path.join(path_poubelles, "poubelle_marron.png")).convert_alpha()
        self.poubelle_verte_base = pygame.image.load(os.path.join(path_poubelles, "poubelle_verte.png")).convert_alpha()
        self.dechet_carton_base = pygame.image.load(os.path.join(path_poubelles, "carton.png")).convert_alpha()
        self.dechet_pomme_base = pygame.image.load(os.path.join(path_poubelles, "pomme.png")).convert_alpha()
        self.dechet_verre_base = pygame.image.load(os.path.join(path_poubelles, "verre.png")).convert_alpha()

        self._create_poubelles()
        self._load_dechets()

        # Variable pour stocker le menu ouvert
        self.menu_tri_actuel = None
        self.poubelle_concernee = None

    def transition_vers(self, nom_salle, image_bg, x_joueur=50):
        """
        Prépare une transition en fondu vers une nouvelle salle.
        """
        if self.faded_direction == 0:
            self.prochaine_salle_nom = nom_salle
            self.prochain_bg = image_bg
            self.prochaine_pos_x = x_joueur
            self.faded_direction = 1

    def _scale_item(self, image, target_width=None, target_height=None):
        """
        Redimensionne une image en conservant son ratio quand nécessaire.
        """
        orig_w, orig_h = image.get_size()
        if target_width is None and target_height is None:
            return image
        if target_width is None:
            target_width = int(orig_w * target_height / orig_h)
        if target_height is None:
            target_height = int(orig_h * target_width / orig_w)
        return pygame.transform.smoothscale(image, (target_width, target_height))

    def _scale_gardien(self, image):
        """
        Applique une taille adaptée aux gardiens en fonction de la largeur de l'écran.
        """
        target_width = max(180, min(360, int(self.WIDTH * 0.18)))
        return self._scale_item(image, target_width=target_width)

    def _ground_offset(self):
        return max(180, int(self.HEIGHT * 0.20))

    def _position_gardiens(self):
        """
        Positionne les gardiens sur l'écran en fonction de la taille de la fenêtre.
        """
        bottom_offset = self._ground_offset() + 20
        self.gardien_rect = self.gardien_img.get_rect()
        self.gardien_rect.centerx = self.WIDTH // 2
        self.gardien_rect.bottom = self.HEIGHT - bottom_offset
        self.gardien_tri_rect = self.gardien_tri_img.get_rect()
        self.gardien_tri_rect.left = max(20, int(self.WIDTH * 0.05))
        self.gardien_tri_rect.bottom = self.HEIGHT - bottom_offset

    def _create_poubelles(self):
        """
        Crée ou met à jour les poubelles de tri affichées à l'écran.
        """
        previous_states = []
        if hasattr(self, "poubelles"):
            previous_states = [p.reussie for p in self.poubelles]

        poubelle_width = max(72, min(140, int(self.WIDTH * 0.09)))
        img_p_jaune = self._scale_item(self.poubelle_jaune_base, target_width=poubelle_width)
        img_p_marron = self._scale_item(self.poubelle_marron_base, target_width=poubelle_width)
        img_p_verte = self._scale_item(self.poubelle_verte_base, target_width=poubelle_width)

        sol_y = self.HEIGHT - self._ground_offset()
        self.poubelles = [
            Poubelle(int(self.WIDTH * 0.25), sol_y, img_p_jaune, "yellow", "recyclable"),
            Poubelle(int(self.WIDTH * 0.5), sol_y, img_p_marron, "brown", "ordure"),
            Poubelle(int(self.WIDTH * 0.75), sol_y, img_p_verte, "green", "verre")
        ]

        if previous_states:
            for poubelle, etat in zip(self.poubelles, previous_states):
                poubelle.reussie = etat

        if hasattr(self, "poubelle_concernee") and self.poubelle_concernee is not None:
            self.poubelle_concernee = next((p for p in self.poubelles if p.type == self.poubelle_concernee.type), self.poubelle_concernee)
            if self.menu_tri_actuel:
                self.ouvrir_menu_tri(self.poubelle_concernee)

    def _load_dechets(self):
        """
        Redimensionne les icônes de déchets selon la taille de l'écran.
        """
        target_width = max(40, min(70, int(self.WIDTH * 0.05)))
        self.img_carton = self._scale_item(self.dechet_carton_base, target_width=target_width)
        self.img_pomme = self._scale_item(self.dechet_pomme_base, target_width=target_width)
        self.img_verre = self._scale_item(self.dechet_verre_base, target_width=target_width)

    def resize(self):
        super().resize()
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))
        self.bg_epreuve1 = pygame.transform.scale(self.bg_epreuve1_base, (self.WIDTH, self.HEIGHT + 60))
        self.bg_epreuve2 = pygame.transform.scale(self.bg_epreuve2_base, (self.WIDTH, self.HEIGHT))
        self.gardien_img = self._scale_gardien(self.gardien_img_base)
        self.gardien_tri_img = self._scale_gardien(self.gardien_tri_img_base)
        self._position_gardiens()
        self._create_poubelles()
        self._load_dechets()
        self.epreuve.resize(self.screen, self.WIDTH, self.HEIGHT, self.player.GROUND + self.player.rect.height, self.player.max_jump_height())

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            # condition pour voir si le joueur ferme la fenêtre
            # print(self.WIDTH, self.HEIGHT) # debug temporaire
            for event in pygame.event.get():
                # regarde si une touche est pressé
                self.event(event)

                # devrait etre ajouter d'une maniere ou d'une autre a la methode event
                # ou tt simplement faire une methode pour la classe game et pas fenetre
                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True # ?

                
                    if event.key == pygame.K_e:
                        # Touche E utilisée pour interagir avec le gardien ou lancer l'épreuve.
                        if self.salle_actuelle == "lumiere" and not self.epreuve.active:
                            if self.epreuve_lumiere_terminee:
                                if self.dialogue_actuel:
                                    self.dialogue_actuel = None
                                else:
                                    self.dialogue_actuel = ("Merci encore d'avoir éteint les lumières!", "black")
                                self.indice_dialogue = -1
                            else:
                                if self.indice_dialogue == -1:
                                    self.indice_dialogue = 0
                                elif self.indice_dialogue < len(self.dialogues_gardien) - 1:
                                    self.indice_dialogue += 1
                                else:
                                    self.indice_dialogue = -1
                                    self.dialogue_actuel = None
                                    ground_y = self.player.GROUND + self.player.rect.height
                                    self.epreuve.lancer(ground_y, self.player.max_jump_height())

                        elif self.salle_actuelle == "tri_dechets":
                            # Gestion des interactions de tri dans la salle recyclage.
                            if self.epreuve_tri_terminee:
                                if self.dialogue_actuel:
                                    self.dialogue_actuel = None
                                else:
                                    self.dialogue_actuel = ("Merci encore pour ton aide ! Nitidopolis respire mieux grâce à toi.", "black")

                            elif not self.tri_autorise:
                                # Affiche une séquence de dialogues explicatifs avant de pouvoir trier.
                                if self.indice_dialogue_tri < len(self.dialogues_gardien_tri) - 1:
                                    self.indice_dialogue_tri += 1
                                    self.dialogue_actuel = (self.dialogues_gardien_tri[self.indice_dialogue_tri], "black")
                                else:
                                    self.indice_dialogue_tri = -1
                                    self.dialogue_actuel = None
                                    self.tri_autorise = True

                            else:
                                if self.dialogue_actuel:
                                    self.dialogue_actuel = None
                                else:
                                    # Si le joueur touche une poubelle, ouvrir le menu de tri.
                                    for p in self.poubelles:
                                        if self.player.rect.colliderect(p.rect):
                                            if hasattr(p, 'reussie') and p.reussie:
                                                self.dialogue_actuel = ("Cette poubelle est déjà bien triée !", "black")
                                            else:
                                                self.ouvrir_menu_tri(p)
                                            break
                                        
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.menu_tri_actuel:
                    choix = self.menu_tri_actuel.check_click(event.pos)
                    if choix:
                        if choix == self.poubelle_concernee.dechet_attendu:
                            self.dialogue_actuel = ("Bravo ! C'est le bon tri.", "green")
                            self.poubelle_concernee.reussie = True 
                            if all(p.reussie for p in self.poubelles):
                                self.geste_count = min(self.geste_max, self.geste_count + 1)
                                self.epreuve_tri_terminee = True
                                self.dialogue_actuel = ("Super ! Ton implication est très utile pour Nitidopolis ! ", "green")
                        else:
                            self.dialogue_actuel = ("Aïe... ce déchet va ailleurs.", "red")
                        self.menu_tri_actuel = None #Ferme le menu                 

            if self.faded_direction == 1:
                # Fondu vers la nouvelle salle : opacité augmente.
                self.fade_opacite += 8
                if self.fade_opacite >= 255:
                    self.fade_opacite = 255
                    self.salle_actuelle = self.prochaine_salle_nom
                    self.background = pygame.transform.scale(self.prochain_bg, (self.WIDTH, self.HEIGHT))
                    self.player.rect.left = self.prochaine_pos_x
                    self.faded_direction = -1

            elif self.faded_direction == -1:
                # Arrivée de la nouvelle salle : opacité diminue.
                self.fade_opacite -= 8
                if self.fade_opacite <= 0:
                    self.fade_opacite = 0
                    self.faded_direction = 0

            # Mise à jour de l'épreuve de lumière même si elle n'est pas active.
            dt = clock.get_time() / 1000
            self.epreuve.update(self.player.rect, dt)

            # Gestion de la fin de l'épreuve de lumière.
            if self.epreuve.termine:
                if self.epreuve.reussite:
                    self.geste_count = min(self.geste_max, self.geste_count + 1)
                    self.dialogue_actuel = ("Bravo ! Toutes les lumières sont éteintes, tu as économisé de l’énergie et protégé la planète !", "green")
                    self.epreuve_lumiere_terminee = True
                else:
                    self.dialogue_actuel = ("Trop lent ! Réessaie de les éteindre.", "red")
                self.epreuve.termine = False


            # Déclenche les transitions de salle lorsque le joueur atteint le bord droit.
            if self.salle_actuelle == "spawn" and self.player.rect.right >= self.WIDTH:
                self.transition_vers("lumiere", self.bg_epreuve1)

            if self.salle_actuelle == "lumiere" and self.player.rect.right >= self.WIDTH and self.epreuve.reussite:
                self.transition_vers("tri_dechets", self.bg_epreuve2)

            if self.salle_actuelle == "tri_dechets" and self.player.rect.right >= self.WIDTH and self.epreuve_tri_terminee:
                self.transition_vers("tri_poubelle", self.bg_epreuve3)

            # Dessine le fond situé derrière les éléments dynamiques.
            self.screen.blit(self.background, (0, 0))

            # Contenu spécifique selon la salle actuelle.
            if self.salle_actuelle == "lumiere":
                self.screen.blit(self.background, (0, -60))
                self.screen.blit(self.gardien_img, self.gardien_rect)
                self.epreuve.draw()

            elif self.salle_actuelle == "tri_dechets":
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.gardien_tri_img, self.gardien_tri_rect)
                for p in self.poubelles:
                    p.draw(self.screen)

            elif self.salle_actuelle == "tri_poubelle":
                self.screen.blit(self.background, (0, 0))
                from lvl.lvl_recyclage import LvlRecyclage
                tri_poubelle = LvlRecyclage()
                tri_poubelle.run()

            else:  # spawn
                self.screen.blit(self.background, (0, 0))

            # Affiche le compteur de gestes écologiques en haut à gauche.
            if self.geste_icon is not None:
                hud_x, hud_y = 10, 10
                self.screen.blit(self.geste_icon, (hud_x, hud_y))
                geste_text = self.font_epreuve.render(f"{self.geste_count}/{self.geste_max}", True, "white")
                text_x = hud_x + self.geste_icon.get_width() + 6
                geste_rect = geste_text.get_rect(midleft=(text_x, hud_y + self.geste_icon.get_height() // 2))
                self.screen.blit(geste_text, geste_rect)

            # --- DESSIN DES ENTITÉS ET INTERFACES ---
            if self.menu_tri_actuel:
                self.menu_tri_actuel.draw(self.screen)

            #Gestion auto du texte de dialogue du gardien
            if self.indice_dialogue != -1:
                self.dialogue_actuel = (self.dialogues_gardien[self.indice_dialogue], "black")


            # Afficher le joueur
            self.screen.blit(self.player.image, self.player.rect)

            self.move = True
            self.player.apply_gravity()

            if self.pressed.get(pygame.K_q) and self.player.rect.left > 0:
                self.player.move_left()
                self.move = False

            if self.pressed.get(pygame.K_d) and self.player.rect.right < self.WIDTH:
                self.player.move_right()
                self.move = False

            # verifie si barre espace est pressé + si le personnage est déjà en train de sauté ou non
            if self.pressed.get(pygame.K_SPACE) and not self.player.jumping:
                self.player.jump()
                self.move = False

            if self.move:
                self.player.idle()

            # Afficher le dialogue si actif
            if self.dialogue_actuel:
                texte, couleur = self.dialogue_actuel
                afficher_dialogue(self.screen, texte, couleur)
                
            if self.fade_opacite > 0:
                self.fade_surface.set_alpha(self.fade_opacite)
                self.screen.blit(self.fade_surface, (0, 0))

            clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()

    def ouvrir_menu_tri(self, poubelle):
        """Ouvre le menu de tri pour la poubelle sélectionnée."""
        self.poubelle_concernee = poubelle
        # Exemple : La poubelle jaune propose Carton vs Pomme
        if poubelle.type == "yellow":
            self.menu_tri_actuel = MenuTri(poubelle.rect, self.img_carton, self.img_pomme, "recyclable", "organique")
        if poubelle.type == "brown":
            self.menu_tri_actuel = MenuTri(poubelle.rect, self.img_pomme, self.img_verre, "ordure", "verre")
        if poubelle.type == "green":
            self.menu_tri_actuel = MenuTri(poubelle.rect, self.img_verre, self.img_carton, "verre", "recyclable")
