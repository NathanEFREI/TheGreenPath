import os
import pygame
from pygame.surface import Surface
from personnage.joueur import Player
from ui.dialogue import afficher_dialogue
from constante import FPS
from levels.epreuve_lumiere import EpreuveLumiere
from .utils import draw_button, confirm_quit


# Instancier la fenêtre de jeu
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
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.VIDEORESIZE:
            self.WIDTH, self.HEIGHT = event.size
            self.resize()
        
        elif event.type == pygame.KEYDOWN:
                # fullscreen ou pas avec f11
                if event.key == pygame.K_F11: # peut faire un dico ou on met une fonction qui fait ca
                    self.fullscreen = not self.fullscreen
                    self.resize()

                # condition fermer la fenêtre avec esc
                elif event.key == pygame.K_ESCAPE:
                    self.running = False


    def resize_obj(self):
        """
        Permet de redimensionner la fenetre et tous les elements dans la liste passée
        """
        # scale des images de base (basique)
        for e in self.elems:
            setattr(self, e, pygame.transform.scale(getattr(self, e + "_base"), (self.WIDTH, self.HEIGHT)))

        # Ceux qui ont deja leur methode resize (que Player pour l'instant)
        ## une liste pour appeler direct resize de l'element ?
        self.player.actu(self.WIDTH, self.HEIGHT)


    def resize(self):
        """
        Permet de passer du fullscreen en mode resize et inversement
        """
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
        # permet d'hériter de la classe parent (fait le init du parent)
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

        # charger le background
        self.background_base = pygame.image.load(image_path).convert()
        # pour eviter la perte d'info lors du scale on differentie l'image de base et celle scale
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))

        self.player = Player(self.WIDTH, self.HEIGHT)  # spawn player avec taille de fenêtre
        self.player.actu(self.WIDTH, self.HEIGHT)
        self.pressed = {}
        self.geste_count = 0
        self.geste_max = 3
        self.geste_icon = None

        self.move: bool

        # État du dialogue (None = pas de dialogue, sinon tuple (texte, couleur))
        self.dialogue_actuel = None

        self.salle_actuelle = "spawn"

        image_path_epreuve1 = os.path.join(base_path, "..", "assets", "epreuve_lumiere_bg.png")
        self.bg_epreuve1_base = pygame.image.load(image_path_epreuve1).convert()
        
        # On agrandit un peu la hauteur pour ne pas avoir de bande noire en bas quand on remonte l'image
        self.bg_epreuve1 = pygame.transform.scale(self.bg_epreuve1_base, (self.WIDTH, self.HEIGHT + 60))

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
        path_gardien = os.path.join(base_path, "..", "assets", "gardien", "gardien-lumiere.png")
        # On charge, on scale, et on crée le rectangle directement
        self.gardien_img = pygame.image.load(path_gardien).convert_alpha()
        self.gardien_img = pygame.transform.scale(self.gardien_img, (360, 160))
        self.gardien_rect = self.gardien_img.get_rect()
        
        # On le centre
        self.gardien_rect.centerx = self.WIDTH // 2
        
        # On le pose tout en bas de l'écran 
        self.gardien_rect.bottom = self.HEIGHT - 240

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
        self.elems = ["background"] # on mettra les plateformes et autres surfaces 

    def transition_vers(self, nom_salle, image_bg, x_joueur=50):
        """
        Cette méthode prépare les données pour le fondu
        """
        if self.faded_direction == 0: 
            self.prochaine_salle_nom = nom_salle
            self.prochain_bg = image_bg
            self.prochaine_pos_x = x_joueur
            self.faded_direction = 1

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

                    # Touche E : afficher/fermer un dialogue (exemple)
                    if event.key == pygame.K_e:
                        if self.salle_actuelle == "lumiere" and not self.epreuve.active:
                            
                            if self.indice_dialogue == -1:
                                self.indice_dialogue = 0
                            
                            elif self.indice_dialogue < len(self.dialogues_gardien) - 1:
                                self.indice_dialogue += 1
                            
                            else:
                                self.indice_dialogue = -1 
                                self.dialogue_actuel = None
                                self.epreuve.lancer()
                       

                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            if self.faded_direction == 1:
                self.fade_opacite += 8
                if self.fade_opacite >= 255:
                    self.fade_opacite = 255

                    self.salle_actuelle = self.prochaine_salle_nom
                    self.background = pygame.transform.scale(self.prochain_bg, (self.WIDTH,self.HEIGHT))
                    self.player.rect.left = self.prochaine_pos_x
                    self.faded_direction = -1

            elif self.faded_direction == -1:
                self.fade_opacite -= 8
                if self.fade_opacite <= 0:
                    self.fade_opacite = 0
                    self.faded_direction = 0

            dt = clock.get_time() / 1000 
            self.epreuve.update(self.player.rect, dt)

            # Gestion de la fin de l'épreuve
            if self.epreuve.termine:
                if self.epreuve.reussite:
                    self.geste_count = min(self.geste_max, self.geste_count + 1)
                    self.dialogue_actuel = ("Bravo ! Toutes les lumières sont éteintes, tu as économisé de l’énergie et protégé la planète !", "green")
                else:
                    self.dialogue_actuel = ("Trop lent ! Réessaie de les éteindre.", "red")
                self.epreuve.termine = False


            if self.salle_actuelle == "spawn" and self.player.rect.right >= self.WIDTH:
                self.transition_vers("lumiere", self.bg_epreuve1)

            # Afficher le background
            self.screen.blit(self.background, (0, 0))
            # appeler le niveau: self.screen.blits() pour mettre les plateformes

            if self.salle_actuelle == "lumiere":
                self.screen.blit(self.background, (0, - 60))
                self.screen.blit(self.gardien_img, self.gardien_rect)
            else:
                self.screen.blit(self.background, (0, 0))

            # Afficher le compteur de gestes écologiques
            if self.geste_icon is not None:
                hud_x, hud_y = 10, 10
                self.screen.blit(self.geste_icon, (hud_x, hud_y))
                geste_text = self.font_epreuve.render(f"{self.geste_count}/{self.geste_max}", True, "white")
                text_x = hud_x + self.geste_icon.get_width() + 6
                geste_rect = geste_text.get_rect(midleft=(text_x, hud_y + self.geste_icon.get_height() // 2))
                self.screen.blit(geste_text, geste_rect)

            self.epreuve.draw()
            self.screen.blit(self.player.image, self.player.rect)

            if self.indice_dialogue != -1:
                self.dialogue_actuel = (self.dialogues_gardien[self.indice_dialogue], "black")

            if self.dialogue_actuel:
                texte, couleur = self.dialogue_actuel
                afficher_dialogue(self.screen, texte, couleur)



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


