# 🌿 The Green Path

> Serious game éducatif sur l'écologie — Python / Pygame

---

## Présentation

The Green Path est un serious game 2D développé en Python avec Pygame. Le joueur incarne un héros qui revient dans sa ville natale, **Nitidopolis**, ravagée par la pollution. Pour la sauver, il doit retrouver des Gardiens de la Nature, relever leurs épreuves et apprendre des gestes écologiques essentiels.

---

## Structure du projet

```
TheGreenPath/
├── main.py                  # Point d'entrée
├── constante.py             # Toutes les constantes du jeu
├── settings.json            # Volume sauvegardé
├── menus/
│   ├── menu.py              # Menu principal
│   └── creer_partie.py      # Popup création de partie
├── game/
│   ├── game.py              # Classe Fenetre + Game (boucle principale)
│   ├── cinematique.py       # Scène d'introduction (slides + texte)
│   ├── parametre.py         # Menu des paramètres (volume)
│   └── utils.py             # Boutons, confirm_quit...
├── personnage/
│   └── joueur.py            # Classe Player (déplacement, saut, gravité)
├── levels/
│   └── epreuve_lumiere.py   # Épreuve du Gardien de la lumière
├── ui/
│   └── dialogue.py          # Affichage des boîtes de dialogue
└── assets/                  # Images, sons, sprites
```

---

## Fonctionnalités

### Menu principal
- Créer une partie (nom de partie + nom du joueur)
- Charger une partie *(à venir)*
- Paramètres : réglage du volume avec sauvegarde dans `settings.json`
- Quitter avec confirmation

### Cinématique d'introduction
- 7 slides narratives avec effet machine à écrire
- Fade in / fade out entre chaque slide
- Musique avec fade in automatique (3 secondes)
- Passage rapide avec `Espace` / `Entrée`, skip total avec `P`

### Gameplay
- Déplacement gauche/droite et saut avec physique simulée (gravité)
- Animation des sprites : marche, saut, idle
- Retournement du sprite selon la direction
- Fullscreen / fenêtré avec `F11`, redimensionnement dynamique

### Épreuve de la lumière
- 5 cibles apparaissent aléatoirement à l'écran
- Le joueur doit toutes les toucher en moins de **10 secondes**
- Chronomètre rouge sous les 5 secondes restantes
- Résultat : réussite ou échec avec message de dialogue

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- Pygame

```bash
pip install pygame
```

### Lancement

```bash
cd TheGreenPath
python main.py
```

---

## Contrôles

| Touche | Action |
|--------|--------|
| `←` / `→` ou `Q` / `D` | Se déplacer |
| `Espace` ou `↑` | Sauter |
| `F11` | Basculer plein écran / fenêtré |
| `Échap` | Quitter (avec confirmation) |
| `P` | Passer la cinématique d'introduction |

---

## Paramètres techniques

Toutes les constantes sont centralisées dans `constante.py` :

| Constante | Valeur | Description |
|-----------|--------|-------------|
| `VELOCITY` | `5` | Vitesse de déplacement (px/frame) |
| `GRAVITY` | `40` | Force de gravité |
| `JUMP_HEIGHT` | `20` | Vitesse initiale du saut (px/frame) |
| `FPS` | `60` | Fréquence d'images |
| `VITESSE_LETTRE` | `30` | Délai entre chaque lettre (ms) |
| `VITESSE_FADE` | `6` | Vitesse des fondus (alpha/frame) |

---

## Auteurs

Projet développé dans le cadre d'un cours de programmation.  
Thème : sensibilisation à l'écologie à travers le jeu vidéo.