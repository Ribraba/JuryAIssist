"""
Tests unitaires pour les structures de données du module pedal.

Tests des dataclasses et enums.
"""

import pytest

from src.devices.pedal import ButtonEvent, PedalInfo, PedalAction


class TestButtonEvent:
    """Tests pour ButtonEvent."""

    def test_button_event_creation_pressed(self):
        """Test création d'un événement pressed."""
        event = ButtonEvent(button_number=1, pressed=True)

        assert event.button_number == 1
        assert event.pressed is True
        assert event.timestamp is None

    def test_button_event_creation_released(self):
        """Test création d'un événement released."""
        event = ButtonEvent(button_number=2, pressed=False, timestamp=123.45)

        assert event.button_number == 2
        assert event.pressed is False
        assert event.timestamp == 123.45

    def test_button_event_invalid_button_number(self):
        """Test validation du numéro de bouton."""
        with pytest.raises(ValueError, match="button_number doit être >= 1"):
            ButtonEvent(button_number=0, pressed=True)

        with pytest.raises(ValueError, match="button_number doit être >= 1"):
            ButtonEvent(button_number=-1, pressed=True)

    def test_button_event_immutable(self):
        """Test que ButtonEvent est immutable (frozen)."""
        event = ButtonEvent(button_number=1, pressed=True)

        with pytest.raises(AttributeError):
            event.button_number = 2


class TestPedalInfo:
    """Tests pour PedalInfo."""

    def test_pedal_info_creation(self):
        """Test création d'un PedalInfo complet."""
        info = PedalInfo(
            vendor_id=0x07B4,
            product_id=0x025F,
            manufacturer="OLYMPUS",
            product_name="RS-31",
            path=b"/dev/hidraw0",
            serial_number="206122002",
        )

        assert info.vendor_id == 0x07B4
        assert info.product_id == 0x025F
        assert info.manufacturer == "OLYMPUS"
        assert info.product_name == "RS-31"
        assert info.path == b"/dev/hidraw0"
        assert info.serial_number == "206122002"

    def test_pedal_info_without_serial(self):
        """Test création sans numéro de série."""
        info = PedalInfo(
            vendor_id=0x07B4,
            product_id=0x025F,
            manufacturer="OLYMPUS",
            product_name="RS-31",
            path=b"/dev/hidraw0",
        )

        assert info.serial_number is None

    def test_pedal_info_str_representation(self):
        """Test représentation textuelle."""
        info = PedalInfo(
            vendor_id=0x07B4,
            product_id=0x025F,
            manufacturer="OLYMPUS",
            product_name="RS-31",
            path=b"/dev/hidraw0",
            serial_number="206122002",
        )

        str_repr = str(info)
        assert "0x07b4" in str_repr
        assert "0x025f" in str_repr
        assert "OLYMPUS" in str_repr
        assert "RS-31" in str_repr
        assert "206122002" in str_repr

    def test_pedal_info_immutable(self):
        """Test que PedalInfo est immutable."""
        info = PedalInfo(
            vendor_id=0x07B4,
            product_id=0x025F,
            manufacturer="OLYMPUS",
            product_name="RS-31",
            path=b"/dev/hidraw0",
        )

        with pytest.raises(AttributeError):
            info.vendor_id = 0x1234


class TestPedalAction:
    """Tests pour l'enum PedalAction."""

    def test_all_actions_exist(self):
        """Test que toutes les actions sont définies."""
        expected_actions = [
            "PLAY_PAUSE",
            "SKIP_FORWARD",
            "SKIP_BACKWARD",
            "STOP",
            "CYCLE_SPEED",
            "MARK_POSITION",
            "UNKNOWN",
        ]

        for action_name in expected_actions:
            assert hasattr(PedalAction, action_name)

    def test_action_values(self):
        """Test les valeurs des actions."""
        assert PedalAction.PLAY_PAUSE.value == "play_pause"
        assert PedalAction.SKIP_FORWARD.value == "skip_forward"
        assert PedalAction.SKIP_BACKWARD.value == "skip_backward"
        assert PedalAction.STOP.value == "stop"

    def test_action_from_string(self):
        """Test création d'une action depuis une string."""
        action = PedalAction("play_pause")
        assert action == PedalAction.PLAY_PAUSE

        with pytest.raises(ValueError):
            PedalAction("invalid_action")
