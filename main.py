#from codecarbon import EmissionsTracker
from menus.menu import main_menu
import sys
import os

from menus.menu import main_menu

# Ajoute la racine du projet au path Python pour éviter les problèmes d'import.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# from codecarbon import EmissionsTracker
# tracker = EmissionsTracker()
# tracker.start()

if __name__ == "__main__":
    # Démarrer le menu principal du jeu.
    main_menu()
    # tracker.stop()  # Arrêter le tracker si activé