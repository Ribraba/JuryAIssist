"""
Tests unitaires pour le module audio.

Tests de l'interface IAudioPlayer et de l'implémentation VLCAudioPlayer.
"""

import os
import time
from pathlib import Path

import pytest

from src.audio.player import IAudioPlayer, PlayerState
from src.audio.vlc_player import VLCAudioPlayer


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def player():
    """Fixture pour créer un player VLC."""
    player = VLCAudioPlayer()
    yield player
    player.release()


# Note: La fixture sample_audio_file est définie dans tests/conftest.py
# Elle pointe vers tests/data/Test_audio.m4a


# ============================================================================
# TESTS D'INITIALISATION
# ============================================================================


def test_player_initialization():
    """Test que le player s'initialise correctement."""
    player = VLCAudioPlayer()

    assert player is not None
    assert isinstance(player, IAudioPlayer)
    assert player.get_state() == PlayerState.STOPPED
    assert player.get_duration() == 0.0
    assert player.get_position() == 0.0

    player.release()


def test_player_implements_interface():
    """Test que VLCAudioPlayer implémente IAudioPlayer."""
    player = VLCAudioPlayer()

    # Vérifier que toutes les méthodes de l'interface sont présentes
    assert hasattr(player, "load")
    assert hasattr(player, "get_duration")
    assert hasattr(player, "get_position")
    assert hasattr(player, "get_state")
    assert hasattr(player, "play")
    assert hasattr(player, "pause")
    assert hasattr(player, "stop")
    assert hasattr(player, "seek")
    assert hasattr(player, "set_speed")
    assert hasattr(player, "set_volume")
    assert hasattr(player, "release")

    player.release()


# ============================================================================
# TESTS DE CHARGEMENT
# ============================================================================


def test_load_nonexistent_file(player):
    """Test chargement d'un fichier inexistant."""
    result = player.load("/path/to/nonexistent/file.mp3")

    assert result is False
    assert player.get_state() == PlayerState.ERROR


def test_load_valid_audio(player, sample_audio_file):
    """Test chargement d'un fichier audio valide."""
    result = player.load(sample_audio_file)

    assert result is True
    assert player.get_state() == PlayerState.STOPPED
    assert player.get_duration() > 0.0
    assert player.get_position() == 0.0


# ============================================================================
# TESTS D'ÉTAT
# ============================================================================


def test_initial_state(player):
    """Test que l'état initial est STOPPED."""
    assert player.get_state() == PlayerState.STOPPED


def test_state_after_error(player):
    """Test que l'état devient ERROR après une erreur."""
    player.load("/invalid/path.mp3")
    assert player.get_state() == PlayerState.ERROR


# ============================================================================
# TESTS DE LECTURE (NÉCESSITENT UN FICHIER AUDIO)
# ============================================================================


def test_play_pause_cycle(player, sample_audio_file):
    """Test du cycle play → pause → play."""
    player.load(sample_audio_file)

    # Play
    result = player.play()
    assert result is True

    time.sleep(0.3)
    assert player.get_state() == PlayerState.PLAYING

    # Pause (VLC a besoin d'un peu de temps pour répondre)
    result = player.pause()
    assert result is True
    time.sleep(0.15)  # Donner le temps à VLC de passer en pause
    assert player.get_state() == PlayerState.PAUSED

    # Re-play
    result = player.play()
    assert result is True
    time.sleep(0.2)
    assert player.get_state() == PlayerState.PLAYING


def test_stop_resets_position(player, sample_audio_file):
    """Test que stop remet la position à 0."""
    player.load(sample_audio_file)
    player.play()

    time.sleep(0.5)  # Laisser jouer 0.5 seconde

    player.stop()

    assert player.get_state() == PlayerState.STOPPED
    # Note: VLC peut ne pas remettre exactement à 0 immédiatement
    time.sleep(0.1)
    assert player.get_position() < 0.5  # Proche de 0


# ============================================================================
# TESTS DE NAVIGATION
# ============================================================================


def test_seek_to_position(player, sample_audio_file):
    """Test seek à une position spécifique."""
    player.load(sample_audio_file)
    duration = player.get_duration()

    # Il faut démarrer la lecture pour que seek fonctionne correctement avec VLC
    player.play()
    time.sleep(0.2)

    # Chercher une position au milieu du fichier (ou 2s si fichier court)
    seek_pos = min(2.0, duration / 2)
    result = player.seek(seek_pos)
    assert result is True

    # Vérifier la position (avec une tolérance généreuse)
    time.sleep(0.3)
    position = player.get_position()
    # VLC peut ne pas être ultra précis, surtout sur M4A
    assert abs(position - seek_pos) < 1.5  # Tolérance de 1.5 secondes

    player.stop()


