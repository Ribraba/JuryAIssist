"""
Interface abstraite pour la transcription audio.

Architecture SOLID :
- Single Responsibility : Transcription audio uniquement
- Dependency Inversion : Interface abstraite pour différents moteurs
- Open/Closed : Extensible (Whisper, Google Speech, etc.)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TranscriptionStatus(Enum):
    """État de la transcription."""

    IDLE = "idle"  # En attente
    PROCESSING = "processing"  # En cours
    COMPLETED = "completed"  # Terminée
    ERROR = "error"  # Erreur


@dataclass
class TranscriptionSegment:
    """
    Segment de transcription avec timing.

    Attributes:
        start: Temps de début en secondes
        end: Temps de fin en secondes
        text: Texte transcrit
        confidence: Confiance (0.0 à 1.0), None si non disponible
    """

    start: float
    end: float
    text: str
    confidence: Optional[float] = None

    def __post_init__(self):
        """Validation des données."""
        if self.start < 0:
            raise ValueError("start doit être >= 0")
        if self.end <= self.start:
            raise ValueError("end doit être > start")
        if self.confidence is not None and not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence doit être entre 0.0 et 1.0")

    @property
    def duration(self) -> float:
        """Durée du segment en secondes."""
        return self.end - self.start


@dataclass
class TranscriptionResult:
    """
    Résultat complet d'une transcription.

    Attributes:
        segments: Liste des segments transcrits
        full_text: Texte complet (concaténation)
        language: Langue détectée (code ISO, ex: "fr", "en")
        status: État de la transcription
        error_message: Message d'erreur si status == ERROR
    """

    segments: List[TranscriptionSegment]
    full_text: str
    language: str
    status: TranscriptionStatus
    error_message: Optional[str] = None

    @property
    def duration(self) -> float:
        """Durée totale couverte par les segments."""
        if not self.segments:
            return 0.0
        return max(seg.end for seg in self.segments)

    @property
    def word_count(self) -> int:
        """Nombre de mots dans le texte complet."""
        return len(self.full_text.split())


class ITranscriber(ABC):
    """
    Interface abstraite pour un moteur de transcription.

    Permet d'implémenter différents moteurs (Whisper, Google Speech, etc.)
    tout en gardant la même interface.
    """

    @abstractmethod
    def transcribe(
        self, audio_path: str, language: Optional[str] = None
    ) -> TranscriptionResult:
        """
        Transcrit un fichier audio.

        Args:
            audio_path: Chemin vers le fichier audio
            language: Code langue (ex: "fr", "en"), None pour détection auto

        Returns:
            TranscriptionResult avec segments et texte complet

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            RuntimeError: Si la transcription échoue

        Examples:
            >>> transcriber = WhisperTranscriber()
            >>> result = transcriber.transcribe("audio.mp3", language="fr")
            >>> print(result.full_text)
            "Bonjour, ceci est un test."
            >>> print(len(result.segments))
            3
        """
        pass

    @abstractmethod
    def transcribe_segment(
        self, audio_path: str, start: float, end: float, language: Optional[str] = None
    ) -> TranscriptionResult:
        """
        Transcrit une portion spécifique d'un fichier audio.

        Args:
            audio_path: Chemin vers le fichier audio
            start: Début du segment en secondes
            end: Fin du segment en secondes
            language: Code langue, None pour détection auto

        Returns:
            TranscriptionResult du segment uniquement

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si start >= end ou hors limites
            RuntimeError: Si la transcription échoue
        """
        pass

    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """
        Retourne la liste des langues supportées.

        Returns:
            Liste des codes ISO de langues (ex: ["fr", "en", "es"])
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Retourne les informations sur le modèle utilisé.

        Returns:
            Dictionnaire avec nom, version, taille, etc.

        Examples:
            >>> transcriber.get_model_info()
            {
                "name": "whisper",
                "size": "base",
                "version": "1.0",
                "parameters": "74M"
            }
        """
        pass
