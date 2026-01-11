"""
Module transcription - Interfaces du domain layer (Qt-free).

Définit l'interface ITranscriber selon le principe SOLID-D.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .entities import TranscriptionResult


class ITranscriber(ABC):
    """
    Interface abstraite pour un moteur de transcription.

    Permet d'implémenter différents moteurs (Whisper, Google Speech, etc.)
    tout en gardant la même interface.

    Principe SOLID :
    - Single Responsibility : Transcription uniquement
    - Dependency Inversion : Code dépend de l'interface
    - Open/Closed : Extensible sans modification
    """

    @abstractmethod
    def transcribe(
        self, audio_path: str, language: Optional[str] = None
    ) -> TranscriptionResult:
        """
        Transcrit un fichier audio complet.

        Args:
            audio_path: Chemin vers le fichier audio
            language: Code langue (ex: "fr", "en"), None pour détection auto

        Returns:
            TranscriptionResult avec segments et texte complet

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
        """
        pass

    @abstractmethod
    def transcribe_segment(
        self,
        audio_path: str,
        start: float,
        end: float,
        language: Optional[str] = None,
    ) -> TranscriptionResult:
        """
        Transcrit une portion spécifique d'un fichier audio.

        Args:
            audio_path: Chemin vers le fichier audio
            start: Début du segment en secondes
            end: Fin du segment en secondes
            language: Code langue, None pour détection auto

        Returns:
            TranscriptionResult du segment filtré

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si start >= end
        """
        pass

    @abstractmethod
    def get_supported_languages(self) -> list[str]:
        """
        Obtient la liste des langues supportées.

        Returns:
            Liste de codes ISO (ex: ["fr", "en", "es"])
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Obtient les informations sur le modèle utilisé.

        Returns:
            Dict avec informations (nom, taille, version, etc.)
        """
        pass

    @abstractmethod
    def release(self) -> None:
        """Libère les ressources du transcriber (modèle en mémoire, etc.)."""
        pass
