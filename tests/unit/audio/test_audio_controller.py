"""
Tests unitaires pour AudioController.

Ces tests vérifient le contrôleur de haut niveau et ses événements Qt.
"""

import time
from unittest.mock import Mock, MagicMock

import pytest
from PyQt5.QtCore import QCoreApplication

from src.audio.controller import AudioController
from src.audio.player import PlayerState
from src.audio.vlc_player import VLCAudioPlayer


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture(scope="session")
def qapp():
    """Fixture pour créer une QApplication (nécessaire pour les signaux Qt)."""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    yield app


@pytest.fixture
def player():
    """Fixture pour créer un player VLC."""
    player = VLCAudioPlayer()
    yield player
    player.release()


@pytest.fixture
def controller(player, qapp):
    """Fixture pour créer un contrôleur."""
    ctrl = AudioController(player, update_interval=50)  # 50ms pour tests rapides
    yield ctrl
    ctrl.release()


@pytest.fixture
def loaded_controller(controller, sample_audio_file, qapp):
    """Fixture pour un contrôleur avec fichier chargé."""
    controller.load_file(sample_audio_file)
    yield controller


# ============================================================================
# TESTS D'INITIALISATION
# ============================================================================


def test_controller_initialization(controller):
    """Test que le contrôleur s'initialise correctement."""
    assert controller is not None
    assert controller.get_state() == PlayerState.STOPPED
    assert controller.get_position() == 0.0
    assert controller.get_speed() == 1.0
    assert controller.get_volume() == 100
    assert controller.get_source_name() is None


def test_controller_has_signals(controller):
    """Test que le contrôleur expose tous les signaux Qt."""
    assert hasattr(controller, "position_changed")
    assert hasattr(controller, "state_changed")
    assert hasattr(controller, "duration_changed")
    assert hasattr(controller, "source_loaded")
    assert hasattr(controller, "speed_changed")
    assert hasattr(controller, "volume_changed")
    assert hasattr(controller, "error_occurred")


# ============================================================================
# TESTS DE CHARGEMENT
# ============================================================================


def test_load_file_success(controller, sample_audio_file, qapp):
    """Test chargement d'un fichier valide."""
    # Mock des signaux
    source_loaded_spy = Mock()
    duration_changed_spy = Mock()

    controller.source_loaded.connect(source_loaded_spy)
    controller.duration_changed.connect(duration_changed_spy)

    # Charger
    result = controller.load_file(sample_audio_file)

    assert result is True
    assert controller.get_duration() > 0.0
    assert controller.get_source_name() == "Test_audio.m4a"
    assert controller.get_state() == PlayerState.STOPPED

    # Vérifier que les signaux ont été émis
    qapp.processEvents()  # Traiter les événements Qt
    assert source_loaded_spy.called
    assert duration_changed_spy.called
    # Note: state_changed n'est émis que si l'état change vraiment


def test_load_file_nonexistent(controller, qapp):
    """Test chargement d'un fichier inexistant."""
    error_spy = Mock()
    controller.error_occurred.connect(error_spy)

    result = controller.load_file("/path/to/nonexistent.mp3")

    assert result is False

    qapp.processEvents()
    assert error_spy.called


# ============================================================================
# TESTS DE LECTURE
# ============================================================================


def test_play(loaded_controller, qapp):
    """Test démarrage de la lecture."""
    state_spy = Mock()
    loaded_controller.state_changed.connect(state_spy)

    result = loaded_controller.play()
    time.sleep(0.3)

    assert result is True
    assert loaded_controller.get_state() == PlayerState.PLAYING

    qapp.processEvents()
    assert state_spy.called

    loaded_controller.stop()


def test_pause(loaded_controller, qapp):
    """Test mise en pause."""
    state_spy = Mock()
    loaded_controller.state_changed.connect(state_spy)

    loaded_controller.play()
    time.sleep(0.3)

    result = loaded_controller.pause()
    time.sleep(0.2)

    assert result is True
    assert loaded_controller.get_state() == PlayerState.PAUSED

    qapp.processEvents()
    # Le signal doit avoir été appelé au moins pour PLAYING
    assert state_spy.call_count >= 1

    loaded_controller.stop()


def test_stop(loaded_controller, qapp):
    """Test arrêt de la lecture."""
    loaded_controller.play()
    time.sleep(0.2)

    state_spy = Mock()
    position_spy = Mock()
    loaded_controller.state_changed.connect(state_spy)
    loaded_controller.position_changed.connect(position_spy)

    result = loaded_controller.stop()
    time.sleep(0.1)

    assert result is True
    assert loaded_controller.get_state() == PlayerState.STOPPED

    qapp.processEvents()
    assert state_spy.called
    assert position_spy.called


def test_toggle_play_pause(loaded_controller, qapp):
    """Test toggle play/pause."""
    # État initial : STOPPED → doit play
    loaded_controller.toggle_play_pause()
    time.sleep(0.2)
    assert loaded_controller.get_state() == PlayerState.PLAYING

    # État PLAYING → doit pause
    loaded_controller.toggle_play_pause()
    time.sleep(0.2)
    assert loaded_controller.get_state() == PlayerState.PAUSED

    # État PAUSED → doit play
    loaded_controller.toggle_play_pause()
    time.sleep(0.2)
    assert loaded_controller.get_state() == PlayerState.PLAYING

    loaded_controller.stop()


