"""
Mappage des boutons de pédale aux actions.

Permet de configurer les actions associées à chaque bouton.
"""

from typing import Dict

from src.domain.devices.interfaces import IActionMapper
from src.domain.devices.entities import PedalAction


class ButtonActionMapper(IActionMapper):
    """
    Mapper configurable pour associer boutons et actions.

    Principe SOLID-S : Responsabilité unique = gérer le mapping
    Principe SOLID-O : Ouvert à l'extension (différentes configurations)
    """

    # Configuration par défaut pour RS-31 (4 boutons)
    # Note: Le bouton physique de gauche est le bouton 3, celui de droite est le bouton 1
    DEFAULT_RS31_MAPPING = {
        1: PedalAction.SKIP_FORWARD,   # Avancer 5s (bouton physique de droite)
        2: PedalAction.PLAY_PAUSE,     # Toggle play/pause (bouton central)
        3: PedalAction.SKIP_BACKWARD,  # Reculer 5s (bouton physique de gauche)
        4: PedalAction.STOP,           # Stop
    }

    def __init__(self, initial_mapping: Dict[int, PedalAction] = None):
        """
        Initialise le mapper.

        Args:
            initial_mapping: Mapping initial {button_number: action}.
                           Si None, utilise DEFAULT_RS31_MAPPING
        """
        if initial_mapping is None:
            self._mapping = self.DEFAULT_RS31_MAPPING.copy()
        else:
            self._mapping = initial_mapping.copy()

    def get_action(self, button_number: int) -> PedalAction:
        """
        Obtient l'action associée à un bouton.

        Args:
            button_number: Numéro du bouton

        Returns:
            Action associée, ou PedalAction.UNKNOWN si non trouvée
        """
        return self._mapping.get(button_number, PedalAction.UNKNOWN)

    def set_action(self, button_number: int, action: PedalAction) -> None:
        """
        Définit l'action pour un bouton.

        Args:
            button_number: Numéro du bouton
            action: Action à associer
        """
        if button_number < 1:
            raise ValueError(f"button_number doit être >= 1, reçu {button_number}")

        self._mapping[button_number] = action

    def get_mapping(self) -> Dict[int, PedalAction]:
        """
        Obtient le mapping complet.

        Returns:
            Copie du dictionnaire {button_number: action}
        """
        return self._mapping.copy()

    def reset_to_default(self) -> None:
        """Réinitialise au mapping par défaut RS-31."""
        self._mapping = self.DEFAULT_RS31_MAPPING.copy()


class CustomActionMapper(IActionMapper):
    """
    Mapper personnalisable pour configurations avancées.

    Permet de créer des mappings complètement personnalisés.
    Principe SOLID-L : Substitution de Liskov - peut remplacer ButtonActionMapper
    """

    def __init__(self):
        """Initialise avec un mapping vide."""
        self._mapping: Dict[int, PedalAction] = {}

    def get_action(self, button_number: int) -> PedalAction:
        """Obtient l'action pour un bouton."""
        return self._mapping.get(button_number, PedalAction.UNKNOWN)

    def set_action(self, button_number: int, action: PedalAction) -> None:
        """Définit l'action pour un bouton."""
        if button_number < 1:
            raise ValueError(f"button_number doit être >= 1, reçu {button_number}")
        self._mapping[button_number] = action

    def get_mapping(self) -> Dict[int, PedalAction]:
        """Obtient le mapping complet."""
        return self._mapping.copy()

    def load_from_dict(self, mapping: Dict[int, str]) -> None:
        """
        Charge un mapping depuis un dictionnaire de strings.

        Args:
            mapping: Dictionnaire {button_number: "action_name"}

        Exemple:
            mapper.load_from_dict({1: "skip_backward", 2: "play_pause"})
        """
        self._mapping = {}
        for button_num, action_str in mapping.items():
            try:
                action = PedalAction(action_str)
                self.set_action(button_num, action)
            except ValueError:
                # Ignorer les actions invalides
                continue

    def save_to_dict(self) -> Dict[int, str]:
        """
        Sauvegarde le mapping sous forme de dictionnaire de strings.

        Returns:
            Dictionnaire {button_number: "action_name"}
        """
        return {btn: action.value for btn, action in self._mapping.items()}
