"""
Tests unitaires pour les parsers d'événements.

Tests des classes RS31EventParser et GenericHIDParser.
"""

import pytest

from src.devices.event_parser import RS31EventParser, GenericHIDParser
from src.devices.pedal import ButtonEvent


class TestRS31EventParser:
    """Tests pour RS31EventParser."""

    def test_parser_initialization(self):
        """Test initialisation du parser."""
        parser = RS31EventParser()
        assert parser._previous_state == {1: False, 2: False, 3: False, 4: False}

    def test_parse_button_1_pressed(self):
        """Test parsing bouton 1 enfoncé."""
        parser = RS31EventParser()

        # Données HID : bouton 1 = byte[2] & 0x01
        raw_data = bytes([0, 0, 0x01, 0])
        events = parser.parse(raw_data)

        assert len(events) == 1
        assert events[0].button_number == 1
        assert events[0].pressed is True

    def test_parse_button_2_pressed(self):
        """Test parsing bouton 2 enfoncé."""
        parser = RS31EventParser()

        # Données HID : bouton 2 = byte[2] & 0x02
        raw_data = bytes([0, 0, 0x02, 0])
        events = parser.parse(raw_data)

        assert len(events) == 1
        assert events[0].button_number == 2
        assert events[0].pressed is True

    def test_parse_button_3_pressed(self):
        """Test parsing bouton 3 enfoncé."""
        parser = RS31EventParser()

        # Données HID : bouton 3 = byte[2] & 0x04
        raw_data = bytes([0, 0, 0x04, 0])
        events = parser.parse(raw_data)

        assert len(events) == 1
        assert events[0].button_number == 3
        assert events[0].pressed is True

    def test_parse_button_4_pressed(self):
        """Test parsing bouton 4 enfoncé."""
        parser = RS31EventParser()

        # Données HID : bouton 4 = byte[3] & 0x02
        raw_data = bytes([0, 0, 0, 0x02])
        events = parser.parse(raw_data)

        assert len(events) == 1
        assert events[0].button_number == 4
        assert events[0].pressed is True

    def test_parse_all_buttons_released(self):
        """Test parsing tous boutons relâchés."""
        parser = RS31EventParser()

        # Appuyer sur le bouton 1
        raw_data = bytes([0, 0, 0x01, 0])
        parser.parse(raw_data)

        # Relâcher tous les boutons
        raw_data = bytes([0, 0, 0, 0])
        events = parser.parse(raw_data)

        assert len(events) == 1
        assert events[0].button_number == 1
        assert events[0].pressed is False

    def test_parse_multiple_buttons_simultaneously(self):
        """Test parsing plusieurs boutons en même temps."""
        parser = RS31EventParser()

        # Boutons 1, 2 et 3 enfoncés (0x01 | 0x02 | 0x04 = 0x07)
        raw_data = bytes([0, 0, 0x07, 0])
        events = parser.parse(raw_data)

        assert len(events) == 3
        button_numbers = [e.button_number for e in events]
        assert 1 in button_numbers
        assert 2 in button_numbers
        assert 3 in button_numbers
        assert all(e.pressed for e in events)

    def test_parse_no_change_no_event(self):
        """Test qu'aucun événement n'est émis si pas de changement."""
        parser = RS31EventParser()

        # Premier appui
        raw_data = bytes([0, 0, 0x01, 0])
        events = parser.parse(raw_data)
        assert len(events) == 1

        # Même état (toujours enfoncé)
        events = parser.parse(raw_data)
        assert len(events) == 0

    def test_parse_press_release_cycle(self):
        """Test cycle complet appui/relâchement."""
        parser = RS31EventParser()

        # 1. Appui bouton 2
        raw_data = bytes([0, 0, 0x02, 0])
        events = parser.parse(raw_data)
        assert len(events) == 1
        assert events[0].pressed is True

        # 2. Relâchement
        raw_data = bytes([0, 0, 0, 0])
        events = parser.parse(raw_data)
        assert len(events) == 1
        assert events[0].pressed is False

        # 3. Ré-appui
        raw_data = bytes([0, 0, 0x02, 0])
        events = parser.parse(raw_data)
        assert len(events) == 1
        assert events[0].pressed is True

    def test_parse_insufficient_data(self):
        """Test parsing avec données insuffisantes."""
        parser = RS31EventParser()

        # Moins de 4 bytes
        raw_data = bytes([0, 0])
        events = parser.parse(raw_data)

        assert len(events) == 0

    def test_reset(self):
        """Test réinitialisation du parser."""
        parser = RS31EventParser()

        # Appuyer sur un bouton
        raw_data = bytes([0, 0, 0x01, 0])
        parser.parse(raw_data)

        # Réinitialiser
        parser.reset()

        # L'état devrait être réinitialisé
        assert parser._previous_state == {1: False, 2: False, 3: False, 4: False}


class TestGenericHIDParser:
    """Tests pour GenericHIDParser."""

    def test_custom_mapping(self):
        """Test parser avec mapping personnalisé."""
        # Mapping personnalisé : 2 boutons
        custom_mapping = {
            1: (0, 0x01),  # byte[0], bit 0
            2: (1, 0x80),  # byte[1], bit 7
        }

        parser = GenericHIDParser(custom_mapping)

        # Bouton 1 enfoncé
        raw_data = bytes([0x01, 0x00])
        events = parser.parse(raw_data)

        assert len(events) == 1
        assert events[0].button_number == 1
        assert events[0].pressed is True

    def test_reset(self):
        """Test réinitialisation du parser générique."""
        custom_mapping = {1: (0, 0x01)}
        parser = GenericHIDParser(custom_mapping)

        # Appuyer sur un bouton
        raw_data = bytes([0x01])
        parser.parse(raw_data)

        # Réinitialiser
        parser.reset()

        # L'état devrait être réinitialisé
        assert parser._previous_state == {1: False}
