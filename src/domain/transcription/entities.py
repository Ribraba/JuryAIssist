"""
Module transcription - Entités du domain layer (Qt-free).

Définit les entités et value objects du domaine transcription.
"""

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
