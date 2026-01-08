"""
Tests unitaires pour le gestionnaire de paramètres.

Teste les fonctionnalités de:
- Chargement/sauvegarde des paramètres
- Valeurs par défaut
- Modification des paramètres
- Persistence sur disque
- Intégration du mode sombre et des bindings de pédale
"""

import pytest
import json
import tempfile
from pathlib import Path

from src.config.settings import SettingsManager, AppSettings


class TestAppSettings:
    """Tests pour la dataclass AppSettings."""

    def test_default_values(self):
        """Vérifie les valeurs par défaut."""
        settings = AppSettings()

        # Paramètres audio
        assert settings.volume == 70
        assert settings.playback_speed == 1.0

        # Paramètres transcription
        assert settings.preferred_language == "fr"
        assert settings.preferred_model == "base"

        # Paramètres interface
        assert settings.window_width == 1440
        assert settings.window_height == 960
        assert settings.dark_mode is False

        # Paramètres pédale (correspond à ButtonActionMapper.DEFAULT_RS31_MAPPING)
        assert settings.pedal_button_1 == "skip_forward"
        assert settings.pedal_button_2 == "play_pause"
        assert settings.pedal_button_3 == "skip_backward"
        assert settings.pedal_button_4 == "stop"

    def test_to_dict(self):
        """Vérifie la conversion en dictionnaire."""
        settings = AppSettings()
        data = settings.to_dict()

        assert isinstance(data, dict)
        assert "volume" in data
        assert "preferred_model" in data
        assert "dark_mode" in data
        assert "pedal_button_1" in data

    def test_from_dict(self):
        """Vérifie la création depuis un dictionnaire."""
        data = {
            "volume": 80,
            "preferred_model": "small",
            "dark_mode": True,
            "pedal_button_1": "play_pause",
        }

        settings = AppSettings.from_dict(data)

        assert settings.volume == 80
        assert settings.preferred_model == "small"
        assert settings.dark_mode is True
        assert settings.pedal_button_1 == "play_pause"

        # Vérifier que les autres paramètres ont les valeurs par défaut
        assert settings.preferred_language == "fr"

    def test_from_dict_with_invalid_keys(self):
        """Vérifie que les clés invalides sont ignorées."""
        data = {
            "volume": 80,
            "invalid_key": "should_be_ignored",
            "another_invalid": 123,
        }

        settings = AppSettings.from_dict(data)

        assert settings.volume == 80
        assert not hasattr(settings, "invalid_key")


