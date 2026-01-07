"""
Widget de timeline avec transcription défilante et opacité progressive.

Ce widget affiche le texte de la transcription horizontalement au-dessus de la timeline,
avec un effet d'opacité progressive : 100% pour le mot actuel, dégradé pour avant/après.

Principes SOLID:
- Single Responsibility: Affiche la transcription avec timeline et gère la synchronisation
- Open/Closed: Extensible via configuration des couleurs et opacités
- Liskov Substitution: Hérite proprement de QWidget
- Interface Segregation: Expose uniquement les méthodes nécessaires
- Dependency Inversion: Accepte les données via interface abstraite
- Tell, Don't Ask: Commande l'affichage plutôt que d'exposer l'état interne
"""
from typing import List, Optional
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QFontMetrics
from PyQt5.QtWidgets import QWidget

from src.transcription.transcriber import TranscriptionSegment
from src.gui.theme import AppColors
from src.gui.resources import get_font


class ScrollingTranscriptTimeline(QWidget):
    """
    Timeline avec transcription défilante et opacité progressive.

    La transcription défile horizontalement au-dessus de la timeline.
    Le mot correspondant à la position actuelle a une opacité de 100%,
    les mots avant et après ont une opacité dégradée.

    Signals:
        position_clicked: Émis quand l'utilisateur clique sur la timeline (position en secondes)
        word_clicked: Émis quand l'utilisateur clique sur un mot (mot, position en secondes)
    """

    position_clicked = pyqtSignal(float)
    word_clicked = pyqtSignal(str, float)

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialise le widget.

        Args:
            parent: Widget parent
        """
        super().__init__(parent)

        # Configuration
        self._duration = 0.0
        self._position = 0.0
        self._segments: List[TranscriptionSegment] = []

        # Style
        self._timeline_height = 40
        self._text_height = 30
        self._total_height = self._timeline_height + self._text_height

        # Opacité
        self._opacity_max = 1.0  # Mot actuel
        self._opacity_min = 0.2  # Mots lointains
        self._opacity_fade_distance = 5  # Nombre de mots pour le dégradé

        # Couleurs
        self._bg_color = QColor(AppColors.BG_TIMELINE)
        self._progress_color = QColor("#000000")  # Noir au lieu de bleu
        self._text_color = QColor(AppColors.TEXT_PRIMARY)

        # Police
        self._font = get_font(20, 500)

        # Taille minimale
        self.setMinimumHeight(self._total_height)
        self.setMaximumHeight(self._total_height)

        # Curseur
        self.setCursor(Qt.PointingHandCursor)

    def set_duration(self, duration: float):
        """
        Définit la durée totale.

        Args:
            duration: Durée en secondes
        """
        self._duration = max(0.0, duration)
        self.update()

    def set_position(self, position: float):
        """
        Définit la position actuelle.

        Args:
            position: Position en secondes
        """
        self._position = max(0.0, min(position, self._duration))
        self.update()

    def set_transcript_segments(self, segments: List[TranscriptionSegment]):
        """
        Définit les segments de transcription.

        Args:
            segments: Liste des segments
        """
        self._segments = segments
        self.update()

    def paintEvent(self, event):
        """Dessine le widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        # 1. Dessiner la timeline (en bas)
        self._draw_timeline(painter, 0, self._text_height, width, self._timeline_height)

        # 2. Dessiner le texte défilant (en haut)
        self._draw_scrolling_text(painter, 0, 0, width, self._text_height)

    def _draw_timeline(self, painter: QPainter, x: int, y: int, width: int, height: int):
        """
        Dessine la barre de timeline.

        Args:
            painter: QPainter
            x, y: Position
            width, height: Dimensions
        """
        # Background
        painter.setBrush(self._bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(x, y, width, height, 4, 4)

        # Progress
        if self._duration > 0:
            progress_width = int(width * (self._position / self._duration))
            painter.setBrush(self._progress_color)
            painter.drawRoundedRect(x, y, progress_width, height, 4, 4)

        # Curseur (handle)
        if self._duration > 0:
            handle_x = int(width * (self._position / self._duration))
            handle_radius = 8
            painter.setBrush(self._progress_color)
            painter.drawEllipse(
                handle_x - handle_radius,
                y + (height // 2) - handle_radius,
                handle_radius * 2,
                handle_radius * 2
            )

    def _draw_scrolling_text(self, painter: QPainter, x: int, y: int, width: int, height: int):
        """
        Dessine le texte défilant avec opacité progressive.

        Args:
            painter: QPainter
            x, y: Position
            width, height: Dimensions
        """
        if not self._segments or self._duration == 0:
            return

        painter.setFont(self._font)

        # Trouver le segment et le mot actuel
        current_word_index = self._find_current_word_index()

        if current_word_index is None:
            return

        # Extraire tous les mots de tous les segments
        all_words = []
        for seg in self._segments:
            words = seg.text.split()
            all_words.extend(words)

        if not all_words:
            return

        # Centre du widget (où le mot actuel sera affiché)
        center_x = width // 2

        # Calculer la position de départ pour que le mot actuel soit centré
        metrics = QFontMetrics(self._font)
        word_spacing = 12  # Espacement entre les mots

        # Position x de départ
        x_offset = center_x

        # Calculer l'offset pour centrer le mot actuel
        for i in range(current_word_index):
            word_width = metrics.horizontalAdvance(all_words[i])
            x_offset -= (word_width + word_spacing)

        # Dessiner les mots avec opacité progressive
        current_x = x_offset

        for i, word in enumerate(all_words):
            word_width = metrics.horizontalAdvance(word)

            # Calculer l'opacité basée sur la distance au mot actuel
            distance = abs(i - current_word_index)
            opacity = self._calculate_opacity(distance)

            # Ne dessiner que si visible et dans les limites du widget
            if current_x + word_width > 0 and current_x < width and opacity > 0:
                color = QColor(self._text_color)
                color.setAlphaF(opacity)
                painter.setPen(color)

                # Dessiner le mot
                painter.drawText(
                    int(current_x),
                    int(y + height // 2 + metrics.ascent() // 2),
                    word
                )

            current_x += word_width + word_spacing

    def _find_current_word_index(self) -> Optional[int]:
        """
        Trouve l'index du mot correspondant à la position actuelle.

        Returns:
            Index du mot, ou None si non trouvé
        """
        if not self._segments:
            return None

        # Trouver le segment actuel
        current_segment_idx = None
        for i, seg in enumerate(self._segments):
            if seg.start <= self._position <= seg.end:
                current_segment_idx = i
                break

        if current_segment_idx is None:
            # Si pas de segment exact, prendre le plus proche
            for i, seg in enumerate(self._segments):
                if seg.start > self._position:
                    current_segment_idx = max(0, i - 1)
                    break
            if current_segment_idx is None:
                current_segment_idx = len(self._segments) - 1

        # Compter les mots avant ce segment
        word_index = 0
        for i in range(current_segment_idx):
            word_index += len(self._segments[i].text.split())

        # Ajouter une estimation dans le segment actuel
        # (On pourrait utiliser word-level timestamps si disponibles)
        seg = self._segments[current_segment_idx]
        words_in_seg = seg.text.split()
        if len(words_in_seg) > 0:
            seg_duration = seg.end - seg.start
            if seg_duration > 0:
                progress_in_seg = (self._position - seg.start) / seg_duration
                word_in_seg = int(progress_in_seg * len(words_in_seg))
                word_index += min(word_in_seg, len(words_in_seg) - 1)

        return word_index

    def _calculate_opacity(self, distance: int) -> float:
        """
        Calcule l'opacité basée sur la distance au mot actuel.

        Args:
            distance: Distance en nombre de mots

        Returns:
            Opacité (0.0 à 1.0)
        """
        if distance == 0:
            return self._opacity_max

        if distance >= self._opacity_fade_distance:
            return self._opacity_min

        # Interpolation linéaire
        ratio = distance / self._opacity_fade_distance
        return self._opacity_max - (self._opacity_max - self._opacity_min) * ratio

    def mousePressEvent(self, event):
        """Gère le clic sur la timeline et sur les mots."""
        if event.button() == Qt.LeftButton and self._duration > 0:
            click_y = event.pos().y()
            click_x = event.pos().x()

            # Clic dans la zone de texte (haut)
            if click_y < self._text_height and self._segments:
                # Trouver le mot cliqué en calculant sa position dans le défilement
                widget_width = self.width()
                widget_center_x = widget_width / 2

                # Décalage du défilement basé sur la position actuelle
                scroll_offset = self._position * self._pixels_per_second

                # Parcourir tous les segments pour trouver celui qui est sous la souris
                for seg in self._segments:
                    # Position du segment sur la timeline
                    seg_time_position = (seg.start + seg.end) / 2
                    seg_x_position = seg_time_position * self._pixels_per_second

                    # Position visible du segment dans le widget
                    seg_visible_x = widget_center_x + (seg_x_position - scroll_offset)

                    # Calculer la largeur approximative du texte (basé sur la longueur)
                    text_width = len(seg.text) * 8  # Approximation: 8px par caractère

                    # Vérifier si le clic est sur ce segment
                    if abs(seg_visible_x - click_x) < text_width / 2:
                        self.word_clicked.emit(seg.text, seg.start)
                        return

            # Clic dans la zone de la timeline (bas)
            elif click_y >= self._text_height:
                position_ratio = click_x / self.width()
                new_position = position_ratio * self._duration
                self.position_clicked.emit(new_position)

    def sizeHint(self):
        """Retourne la taille suggérée."""
        from PyQt5.QtCore import QSize
        return QSize(800, self._total_height)
