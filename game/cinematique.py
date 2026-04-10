from __future__ import annotations
from constante import VITESSE_LETTRE, VITESSE_FADE
from game.game import Fenetre
import os
import pygame
from ui.dialogue import afficher_dialogue

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SLIDES = [
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "ville1-nopollution.png"),
        "texte": "Il y a longtemps, Nitidopolis était une ville où il faisait bon vivre. "
                 "Les arbres bordaient chaque rue, l'air était pur, et la nature et les "
                 "hommes coexistaient en harmonie.",
        "duree_min": 3000,
    },
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "ville1.png"),
        "texte": "Mais les années ont passé. Les usines ont grandi, les déchets se sont "
                 "accumulés, et personne n'a rien fait. Aujourd'hui, Nitidopolis étouffe "
                 "sous la pollution.",
        "duree_min": 3000,
    },
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "ville1.png"),
        "texte": "Tu es parti il y a longtemps. Mais quelque chose t'a ramené ici, dans "
                 "ta ville natale. Tu ne reconnais plus les rues que tu aimais.",
        "duree_min": 3000,
    },
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "slide_gardiens.png"),
        "texte": "On dit que des gardiens de la nature veillent encore dans les zones "
                 "épargnées. Chacun détient un savoir, un geste simple mais essentiel "
                 "pour faire renaître la vie.",
        "duree_min": 3000,
    },
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "slide_gardiens.png"),
        "texte": "Tu devras les trouver, relever leurs épreuves, et apprendre leurs "
                 "secrets. Ce n'est qu'armé de ces gestes que tu pourras revenir "
                 "sauver Nitidopolis.",
        "duree_min": 3000,
    },
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "Commande.png"),
        "texte": "Voici des commandes qui pourront t'aider dans ta quête :\n",
        "duree_min": 3000,
    },
    {
        "image": os.path.join(BASE_DIR, "assets", "cinematique", "slide_appel.png"),
        "texte": "Nitidopolis t'attend. Son avenir est entre tes mains.",
        "duree_min": 3000,
    },
]




class SceneCinematique():
    def __init__(self, screen: pygame.Surface, callback_fin):
        
        self.screen       = screen
        self.callback_fin = callback_fin
        self.WIDTH, self.HEIGHT = screen.get_size()

        #Musique avec fade in automatique
        musique = os.path.join(BASE_DIR, "assets", "Sound", "musique_cinematique.mp3")
        try:
            pygame.mixer.music.load(musique)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1, fade_ms=3000)  # fade in 3s
        except Exception:
            pass

        # Fade écran
        self.fade_surface   = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.fade_alpha     = 255
        self.fade_direction = -1
        self.en_transition  = False
        self.terminee       = False

        self.font_hint = pygame.font.SysFont("arial", 20)

        self._charger_slide(0)

    # ------------------------------
    # Slides
    # ------------------------------

    def _charger_slide(self, index: int) -> None:
        self.index_slide = index
        slide = SLIDES[index]

        try:
            img = pygame.image.load(slide["image"]).convert()
            self.background = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
        except Exception:
            self.background = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.background.fill((15, 15, 25))

        self.texte_complet = slide["texte"]
        self.texte_affiche = ""
        self.index_lettre  = 0
        self.timer_lettre  = 0

        self.timer_slide = 0
        self.slide_prete = False

    def _texte_termine(self) -> bool:
        return self.index_lettre >= len(self.texte_complet)

    def _completer_texte(self) -> None:
        self.texte_affiche = self.texte_complet
        self.index_lettre  = len(self.texte_complet)

    def _passer_suivante(self) -> None:
        if not self.slide_prete or self.en_transition:
            return
        self.en_transition  = True
        self.fade_direction = 1

    # ------------------------------
    # Events
    # ------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_SPACE, pygame.K_RETURN):
            if not self._texte_termine():
                self._completer_texte()
            else:
                self._passer_suivante()

    # ------------------------------
    # Update
    # ------------------------------

    def update(self, dt: int) -> None:
        if self.terminee:
            return

        # Machine à écrire
        if not self._texte_termine():
            self.timer_lettre += dt
            while self.timer_lettre >= VITESSE_LETTRE and not self._texte_termine():
                self.texte_affiche += self.texte_complet[self.index_lettre]
                self.index_lettre += 1
                self.timer_lettre -= VITESSE_LETTRE

        # Temps minimum
        self.timer_slide += dt
        if self.timer_slide >= SLIDES[self.index_slide]["duree_min"]:
            self.slide_prete = True

        # Fade écran
        if self.fade_direction == 1:
            self.fade_alpha = min(255, self.fade_alpha + VITESSE_FADE)
            if self.fade_alpha == 255:
                if self.index_slide + 1 < len(SLIDES):
                    self._charger_slide(self.index_slide + 1)
                    self.fade_direction = -1
                    self.en_transition  = False
                else:
                    #ade out musique simple
                    pygame.mixer.music.fadeout(2000)
                    self.terminee = True

        elif self.fade_direction == -1:
            self.fade_alpha = max(0, self.fade_alpha - VITESSE_FADE)
            if self.fade_alpha == 0:
                self.fade_direction = 0

    # ------------------------------
    # Draw
    # ------------------------------

    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))

        if self.texte_affiche.strip():
            afficher_dialogue(
                self.screen,
                self.texte_affiche,
                couleur=(15, 15, 40),
                position="bas",
                taille_police=28,
                couleur_texte=(230, 230, 230),
                couleur_bordure=(70, 70, 100),
                epaisseur_bordure=3,
            )

        if self.slide_prete and self._texte_termine():
            if (pygame.time.get_ticks() // 600) % 2 == 0:
                hint = self.font_hint.render(
                    "[ Espace ] continuer",
                    True,
                    (160, 160, 160),
                )
                rect = hint.get_rect(
                    centerx=self.WIDTH // 2,
                    bottom=self.HEIGHT - 10,
                )
                self.screen.blit(hint, rect)

        if self.fade_alpha > 0:
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))