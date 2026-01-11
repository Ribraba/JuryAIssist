"""
Module devices - Interfaces du domain layer (Qt-free).

Définit les interfaces pour les périphériques (pédales USB HID).
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable
from .entities import PedalInfo, ButtonEvent, PedalAction


class IPedalDetector(ABC):
    """
    Interface pour la détection de pédales USB HID.

    Principe SOLID:
    - Single Responsibility: Détecter les pédales uniquement
    - Dependency Inversion: Abstraction pour différents types de détection
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

    Principe SOLID:
    - Single Responsibility: Parser les données brutes
    - Open/Closed: Ouvert à l'extension (différents parsers pour différentes pédales)
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

    Principe SOLID:
    - Single Responsibility: Mapper boutons → actions
    - Open/Closed: Ouvert à l'extension (configurations différentes)
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
        Définit l'action associée à un bouton.

        Args:
            button_number: Numéro du bouton
            action: Action à associer
        """
        pass


class IPedalReader(ABC):
    """
    Interface pour la lecture des événements HID.

    Principe SOLID:
    - Single Responsibility: Lire les événements HID
    - Dependency Inversion: Abstraction de la lecture
    """

    @abstractmethod
    def start(self) -> bool:
        """
        Démarre la lecture des événements.

        Returns:
            True si démarrage réussi, False sinon
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """Arrête la lecture des événements."""
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """Vérifie si la lecture est en cours."""
        pass
