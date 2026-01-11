"""
Module devices - Événements du domain layer (Qt-free).

Définit les événements métier pour la communication entre le domain et la présentation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from .entities import PedalAction


class PedalEventType(Enum):
    """Types d'événements de pédale."""

    ACTION_TRIGGERED = "action_triggered"
    BUTTON_PRESSED = "button_pressed"
    BUTTON_RELEASED = "button_released"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class PedalEvent:
    """
    Événement de pédale du domain layer.

    Encapsule toutes les informations nécessaires pour notifier
    les observateurs des changements liés à la pédale.
    """

    type: PedalEventType
    action: Optional[PedalAction] = None
    button_number: Optional[int] = None
    message: Optional[str] = None
