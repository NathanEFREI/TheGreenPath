import os
from pygame.surface import Surface


# Ce module charge les sprites depuis les dossiers d'assets de manière générique.

def recup_sprite(dir: str, func) -> list[Surface]:
    """Charge tous les fichiers d'un dossier et retourne une liste de surfaces.

    dir: nom du sous-dossier d'assets à lire.
    func: fonction de chargement et de redimensionnement de l'image.
    """

    path = os.path.dirname(__file__) + "\\" + dir

    if not os.path.isdir(path):
        raise Exception(f"Le chemin ne fais pas référence à un dossier existant: {path}")

    return [func(path + "\\" + file) for file in sorted(os.listdir(path))]