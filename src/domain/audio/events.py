"""
Module audio - Événements du domain layer (Qt-free).

Définit les événements métier pour la communication entre le domain et la présentation.
Utilise le pattern Observer sans dépendre de Qt.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .entities import PlayerState


class AudioEventType(Enum):
    """Types d'événements audio."""

    POSITION_CHANGED = "position_changed"
    STATE_CHANGED = "state_changed"
    DURATION_CHANGED = "duration_changed"
    SOURCE_LOADED = "source_loaded"
    SPEED_CHANGED = "speed_changed"
    VOLUME_CHANGED = "volume_changed"
    ERROR = "error"


@dataclass
class AudioEvent:
    """
    Événement audio du domain layer.

    Encapsule toutes les informations nécessaires pour notifier
    les observateurs des changements dans le domaine audio.
    """

    type: AudioEventType
    position: Optional[float] = None
    duration: Optional[float] = None
    state: Optional[PlayerState] = None
    source_name: Optional[str] = None
    speed: Optional[float] = None
    volume: Optional[int] = None
    message: Optional[str] = None
