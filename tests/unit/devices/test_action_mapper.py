"""
Tests unitaires pour les mappers d'actions.

Tests des classes ButtonActionMapper et CustomActionMapper.
"""

import pytest

from src.devices.action_mapper import ButtonActionMapper, CustomActionMapper
from src.devices.pedal import PedalAction


class TestButtonActionMapper:
    """Tests pour ButtonActionMapper."""

    def test_default_mapping(self):
        """Test mapping par défaut RS-31."""
        mapper = ButtonActionMapper()

        assert mapper.get_action(1) == PedalAction.SKIP_BACKWARD
        assert mapper.get_action(2) == PedalAction.PLAY_PAUSE
        assert mapper.get_action(3) == PedalAction.SKIP_FORWARD
        assert mapper.get_action(4) == PedalAction.STOP

    def test_physical_button_mapping(self):
        """
        Test que le mapping correspond à la disposition physique de la pédale.

        Disposition physique RS-31:
        [BTN 1: gauche] [BTN 2: centre] [BTN 3: droite] [BTN 4]

        Fonctions attendues:
        - Bouton gauche (1) → Reculer
        - Bouton centre (2) → Play/Pause
        - Bouton droit (3) → Avancer
        - Bouton 4 → Stop
        """
        mapper = ButtonActionMapper()

        # Bouton physique gauche (1) = Reculer
        assert mapper.get_action(1) == PedalAction.SKIP_BACKWARD, \
            "Le bouton gauche (1) doit reculer de 5s"

        # Bouton physique centre (2) = Play/Pause
        assert mapper.get_action(2) == PedalAction.PLAY_PAUSE, \
            "Le bouton central (2) doit faire play/pause"

        # Bouton physique droit (3) = Avancer
        assert mapper.get_action(3) == PedalAction.SKIP_FORWARD, \
            "Le bouton droit (3) doit avancer de 5s"

        # Bouton 4 = Stop
        assert mapper.get_action(4) == PedalAction.STOP, \
            "Le bouton 4 doit arrêter la lecture"

    def test_custom_initial_mapping(self):
        """Test avec mapping initial personnalisé."""
        custom_mapping = {
            1: PedalAction.PLAY_PAUSE,
            2: PedalAction.STOP,
        }

        mapper = ButtonActionMapper(initial_mapping=custom_mapping)

        assert mapper.get_action(1) == PedalAction.PLAY_PAUSE
        assert mapper.get_action(2) == PedalAction.STOP
        # Boutons non définis retournent UNKNOWN
        assert mapper.get_action(3) == PedalAction.UNKNOWN

    def test_get_action_unknown_button(self):
        """Test get_action pour bouton non mappé."""
        mapper = ButtonActionMapper()

        assert mapper.get_action(99) == PedalAction.UNKNOWN

    def test_set_action(self):
        """Test modification d'une action."""
        mapper = ButtonActionMapper()

        # Modifier l'action du bouton 1
        mapper.set_action(1, PedalAction.CYCLE_SPEED)

        assert mapper.get_action(1) == PedalAction.CYCLE_SPEED
        # Les autres ne changent pas
        assert mapper.get_action(2) == PedalAction.PLAY_PAUSE

    def test_set_action_invalid_button(self):
        """Test set_action avec numéro invalide."""
        mapper = ButtonActionMapper()

        with pytest.raises(ValueError, match="button_number doit être >= 1"):
            mapper.set_action(0, PedalAction.STOP)

        with pytest.raises(ValueError, match="button_number doit être >= 1"):
            mapper.set_action(-1, PedalAction.STOP)

    def test_get_mapping(self):
        """Test obtention du mapping complet."""
        mapper = ButtonActionMapper()

        mapping = mapper.get_mapping()

        assert isinstance(mapping, dict)
        assert len(mapping) == 4
        assert mapping[1] == PedalAction.SKIP_BACKWARD
        assert mapping[2] == PedalAction.PLAY_PAUSE

        # Vérifier que c'est une copie (pas la référence)
        mapping[1] = PedalAction.STOP
        assert mapper.get_action(1) == PedalAction.SKIP_BACKWARD

    def test_reset_to_default(self):
        """Test réinitialisation au mapping par défaut."""
        mapper = ButtonActionMapper()

        # Modifier le mapping
        mapper.set_action(1, PedalAction.MARK_POSITION)
        mapper.set_action(2, PedalAction.CYCLE_SPEED)

        # Réinitialiser
        mapper.reset_to_default()

        # Vérifier que c'est revenu au défaut
        assert mapper.get_action(1) == PedalAction.SKIP_BACKWARD
        assert mapper.get_action(2) == PedalAction.PLAY_PAUSE


