"""
Module de lecture audio - Interface abstraite.

Définit l'interface IAudioPlayer selon le principe SOLID-D (Dependency Inversion).
Toute implémentation de lecteur audio doit respecter cette interface.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class PlayerState(Enum):
    """États possibles du lecteur audio."""

    STOPPED = "stopped"  # Arrêté, position à 0
    PLAYING = "playing"  # En cours de lecture
    PAUSED = "paused"  # En pause, position conservée
    ERROR = "error"  # Erreur (fichier invalide, codec manquant, etc.)


class IAudioPlayer(ABC):
    """
    Interface abstraite pour tout lecteur audio.

    Cette interface garantit que n'importe quelle implémentation
    (VLC, pygame, pyaudio, etc.) peut être utilisée de manière interchangeable.

    Principe SOLID appliqué :
    - Single Responsibility : Lecture audio uniquement
    - Interface Segregation : Méthodes minimales et nécessaires
    - Dependency Inversion : Le code dépend de cette interface, pas d'une implémentation
    """

    @abstractmethod
    def load(self, filepath: str) -> bool:
        """
        Charge un fichier audio.

        Args:
            filepath: Chemin absolu vers le fichier audio (MP3, WAV, M4A, DSS, etc.)

        Returns:
            True si le chargement a réussi, False sinon

        Note:
            Après chargement réussi, l'état devient STOPPED et position = 0.0
        """
        pass

    @abstractmethod
    def get_duration(self) -> float:
        """
        Obtient la durée totale du fichier audio.

        Returns:
            Durée en secondes (float)
            0.0 si aucun fichier chargé ou erreur

        Example:
            >>> player.load("audio.mp3")
            >>> duration = player.get_duration()  # Ex: 125.5 (= 2min 5.5s)
        """
        pass

    @abstractmethod
    def get_position(self) -> float:
        """
        Obtient la position actuelle de lecture.

        Returns:
            Position en secondes (float)
            0.0 si aucun fichier chargé

        Example:
            >>> player.play()
            >>> time.sleep(2)
            >>> pos = player.get_position()  # Ex: 2.1
        """
        pass

    @abstractmethod
    def get_state(self) -> PlayerState:
        """
        Obtient l'état actuel du lecteur.

        Returns:
            État du lecteur (PlayerState enum)

        Example:
            >>> player.load("audio.mp3")
            >>> player.get_state()  # PlayerState.STOPPED
            >>> player.play()
            >>> player.get_state()  # PlayerState.PLAYING
        """
        pass

    @abstractmethod
    def play(self) -> bool:
        """
        Démarre la lecture.

        Returns:
            True si lecture démarrée, False si erreur

        Note:
            - Si en pause : reprend depuis la position actuelle
            - Si arrêté : démarre depuis la position actuelle (généralement 0)
            - État résultant : PLAYING
        """
        pass

    @abstractmethod
    def pause(self) -> bool:
        """
        Met la lecture en pause.

        Returns:
            True si mise en pause réussie, False sinon

        Note:
            - Conserve la position actuelle
            - État résultant : PAUSED
        """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """
        Arrête la lecture et remet la position à 0.

        Returns:
            True si arrêt réussi, False sinon

        Note:
            - Position redevient 0.0
            - État résultant : STOPPED
        """
        pass

    @abstractmethod
    def seek(self, position: float) -> bool:
        """
        Se déplace à une position spécifique.

        Args:
            position: Position en secondes (0.0 à duration)

        Returns:
            True si seek réussi, False sinon

        Note:
            - Si position < 0 : clampé à 0
            - Si position > duration : clampé à duration
            - État conservé (PLAYING reste PLAYING, PAUSED reste PAUSED)
        """
        pass

    @abstractmethod
    def set_speed(self, speed: float) -> bool:
        """
        Définit la vitesse de lecture.

        Args:
            speed: Vitesse de lecture (0.5 à 2.0)
                  1.0 = vitesse normale
                  0.5 = moitié de la vitesse
                  2.0 = double vitesse

        Returns:
            True si changement réussi, False sinon

        Note:
            - Le pitch doit être préservé (pas de voix de canard)
            - Si speed hors limites : clampé à [0.5, 2.0]
        """
        pass

    @abstractmethod
    def set_volume(self, volume: int) -> bool:
        """
        Définit le volume de lecture.

        Args:
            volume: Volume en pourcentage (0 à 100)
                   0 = muet
                   100 = volume maximum

        Returns:
            True si changement réussi, False sinon

        Note:
            - Si volume < 0 : clampé à 0
            - Si volume > 100 : clampé à 100
        """
        pass

    @abstractmethod
    def release(self) -> None:
        """
        Libère les ressources du lecteur.

        Note:
            À appeler avant de détruire l'instance.
            Arrête la lecture et ferme le fichier.
        """
        pass
