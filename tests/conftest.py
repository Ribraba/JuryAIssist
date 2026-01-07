"""
Configuration pytest et fixtures globales.

Ce fichier est automatiquement chargé par pytest.
"""

import os
import sys
from pathlib import Path

import pytest
from PyQt5.QtWidgets import QApplication

# Ajouter le répertoire src au PYTHONPATH pour les imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session", autouse=True)
def qapp_global():
    """
    Crée une QApplication globale pour tous les tests.

    Cette fixture est auto-utilisée (autouse=True) pour garantir
    qu'une QApplication existe avant que n'importe quel test ne s'exécute,
    ce qui est nécessaire pour les tests GUI.
    """
    # Créer une QApplication si elle n'existe pas déjà
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    yield app

    # Pas besoin de quit() car pytest-qt gère le cleanup


@pytest.fixture(scope="session")
def test_data_dir():
    """Répertoire contenant les fichiers de test."""
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def sample_audio_files(test_data_dir):
    """
    Dictionnaire de fichiers audio de test.

    Returns:
        dict: Mapping format → chemin du fichier
              Ex: {"mp3": "/path/to/test.mp3", "wav": "/path/to/test.wav"}

    Note:
        Pour l'instant, retourne un dict vide.
        À remplir quand on aura des fichiers de test.
    """
    # Chercher des fichiers audio dans tests/data/
    audio_files = {}

    if test_data_dir.exists():
        for ext in ["mp3", "wav", "m4a", "dss"]:
            pattern = f"*.{ext}"
            files = list(test_data_dir.glob(pattern))
            if files:
                audio_files[ext] = str(files[0])

    return audio_files


@pytest.fixture
def mock_audio_file(tmp_path):
    """
    Crée un fichier audio factice pour les tests.

    Note: Ce n'est PAS un vrai fichier audio, juste un fichier vide.
    Pour tester la lecture réelle, utilisez sample_audio_files.
    """
    fake_audio = tmp_path / "fake_audio.mp3"
    fake_audio.write_bytes(b"")  # Fichier vide
    return str(fake_audio)


@pytest.fixture(scope="session")
def sample_audio_file(test_data_dir):
    """
    Fixture pour obtenir le fichier audio de test principal.

    Returns:
        str: Chemin absolu vers Test_audio.m4a

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    audio_file = test_data_dir / "Test_audio.m4a"
    if not audio_file.exists():
        raise FileNotFoundError(
            f"Fichier audio de test non trouvé: {audio_file}\n"
            f"Assurez-vous que Test_audio.m4a est dans {test_data_dir}"
        )
    return str(audio_file)
