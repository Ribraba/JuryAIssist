"""
Gestionnaire de configuration persistante de l'application.

Principe SOLID:
- Single Responsibility: Gère uniquement la persistence des préférences utilisateur
- Open/Closed: Extensible pour ajouter de nouveaux paramètres
- Dependency Inversion: Interface abstraite pour le stockage

Fichier de configuration: ~/.juryaissist/config.json
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class AppSettings:
    """
    Paramètres de l'application.

    Attributes:
        volume: Volume audio (0-100)
        playback_speed: Vitesse de lecture (0.5-2.0)
        preferred_language: Langue préférée pour la transcription
        preferred_model: Modèle Whisper préféré (tiny, base, small, medium, large)
        window_width: Largeur de la fenêtre
        window_height: Hauteur de la fenêtre
        last_audio_directory: Dernier répertoire d'ouverture de fichier
        dark_mode: Mode sombre activé (True) ou clair (False)
        pedal_button_1: Action du bouton 1 de la pédale
        pedal_button_2: Action du bouton 2 de la pédale
        pedal_button_3: Action du bouton 3 de la pédale
        pedal_button_4: Action du bouton 4 de la pédale
    """

    volume: int = 70
    playback_speed: float = 1.0
    preferred_language: str = "fr"
    preferred_model: str = "base"
    window_width: int = 1440
    window_height: int = 960
    last_audio_directory: str = str(Path.home())
    dark_mode: bool = False

    # Configuration pédale (actions par défaut - correspond à ButtonActionMapper.DEFAULT_RS31_MAPPING)
    pedal_button_1: str = "skip_forward"   # Bouton 1 physique (droite)
    pedal_button_2: str = "play_pause"     # Bouton 2 physique (centre)
    pedal_button_3: str = "skip_backward"  # Bouton 3 physique (gauche)
    pedal_button_4: str = "stop"           # Bouton 4

    def to_dict(self) -> Dict[str, Any]:
        """Convertit en dictionnaire."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppSettings":
        """Crée depuis un dictionnaire."""
        # Filtrer les clés invalides
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)


class SettingsManager:
    """
    Gestionnaire centralisé des paramètres de l'application.

    Responsabilités:
    - Charger et sauvegarder les paramètres
    - Fournir des valeurs par défaut
    - Créer le répertoire de configuration si nécessaire

    Usage:
        >>> settings = get_settings()
        >>> settings.set('volume', 80)
        >>> volume = settings.get('volume')  # 80
        >>> settings.save()
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialise le gestionnaire de paramètres.

        Args:
            config_path: Chemin vers le fichier de config (par défaut: ~/.juryaissist/config.json)
        """
        if config_path is None:
            self.config_dir = Path.home() / ".juryaissist"
            self.config_path = self.config_dir / "config.json"
        else:
            self.config_path = config_path
            self.config_dir = config_path.parent

        # Charger ou créer les paramètres
        self.settings = self._load()

    def _load(self) -> AppSettings:
        """
        Charge les paramètres depuis le fichier.

        Returns:
            AppSettings avec les paramètres chargés ou par défaut
        """
        # Créer le répertoire si nécessaire
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Charger depuis le fichier s'il existe
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return AppSettings.from_dict(data)
            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️  Erreur lors du chargement de la config: {e}")
                print("   Utilisation des paramètres par défaut")

        # Retourner les paramètres par défaut
        return AppSettings()

    def save(self) -> bool:
        """
        Sauvegarde les paramètres dans le fichier.

        Returns:
            True si la sauvegarde a réussi, False sinon
        """
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except OSError as e:
            print(f"⚠️  Erreur lors de la sauvegarde de la config: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère un paramètre.

        Args:
            key: Nom du paramètre
            default: Valeur par défaut si le paramètre n'existe pas

        Returns:
            Valeur du paramètre ou default
        """
        return getattr(self.settings, key, default)

    def set(self, key: str, value: Any):
        """
        Définit un paramètre.

        Args:
            key: Nom du paramètre
            value: Nouvelle valeur
        """
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
        else:
            print(f"⚠️  Paramètre inconnu: {key}")

    def reset_to_defaults(self):
        """Réinitialise tous les paramètres aux valeurs par défaut."""
        self.settings = AppSettings()
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Retourne tous les paramètres sous forme de dictionnaire."""
        return self.settings.to_dict()


# Instance globale (singleton)
_settings_manager: Optional[SettingsManager] = None


def get_settings() -> SettingsManager:
    """
    Retourne l'instance unique du gestionnaire de paramètres.

    Returns:
        SettingsManager singleton
    """
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
