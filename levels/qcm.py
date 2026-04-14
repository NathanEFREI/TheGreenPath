import pygame

class QCM:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        
        self.questions = [
            {
                "titre": "Gardien Lumière : Pourquoi éteindre la lumière ?",
                "reponses": ["Économiser l'énergie", "Les ampoules ont peur", "Pour faire joli"],
                "correct": 0
            },
            {
                "titre": "Gardien Tri : Où va le carton propre ?",
                "reponses": ["Poubelle Verte", "Poubelle Jaune", "Par terre"],
                "correct": 1
            },
            {
                "titre": "Dernier geste : Pour économiser l'eau...",
                "reponses": ["Je prends un bain", "Je laisse couler", "Je prends une douche"],
                "correct": 2
            }
        ]
        
        self.indice_question = 0
        self.score = 0
        self.active = False
        self.termine = False
        self.boutons = []

    def lancer(self):
        self.active = True
        self.indice_question = 0
        self.score = 0
        self.termine = False
        self.generer_boutons()

    def generer_boutons(self):
        self.boutons = []
        if self.indice_question < len(self.questions):
            for i in range(3):
                rect = pygame.Rect(self.width // 4, 200 + i * 80, self.width // 2, 60)
                self.boutons.append(rect)

    def update(self, event):
        if not self.active or self.termine:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.boutons):
                if rect.collidepoint(event.pos):
                    # Vérifier si c'est la bonne réponse
                    if i == self.questions[self.indice_question]["correct"]:
                        self.score += 1
                    
                    # Passer à la suivante
                    self.indice_question += 1
                    if self.indice_question >= len(self.questions):
                        self.termine = True
                    else:
                        self.generer_boutons()

    def draw(self):
        if not self.active:
            return

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        if not self.termine:
            q = self.questions[self.indice_question]
            # Afficher la question
            txt_q = self.font.render(q["titre"], True, "white")
            self.screen.blit(txt_q, (self.width // 2 - txt_q.get_width() // 2, 100))

            # Afficher les boutons
            for i, rect in enumerate(self.boutons):
                pygame.draw.rect(self.screen, (100, 100, 100), rect, border_radius=10)
                txt_r = self.font.render(q["reponses"][i], True, "white")
                self.screen.blit(txt_r, (rect.centerx - txt_r.get_width() // 2, rect.centery - txt_r.get_height() // 2))
        else:
            # Score final
            txt_fin = self.font.render(f"Fini ! Score : {self.score}/{len(self.questions)}", True, "gold")
            self.screen.blit(txt_fin, (self.width // 2 - txt_fin.get_width() // 2, self.height // 2))
            txt_esc = self.font.render("Appuyez sur E pour quitter", True, "white")
            self.screen.blit(txt_esc, (self.width // 2 - txt_esc.get_width() // 2, self.height // 2 + 60))