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
        info = pygame.display.Info()

        # Récupérer la résolution de l'écran
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        # Créer la fenêtre avec bordure
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
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
            info = pygame.display.Info()
            self.WIDTH, self.HEIGHT = info.current_w, info.current_h
            mode = pygame.FULLSCREEN
            dim = (self.WIDTH, self.HEIGHT)
        else:
            mode = pygame.RESIZABLE
            dim = (int(self.WIDTH * 0.98), int(self.HEIGHT * 0.98))
        self.screen = pygame.display.set_mode(dim, mode)
        if self.elems is not None:
            self.resize_obj()



class Game(Fenetre):
    def __init__(self):
        # permet d'hériter de la classe parent (fait le init du parent)
        super().__init__("The Green Path")
        pygame.mixer.init()
        # Chemin absolu vers le dossier du fichier .py
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "..", "assets", "ville1.png")

        # Musique du jeu
        music_path = os.path.join(base_path, "..", "assets", "Sound", "Lobby Time.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # charger le background
        self.background_base = pygame.image.load(image_path).convert()
        # pour eviter la perte d'info lors du scale on differentie l'image de base et celle scale
        self.background = pygame.transform.scale(self.background_base, (self.WIDTH, self.HEIGHT))

        self.player = Player(self.WIDTH, self.HEIGHT)  # spawn player avec taille de fenêtre
        self.player.actu(self.WIDTH, self.HEIGHT)
        self.pressed = {} 
 
        self.move: bool

        # État du dialogue (None = pas de dialogue, sinon tuple (texte, couleur))
        self.dialogue_actuel = None

        self.salle_actuelle = "spawn"
        image_path_epreuve1 = os.path.join(base_path, "..", "assets", "provisoirebg.png")
        self.bg_epreuve1 = pygame.image.load(image_path_epreuve1).convert()

        self.fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.fade_surface.fill((0,0,0))
        self.fade_opacite = 0
        self.faded_direction = 0

        self.prochaine_salle_nom = ""
        self.prochain_bg = None
        self.prochaine_pos_x = 50        
        
        self.font_epreuve = pygame.font.SysFont("Arial", 30, bold = True)
        self.epreuve = EpreuveLumiere(self.screen, self.font_epreuve, self.WIDTH, self.HEIGHT)
        # Element a redimensionner
        self.elems = ["background"] # on mettra les plateformes et autres surfaces 

    def transition_vers(self, nom_salle, image_bg, x_joueur=50):
        """Cette méthode prépare les données pour le fondu"""
        if self.faded_direction == 0: 
            self.prochaine_salle_nom = nom_salle
            self.prochain_bg = image_bg
            self.prochaine_pos_x = x_joueur
            self.faded_direction = 1

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            #print(f"Sallle: {self.salle_actuelle} | Pos: {self.player.rect.right} | Goal: {self.WIDTH}")
            #print(f"Direction fondu: {self.faded_direction} | Opacité: {self.fade_opacite}")
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
                        if self.dialogue_actuel:
                            self.dialogue_actuel = None  # Fermer le dialogue
                        elif self.salle_actuelle == "lumiere" and not self.epreuve.active:
                            self.epreuve.lancer()
                            self.dialogue_actuel = ("Vite ! Eteins les lumières !", "orange")
                       

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
                    self.dialogue_actuel = ("Gagné ! La ville dépense moins!", "green")
                else:
                    self.dialogue_actuel = ("Trop lent ! Réessaie de les éteindre.", "red")
                self.epreuve.termine = False


            if self.salle_actuelle == "spawn" and self.player.rect.right >= self.WIDTH:
                self.transition_vers("lumiere", self.bg_epreuve1)

            # Afficher le background
            self.screen.blit(self.background, (0, 0))
            # appeler le niveau: self.screen.blits() pour mettre les plateformes

            #pour afficher les ampoules
            self.epreuve.draw()

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


