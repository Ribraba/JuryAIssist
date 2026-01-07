"""
Configuration pytest pour les tests GUI.

Assure qu'une QApplication existe avant tous les tests GUI.
"""

import pytest
from PyQt5.QtWidgets import QApplication


@pytest.fixture(scope="session", autouse=True)
def qapp_session():
    """
    Crée une QApplication pour toute la session de tests GUI.

    Cette fixture est auto-utilisée (autouse=True) pour garantir
    qu'une QApplication existe avant que les tests GUI ne s'exécutent.
    """
    # Créer une QApplication si elle n'existe pas déjà
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    yield app

    # Pas besoin de quit() car pytest-qt gère le cleanup
