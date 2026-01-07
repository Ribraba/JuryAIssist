"""
Icônes SVG pour l'interface graphique.

Icônes minimalistes et modernes sans emojis.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication


def create_icon_from_svg(svg_data: str, size: int = 24, color: str = "#1D1D1F") -> QIcon:
    """
    Crée une icône Qt à partir de données SVG.

    Args:
        svg_data: Données SVG (sans balise <svg>)
        size: Taille de l'icône en pixels
        color: Couleur de l'icône

    Returns:
        QIcon créée
    """
    # Créer le SVG complet
    full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="{color}">
        {svg_data}
    </svg>'''

    # Créer le renderer
    renderer = QSvgRenderer(full_svg.encode())

    # Créer le pixmap
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(0, 0, 0, 0))  # Transparent

    # Dessiner
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)


class Icons:
    """Gestionnaire d'icônes SVG."""

    @staticmethod
    def play(color: str = "#34C759") -> QIcon:
        """Icône Play."""
        svg = '<path d="M8 5v14l11-7z"/>'
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def pause(color: str = "#34C759") -> QIcon:
        """Icône Pause."""
        svg = '<path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>'
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def stop(color: str = "#FF3B30") -> QIcon:
        """Icône Stop."""
        svg = '<rect x="6" y="6" width="12" height="12" rx="1"/>'
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def skip_back(color: str = "#1D1D1F") -> QIcon:
        """Icône Skip Backward."""
        svg = '''
            <path d="M11 18V6l-8.5 6 8.5 6zm.5-6l8.5 6V6l-8.5 6z"/>
        '''
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def skip_forward(color: str = "#1D1D1F") -> QIcon:
        """Icône Skip Forward."""
        svg = '''
            <path d="M4 18l8.5-6L4 6v12zm9-12v12l8.5-6L13 6z"/>
        '''
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def folder(color: str = "#007AFF") -> QIcon:
        """Icône Folder."""
        svg = '''
            <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
        '''
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def speed(color: str = "#007AFF") -> QIcon:
        """Icône Speed."""
        svg = '''
            <path d="M20.38 8.57l-1.23 1.85a8 8 0 0 1-.22 7.58H5.07A8 8 0 0 1 15.58 6.85l1.85-1.23A10 10 0 0 0 3.35 19a2 2 0 0 0 1.72 1h13.85a2 2 0 0 0 1.74-1 10 10 0 0 0-.27-10.44z"/>
            <path d="M10.59 15.41a2 2 0 0 0 2.83 0l5.66-8.49-8.49 5.66a2 2 0 0 0 0 2.83z"/>
        '''
        return create_icon_from_svg(svg, 24, color)

    @staticmethod
    def audio_file(color: str = "#6E6E73") -> QIcon:
        """Icône Audio File."""
        svg = '''
            <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16h-3v-5.5c0-.83-.67-1.5-1.5-1.5S10 11.67 10 12.5s.67 1.5 1.5 1.5c.19 0 .37-.03.54-.08V18H9v-5.5C9 11.12 10.12 10 11.5 10s2.5 1.12 2.5 2.5V18zm-3-8V3.5L18.5 9H13z"/>
        '''
        return create_icon_from_svg(svg, 24, color)
