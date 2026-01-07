"""
Implémentation VLC du lecteur audio.

Implémentation concrète de IAudioPlayer utilisant python-vlc.
"""

import os
from typing import Optional

try:
    import vlc
except ImportError:
    vlc = None  # Géré dans __init__

from .player import IAudioPlayer, PlayerState


class VLCAudioPlayer(IAudioPlayer):
    """
    Lecteur audio basé sur VLC.

    Avantages de VLC :
    - Support de nombreux formats (MP3, WAV, M4A, DSS, FLAC, etc.)
    - Contrôle précis de la vitesse avec préservation du pitch
    - Très stable et testé
    - Cross-platform (Windows, macOS, Linux)

    Note:
        VLC doit être installé sur le système.
    """

    def __init__(self):
        """
        Initialise le lecteur VLC.

        Raises:
            ImportError: Si python-vlc n'est pas installé
            RuntimeError: Si VLC n'est pas installé sur le système
        """
        if vlc is None:
            raise ImportError(
                "python-vlc n'est pas installé. "
                "Installez-le avec: pip install python-vlc"
            )

        # Créer l'instance VLC
        try:
            self._instance = vlc.Instance()
            self._player = self._instance.media_player_new()
        except Exception as e:
            raise RuntimeError(
                f"Impossible d'initialiser VLC. Assurez-vous que VLC est installé. Erreur: {e}"
            )

        self._current_file: Optional[str] = None
        self._duration: float = 0.0
        self._state: PlayerState = PlayerState.STOPPED

    def load(self, filepath: str) -> bool:
        """Charge un fichier audio."""
        # Vérifier que le fichier existe
        if not os.path.exists(filepath):
            self._state = PlayerState.ERROR
            return False

        try:
            import time

            # Créer un media VLC
            media = self._instance.media_new(filepath)
            if media is None:
                self._state = PlayerState.ERROR
                return False

            # Définir le media dans le player
            self._player.set_media(media)

            # Parse le media pour obtenir la durée avec timeout
            # VLC peut prendre du temps pour certains formats (M4A, etc.)
            media.parse()

            # Attendre que le parsing soit terminé (max 2 secondes)
            timeout = 20  # 20 * 0.1s = 2 secondes
            attempts = 0
            while attempts < timeout:
                duration_ms = media.get_duration()
                if duration_ms > 0:
                    self._duration = duration_ms / 1000.0
                    break
                time.sleep(0.1)
                attempts += 1

            # Si après timeout on n'a toujours pas la durée, fallback
            if self._duration <= 0:
                # Fallback : démarrer brièvement le player pour obtenir la durée
                self._player.play()
                time.sleep(0.3)
                duration_ms = self._player.get_length()
                if duration_ms > 0:
                    self._duration = duration_ms / 1000.0
                self._player.stop()
                time.sleep(0.1)

            # Vérifier qu'on a bien une durée
            if self._duration <= 0:
                print(f"Impossible d'obtenir la durée de {filepath}")
                self._state = PlayerState.ERROR
                return False

            self._current_file = filepath
            self._state = PlayerState.STOPPED

            return True

        except Exception as e:
            print(f"Erreur lors du chargement de {filepath}: {e}")
            self._state = PlayerState.ERROR
            return False

    def get_duration(self) -> float:
        """Obtient la durée totale."""
        return self._duration

    def get_position(self) -> float:
        """Obtient la position actuelle."""
        if not self._current_file:
            return 0.0

        try:
            # Position en millisecondes
            pos_ms = self._player.get_time()
            if pos_ms < 0:
                return 0.0
            return pos_ms / 1000.0
        except Exception:
            return 0.0

    def get_state(self) -> PlayerState:
        """Obtient l'état actuel."""
        # Synchroniser l'état avec VLC
        if self._current_file:
            vlc_state = self._player.get_state()

            if vlc_state == vlc.State.Playing:
                self._state = PlayerState.PLAYING
            elif vlc_state == vlc.State.Paused:
                self._state = PlayerState.PAUSED
            elif vlc_state in (vlc.State.Stopped, vlc.State.Ended):
                self._state = PlayerState.STOPPED
            elif vlc_state == vlc.State.Error:
                self._state = PlayerState.ERROR

        return self._state

    def play(self) -> bool:
        """Démarre la lecture."""
        if not self._current_file:
            return False

        try:
            # Si déjà en lecture, ne rien faire
            current_vlc_state = self._player.get_state()
            if current_vlc_state == vlc.State.Playing:
                return True

            result = self._player.play()
            if result == 0:  # VLC retourne 0 si succès
                self._state = PlayerState.PLAYING
                return True
            return False
        except Exception as e:
            print(f"Erreur play: {e}")
            self._state = PlayerState.ERROR
            return False

    def pause(self) -> bool:
        """Met en pause."""
        if not self._current_file:
            return False

        try:
            # Si déjà en pause, ne rien faire
            current_vlc_state = self._player.get_state()
            if current_vlc_state == vlc.State.Paused:
                return True

            self._player.pause()
            self._state = PlayerState.PAUSED
            return True
        except Exception as e:
            print(f"Erreur pause: {e}")
            return False

    def stop(self) -> bool:
        """Arrête la lecture."""
        if not self._current_file:
            return False

        try:
            self._player.stop()
            self._state = PlayerState.STOPPED
            return True
        except Exception as e:
            print(f"Erreur stop: {e}")
            return False

    def seek(self, position: float) -> bool:
        """Se déplace à une position."""
        if not self._current_file or self._duration <= 0:
            return False

        try:
            # Clamper la position
            position = max(0.0, min(position, self._duration))

            # VLC utilise des millisecondes
            position_ms = int(position * 1000)
            self._player.set_time(position_ms)

            return True
        except Exception as e:
            print(f"Erreur seek: {e}")
            return False

    def set_speed(self, speed: float) -> bool:
        """Définit la vitesse de lecture."""
        try:
            # Clamper la vitesse entre 0.5 et 2.0
            speed = max(0.5, min(speed, 2.0))

            # VLC : set_rate() - 1.0 = vitesse normale
            self._player.set_rate(speed)

            return True
        except Exception as e:
            print(f"Erreur set_speed: {e}")
            return False

    def set_volume(self, volume: int) -> bool:
        """Définit le volume de lecture."""
        try:
            # Clamper le volume entre 0 et 100
            volume = max(0, min(volume, 100))

            # VLC : audio_set_volume() - 0 à 100
            self._player.audio_set_volume(volume)

            return True
        except Exception as e:
            print(f"Erreur set_volume: {e}")
            return False

    def release(self) -> None:
        """Libère les ressources."""
        try:
            if self._player:
                self._player.stop()
        except Exception as e:
            print(f"Erreur lors de l'arrêt: {e}")

        # Ne pas appeler release() sur player et instance
        # car cela cause des crashes avec VLC dans certains contextes
        # Les ressources seront libérées automatiquement par Python GC

        self._current_file = None
        self._duration = 0.0
        self._state = PlayerState.STOPPED
