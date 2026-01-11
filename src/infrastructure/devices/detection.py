"""
Implémentation de la détection de pédales Olympus.

Utilise hidapi pour détecter les périphériques USB HID.
"""

from typing import Optional

try:
    import hid
except ImportError:
    hid = None

from src.devices.pedal import IPedalDetector, PedalInfo


class OlympusPedalDetector(IPedalDetector):
    """
    Détecteur de pédales Olympus RS-31.

    Implémentation concrète de IPedalDetector pour les pédales Olympus.
    Principe SOLID-S : Responsabilité unique = détecter pédales Olympus
    """

    # Identifiants USB de la pédale Olympus RS-31
    OLYMPUS_VENDOR_ID = 0x07B4
    RS31_PRODUCT_ID = 0x025F

    def __init__(self):
        """Initialise le détecteur."""
        if hid is None:
            raise ImportError(
                "Le module 'hid' n'est pas disponible. "
                "Installez-le avec: pip install hidapi"
            )

    def detect(self) -> Optional[PedalInfo]:
        """
        Détecte une pédale Olympus RS-31 connectée.

        Returns:
            PedalInfo si trouvée, None sinon
        """
        devices = hid.enumerate(self.OLYMPUS_VENDOR_ID, self.RS31_PRODUCT_ID)

        if devices:
            device = devices[0]  # Prendre la première trouvée
            return self._create_pedal_info(device)

        return None

    def list_all_devices(self) -> list[PedalInfo]:
        """
        Liste tous les périphériques HID détectés.

        Returns:
            Liste de tous les devices HID (pour debug)
        """
        all_devices = hid.enumerate()
        result = []

        for device in all_devices:
            try:
                info = self._create_pedal_info(device)
                result.append(info)
            except Exception:
                # Ignorer les devices qui causent des erreurs
                continue

        return result

    def _create_pedal_info(self, device: dict) -> PedalInfo:
        """
        Crée un PedalInfo depuis un dictionnaire hid.

        Args:
            device: Dictionnaire retourné par hid.enumerate()

        Returns:
            PedalInfo correspondant
        """
        return PedalInfo(
            vendor_id=device["vendor_id"],
            product_id=device["product_id"],
            manufacturer=device.get("manufacturer_string", "Unknown"),
            product_name=device.get("product_string", "Unknown"),
            path=device["path"],
            serial_number=device.get("serial_number"),
        )
