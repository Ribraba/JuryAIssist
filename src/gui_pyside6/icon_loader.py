"""
Chargeur d'icônes SVG pour l'interface PySide6.
Respecte les principes SOLID + Tell, Don't Ask.
"""

from pathlib import Path
from typing import Dict, Optional
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt


class IconLoader:
    """
    Gestionnaire de chargement des icônes SVG avec cache.

    Principes SOLID appliqués:
    - Single Responsibility: Charge et met en cache les icônes SVG
    - Open/Closed: Extensible pour d'autres formats sans modification
    - Liskov Substitution: Interface cohérente
    - Interface Segregation: Interface minimale
    - Dependency Inversion: Utilise des abstractions Qt

    Tell, Don't Ask: Les méthodes commandent plutôt qu'interroger.
    """

    _instance: Optional['IconLoader'] = None
    _icons_cache: Dict[str, QIcon] = {}

    def __new__(cls) -> 'IconLoader':
        """Singleton pour éviter les chargements multiples."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_paths()
        return cls._instance

    def _init_paths(self) -> None:
        """Initialise les chemins vers les icônes."""
        self.icons_dir: Path = Path(__file__).parent / "icons"
        if not self.icons_dir.exists():
            raise FileNotFoundError(
                f"Le dossier d'icônes n'existe pas: {self.icons_dir}"
            )

    def load_icon(self, name: str, size: int = 24) -> QIcon:
        """
        Charge une icône SVG avec mise en cache.

        Args:
            name: Nom du fichier SVG (sans extension)
            size: Taille de l'icône en pixels

        Returns:
            QIcon: L'icône chargée

        Raises:
            FileNotFoundError: Si l'icône n'existe pas
        """
        cache_key = f"{name}_{size}"

        # Retourner depuis le cache si disponible
        if cache_key in self._icons_cache:
            return self._icons_cache[cache_key]

        icon_path = self.icons_dir / f"{name}.svg"

        if not icon_path.exists():
            raise FileNotFoundError(
                f"Icône SVG non trouvée: {icon_path}\n"
                f"Fichiers disponibles: {list(self.icons_dir.glob('*.svg'))}"
            )

        # Charger et rendre le SVG
        icon = self._render_svg(icon_path, size)

        # Mettre en cache
        self._icons_cache[cache_key] = icon

        return icon

    def _render_svg(self, path: Path, size: int) -> QIcon:
        """
        Rend un fichier SVG en QIcon.

        Args:
            path: Chemin vers le fichier SVG
            size: Taille en pixels

        Returns:
            QIcon: L'icône rendue
        """
        renderer = QSvgRenderer(str(path))

        if not renderer.isValid():
            raise ValueError(f"SVG invalide: {path}")

        # Créer un pixmap transparent
        pixmap = QPixmap(QSize(size, size))
        pixmap.fill(Qt.GlobalColor.transparent)

        # Rendre le SVG sur le pixmap
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)

    @classmethod
    def get_icon(cls, name: str, size: int = 24) -> QIcon:
        """
        Méthode statique pour récupérer une icône.

        Args:
            name: Nom de l'icône (sans extension)
            size: Taille en pixels

        Returns:
            QIcon: L'icône chargée
        """
        loader = cls()
        return loader.load_icon(name, size)
