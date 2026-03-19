import os
import pygame
from personnage.joueur import Player
from ui.dialogue import afficher_dialogue

# CONSTANTES RÉAJUSTABLE
FPS = 60


# Instancier la fenêtre de jeu
class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()

        # Récupérer la résolution de l'écran
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        # Créer la fenêtre avec bordure
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("The Green Path")

        # Chemin absolu vers le dossier du fichier .py
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "..", "assets", "ville1.png")

        # charger le background
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.player = Player()  # spawn player
        self.pressed = {}

        self.running = True
        self.move: bool
        # État du dialogue (None = pas de dialogue, sinon tuple (texte, couleur))
        self.dialogue_actuel = None

    # Fonction qui permet de lancer la fenêtre de jeu
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            # condition pour voir si le joueur ferme la fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # condition fermer la fenêtre avec esc
                elif event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    # Touche E : afficher/fermer un dialogue (exemple)
                    if event.key == pygame.K_e:
                        if self.dialogue_actuel:
                            self.dialogue_actuel = None  # Fermer le dialogue
                        else:
                            # Exemple : afficher un dialogue du joueur (bleu)
                            self.dialogue_actuel = (
                                "Bonjour ! Je suis le protecteur de la nature.",
                                "dodgerblue",
                            )
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            # Afficher le background
            self.screen.blit(self.background, (0, 0))
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

            clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()