class TestSettingsManager:
    """Tests pour le gestionnaire de paramètres."""

    @pytest.fixture
    def temp_config_path(self):
        """Crée un fichier de config temporaire."""
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "test_config.json"
        yield config_path
        # Cleanup
        if config_path.exists():
            config_path.unlink()
        temp_dir.rmdir()

    def test_init_with_default_path(self):
        """Vérifie l'initialisation avec le chemin par défaut."""
        manager = SettingsManager()

        assert manager.config_dir == Path.home() / ".juryaissist"
        assert manager.config_path == Path.home() / ".juryaissist" / "config.json"
        assert isinstance(manager.settings, AppSettings)

    def test_init_with_custom_path(self, temp_config_path):
        """Vérifie l'initialisation avec un chemin personnalisé."""
        manager = SettingsManager(config_path=temp_config_path)

        assert manager.config_path == temp_config_path
        assert isinstance(manager.settings, AppSettings)

    def test_get_default_values(self, temp_config_path):
        """Vérifie la récupération des valeurs par défaut."""
        manager = SettingsManager(config_path=temp_config_path)

        assert manager.get("volume") == 70
        assert manager.get("preferred_model") == "base"
        assert manager.get("dark_mode") is False

    def test_get_with_custom_default(self, temp_config_path):
        """Vérifie la récupération avec valeur par défaut personnalisée."""
        manager = SettingsManager(config_path=temp_config_path)

        assert manager.get("nonexistent_key", "default_value") == "default_value"

    def test_set_and_get(self, temp_config_path):
        """Vérifie la modification des paramètres."""
        manager = SettingsManager(config_path=temp_config_path)

        manager.set("volume", 85)
        manager.set("preferred_model", "large")
        manager.set("dark_mode", True)

        assert manager.get("volume") == 85
        assert manager.get("preferred_model") == "large"
        assert manager.get("dark_mode") is True

    def test_set_invalid_key(self, temp_config_path, capsys):
        """Vérifie le comportement avec une clé invalide."""
        manager = SettingsManager(config_path=temp_config_path)

        manager.set("invalid_key", "value")

        captured = capsys.readouterr()
        assert "Paramètre inconnu" in captured.out

    def test_save_and_load(self, temp_config_path):
        """Vérifie la sauvegarde et le chargement."""
        # Créer et sauvegarder
        manager1 = SettingsManager(config_path=temp_config_path)
        manager1.set("volume", 90)
        manager1.set("preferred_model", "medium")
        manager1.set("dark_mode", True)
        manager1.set("pedal_button_1", "stop")

        assert manager1.save() is True
        assert temp_config_path.exists()

        # Charger dans un nouveau manager
        manager2 = SettingsManager(config_path=temp_config_path)

        assert manager2.get("volume") == 90
        assert manager2.get("preferred_model") == "medium"
        assert manager2.get("dark_mode") is True
        assert manager2.get("pedal_button_1") == "stop"

    def test_save_creates_directory(self, temp_config_path):
        """Vérifie que save() crée le répertoire si nécessaire."""
        # Supprimer le répertoire parent
        if temp_config_path.parent.exists():
            temp_config_path.parent.rmdir()

        manager = SettingsManager(config_path=temp_config_path)
        assert manager.save() is True
        assert temp_config_path.parent.exists()

    def test_get_all(self, temp_config_path):
        """Vérifie la récupération de tous les paramètres."""
        manager = SettingsManager(config_path=temp_config_path)
        manager.set("volume", 75)

        all_settings = manager.get_all()

        assert isinstance(all_settings, dict)
        assert all_settings["volume"] == 75
        assert "preferred_model" in all_settings
        assert "dark_mode" in all_settings
        assert "pedal_button_1" in all_settings

    def test_reset_to_defaults(self, temp_config_path):
        """Vérifie la réinitialisation aux valeurs par défaut."""
        manager = SettingsManager(config_path=temp_config_path)

        # Modifier des valeurs
        manager.set("volume", 100)
        manager.set("dark_mode", True)
        manager.set("preferred_model", "large")

        # Réinitialiser
        manager.reset_to_defaults()

        assert manager.get("volume") == 70
        assert manager.get("dark_mode") is False
        assert manager.get("preferred_model") == "base"

    def test_load_corrupted_config(self, temp_config_path, capsys):
        """Vérifie le comportement avec un fichier de config corrompu."""
        # Créer un fichier JSON invalide
        temp_config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_config_path, "w") as f:
            f.write("invalid json {{{")

        # Charger devrait utiliser les valeurs par défaut
        manager = SettingsManager(config_path=temp_config_path)

        captured = capsys.readouterr()
        assert "Erreur lors du chargement" in captured.out

        # Vérifier que les valeurs par défaut sont utilisées
        assert manager.get("volume") == 70
        assert manager.get("preferred_model") == "base"


