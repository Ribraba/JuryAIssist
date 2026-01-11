"""
Classe principale pour la pédale Olympus avec signaux Qt.

Intègre tous les composants (détection, lecture, parsing, mapping) dans une classe Qt.
"""

from typing import Optional

from PySide6.QtCore import QObject, QThread, Signal

from src.devices.pedal import (
    IPedalDetector,
    IEventParser,
    IActionMapper,
    ButtonEvent,
    PedalAction,
    PedalInfo,
)
from src.devices.detection import OlympusPedalDetector
from src.devices.event_parser import RS31EventParser
from src.devices.action_mapper import ButtonActionMapper
from src.devices.hid_reader import HIDReader


class PedalReaderThread(QThread):
    """
    Thread Qt pour la lecture continue des événements de pédale.

    Principe SOLID-S : Responsabilité unique = gérer le thread de lecture
    """

    event_received = Signal(ButtonEvent)

    def __init__(self, reader: HIDReader):
        """
        Initialise le thread.

        Args:
            reader: Lecteur HID configuré
        """
        super().__init__()
        self._reader = reader
        self._running = False

    def run(self):
        """Boucle de lecture (exécutée dans le thread)."""
        self._running = True

        # Callback appelé par le HIDReader
        def on_event(event: ButtonEvent):
            self.event_received.emit(event)

        self._reader._callback = on_event

        # Démarrer la lecture
        if self._reader.start():
            self._reader.read_loop(poll_interval=0.01)

    def stop(self):
        """Arrête le thread."""
        self._running = False
        self._reader.stop()
        self.quit()
        self.wait()


class OlympusPedal(QObject):
    """
    Classe principale pour gérer la pédale Olympus RS-31 avec Qt.

    Cette classe intègre tous les composants (détection, parsing, mapping)
    et émet des signaux Qt pour les actions détectées.

    Principe SOLID-S : Responsabilité unique = orchestrer la pédale
    Principe SOLID-D : Dépend d'abstractions (interfaces)
    Principe SOLID-O : Ouvert à l'extension (peut accepter d'autres parsers/mappers)

    Signaux:
        action_triggered: Émis quand une action est détectée (PedalAction)
        button_pressed: Émis quand un bouton est enfoncé (int)
        button_released: Émis quand un bouton est relâché (int)
        connected: Émis quand la pédale est connectée
        disconnected: Émis quand la pédale est déconnectée
        error: Émis en cas d'erreur (str)
    """

    action_triggered = Signal(PedalAction)
    button_pressed = Signal(int)  # button_number
    button_released = Signal(int)  # button_number
    connected = Signal()
    disconnected = Signal()
    error = Signal(str)

    def __init__(
        self,
        detector: Optional[IPedalDetector] = None,
        parser: Optional[IEventParser] = None,
        mapper: Optional[IActionMapper] = None,
    ):
        """
        Initialise la pédale Olympus.

        Args:
            detector: Détecteur de pédale (None = OlympusPedalDetector par défaut)
            parser: Parser d'événements (None = RS31EventParser par défaut)
            mapper: Mapper d'actions (None = ButtonActionMapper par défaut)

        Principe SOLID-D : Injection de dépendances (peut accepter n'importe quelle implémentation)
        """
        super().__init__()

        # Injection de dépendances avec valeurs par défaut
        self._detector = detector or OlympusPedalDetector()
        self._parser = parser or RS31EventParser()
        self._mapper = mapper or ButtonActionMapper()

        self._pedal_info: Optional[PedalInfo] = None
        self._reader: Optional[HIDReader] = None
        self._thread: Optional[PedalReaderThread] = None

    def detect(self) -> bool:
        """
        Détecte et se connecte à une pédale.

        Returns:
            True si pédale détectée et connectée, False sinon
        """
        try:
            self._pedal_info = self._detector.detect()

            if self._pedal_info is None:
                self.error.emit("Aucune pédale Olympus RS-31 détectée")
                return False

            return True

        except Exception as e:
            self.error.emit(f"Erreur de détection: {str(e)}")
            return False

    def connect(self) -> bool:
        """
        Se connecte à la pédale et démarre la lecture.

        Returns:
            True si connecté avec succès, False sinon
        """
        if self._pedal_info is None:
            if not self.detect():
                return False

        try:
            # Créer le lecteur HID
            self._reader = HIDReader(
                pedal_info=self._pedal_info,
                event_parser=self._parser,
            )

            # Créer et démarrer le thread de lecture
            self._thread = PedalReaderThread(self._reader)
            self._thread.event_received.connect(self._on_event_received)
            self._thread.start()

            self.connected.emit()
            return True

        except Exception as e:
            self.error.emit(f"Erreur de connexion: {str(e)}")
            return False

    def disconnect(self) -> None:
        """Déconnecte la pédale."""
        if self._thread:
            self._thread.stop()
            self._thread = None

        if self._reader:
            self._reader = None

        self.disconnected.emit()

    def is_connected(self) -> bool:
        """
        Vérifie si la pédale est connectée.

        Returns:
            True si connectée, False sinon
        """
        return (
            self._thread is not None
            and self._thread.isRunning()
            and self._reader is not None
            and self._reader.is_running()
        )

    def get_pedal_info(self) -> Optional[PedalInfo]:
        """
        Obtient les informations sur la pédale détectée.

        Returns:
            PedalInfo si pédale détectée, None sinon
        """
        return self._pedal_info

    def get_action_mapping(self) -> dict:
        """
        Obtient le mapping actuel des actions.

        Returns:
            Dictionnaire {button_number: PedalAction}
        """
        return self._mapper.get_mapping()

    def set_action(self, button_number: int, action: PedalAction) -> None:
        """
        Définit l'action pour un bouton.

        Args:
            button_number: Numéro du bouton
            action: Action à associer
        """
        self._mapper.set_action(button_number, action)

    def _on_event_received(self, event: ButtonEvent):
        """
        Callback appelé quand un événement est reçu.

        Args:
            event: Événement de bouton reçu
        """
        # Émettre les signaux de bouton
        if event.pressed:
            self.button_pressed.emit(event.button_number)

            # Obtenir et émettre l'action
            action = self._mapper.get_action(event.button_number)
            if action != PedalAction.UNKNOWN:
                self.action_triggered.emit(action)
        else:
            self.button_released.emit(event.button_number)

    def __del__(self):
        """Destructeur : s'assure que la pédale est déconnectée."""
        self.disconnect()
