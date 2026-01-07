"""
Widget Timeline selon Phase 3.1.2 de la roadmap.

Fonctionnalités :
- Barre de progression visuelle
- Curseur de position actuelle
- Clic pour se déplacer dans l'audio
- Marqueurs pour segments de transcription
- Affichage du temps actuel et total
"""

from typing import Dict, List

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QMouseEvent
from PyQt5.QtWidgets import QWidget

from src.audio.timeline import TimeUtils


class TimelineWidget(QWidget):
    """
    Widget de timeline graphique avec curseur et marqueurs.

    Permet de visualiser et contrôler la position dans l'audio.
    """

    # Signal émis quand l'utilisateur clique sur la timeline
    position_changed = pyqtSignal(float)  # Nouvelle position en secondes

    def __init__(self, parent=None):
        """Initialise le widget."""
        super().__init__(parent)

        # État
        self._duration = 0.0  # Durée totale en secondes
        self._position = 0.0  # Position actuelle en secondes
        self._markers: Dict[float, str] = {}  # Position → Label

        # Configuration
        self.setMinimumHeight(80)
        self.setMaximumHeight(120)

        # Style
        self._bg_color = QColor("#2a2a2a")
        self._progress_color = QColor("#4a9eff")
        self._cursor_color = QColor("#ffffff")
        self._marker_color = QColor("#ffa500")
        self._text_color = QColor("#cccccc")

    def set_duration(self, duration: float) -> None:
        """
        Définit la durée totale de l'audio.

        Args:
            duration: Durée en secondes
        """
        self._duration = max(0.0, duration)
        self.update()

    def set_position(self, position: float) -> None:
        """
        Définit la position actuelle.

        Args:
            position: Position en secondes
        """
        self._position = max(0.0, min(position, self._duration))
        self.update()

    def add_marker(self, position: float, label: str) -> None:
        """
        Ajoute un marqueur à une position donnée.

        Args:
            position: Position du marqueur en secondes
            label: Libellé du marqueur
        """
        if 0 <= position <= self._duration:
            self._markers[position] = label
            self.update()

    def clear_markers(self) -> None:
        """Supprime tous les marqueurs."""
        self._markers.clear()
        self.update()

    def paintEvent(self, event):
        """Dessine la timeline."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # Fond
        painter.fillRect(0, 0, width, height, self._bg_color)

        # Barre de progression
        timeline_y = height // 2 - 10
        timeline_height = 20

        # Bordure
        painter.setPen(QPen(QColor("#555555"), 1))
        painter.drawRect(0, timeline_y, width - 1, timeline_height)

        if self._duration > 0:
            # Progression
            progress_width = int((self._position / self._duration) * width)
            painter.fillRect(1, timeline_y + 1, progress_width - 1, timeline_height - 1, self._progress_color)

            # Marqueurs
            for marker_pos, label in self._markers.items():
                x = int((marker_pos / self._duration) * width)
                painter.setPen(QPen(self._marker_color, 2))
                painter.drawLine(x, timeline_y, x, timeline_y + timeline_height)

            # Curseur de position
            cursor_x = int((self._position / self._duration) * width)
            painter.setPen(QPen(self._cursor_color, 3))
            painter.drawLine(cursor_x, timeline_y - 5, cursor_x, timeline_y + timeline_height + 5)

        # Affichage des temps
        painter.setFont(QFont("Arial", 10))
        painter.setPen(self._text_color)

        # Temps actuel (gauche)
        current_time_str = TimeUtils.seconds_to_timestamp(self._position)
        painter.drawText(5, timeline_y - 10, current_time_str)

        # Temps total (droite)
        total_time_str = TimeUtils.seconds_to_timestamp(self._duration)
        painter.drawText(width - 70, timeline_y - 10, total_time_str)

    def mousePressEvent(self, event: QMouseEvent):
        """Gère le clic sur la timeline."""
        if event.button() == Qt.LeftButton and self._duration > 0:
            # Calculer la nouvelle position
            x = event.pos().x()
            width = self.width()
            new_position = (x / width) * self._duration

            # Émettre le signal
            self.position_changed.emit(new_position)
