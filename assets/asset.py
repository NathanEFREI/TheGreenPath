import os
from pygame.surface import Surface


def recup_sprite(dir: str, func) -> list[Surface]:
    """ 
    si ta pas compris tu peux developper le code, il est en mode factoriser si tu preferes
    sorted pas obliger d'apres un test mais mieux vaut etre prudent
    """

    path = os.path.dirname(__file__) + "\\"+ dir
    
    if not os.path.isdir(path):
        raise Exception(f"Le chemin ne fais pas référence à un dossier existant: {path}")
    
    return [func(path + "\\" + file) for file in sorted(os.listdir(path))]