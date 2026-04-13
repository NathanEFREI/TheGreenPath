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

    def lancer(self, ground_y=None, player_jump_height=None):
        self.active = True
        self.termine = False
        self.temps_restant = 10.0
        self.cibles = []
        self.ground_y = ground_y
        self.player_jump_height = player_jump_height
        
        screen_w, screen_h = self.screen.get_size()
        
        if ground_y is None or player_jump_height is None:
            ground_offset = max(180, int(screen_h * 0.20))
            ground_y = screen_h - ground_offset
            player_jump_height = max(120, int(screen_h * 0.20))

        min_y = max(80, int(ground_y - player_jump_height))
        max_y = min(int(ground_y - 40), screen_h - 40)
        if max_y <= min_y:
            max_y = min_y + 1
        
        for i in range(5):
            x = random.randint(100, screen_w - 100)
            y = random.randint(min_y, max_y)
            self.cibles.append(pygame.Rect(x, y, 40, 40))

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

    def resize(self, screen, width, height, ground_y=None, player_jump_height=None):
        old_width, old_height = self.WIDTH, self.HEIGHT
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        if ground_y is not None:
            self.ground_y = ground_y
        if player_jump_height is not None:
            self.player_jump_height = player_jump_height
        if not self.active or old_width <= 0 or old_height <= 0:
            return

        min_y = max(0, int(self.ground_y - self.player_jump_height))
        max_y = min(int(self.ground_y - 40), height - 40)
        if max_y <= min_y:
            max_y = min_y + 1

        for cible in self.cibles:
            rel_x = cible.x / old_width
            rel_y = cible.y / old_height
            new_x = int(rel_x * width)
            new_y = int(rel_y * height)
            new_x = max(100, min(width - 100, new_x))
            cible.x = new_x
            cible.y = max(min_y, min(max_y, new_y))

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