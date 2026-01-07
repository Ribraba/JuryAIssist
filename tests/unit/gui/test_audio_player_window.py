"""
Tests unitaires pour AudioPlayerWindow.

Valide l'injection de dépendances (SOLID-D).
"""

import pytest
from unittest.mock import Mock

from src.gui.audio_player_window import AudioPlayerWindow
from src.audio.controller import AudioController
from src.audio.vlc_player import VLCAudioPlayer


class TestAudioPlayerWindowSOLID:
    """Tests du principe SOLID-D pour AudioPlayerWindow."""

    def test_creates_own_controller_when_none_provided(self, qapp, qtbot):
        """Test création de son propre controller si None fourni."""
        # Créer sans controller (mode standalone)
        window = AudioPlayerWindow()
        qtbot.addWidget(window)

        # Vérifier qu'il a créé son propre controller
        assert window._controller is not None
        assert window._player is not None
        assert window._owns_controller is True

    def test_uses_injected_controller(self, qapp, qtbot):
        """Test utilisation du controller injecté (SOLID-D)."""
        # Créer un controller externe
        player = VLCAudioPlayer()
        controller = AudioController(player)

        # Injecter le controller (mode intégré)
        window = AudioPlayerWindow(controller=controller)
        qtbot.addWidget(window)

        # Vérifier qu'il utilise le controller injecté
        assert window._controller is controller
        assert window._player is player
        assert window._owns_controller is False

    def test_does_not_release_injected_controller(self, qapp, qtbot):
        """Test que le controller injecté n'est PAS libéré à la fermeture."""
        # Mock controller
        mock_controller = Mock(spec=AudioController)
        mock_controller._player = Mock()

        # Injecter le mock
        window = AudioPlayerWindow(controller=mock_controller)
        qtbot.addWidget(window)

        # Fermer la fenêtre
        window.close()

        # Vérifier que release() n'a PAS été appelé
        # (le propriétaire du controller le libérera)
        mock_controller.release.assert_not_called()

    def test_releases_own_controller(self, qapp, qtbot):
        """Test que son propre controller EST libéré à la fermeture."""
        # Créer window avec son propre controller
        window = AudioPlayerWindow()
        qtbot.addWidget(window)

        # Mock la méthode release
        original_release = window._controller.release
        window._controller.release = Mock(wraps=original_release)

        # Fermer la fenêtre
        window.close()

        # Vérifier que release() a été appelé
        window._controller.release.assert_called_once()


class TestAudioPlayerWindowIntegration:
    """Tests d'intégration pour AudioPlayerWindow."""

    def test_shared_controller_updates_both_windows(self, qapp, qtbot):
        """Test que deux fenêtres partageant un controller se synchronisent."""
        # Créer un controller partagé
        player = VLCAudioPlayer()
        controller = AudioController(player)

        # Créer deux fenêtres avec le même controller
        window1 = AudioPlayerWindow(controller=controller)
        window2 = AudioPlayerWindow(controller=controller)
        qtbot.addWidget(window1)
        qtbot.addWidget(window2)

        # Vérifier qu'elles partagent le même controller
        assert window1._controller is window2._controller
        assert window1._controller is controller

    def test_independent_controllers_do_not_interfere(self, qapp, qtbot):
        """Test que des controllers indépendants ne s'interfèrent pas."""
        # Créer deux fenêtres avec leurs propres controllers
        window1 = AudioPlayerWindow()
        window2 = AudioPlayerWindow()
        qtbot.addWidget(window1)
        qtbot.addWidget(window2)

        # Vérifier qu'ils ont des controllers différents
        assert window1._controller is not window2._controller
        assert window1._player is not window2._player
