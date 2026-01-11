"""
Module devices - Entités du domain layer (Qt-free).

Définit les entités et value objects du domaine devices (pédales).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PedalAction(Enum):
    """Actions possibles d'une pédale."""

    PLAY_PAUSE = "play_pause"
    SKIP_FORWARD = "skip_forward"
    SKIP_BACKWARD = "skip_backward"
    STOP = "stop"
    CYCLE_SPEED = "cycle_speed"
    MARK_POSITION = "mark_position"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ButtonEvent:
    """
    Événement d'un bouton de pédale.

    Attributes:
        button_number: Numéro du bouton (1-4 pour RS-31)
        pressed: True si le bouton est enfoncé, False s'il est relâché
        timestamp: Timestamp de l'événement (optionnel)
    """

    button_number: int
    pressed: bool
    timestamp: Optional[float] = None

    def __post_init__(self):
        """Validation après initialisation."""
        if self.button_number < 1:
            raise ValueError(f"button_number doit être >= 1, reçu {self.button_number}")


@dataclass(frozen=True)
class PedalInfo:
    """
    Informations sur une pédale détectée.

    Attributes:
        vendor_id: Identifiant du vendeur (ex: 0x07b4 pour Olympus)
        product_id: Identifiant du produit (ex: 0x025f pour RS-31)
        manufacturer: Nom du fabricant
        product_name: Nom du produit
        serial_number: Numéro de série (optionnel)
        path: Chemin du device HID
    """

    vendor_id: int
    product_id: int
    manufacturer: str
    product_name: str
    path: bytes
    serial_number: Optional[str] = None

    def __str__(self) -> str:
        """Représentation textuelle."""
        parts = [
            f"Vendor ID: 0x{self.vendor_id:04x}",
            f"Product ID: 0x{self.product_id:04x}",
            f"Manufacturer: {self.manufacturer}",
            f"Product: {self.product_name}",
        ]
        if self.serial_number:
            parts.append(f"Serial: {self.serial_number}")
        return " | ".join(parts)
