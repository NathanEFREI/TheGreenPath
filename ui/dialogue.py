from __future__ import annotations

import pygame


def _couper_texte(font: pygame.font.Font, texte: str, largeur_max: int) -> list[str]:


    mots = texte.split()
    lignes = []
    ligne_actuelle = ""
    
    for mot in mots:
        test_ligne = f"{ligne_actuelle} {mot}".strip() if ligne_actuelle else mot
        largeur_texte, _ = font.size(test_ligne)
        
        if largeur_texte <= largeur_max:
            ligne_actuelle = test_ligne
        else:
            if ligne_actuelle:
                lignes.append(ligne_actuelle)
            # Si un seul mot est trop long, on le coupe
            if font.size(mot)[0] > largeur_max:
                while mot:
                    for i in range(len(mot), 0, -1):
                        if font.size(mot[:i])[0] <= largeur_max:
                            lignes.append(mot[:i])
                            mot = mot[i:]
                            break
                    else:
                        lignes.append(mot[0])
                        mot = mot[1:]
                ligne_actuelle = ""
            else:
                ligne_actuelle = mot
    
    if ligne_actuelle:
        lignes.append(ligne_actuelle)
    
    return lignes


def afficher_dialogue(
    screen: pygame.Surface,
    texte: str,
    couleur: str | tuple[int, int, int],
    *,
    position: str = "bas",
    marge: int = 40,
    padding: int = 25,
    taille_police: int = 28,
    nom_police: str = None,
    couleur_texte: str | tuple[int, int, int] = (255, 255, 255),
    couleur_bordure: str | tuple[int, int, int] = (50, 50, 50),
    epaisseur_bordure: int = 4,
) -> pygame.Rect:

    # Conversion de la couleur si c'est une chaîne
    if isinstance(couleur, str):
        couleur = pygame.Color(couleur)
    elif isinstance(couleur, tuple):
        couleur = pygame.Color(*couleur[:3])
    
    largeur_ecran, hauteur_ecran = screen.get_size()
    
    # Police pour le texte
    if nom_police:
        try:
            font = pygame.font.SysFont(nom_police, taille_police)
        except Exception:
            font = pygame.font.SysFont(None, taille_police)
    else:
        font = pygame.font.SysFont("arial", taille_police)
    
    # Découper le texte en lignes
    largeur_max_texte = largeur_ecran - 2 * marge - 2 * padding
    lignes = _couper_texte(font, texte, largeur_max_texte)
    
    # Calculer les dimensions de la boîte
    hauteur_ligne = font.get_height() + 4
    hauteur_texte = len(lignes) * hauteur_ligne
    largeur_boite = min(
        max(font.size(ligne)[0] for ligne in lignes) + 2 * padding if lignes else 200,
        largeur_ecran - 2 * marge
    )
    hauteur_boite = hauteur_texte + 2 * padding
    
    # Positionner la boîte
    x = (largeur_ecran - largeur_boite) // 2
    
    if position == "bas":
        y = hauteur_ecran - hauteur_boite - marge
    elif position == "haut":
        y = marge
    else:  # centre
        y = (hauteur_ecran - hauteur_boite) // 2
    
    rect_boite = pygame.Rect(x, y, largeur_boite, hauteur_boite)
    
    # Dessiner la boîte avec bordure arrondie
    pygame.draw.rect(
        screen,
        couleur_bordure,
        rect_boite.inflate(epaisseur_bordure * 2, epaisseur_bordure * 2),
        border_radius=12,
    )
    pygame.draw.rect(
        screen,
        couleur,
        rect_boite,
        border_radius=10,
    )
    
    # Dessiner le texte
    y_texte = y + padding
    for ligne in lignes:
        surface_texte = font.render(ligne, True, couleur_texte)
        rect_texte = surface_texte.get_rect(centerx=largeur_ecran // 2, top=y_texte)
        screen.blit(surface_texte, rect_texte)
        y_texte += hauteur_ligne
    
    return rect_boite


def afficher_dialogue_avec_nom(
    screen: pygame.Surface,
    texte: str,
    couleur: str | tuple[int, int, int],
    nom_locuteur: str = "",
    **kwargs,
) -> pygame.Rect:

    rect = afficher_dialogue(screen, texte, couleur, **kwargs)
    
    if nom_locuteur:
        font = pygame.font.SysFont("arial", kwargs.get("taille_police", 28) - 4)
        surface_nom = font.render(nom_locuteur, True, (200, 200, 200))
        largeur_ecran = screen.get_size()[0]
        rect_nom = surface_nom.get_rect(centerx=largeur_ecran // 2, bottom=rect.top - 5)
        screen.blit(surface_nom, rect_nom)
    
    return rect
