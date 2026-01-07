"""
Contrôleur audio de haut niveau.

Fournit une interface simplifiée pour contrôler la lecture audio
et émet des événements Qt pour synchroniser l'interface graphique.

Architecture SOLID :
- Single Responsibility : Contrôle de la lecture uniquement
- Dependency Inversion : Dépend de IAudioPlayer, pas d'une implémentation
- Open/Closed : Extensible via IAudioPlayer
"""

from typing import Optional

from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from .player import IAudioPlayer, PlayerState
from .source import IAudioSource, FileAudioSource


class AudioController(QObject):
    """
    Contrôleur audio de haut niveau avec événements Qt.

    Responsabilités :
    - Contrôles simplifiés (toggle play/pause, skip, etc.)
    - Émission d'événements pour synchroniser la GUI
    - Gestion du timer pour mise à jour de la position
    - Interface simple pour la pédale et l'interface

    Signals Qt émis :
    - position_changed(float) : Position actuelle en secondes
    - state_changed(PlayerState) : Nouvel état du player
    - duration_changed(float) : Durée du fichier
    - source_loaded(str) : Nouvelle source chargée
    - speed_changed(float) : Vitesse de lecture
    - error_occurred(str) : Erreur survenue
    """

    # Signaux Qt
    position_changed = pyqtSignal(float)  # Position en secondes
    state_changed = pyqtSignal(object)  # PlayerState
    duration_changed = pyqtSignal(float)  # Durée en secondes
    source_loaded = pyqtSignal(str)  # Nom de la source
    speed_changed = pyqtSignal(float)  # Vitesse (0.5 - 2.0)
    volume_changed = pyqtSignal(int)  # Volume (0 - 100)
    error_occurred = pyqtSignal(str)  # Message d'erreur

    def __init__(self, player: IAudioPlayer, update_interval: int = 100):
        """
        Initialise le contrôleur audio.

        Args:
            player: Instance de IAudioPlayer à contrôler
            update_interval: Intervalle de mise à jour de la position en ms (défaut: 100ms)
        """
        super().__init__()

        self._player = player
        self._current_source: Optional[IAudioSource] = None
        self._current_speed = 1.0
        self._current_volume = 100  # Volume par défaut à 100%

        # Timer pour mise à jour régulière de la position
        self._position_timer = QTimer()
        self._position_timer.setInterval(update_interval)
        self._position_timer.timeout.connect(self._update_position)

        # État précédent pour détecter les changements
        self._last_position = 0.0
        self._last_state = PlayerState.STOPPED

        # Debounce pour éviter les surcharges VLC
        self._seek_timer = QTimer()
        self._seek_timer.setSingleShot(True)
        self._seek_timer.timeout.connect(self._execute_pending_seek)
        self._pending_seek_position: Optional[float] = None

    def load_file(self, filepath: str) -> bool:
        """
        Charge un fichier audio.

        Args:
            filepath: Chemin absolu vers le fichier audio

        Returns:
            True si chargement réussi, False sinon

        Emits:
            source_loaded(str) : Si succès
            duration_changed(float) : Si succès
            state_changed(PlayerState) : Nouveau état
            error_occurred(str) : Si erreur
        """
        # Créer la source
        source = FileAudioSource(filepath)

        # Vérifier disponibilité
        if not source.is_available():
            self.error_occurred.emit(f"Fichier non trouvé: {filepath}")
            return False

        # Charger dans le player
        success = self._player.load(source.get_uri())

        if success:
            self._current_source = source
            duration = self._player.get_duration()

            # Émettre les signaux
            self.source_loaded.emit(source.get_display_name())
            self.duration_changed.emit(duration)
            self._emit_state_change()

            return True
        else:
            self.error_occurred.emit(f"Impossible de charger: {filepath}")
            return False

    def play(self) -> bool:
        """
        Démarre la lecture.

        Returns:
            True si lecture démarrée, False sinon

        Emits:
            state_changed(PlayerState) : Nouvel état
        """
        success = self._player.play()

        if success:
            self._position_timer.start()
            self._emit_state_change()

        return success

    def pause(self) -> bool:
        """
        Met en pause.

        Returns:
            True si pause réussie, False sinon

        Emits:
            state_changed(PlayerState) : Nouvel état
        """
        success = self._player.pause()

        if success:
            self._position_timer.stop()
            self._emit_state_change()

        return success

    def stop(self) -> bool:
        """
        Arrête la lecture et remet à 0.

        Returns:
            True si arrêt réussi, False sinon

        Emits:
            state_changed(PlayerState) : Nouvel état
            position_changed(float) : Position = 0
        """
        success = self._player.stop()

        if success:
            self._position_timer.stop()
            self._emit_state_change()
            self.position_changed.emit(0.0)

        return success

    def toggle_play_pause(self) -> bool:
        """
        Bascule entre play et pause.

        Returns:
            True si succès, False sinon

        Emits:
            state_changed(PlayerState) : Nouvel état
        """
        state = self._player.get_state()

        if state == PlayerState.PLAYING:
            return self.pause()
        else:
            return self.play()

    def skip_forward(self, seconds: float = 5.0) -> bool:
        """
        Avance de X secondes.

        Args:
            seconds: Nombre de secondes à avancer (défaut: 5.0)

        Returns:
            True si succès, False sinon

        Emits:
            position_changed(float) : Nouvelle position
        """
        current = self._player.get_position()
        new_position = current + seconds

        success = self._player.seek(new_position)

        if success:
            # Forcer la mise à jour immédiate
            self._update_position()

        return success

    def skip_backward(self, seconds: float = 5.0) -> bool:
        """
        Recule de X secondes.

        Args:
            seconds: Nombre de secondes à reculer (défaut: 5.0)

        Returns:
            True si succès, False sinon

        Emits:
            position_changed(float) : Nouvelle position
        """
        current = self._player.get_position()
        new_position = max(0.0, current - seconds)

        success = self._player.seek(new_position)

        if success:
            # Forcer la mise à jour immédiate
            self._update_position()

        return success

    def seek(self, position: float) -> bool:
        """
        Se déplace à une position.

        Args:
            position: Position en secondes

        Returns:
            True si succès, False sinon

        Emits:
            position_changed(float) : Nouvelle position

        Note:
            Cette méthode utilise un debounce pour éviter de surcharger VLC
            avec trop de seek() rapides. Le seek réel sera exécuté après 50ms
            si aucun autre seek n'est demandé entretemps.
        """
        # Stocker la position demandée
        self._pending_seek_position = position

        # Redémarrer le timer (annule le seek précédent si en attente)
        self._seek_timer.stop()
        self._seek_timer.start(50)  # 50ms debounce

        return True

    def set_speed(self, speed: float) -> bool:
        """
        Définit la vitesse de lecture.

        Args:
            speed: Vitesse (0.5 à 2.0)

        Returns:
            True si succès, False sinon

        Emits:
            speed_changed(float) : Nouvelle vitesse
        """
        success = self._player.set_speed(speed)

        if success:
            self._current_speed = speed
            self.speed_changed.emit(speed)

        return success

    def cycle_speed(self) -> float:
        """
        Cycle entre les vitesses prédéfinies : 1.0x → 1.5x → 2.0x → 1.0x.

        Returns:
            Nouvelle vitesse

        Emits:
            speed_changed(float) : Nouvelle vitesse
        """
        # Définir les vitesses
        speeds = [1.0, 1.5, 2.0]

        # Trouver la vitesse actuelle
        try:
            current_index = speeds.index(self._current_speed)
            next_index = (current_index + 1) % len(speeds)
        except ValueError:
            # Si vitesse non standard, revenir à 1.0
            next_index = 0

        new_speed = speeds[next_index]
        self.set_speed(new_speed)

        return new_speed

    def set_volume(self, volume: int) -> bool:
        """
        Définit le volume de lecture.

        Args:
            volume: Volume (0 à 100)

        Returns:
            True si succès, False sinon

        Emits:
            volume_changed(int) : Nouveau volume
        """
        success = self._player.set_volume(volume)

        if success:
            self._current_volume = volume
            self.volume_changed.emit(volume)

        return success

    def get_position(self) -> float:
        """Obtient la position actuelle en secondes."""
        return self._player.get_position()

    def get_duration(self) -> float:
        """Obtient la durée totale en secondes."""
        return self._player.get_duration()

    def get_state(self) -> PlayerState:
        """Obtient l'état actuel du player."""
        return self._player.get_state()

    def get_speed(self) -> float:
        """Obtient la vitesse actuelle."""
        return self._current_speed

    def get_volume(self) -> int:
        """Obtient le volume actuel."""
        return self._current_volume

    def get_source_name(self) -> Optional[str]:
        """Obtient le nom de la source actuelle."""
        if self._current_source:
            return self._current_source.get_display_name()
        return None

    def release(self) -> None:
        """Libère les ressources."""
        self._position_timer.stop()
        self._player.release()

    # Méthodes privées

    def _update_position(self) -> None:
        """
        Met à jour la position et émet le signal si changement.

        Called by: QTimer
        """
        current_position = self._player.get_position()

        # Émettre seulement si changement significatif (> 0.1s)
        if abs(current_position - self._last_position) > 0.1:
            self.position_changed.emit(current_position)
            self._last_position = current_position

        # Vérifier si l'état a changé
        self._emit_state_change()

    def _emit_state_change(self) -> None:
        """Émet state_changed si l'état a changé."""
        current_state = self._player.get_state()

        if current_state != self._last_state:
            self.state_changed.emit(current_state)
            self._last_state = current_state

    def _execute_pending_seek(self) -> None:
        """
        Exécute le seek en attente (appelé par le timer de debounce).

        Cette méthode est appelée après le délai de debounce pour éviter
        de surcharger VLC avec trop d'appels seek() rapides.
        """
        if self._pending_seek_position is not None:
            position = self._pending_seek_position
            self._pending_seek_position = None

            # Exécuter le seek réel
            success = self._player.seek(position)

            if success:
                self._update_position()
