"""
Module audio - Interfaces du domain layer (Qt-free).

Définit les interfaces IAudioPlayer et IAudioSource selon le principe SOLID-D.
Ces interfaces sont indépendantes de toute implémentation et de tout framework UI.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .entities import PlayerState


class IAudioPlayer(ABC):
    """
    Interface abstraite pour tout lecteur audio.

    Cette interface garantit que n'importe quelle implémentation
    (VLC, GStreamer, pygame, etc.) peut être utilisée de manière interchangeable.

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
        """Obtient la durée totale du fichier audio en secondes."""
        pass

    @abstractmethod
    def get_position(self) -> float:
        """Obtient la position actuelle de lecture en secondes."""
        pass

    @abstractmethod
    def get_state(self) -> PlayerState:
        """Obtient l'état actuel du lecteur."""
        pass

    @abstractmethod
    def play(self) -> bool:
        """Démarre la lecture."""
        pass

    @abstractmethod
    def pause(self) -> bool:
        """Met la lecture en pause."""
        pass

    @abstractmethod
    def stop(self) -> bool:
        """Arrête la lecture et remet la position à 0."""
        pass

    @abstractmethod
    def seek(self, position: float) -> bool:
        """Se déplace à une position spécifique."""
        pass

    @abstractmethod
    def set_speed(self, speed: float) -> bool:
        """Définit la vitesse de lecture (0.5 à 2.0)."""
        pass

    @abstractmethod
    def set_volume(self, volume: int) -> bool:
        """Définit le volume de lecture (0 à 100)."""
        pass

    @abstractmethod
    def release(self) -> None:
        """Libère les ressources du lecteur."""
        pass


class IAudioSource(ABC):
    """
    Interface abstraite pour une source audio.

    Permet de supporter différentes sources :
    - Fichiers locaux
    - URLs distantes (futur)
    - Flux audio en direct (futur)
    """

    @abstractmethod
    def get_uri(self) -> str:
        """Obtient l'URI de la source audio."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si la source est disponible."""
        pass

    @abstractmethod
    def get_display_name(self) -> str:
        """Obtient le nom d'affichage de la source."""
        pass
