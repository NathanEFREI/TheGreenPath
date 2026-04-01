# main.py (à la racine)
#from codecarbon import EmissionsTracker
from game.menu import main_menu
import sys
import os

# Ajoute la racine au path pour que tous les imports fonctionnent
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# tracker = EmissionsTracker()
# tracker.start()

if __name__ == "__main__":
    #try:
    main_menu()
    #finally:
        #tracker.stop()