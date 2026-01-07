"""
Lecteur d'événements HID pour pédales.

Gère la lecture continue des événements depuis le périphérique HID.
"""

import time
from typing import Optional, Callable

try:
    import hid
except ImportError:
    hid = None

from src.devices.pedal import IPedalReader, PedalInfo, ButtonEvent, IEventParser


class HIDReader(IPedalReader):
    """
    Lecteur d'événements HID synchrone.

    Principe SOLID-S : Responsabilité unique = lire les événements HID
    Principe SOLID-D : Dépend de IEventParser (abstraction)

    Note: Cette classe est synchrone. Pour une utilisation dans Qt,
    elle sera wrappée dans un QThread (voir olympus_pedal.py)
    """

    def __init__(
        self,
        pedal_info: PedalInfo,
        event_parser: IEventParser,
        event_callback: Optional[Callable[[ButtonEvent], None]] = None,
    ):
        """
        Initialise le lecteur HID.

        Args:
            pedal_info: Informations sur la pédale à ouvrir
            event_parser: Parser pour décoder les événements
            event_callback: Fonction appelée pour chaque événement détecté
        """
        if hid is None:
            raise ImportError(
                "Le module 'hid' n'est pas disponible. "
                "Installez-le avec: pip install hidapi"
            )

        self._pedal_info = pedal_info
        self._parser = event_parser
        self._callback = event_callback
        self._device: Optional[hid.device] = None
        self._running = False

    def start(self) -> bool:
        """
        Ouvre le périphérique HID.

        Returns:
            True si ouvert avec succès, False sinon
        """
        try:
            self._device = hid.device()
            self._device.open_path(self._pedal_info.path)
            self._device.set_nonblocking(True)
            self._running = True
            return True
        except Exception as e:
            print(f"Erreur lors de l'ouverture du périphérique: {e}")
            self._device = None
            self._running = False
            return False

    def stop(self) -> None:
        """Ferme le périphérique HID."""
        self._running = False
        if self._device:
            try:
                self._device.close()
            except Exception:
                pass
            self._device = None

    def is_running(self) -> bool:
        """
        Vérifie si le lecteur est actif.

        Returns:
            True si actif, False sinon
        """
        return self._running and self._device is not None

    def read_once(self, timeout_ms: int = 100) -> list[ButtonEvent]:
        """
        Lit les événements une fois (mode non-bloquant).

        Args:
            timeout_ms: Timeout de lecture en millisecondes

        Returns:
            Liste d'événements détectés (peut être vide)
        """
        if not self.is_running():
            return []

        try:
            # Lire les données (64 bytes pour RS-31)
            data = self._device.read(64, timeout_ms)

            if data:
                # Parser les événements
                events = self._parser.parse(bytes(data))

                # Appeler le callback pour chaque événement
                if self._callback:
                    for event in events:
                        self._callback(event)

                return events

        except Exception as e:
            print(f"Erreur lors de la lecture: {e}")
            self.stop()

        return []

    def read_loop(self, poll_interval: float = 0.01) -> None:
        """
        Boucle de lecture continue (bloquante).

        Cette méthode doit être exécutée dans un thread séparé.

        Args:
            poll_interval: Intervalle entre les lectures (en secondes)
        """
        while self._running:
            self.read_once(timeout_ms=10)
            time.sleep(poll_interval)

    def __enter__(self):
        """Context manager : entrée."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager : sortie."""
        self.stop()