# ============================================================================
# TESTS DE NAVIGATION
# ============================================================================


def test_skip_forward(loaded_controller, qapp):
    """Test avance de 5 secondes."""
    loaded_controller.play()
    time.sleep(0.3)

    initial_pos = loaded_controller.get_position()

    position_spy = Mock()
    loaded_controller.position_changed.connect(position_spy)

    result = loaded_controller.skip_forward(2.0)
    time.sleep(0.3)

    assert result is True
    new_pos = loaded_controller.get_position()
    assert new_pos > initial_pos

    qapp.processEvents()
    assert position_spy.called

    loaded_controller.stop()


def test_skip_backward(loaded_controller, qapp):
    """Test recul de 5 secondes."""
    loaded_controller.play()
    time.sleep(0.3)
    loaded_controller.seek(5.0)
    time.sleep(0.3)

    initial_pos = loaded_controller.get_position()

    position_spy = Mock()
    loaded_controller.position_changed.connect(position_spy)

    result = loaded_controller.skip_backward(2.0)
    time.sleep(0.3)

    assert result is True
    new_pos = loaded_controller.get_position()
    assert new_pos < initial_pos

    qapp.processEvents()
    assert position_spy.called

    loaded_controller.stop()


def test_seek(loaded_controller, qapp):
    """Test seek à une position."""
    loaded_controller.play()
    time.sleep(0.2)

    position_spy = Mock()
    loaded_controller.position_changed.connect(position_spy)

    result = loaded_controller.seek(2.0)
    time.sleep(0.3)

    assert result is True
    position = loaded_controller.get_position()
    assert abs(position - 2.0) < 1.5  # Tolérance VLC

    qapp.processEvents()
    assert position_spy.called

    loaded_controller.stop()


# ============================================================================
# TESTS DE VITESSE
# ============================================================================


def test_set_speed(loaded_controller, qapp):
    """Test changement de vitesse."""
    speed_spy = Mock()
    loaded_controller.speed_changed.connect(speed_spy)

    result = loaded_controller.set_speed(1.5)

    assert result is True
    assert loaded_controller.get_speed() == 1.5

    qapp.processEvents()
    assert speed_spy.called


def test_cycle_speed(loaded_controller, qapp):
    """Test cycle des vitesses."""
    # 1.0 → 1.5
    speed = loaded_controller.cycle_speed()
    assert speed == 1.5
    assert loaded_controller.get_speed() == 1.5

    # 1.5 → 2.0
    speed = loaded_controller.cycle_speed()
    assert speed == 2.0
    assert loaded_controller.get_speed() == 2.0

    # 2.0 → 1.0
    speed = loaded_controller.cycle_speed()
    assert speed == 1.0
    assert loaded_controller.get_speed() == 1.0


def test_set_volume(loaded_controller, qapp):
    """Test changement de volume."""
    volume_spy = Mock()
    loaded_controller.volume_changed.connect(volume_spy)

    result = loaded_controller.set_volume(50)

    assert result is True
    assert loaded_controller.get_volume() == 50

    qapp.processEvents()
    assert volume_spy.called


def test_volume_range(loaded_controller, qapp):
    """Test que le volume accepte les valeurs 0-100."""
    # Volume minimum
    result = loaded_controller.set_volume(0)
    assert result is True
    assert loaded_controller.get_volume() == 0

    # Volume maximum
    result = loaded_controller.set_volume(100)
    assert result is True
    assert loaded_controller.get_volume() == 100

    # Volume moyen
    result = loaded_controller.set_volume(75)
    assert result is True
    assert loaded_controller.get_volume() == 75


# ============================================================================
# TESTS DES ÉVÉNEMENTS
# ============================================================================


@pytest.mark.slow
def test_position_updates_during_playback(loaded_controller, qapp):
    """Test que la position est mise à jour pendant la lecture."""
    position_spy = Mock()
    loaded_controller.position_changed.connect(position_spy)

    loaded_controller.play()

    # Attendre que le timer se déclenche plusieurs fois
    time.sleep(0.5)
    qapp.processEvents()

    # Le signal doit avoir été émis au moins une fois
    assert position_spy.call_count >= 1

    loaded_controller.stop()


# ============================================================================
# TESTS SANS FICHIER CHARGÉ
# ============================================================================


def test_play_without_file(controller):
    """Test play sans fichier chargé."""
    result = controller.play()
    assert result is False


def test_pause_without_file(controller):
    """Test pause sans fichier chargé."""
    result = controller.pause()
    assert result is False


def test_stop_without_file(controller):
    """Test stop sans fichier chargé."""
    result = controller.stop()
    assert result is False


# ============================================================================
# TESTS DE LIBÉRATION
# ============================================================================


def test_release_stops_timer(loaded_controller, qapp):
    """Test que release arrête le timer."""
    loaded_controller.play()
    time.sleep(0.2)

    # Le timer doit être actif
    assert loaded_controller._position_timer.isActive()

    loaded_controller.release()

    # Le timer doit être arrêté
    assert not loaded_controller._position_timer.isActive()
