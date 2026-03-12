import os
import pygame
from personnage.joueur import Player 




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
        image_path = os.path.join(base_path,"..", "assets", "ville1.png")

        #charger le background
        self.background = pygame.image.load(image_path).convert()
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        
        self.player = Player()  # spawn player
        self.pressed = {}

        print(self.pressed)

        self.running = True


    # Fonction qui permet de lancer la fenêtre de jeu
    def run(self):
        while self.running:
            #condition pour voir si le joueur ferme la fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #condition pour faire avancer le jouer / fermer la fenêtre avec esc
                elif event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

            # Afficher le background
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image,self.player.rect)
            
            if self.pressed.get(pygame.K_q) and self.player.rect.x > -5:
                self.player.move_left()
            elif self.pressed.get(pygame.K_d) and self.player.rect.x < self.WIDTH-25:
                self.player.move_right()

            pygame.display.flip()
        print(self.WIDTH)
        pygame.quit()


