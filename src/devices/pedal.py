"""
Interfaces et structures de données pour les pédales.

Ce module définit les abstractions pour supporter différents types de pédales.
Principe SOLID-D : Dépendre d'abstractions, pas d'implémentations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


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


class IPedalDetector(ABC):
    """
    Interface pour la détection de pédales USB HID.

    Principe SOLID-S : Responsabilité unique = détecter les pédales
    Principe SOLID-D : Abstraction pour différents types de détection
    """

    @abstractmethod
    def detect(self) -> Optional[PedalInfo]:
        """
        Détecte une pédale compatible.

        Returns:
            PedalInfo si une pédale est trouvée, None sinon
        """
        pass

    @abstractmethod
    def list_all_devices(self) -> list[PedalInfo]:
        """
        Liste tous les périphériques HID détectés.

        Returns:
            Liste de PedalInfo pour tous les devices
        """
        pass


class IEventParser(ABC):
    """
    Interface pour parser les événements HID bruts.

    Principe SOLID-S : Responsabilité unique = parser les données brutes
    Principe SOLID-O : Ouvert à l'extension (différents parsers pour différentes pédales)
    """

    @abstractmethod
    def parse(self, raw_data: bytes) -> list[ButtonEvent]:
        """
        Parse les données HID brutes en événements de boutons.

        Args:
            raw_data: Données brutes du périphérique HID

        Returns:
            Liste d'événements de boutons détectés
        """
        pass


class IActionMapper(ABC):
    """
    Interface pour mapper les boutons aux actions.

    Principe SOLID-S : Responsabilité unique = mapper boutons → actions
    Principe SOLID-O : Ouvert à l'extension (configurations différentes)
    """

    @abstractmethod
    def get_action(self, button_number: int) -> PedalAction:
        """
        Obtient l'action associée à un bouton.

        Args:
            button_number: Numéro du bouton

        Returns:
            Action associée au bouton
        """
        pass

    @abstractmethod
    def set_action(self, button_number: int, action: PedalAction) -> None:
        """
        Définit l'action pour un bouton.

        Args:
            button_number: Numéro du bouton
            action: Action à associer
        """
        pass

    @abstractmethod
    def get_mapping(self) -> Dict[int, PedalAction]:
        """
        Obtient le mapping complet.

        Returns:
            Dictionnaire {button_number: action}
        """
        pass


class IPedalReader(ABC):
    """
    Interface pour lire les événements d'une pédale.

    Principe SOLID-S : Responsabilité unique = lire les événements HID
    Principe SOLID-I : Interface minimale, seulement ce qui est nécessaire
    """

    @abstractmethod
    def start(self) -> bool:
        """
        Démarre la lecture des événements.

        Returns:
            True si démarré avec succès, False sinon
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """Arrête la lecture des événements."""
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """
        Vérifie si le lecteur est actif.

        Returns:
            True si actif, False sinon
        """
        pass
