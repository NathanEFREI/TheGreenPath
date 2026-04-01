# main.py (à la racine)
import sys
import os

# Ajoute la racine au path pour que tous les imports fonctionnent
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.menu import main_menu

if __name__ == "__main__":
    main_menu()