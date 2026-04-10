import pygame
import random

class EpreuveLumiere:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.WIDTH = width
        self.HEIGHT = height
        
        self.active = False
        self.termine = False
        self.reussite = False
        self.temps_restant = 10.0
        self.cibles = []

    def lancer(self):
        self.active = True
        self.termine = False
        self.temps_restant = 10.0
        self.cibles = [pygame.Rect(random.randint(100, self.WIDTH-100), 
                                   random.randint(100, self.HEIGHT-200), 40, 40) for _ in range(5)]

    def update(self, player_rect, dt):
        if not self.active: return
        
        self.temps_restant -= dt
        if self.temps_restant <= 0:
            self.active = False
            self.termine = True
            self.reussite = False
            
        for cible in self.cibles[:]:
            if player_rect.colliderect(cible):
                self.cibles.remove(cible)

        if len(self.cibles) == 0:
            self.active = False
            self.termine = True
            self.reussite = True

    def draw(self):
        if not self.active: return
        for cible in self.cibles:
            pygame.draw.circle(self.screen, (255, 255, 0), cible.center, 20)
        
        timer_surf = self.font.render(f"Temps: {int(self.temps_restant)}s", True, (255, 255, 255))
        self.screen.blit(timer_surf, (self.WIDTH // 2, 50))

        #Couleur du chrono
        couleur_chrono = (255, 0, 0) if self.temps_restant < 5 else (255, 255, 255)
        
        # 2. Préparer le texte (on arrondit à une décimale pour le style)
        texte_temps = f"Temps restant : {max(0, self.temps_restant):.1f}s"
        surface_chrono = self.font.render(texte_temps, True, couleur_chrono)
        
        # 3. Positionner en haut au centre
        rect_chrono = surface_chrono.get_rect(center=(self.WIDTH // 2, 50))
        
        # 4. Optionnel : dessiner un petit fond sombre derrière le texte pour la lisibilité
        fond_rect = rect_chrono.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), fond_rect, border_radius=10)
        
        # 5. Afficher sur l'écran
        self.screen.blit(surface_chrono, rect_chrono)