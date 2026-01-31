import pygame

pygame.init()

# Instancier la fenêtre de jeu
class Game:
    def __init__(self):
        info = pygame.display.Info()
        # Récupérer la résolution de l'écran (un peu moins pour voir la croix)
        WIDTH, HEIGHT = info.current_w, info.current_h - 60
        # Créer la fenêtre avec bordure
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("EcoGame")
        self.running = True

    # Fonction qui permet de lancer la fenêtre de jeu
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()  

# Créer et lancer le jeu
game = Game()
game.run()