class TestPedalConfiguration:
    """Tests spécifiques à la configuration de la pédale."""

    @pytest.fixture
    def temp_config_path(self):
        """Crée un fichier de config temporaire."""
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "test_config.json"
        yield config_path
        # Cleanup
        if config_path.exists():
            config_path.unlink()
        temp_dir.rmdir()

    def test_pedal_default_mapping(self, temp_config_path):
        """Vérifie le mapping par défaut de la pédale."""
        manager = SettingsManager(config_path=temp_config_path)

        # Mapping par défaut selon settings.py (correspond à ButtonActionMapper.DEFAULT_RS31_MAPPING)
        assert manager.get("pedal_button_1") == "skip_forward"
        assert manager.get("pedal_button_2") == "play_pause"
        assert manager.get("pedal_button_3") == "skip_backward"
        assert manager.get("pedal_button_4") == "stop"

    def test_pedal_custom_mapping(self, temp_config_path):
        """Vérifie le mapping personnalisé de la pédale."""
        manager = SettingsManager(config_path=temp_config_path)

        # Modifier le mapping
        manager.set("pedal_button_1", "play_pause")
        manager.set("pedal_button_2", "stop")
        manager.set("pedal_button_3", "skip_forward")
        manager.set("pedal_button_4", "skip_backward")

        manager.save()

        # Recharger et vérifier
        manager2 = SettingsManager(config_path=temp_config_path)
        assert manager2.get("pedal_button_1") == "play_pause"
        assert manager2.get("pedal_button_2") == "stop"
        assert manager2.get("pedal_button_3") == "skip_forward"
        assert manager2.get("pedal_button_4") == "skip_backward"


class TestDarkModeConfiguration:
    """Tests spécifiques au mode sombre."""

    @pytest.fixture
    def temp_config_path(self):
        """Crée un fichier de config temporaire."""
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "test_config.json"
        yield config_path
        # Cleanup
        if config_path.exists():
            config_path.unlink()
        temp_dir.rmdir()

    def test_dark_mode_default(self, temp_config_path):
        """Vérifie que le mode sombre est désactivé par défaut."""
        manager = SettingsManager(config_path=temp_config_path)
        assert manager.get("dark_mode") is False

    def test_dark_mode_enable(self, temp_config_path):
        """Vérifie l'activation du mode sombre."""
        manager = SettingsManager(config_path=temp_config_path)

        manager.set("dark_mode", True)
        manager.save()

        # Recharger et vérifier
        manager2 = SettingsManager(config_path=temp_config_path)
        assert manager2.get("dark_mode") is True

    def test_dark_mode_toggle(self, temp_config_path):
        """Vérifie le basculement du mode sombre."""
        manager = SettingsManager(config_path=temp_config_path)

        # Activer
        manager.set("dark_mode", True)
        assert manager.get("dark_mode") is True

        # Désactiver
        manager.set("dark_mode", False)
        assert manager.get("dark_mode") is False


class TestWhisperConfiguration:
    """Tests spécifiques à la configuration Whisper."""

    @pytest.fixture
    def temp_config_path(self):
        """Crée un fichier de config temporaire."""
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "test_config.json"
        yield config_path
        # Cleanup
        if config_path.exists():
            config_path.unlink()
        temp_dir.rmdir()

    def test_whisper_model_default(self, temp_config_path):
        """Vérifie le modèle par défaut."""
        manager = SettingsManager(config_path=temp_config_path)
        assert manager.get("preferred_model") == "base"

    def test_whisper_model_change(self, temp_config_path):
        """Vérifie le changement de modèle."""
        manager = SettingsManager(config_path=temp_config_path)

        for model in ["tiny", "base", "small", "medium", "large"]:
            manager.set("preferred_model", model)
            assert manager.get("preferred_model") == model

    def test_whisper_language_default(self, temp_config_path):
        """Vérifie la langue par défaut."""
        manager = SettingsManager(config_path=temp_config_path)
        assert manager.get("preferred_language") == "fr"

    def test_whisper_language_change(self, temp_config_path):
        """Vérifie le changement de langue."""
        manager = SettingsManager(config_path=temp_config_path)

        manager.set("preferred_language", "en")
        assert manager.get("preferred_language") == "en"

        manager.set("preferred_language", "es")
        assert manager.get("preferred_language") == "es"