class TestCustomActionMapper:
    """Tests pour CustomActionMapper."""

    def test_empty_initial_mapping(self):
        """Test mapping vide initial."""
        mapper = CustomActionMapper()

        # Tous les boutons devraient retourner UNKNOWN
        assert mapper.get_action(1) == PedalAction.UNKNOWN
        assert mapper.get_action(2) == PedalAction.UNKNOWN

    def test_set_and_get_action(self):
        """Test définition et récupération d'action."""
        mapper = CustomActionMapper()

        mapper.set_action(1, PedalAction.PLAY_PAUSE)
        mapper.set_action(2, PedalAction.STOP)

        assert mapper.get_action(1) == PedalAction.PLAY_PAUSE
        assert mapper.get_action(2) == PedalAction.STOP
        assert mapper.get_action(3) == PedalAction.UNKNOWN

    def test_load_from_dict(self):
        """Test chargement depuis un dictionnaire de strings."""
        mapper = CustomActionMapper()

        config = {
            1: "play_pause",
            2: "skip_forward",
            3: "stop",
        }

        mapper.load_from_dict(config)

        assert mapper.get_action(1) == PedalAction.PLAY_PAUSE
        assert mapper.get_action(2) == PedalAction.SKIP_FORWARD
        assert mapper.get_action(3) == PedalAction.STOP

    def test_load_from_dict_invalid_action(self):
        """Test chargement avec action invalide (doit être ignorée)."""
        mapper = CustomActionMapper()

        config = {
            1: "play_pause",
            2: "invalid_action",  # Invalide, sera ignorée
            3: "stop",
        }

        mapper.load_from_dict(config)

        assert mapper.get_action(1) == PedalAction.PLAY_PAUSE
        assert mapper.get_action(2) == PedalAction.UNKNOWN  # Ignorée
        assert mapper.get_action(3) == PedalAction.STOP

    def test_save_to_dict(self):
        """Test sauvegarde vers un dictionnaire de strings."""
        mapper = CustomActionMapper()

        mapper.set_action(1, PedalAction.PLAY_PAUSE)
        mapper.set_action(2, PedalAction.SKIP_BACKWARD)

        saved = mapper.save_to_dict()

        assert saved == {
            1: "play_pause",
            2: "skip_backward",
        }

    def test_load_save_roundtrip(self):
        """Test cycle complet load → save."""
        mapper1 = CustomActionMapper()

        original_config = {
            1: "play_pause",
            2: "skip_forward",
            3: "stop",
            4: "cycle_speed",
        }

        mapper1.load_from_dict(original_config)
        saved_config = mapper1.save_to_dict()

        # Créer un nouveau mapper et charger
        mapper2 = CustomActionMapper()
        mapper2.load_from_dict(saved_config)

        # Vérifier que c'est identique
        assert mapper2.get_action(1) == PedalAction.PLAY_PAUSE
        assert mapper2.get_action(2) == PedalAction.SKIP_FORWARD
        assert mapper2.get_action(3) == PedalAction.STOP
        assert mapper2.get_action(4) == PedalAction.CYCLE_SPEED

    def test_get_mapping(self):
        """Test obtention du mapping complet."""
        mapper = CustomActionMapper()

        mapper.set_action(1, PedalAction.PLAY_PAUSE)
        mapper.set_action(2, PedalAction.STOP)

        mapping = mapper.get_mapping()

        assert mapping == {
            1: PedalAction.PLAY_PAUSE,
            2: PedalAction.STOP,
        }

        # Vérifier que c'est une copie
        mapping[1] = PedalAction.SKIP_FORWARD
        assert mapper.get_action(1) == PedalAction.PLAY_PAUSE
