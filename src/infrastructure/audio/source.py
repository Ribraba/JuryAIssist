"""
Interface pour les sources audio.

Cette interface permet de supporter différentes sources audio :
- Fichiers locaux (implémentation actuelle)
- URLs distantes (V2.0)
- Flux audio en direct (V2.0)
- Microphone (V2.0)

Principe SOLID : Dependency Inversion et Open/Closed.
"""

from abc import ABC, abstractmethod
from typing import Optional


class IAudioSource(ABC):
    """
    Interface abstraite pour une source audio.

    Cette interface anticipative permettra d'ajouter facilement
    de nouvelles sources audio sans modifier le code existant.

    Note: Pour V1.0, seule FileAudioSource sera implémentée.
    """

    @abstractmethod
    def get_uri(self) -> str:
        """
        Obtient l'URI de la source audio.

        Returns:
            URI de la source (chemin fichier, URL, etc.)

        Example:
            >>> source.get_uri()
            '/path/to/audio.mp3'
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Vérifie si la source est disponible.

        Returns:
            True si la source est accessible, False sinon

        Example:
            >>> source.is_available()
            True
        """
        pass

    @abstractmethod
    def get_display_name(self) -> str:
        """
        Obtient le nom d'affichage de la source.

        Returns:
            Nom lisible pour l'utilisateur

        Example:
            >>> source.get_display_name()
            'audio.mp3'
        """
        pass


class FileAudioSource(IAudioSource):
    """
    Source audio basée sur un fichier local.

    Implémentation simple pour V1.0.
    """

    def __init__(self, filepath: str):
        """
        Initialise une source audio fichier.

        Args:
            filepath: Chemin absolu vers le fichier audio
        """
        self._filepath = filepath

    def get_uri(self) -> str:
        """Retourne le chemin du fichier."""
        return self._filepath

    def is_available(self) -> bool:
        """Vérifie que le fichier existe."""
        import os
        return os.path.exists(self._filepath)

    def get_display_name(self) -> str:
        """Retourne le nom du fichier."""
        import os
        return os.path.basename(self._filepath)

    def __repr__(self) -> str:
        return f"FileAudioSource('{self._filepath}')"
