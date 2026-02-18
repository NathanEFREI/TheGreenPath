import os
from pygame import *

init()

# Instancier la fenêtre de jeu
class Game:
    def __init__(self):
        info = display.Info()
        # Récupérer la résolution de l'écran 
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h

        # Créer la fenêtre avec bordure
        self.screen = display.set_mode((self.WIDTH, self.HEIGHT), RESIZABLE)
        display.set_caption("The Green Path")

        # Chemin absolu vers le dossier du fichier .py
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "assets", "ville1.png")
        self.background = image.load(image_path).convert()
        self.background = transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.running = True

    # Fonction qui permet de lancer la fenêtre de jeu
    def run(self):
        while self.running:
            for e in event.get():   # on évite d’écraser "event"
                if e.type == QUIT:
                    self.running = False

            # Afficher le background
            self.screen.blit(self.background, (0, 0))
            display.flip()

        quit()

# Créer et lancer le jeu
game = Game()
game.run()
