# Ce fichier regroupe les constantes utilisées dans le jeu.
# Elles servent à calibrer le comportement du joueur, la cadence du jeu
# et les effets de cinématique.

### Constantes de mise à l'échelle du joueur
# Ces ratios permettent d'adapter le joueur à la résolution de l'écran.
PLAYER_SCALE_W = 80 / 2560
PLAYER_SCALE_H = 80 / 1600
X_RATIO = 200 / 2560
Y_RATIO = 1024 / 1440

# Liste des états de sprite pris en charge pour le joueur.
INIT_SPRITE = ["walk", "jump", "idle"]

# Vitesse de déplacement horizontale du joueur.
VELOCITY = 5


### Constantes générales du jeu
# Nombre d'images par seconde cible.
FPS = 60


### Constantes de cinématique
# Vitesse d'affichage des lettres dans les slides.
VITESSE_LETTRE = 30
# Vitesse du fondu entrant/sortant de la cinématique.
VITESSE_FADE = 6