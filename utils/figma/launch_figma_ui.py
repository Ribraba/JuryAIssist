"""
Script de lancement pour la nouvelle interface Figma.

Permet de tester la nouvelle interface en parallèle de l'ancienne.
"""
import sys
from PyQt5.QtWidgets import QApplication

from src.gui.main_window_figma import MainWindowFigma


def main():
    """Lance l'application avec l'interface Figma."""
    app = QApplication(sys.argv)

    # Créer et afficher la fenêtre
    window = MainWindowFigma()
    window.show()

    # Lancer la boucle d'événements
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
