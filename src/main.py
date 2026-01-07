"""
Point d'entrée de l'application JuryAIssist.

Lance l'interface graphique complète avec lecteur audio et transcription.
"""

import sys

from PyQt5.QtWidgets import QApplication

from src.gui.main_window import MainWindow


def main():
    """Lance l'application."""
    # Créer l'application Qt
    app = QApplication(sys.argv)

    # Configurer le nom de l'application
    app.setApplicationName("JuryAIssist")
    app.setOrganizationName("JuryAIssist")

    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()

    # Lancer la boucle d'événements
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
