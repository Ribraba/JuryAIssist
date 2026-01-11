"""
Module transcription - Événements du domain layer (Qt-free).

Définit les événements métier pour la communication entre le domain et la présentation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .entities import TranscriptionResult


class TranscriptionEventType(Enum):
    """Types d'événements de transcription."""

    STARTED = "started"
    PROGRESS = "progress"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class TranscriptionEvent:
    """
    Événement de transcription du domain layer.

    Encapsule toutes les informations nécessaires pour notifier
    les observateurs des changements dans le processus de transcription.
    """

    type: TranscriptionEventType
    progress_percent: Optional[int] = None  # 0-100
    result: Optional[TranscriptionResult] = None
    message: Optional[str] = None