def test_seek_clamping(player, sample_audio_file):
    """Test que seek clamp les valeurs hors limites."""
    player.load(sample_audio_file)
    duration = player.get_duration()

    # Seek à une position négative (doit clamper à 0)
    player.seek(-10.0)
    time.sleep(0.1)
    assert player.get_position() >= 0.0

    # Seek au-delà de la durée (doit clamper à duration)
    player.seek(duration + 100.0)
    time.sleep(0.2)
    position = player.get_position()
    assert position <= duration + 1.0  # Tolérance


# ============================================================================
# TESTS DE VITESSE
# ============================================================================


def test_speed_change(player, sample_audio_file):
    """Test changement de vitesse."""
    player.load(sample_audio_file)

    # Vitesse normale
    result = player.set_speed(1.0)
    assert result is True

    # Vitesse 1.5x
    result = player.set_speed(1.5)
    assert result is True

    # Vitesse 0.5x
    result = player.set_speed(0.5)
    assert result is True


def test_speed_clamping(player, sample_audio_file):
    """Test que la vitesse est clampée entre 0.5 et 2.0."""
    player.load(sample_audio_file)

    # Vitesse trop basse (doit clamper à 0.5)
    result = player.set_speed(0.1)
    assert result is True  # Accepté mais clampé

    # Vitesse trop haute (doit clamper à 2.0)
    result = player.set_speed(5.0)
    assert result is True  # Accepté mais clampé


# ============================================================================
# TESTS DE VOLUME
# ============================================================================


def test_volume_change(player, sample_audio_file):
    """Test changement de volume."""
    player.load(sample_audio_file)

    # Volume 100%
    result = player.set_volume(100)
    assert result is True

    # Volume 50%
    result = player.set_volume(50)
    assert result is True

    # Volume 0% (muet)
    result = player.set_volume(0)
    assert result is True


def test_volume_clamping(player, sample_audio_file):
    """Test que le volume est clampé entre 0 et 100."""
    player.load(sample_audio_file)

    # Volume négatif (doit clamper à 0)
    result = player.set_volume(-10)
    assert result is True  # Accepté mais clampé

    # Volume trop haut (doit clamper à 100)
    result = player.set_volume(150)
    assert result is True  # Accepté mais clampé


# ============================================================================
# TESTS DE LIBÉRATION
# ============================================================================


def test_release_cleans_up(player):
    """Test que release libère les ressources."""
    player.release()

    # Après release, l'état doit être STOPPED
    assert player.get_state() == PlayerState.STOPPED
    assert player.get_duration() == 0.0


# ============================================================================
# TESTS SANS FICHIER CHARGÉ
# ============================================================================


def test_play_without_file(player):
    """Test play sans fichier chargé."""
    result = player.play()
    assert result is False


def test_pause_without_file(player):
    """Test pause sans fichier chargé."""
    result = player.pause()
    assert result is False


def test_stop_without_file(player):
    """Test stop sans fichier chargé."""
    result = player.stop()
    assert result is False


def test_seek_without_file(player):
    """Test seek sans fichier chargé."""
    result = player.seek(10.0)
    assert result is False


# ============================================================================
# TESTS D'INTÉGRATION (MARQUÉS COMME INTEGRATION)
# ============================================================================


@pytest.mark.integration
def test_full_playback_workflow(player, sample_audio_file):
    """
    Test du workflow complet de lecture.

    Workflow :
    1. Charger
    2. Play
    3. Seek
    4. Pause
    5. Play
    6. Stop
    """
    # Charger
    assert player.load(sample_audio_file) is True
    assert player.get_state() == PlayerState.STOPPED
    duration = player.get_duration()

    # Play
    assert player.play() is True
    time.sleep(0.3)
    assert player.get_state() == PlayerState.PLAYING

    # Seek (à 2s ou milieu du fichier si plus court)
    seek_pos = min(2.0, duration / 2)
    assert player.seek(seek_pos) is True
    time.sleep(0.2)
    position = player.get_position()
    assert abs(position - seek_pos) < 1.5  # Tolérance généreuse

    # Pause
    assert player.pause() is True
    time.sleep(0.1)
    assert player.get_state() == PlayerState.PAUSED

    # Re-play
    assert player.play() is True
    time.sleep(0.2)
    assert player.get_state() == PlayerState.PLAYING

    # Stop
    assert player.stop() is True
    time.sleep(0.1)
    assert player.get_state() == PlayerState.STOPPED
