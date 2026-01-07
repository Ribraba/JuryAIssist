"""
Parsers d'événements pour différentes pédales.

Implémentation du parsing des données HID brutes.
"""

from typing import Dict, Tuple

from src.devices.pedal import IEventParser, ButtonEvent


class RS31EventParser(IEventParser):
    """
    Parser d'événements pour la pédale Olympus RS-31.

    Principe SOLID-S : Responsabilité unique = parser les données RS-31
    Principe SOLID-O : Peut être étendu pour d'autres modèles Olympus

    Format des données HID (64 bytes) :
    - byte[0-1] : Toujours 0
    - byte[2] : Masques pour boutons 1-3 (bits 0, 1, 2)
    - byte[3] : Masque pour bouton 4 (bit 1)
    - byte[4-63] : Non utilisés

    Mapping :
    - Bouton 1 : byte[2] & 0x01
    - Bouton 2 : byte[2] & 0x02
    - Bouton 3 : byte[2] & 0x04
    - Bouton 4 : byte[3] & 0x02
    """

    # Mapping : {button_number: (byte_index, bit_mask)}
    BUTTON_MASKS: Dict[int, Tuple[int, int]] = {
        1: (2, 0x01),  # byte[2], bit 0
        2: (2, 0x02),  # byte[2], bit 1
        3: (2, 0x04),  # byte[2], bit 2
        4: (3, 0x02),  # byte[3], bit 1
    }

    def __init__(self):
        """Initialise le parser."""
        # Garder l'état précédent pour détecter les changements
        self._previous_state: Dict[int, bool] = {1: False, 2: False, 3: False, 4: False}

    def parse(self, raw_data: bytes) -> list[ButtonEvent]:
        """
        Parse les données HID brutes de la RS-31.

        Args:
            raw_data: Données brutes (64 bytes) de la pédale

        Returns:
            Liste d'événements de boutons détectés (pressed ou released)
        """
        if len(raw_data) < 4:
            return []

        events = []

        for button_num, (byte_idx, mask) in self.BUTTON_MASKS.items():
            # Vérifier si le bouton est pressé
            is_pressed = bool(raw_data[byte_idx] & mask)

            # Détecter un changement d'état
            if is_pressed != self._previous_state[button_num]:
                events.append(ButtonEvent(button_number=button_num, pressed=is_pressed))
                self._previous_state[button_num] = is_pressed

        return events

    def reset(self) -> None:
        """Réinitialise l'état du parser."""
        self._previous_state = {1: False, 2: False, 3: False, 4: False}


class GenericHIDParser(IEventParser):
    """
    Parser générique pour pédales HID simples.

    Peut être utilisé pour d'autres pédales avec format similaire.
    Principe SOLID-O : Extension pour supporter d'autres pédales
    """

    def __init__(self, button_masks: Dict[int, Tuple[int, int]]):
        """
        Initialise le parser générique.

        Args:
            button_masks: Mapping {button_number: (byte_index, bit_mask)}
        """
        self._button_masks = button_masks
        self._previous_state: Dict[int, bool] = {
            btn: False for btn in button_masks.keys()
        }

    def parse(self, raw_data: bytes) -> list[ButtonEvent]:
        """
        Parse les données HID avec le mapping fourni.

        Args:
            raw_data: Données brutes du périphérique

        Returns:
            Liste d'événements détectés
        """
        events = []

        for button_num, (byte_idx, mask) in self._button_masks.items():
            if len(raw_data) <= byte_idx:
                continue

            is_pressed = bool(raw_data[byte_idx] & mask)

            if is_pressed != self._previous_state[button_num]:
                events.append(ButtonEvent(button_number=button_num, pressed=is_pressed))
                self._previous_state[button_num] = is_pressed

        return events

    def reset(self) -> None:
        """Réinitialise l'état du parser."""
        self._previous_state = {btn: False for btn in self._button_masks.keys()}
