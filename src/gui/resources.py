"""
Gestion des ressources de l'application (polices, icônes).

Principe SOLID:
- Single Responsibility: Gère uniquement le chargement des ressources
- Open/Closed: Extensible pour d'autres types de ressources
"""
from pathlib import Path
from typing import Optional
from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication


class ResourceManager:
    """
    Gestionnaire centralisé des ressources de l'application.

    Responsabilités:
    - Charger les icônes SVG
    - Gérer les polices (Inter avec fallback)
    """

    _instance: Optional['ResourceManager'] = None
    _icons_loaded = False
    _font_loaded = False

    def __new__(cls):
        """Singleton pattern pour éviter de charger les ressources plusieurs fois."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialise le gestionnaire."""
        self._icons_dir = Path(__file__).parent / "icons_figma"
        self._fonts_dir = Path(__file__).parent / "fonts"
        self._icon_cache = {}

    def load_icon(self, name: str) -> QIcon:
        """
        Charge une icône SVG depuis le dossier icons_figma.

        Args:
            name: Nom de l'icône (sans extension)

        Returns:
            QIcon chargée (ou icône vide si non trouvée)
        """
        # Utiliser le cache
        if name in self._icon_cache:
            return self._icon_cache[name]

        # Chercher le fichier SVG
        icon_path = self._icons_dir / f"{name}.svg"

        if icon_path.exists():
            icon = QIcon(str(icon_path))
            self._icon_cache[name] = icon
            return icon
        else:
            # Retourner une icône vide si non trouvée
            print(f"⚠️  Icon not found: {icon_path}")
            return QIcon()

    def get_inter_font(self, size: int, weight: int = 400) -> QFont:
        """
        Retourne la police Inter avec la taille et le poids spécifiés.

        Args:
            size: Taille de la police en pixels
            weight: Poids de la police (400=Regular, 500=Medium, 600=SemiBold)

        Returns:
            QFont configurée
        """
        # Tenter de charger Inter depuis les fonts système ou locales
        font = QFont("Inter", size)

        # Mapper le poids Figma vers QFont weight
        qt_weight = self._map_font_weight(weight)
        font.setWeight(qt_weight)

        # Fallback si Inter n'est pas disponible
        font.setStyleHint(QFont.SansSerif)
        font.setFamily("Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif")

        return font

    def _map_font_weight(self, figma_weight: int) -> int:
        """
        Convertit les poids Figma en poids QFont.

        Args:
            figma_weight: Poids Figma (100-900)

        Returns:
            Poids QFont
        """
        # Mapping Figma weight -> QFont weight
        weight_map = {
            400: QFont.Normal,      # Regular
            500: QFont.Medium,      # Medium
            600: QFont.DemiBold,    # SemiBold
            700: QFont.Bold,        # Bold
        }
        return weight_map.get(figma_weight, QFont.Normal)

    def load_custom_fonts(self):
        """
        Charge les polices personnalisées depuis le dossier fonts.

        Cette méthode tente de charger les fichiers .ttf/.otf du dossier fonts
        pour rendre Inter disponible dans l'application.
        """
        if self._font_loaded:
            return

        if not self._fonts_dir.exists():
            print(f"⚠️  Fonts directory not found: {self._fonts_dir}")
            return

        # Charger tous les fichiers de police
        font_files = list(self._fonts_dir.glob("**/*.ttf")) + list(self._fonts_dir.glob("**/*.otf"))

        if not font_files:
            print(f"⚠️  No font files found in {self._fonts_dir}")
            print("   Using system fallback fonts")
            return

        for font_file in font_files:
            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"✓ Loaded font: {font_file.name} ({', '.join(families)})")
            else:
                print(f"✗ Failed to load font: {font_file.name}")

        self._font_loaded = True


# Instance globale
_resource_manager = ResourceManager()


def get_icon(name: str) -> QIcon:
    """
    Fonction utilitaire pour charger une icône.

    Args:
        name: Nom de l'icône (sans extension)

    Returns:
        QIcon
    """
    return _resource_manager.load_icon(name)


def get_font(size: int, weight: int = 400) -> QFont:
    """
    Fonction utilitaire pour obtenir la police Inter.

    Args:
        size: Taille en pixels
        weight: Poids (400, 500, 600, etc.)

    Returns:
        QFont configurée
    """
    return _resource_manager.get_inter_font(size, weight)


def load_fonts():
    """Charge les polices personnalisées au démarrage de l'application."""
    _resource_manager.load_custom_fonts()
