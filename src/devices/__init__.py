"""
Module de gestion des périphériques.

Gère la détection et la communication avec les pédales USB
(Olympus RS-31 et autres modèles compatibles).

Exemple d'utilisation:
    from src.devices import OlympusPedal, PedalAction

    pedal = OlympusPedal()
    if pedal.detect() and pedal.connect():
        pedal.action_triggered.connect(lambda action: print(f"Action: {action}"))
"""

from src.devices.pedal import (
    PedalAction,
    ButtonEvent,
    PedalInfo,
    IPedalDetector,
    IEventParser,
    IActionMapper,
    IPedalReader,
)
from src.devices.olympus_pedal import OlympusPedal
from src.devices.detection import OlympusPedalDetector
from src.devices.event_parser import RS31EventParser, GenericHIDParser
from src.devices.action_mapper import ButtonActionMapper, CustomActionMapper
from src.devices.hid_reader import HIDReader

__all__ = [
    # Classes principales
    "OlympusPedal",
    # Enums et dataclasses
    "PedalAction",
    "ButtonEvent",
    "PedalInfo",
    # Interfaces (pour extension)
    "IPedalDetector",
    "IEventParser",
    "IActionMapper",
    "IPedalReader",
    # Implémentations concrètes
    "OlympusPedalDetector",
    "RS31EventParser",
    "GenericHIDParser",
    "ButtonActionMapper",
    "CustomActionMapper",
    "HIDReader",
]
