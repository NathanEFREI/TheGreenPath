import os
import pygame
from pygame.surface import Surface
from personnage.joueur import Player
from ui.dialogue import afficher_dialogue
from constante import FPS
from levels.epreuve_lumiere import EpreuveLumiere
from levels.epreuve_poubelle import Poubelle
from levels.menu_tri_poubelle import MenuTri
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
        self.epreuve_lumiere_terminee = False

        image_path_epreuve1 = os.path.join(base_path, "..", "assets", "epreuve_lumiere_bg.png")
        self.bg_epreuve1_base = pygame.image.load(image_path_epreuve1).convert()
        
        # On agrandit un peu la hauteur pour ne pas avoir de bande noire en bas quand on remonte l'image
        self.bg_epreuve1 = pygame.transform.scale(self.bg_epreuve1_base, (self.WIDTH, self.HEIGHT + 60))

        image_path_epreuve2 = os.path.join(base_path, "..", "assets", "provisoirebg.png")
        self.bg_epreuve2_base = pygame.image.load(image_path_epreuve2).convert()
        self.bg_epreuve2 = pygame.transform.scale(self.bg_epreuve2_base, (self.WIDTH, self.HEIGHT))
        

        self.fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.fade_surface.fill((0,0,0))
        self.fade_opacite = 0
        self.faded_direction = 0

        self.prochaine_salle_nom = ""
        self.prochain_bg = None
        self.prochaine_pos_x = 50        
        

        self.font_epreuve = pygame.font.SysFont("Arial", 30, bold = True)
        self.epreuve = EpreuveLumiere(self.screen, self.font_epreuve, self.WIDTH, self.HEIGHT)

        #gardien epreuve lumiere
        path_gardien_lumiere = os.path.join(base_path, "..", "assets", "gardien", "gardien-lumiere.png")
        self.gardien_img = pygame.image.load(path_gardien_lumiere).convert_alpha()
        self.gardien_img = pygame.transform.scale(self.gardien_img, (360, 160))
        self.gardien_rect = self.gardien_img.get_rect()
        self.gardien_rect.centerx = self.WIDTH // 2
        self.gardien_rect.bottom = self.HEIGHT - 240
        
        #gardien epreuve recyclage
        path_gardien_tri = os.path.join(base_path, "..", "assets", "gardien", "gardien-recyclager.png")
        self.gardien_tri_img = pygame.image.load(path_gardien_tri).convert_alpha()
        self.gardien_tri_img = pygame.transform.scale(self.gardien_tri_img, (360, 160))
        self.gardien_tri_rect = self.gardien_tri_img.get_rect()
        
        self.gardien_tri_rect.left = 50
        self.gardien_tri_rect.bottom = self.HEIGHT - 240

        self.dialogues_gardien_tri = [
            "Je suis le gardien du recyclage, celui qui veille à ce que chaque déchet trouve sa place.",
            "Rien ne doit être perdu, car même ce que l'on jette peut encore servir.",
            "Les déchets mal triés polluent la nature, mais recyclés, ils deviennent de nouvelles ressources.",
            "Voici ton épreuve : ramasse les déchets et place-les dans la bonne poubelle.",
            "Chaque erreur de tri peut nuire à l'équilibre de la nature ! Prêt ?"
        ]
        self.indice_dialogue_tri = -1
        self.tri_autorise = False  

        self.epreuve_tri_terminee = False 
        self.tri_autorise = False



        # Liste des répliques du Gardien
        self.dialogues_gardien = [
            "Je suis le gardien de la lumière, celui qui veille à l'énergie.",
            "Éteindre la lumière quand on sort est un geste très important.",
            "Produire de l'électricité pollue parfois la nature.",
            "En éteignant, tu aides les animaux, les plantes et l'air !",
            "Voici ton épreuve : éteins tout le plus vite possible. Prêt ?"
        ]
        self.indice_dialogue = -1

        # Element a redimensionner
        self.elems = ["background"] # on mettra les plateformes et autres surfaces 


        path_poubelles = os.path.join(base_path, "..", "assets")

        img_p_jaune = pygame.transform.scale(pygame.image.load(os.path.join(path_poubelles, "poubelle_jaune.png")).convert_alpha(), (80,100))
        img_p_marron = pygame.transform.scale(pygame.image.load(os.path.join(path_poubelles, "poubelle_marron.png")).convert_alpha(), (80,100))
        img_p_verte = pygame.transform.scale(pygame.image.load(os.path.join(path_poubelles, "poubelle_verte.png")).convert_alpha(), (80,100))

        sol_y = self.HEIGHT - 240
        self.poubelles = [
            Poubelle(self.WIDTH // 4, sol_y, img_p_jaune, "yellow", "recyclable"),
            Poubelle(self.WIDTH // 2, sol_y, img_p_marron, "brown", "ordure"),
            Poubelle(3 * self.WIDTH // 4, sol_y,img_p_verte,  "green", "verre")
        ]

        path_dechets = os.path.join(base_path, "..", "assets")
        self.img_carton = pygame.transform.scale(pygame.image.load(os.path.join(path_dechets, "carton.png")).convert_alpha(), (50, 50))
        self.img_pomme = pygame.transform.scale(pygame.image.load(os.path.join(path_dechets, "pomme.png")).convert_alpha(), (50, 50))
        self.img_verre = pygame.transform.scale(pygame.image.load(os.path.join(path_dechets, "verre.png")).convert_alpha(), (50, 50))
        
        # Variable pour stocker le menu ouvert
        self.menu_tri_actuel = None
        self.poubelle_concernee = None

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
            # condition pour voir si le joueur ferme la fenêtre
            # print(self.WIDTH, self.HEIGHT) # debug temporaire
            for event in pygame.event.get():
                # regarde si une touche est pressé
                self.event(event)

                # devrait etre ajouter d'une maniere ou d'une autre a la methode event
                # ou tt simplement faire une methode pour la classe game et pas fenetre
                if event.type == pygame.KEYDOWN:
                    self.pressed[event.key] = True # ?

                
                    if event.key == pygame.K_e:
                        # --- LOGIQUE SALLE LUMIÈRE ---
                        if self.salle_actuelle == "lumiere" and not self.epreuve.active:
                            if self.epreuve_lumiere_terminee:
                                if self.dialogue_actuel:
                                    self.dialogue_actuel = None
                                else:
                                    self.dialogue_actuel = ("Merci encore d'avoir éteint les lumières!", "black")
                                self.indice_dialogue = -1
                            else:
                                if self.indice_dialogue == -1:
                                    self.indice_dialogue = 0
                                elif self.indice_dialogue < len(self.dialogues_gardien) - 1:
                                    self.indice_dialogue += 1
                                else:
                                    self.indice_dialogue = -1 
                                    self.dialogue_actuel = None
                                    self.epreuve.lancer()

                        elif self.salle_actuelle == "tri_dechets":
                            # Cas 1 : L'épreuve est terminée, on affiche juste un message de remerciement
                            if self.epreuve_tri_terminee:
                                if self.dialogue_actuel:
                                    self.dialogue_actuel = None
                                else:
                                    self.dialogue_actuel = ("Merci encore pour ton aide ! Nitidopolis respire mieux grâce à toi.", "black")

                            elif not self.tri_autorise:
                                if self.indice_dialogue_tri < len(self.dialogues_gardien_tri) - 1:
                                    self.indice_dialogue_tri += 1
                                    self.dialogue_actuel = (self.dialogues_gardien_tri[self.indice_dialogue_tri], "black")
                                else:
                                    self.indice_dialogue_tri = -1
                                    self.dialogue_actuel = None
                                    self.tri_autorise = True # Maintenant on peut trier !

                            else: 
                                if self.dialogue_actuel:
                                    self.dialogue_actuel = None
                                else:
                                    for p in self.poubelles:
                                        if self.player.rect.colliderect(p.rect):
                                            if hasattr(p, 'reussie') and p.reussie:
                                                self.dialogue_actuel = ("Cette poubelle est déjà bien triée !", "black")
                                            else:
                                                self.ouvrir_menu_tri(p)
                                            break # On arrête la boucle dès qu'on a trouvé la poubelle touchée
                                        
                elif event.type == pygame.KEYUP:
                    self.pressed[event.key] = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.menu_tri_actuel:
                    choix = self.menu_tri_actuel.check_click(event.pos)
                    if choix:
                        if choix == self.poubelle_concernee.dechet_attendu:
                            self.dialogue_actuel = ("Bravo ! C'est le bon tri.", "green")
                            self.poubelle_concernee.reussie = True 
                            if all(p.reussie for p in self.poubelles):
                                self.epreuve_tri_terminee = True
                                self.dialogue_actuel = ("Super ! Ton implication est très utile pour Nitidopolis ! ", "green")
                        else:
                            self.dialogue_actuel = ("Aïe... ce déchet va ailleurs.", "red")
                        self.menu_tri_actuel = None #Ferme le menu                 

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
                    self.epreuve_lumiere_terminee = True
                else:
                    self.dialogue_actuel = ("Trop lent ! Réessaie de les éteindre.", "red")
                self.epreuve.termine = False


            if self.salle_actuelle == "spawn" and self.player.rect.right >= self.WIDTH:
                self.transition_vers("lumiere", self.bg_epreuve1)

            if self.salle_actuelle == "lumiere" and self.player.rect.right >= self.WIDTH and self.epreuve.reussite:
                self.transition_vers("tri_dechets", self.bg_epreuve2)

            # Afficher le background
            self.screen.blit(self.background, (0, 0))
            # appeler le niveau: self.screen.blits() pour mettre les plateformes


  
            if self.salle_actuelle == "lumiere":
                self.screen.blit(self.background, (0, -60)) # On remonte un peu pour le décor
                self.screen.blit(self.gardien_img, self.gardien_rect)
                self.epreuve.draw() # Ampoules uniquement ici
                
            elif self.salle_actuelle == "tri_dechets":
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.gardien_tri_img, self.gardien_tri_rect)
                for p in self.poubelles:
                    p.draw(self.screen) # Poubelles uniquement ici

            else: #Spawn
                self.screen.blit(self.background, (0, 0))

            # --- 2. DESSIN DES ENTITÉS ET INTERFACES ---
            if self.menu_tri_actuel:
                self.menu_tri_actuel.draw(self.screen)

            #Gestion auto du texte de dialogue du gardien
            if self.indice_dialogue != -1:
                self.dialogue_actuel = (self.dialogues_gardien[self.indice_dialogue], "black")


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

    def ouvrir_menu_tri(self, poubelle):
        self.poubelle_concernee = poubelle
        # Exemple : La poubelle jaune propose Carton vs Pomme
        if poubelle.type == "yellow":
            self.menu_tri_actuel = MenuTri(poubelle.rect, self.img_carton, self.img_pomme, "recyclable", "organique")
        if poubelle.type == "brown":
            self.menu_tri_actuel = MenuTri(poubelle.rect, self.img_pomme, self.img_verre, "ordure", "verre")
        if poubelle.type == "green":
            self.menu_tri_actuel = MenuTri(poubelle.rect, self.img_verre, self.img_carton, "verre", "recyclable")
