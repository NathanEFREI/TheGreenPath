import pygame

class QCM:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        
        self.questions = [
            {
                "titre": "Pourquoi éteindre la lumière en partant ?",
                "reponses": ["Pour économiser l'énergie", "Pour faire joli", "Car les ampoules ont peur"],
                "correct": 0
            },
            {
                "titre": "Quel est l'impact du gaspillage d'énergie ?",
                "reponses": ["Ça crée de la pluie", "Ça pollue l'air et la nature", "Aucun impact"],
                "correct": 1
            },
            {
                "titre": "Que deviennent les déchets bien triés ?",
                "reponses": ["Ils disparaissent", "De nouvelles ressources", "De la nourriture"],
                "correct": 1
            },
            {
                "titre": "Où doit-on jeter un carton propre ?",
                "reponses": ["Poubelle Verte", "Poubelle Marron", "Poubelle Jaune"],
                "correct": 2
            },
            {
                "titre": "Quel est le risque d'un mauvais tri ?",
                "reponses": ["Polluer la nature", "Casser la poubelle", "Changer le temps"],
                "correct": 0
            },
            {
                "titre": "Que suit le compteur en haut à gauche ?",
                "reponses": ["Ta vitesse", "Tes gestes écologiques", "Ton nombre de pas"],
                "correct": 1
            },
            {
                "titre": "Comment s'appelle la 1ère phase du lancer ?",
                "reponses": ["Phase de Vol", "Phase de Visée", "Phase de Panique"],
                "correct": 1
            },
            {
                "titre": "Éteindre les lumières aide aussi...",
                "reponses": ["Les animaux et plantes", "À dormir plus vite", "À manger mieux"],
                "correct": 0
            },
            {
                "titre": "Où jeter un reste de pomme ?",
                "reponses": ["Poubelle Jaune", "Poubelle Verte", "Poubelle Marron"],
                "correct": 2
            },
            {
                "titre": "Quelle est la leçon des Gardiens ?",
                "reponses": ["Chaque petit geste compte", "Il faut tout acheter", "C'est trop difficile"],
                "correct": 0
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