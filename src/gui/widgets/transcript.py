"""
Panneau de transcription brute redesigné selon Figma.

Version lecture seule avec en-tête "Transcription brute" / "Lecture".

Principes SOLID:
- Single Responsibility: Affiche la transcription brute en lecture seule
- Open/Closed: Extensible via héritage
- Liskov Substitution: Compatible avec l'interface du panneau original
- Interface Segregation: Signaux minimaux et ciblés
- Dependency Inversion: Accepte des TranscriptionSegment abstraits
"""
from typing import List, Optional
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QFrame,
)
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor

from src.transcription.transcriber import TranscriptionSegment
from src.gui.resources import get_font
from src.gui.theme import AppSpacing, AppColors


class TranscriptPanel(QWidget):
    """
    Panneau de transcription brute selon le design Figma.

    Affiche:
    - En-tête avec "Transcription brute" et "Lecture"
    - Zone de texte lecture seule avec la transcription
    - Surlignage du segment actuel

    Signals:
        word_clicked: Émis quand un mot est cliqué (word, position)
    """

    word_clicked = pyqtSignal(str, int)

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialise le panneau.

        Args:
            parent: Widget parent
        """
        super().__init__(parent)

        # État
        self._segments: List[TranscriptionSegment] = []
        self._current_segment_index: Optional[int] = None

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(AppSpacing.MD)

        # En-tête
        self._create_header(main_layout)

        # Zone de transcription
        self._create_transcript_area(main_layout)

    def _create_header(self, layout: QVBoxLayout):
        """
        Crée l'en-tête avec titres.

        Args:
            layout: Layout parent
        """
        header_widget = QWidget()
        header_widget.setObjectName("sectionHeader")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(AppSpacing.MD, AppSpacing.MD, AppSpacing.MD, 0)
        header_layout.setSpacing(AppSpacing.SM)

        # Titre principal
        title_label = QLabel("Transcription brute")
        title_label.setObjectName("sectionTitle")
        title_label.setFont(get_font(34, 600))
        title_label.setStyleSheet(f"""
            color: {AppColors.TEXT_PRIMARY};
            letter-spacing: -0.68px;
        """)
        header_layout.addWidget(title_label)

        # Sous-titre
        subtitle_label = QLabel("Lecture")
        subtitle_label.setObjectName("sectionSubtitle")
        subtitle_label.setFont(get_font(16, 400))
        subtitle_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header_widget)

    def _create_transcript_area(self, layout: QVBoxLayout):
        """
        Crée la zone de transcription.

        Args:
            layout: Layout parent
        """
        # Zone de texte
        self._text_edit = QTextEdit()
        self._text_edit.setObjectName("transcriptPanel")
        self._text_edit.setReadOnly(True)
        self._text_edit.setFont(get_font(20, 500))
        self._text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {AppColors.BG_PRIMARY};
                border: none;
                color: {AppColors.TEXT_PRIMARY};
                letter-spacing: -0.4px;
                padding: {AppSpacing.MD}px;
            }}
        """)

        # Activer le curseur de souris pour les clics
        self._text_edit.viewport().setCursor(Qt.PointingHandCursor)
        self._text_edit.mousePressEvent = self._on_text_clicked

        layout.addWidget(self._text_edit, 1)

    def set_transcript_segments(self, segments: List[TranscriptionSegment]):
        """
        Définit les segments de transcription.

        Args:
            segments: Liste des segments
        """
        self._segments = segments

        # Construire le texte complet
        text_parts = []
        for seg in segments:
            text_parts.append(seg.text)

        full_text = "\n\n".join(text_parts)
        self._text_edit.setPlainText(full_text)

    def highlight_segment_at_time(self, time: float):
        """
        Surligne le segment correspondant au temps donné.

        Args:
            time: Temps en secondes
        """
        if not self._segments:
            return

        # Trouver le segment actuel
        segment_index = None
        for i, seg in enumerate(self._segments):
            if seg.start <= time <= seg.end:
                segment_index = i
                break

        # Si pas de changement, ne rien faire
        if segment_index == self._current_segment_index:
            return

        self._current_segment_index = segment_index

        # Effacer le surlignage précédent
        cursor = self._text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(AppColors.BG_PRIMARY))
        cursor.setCharFormat(fmt)

        # Surligner le nouveau segment
        if segment_index is not None:
            # Calculer la position du segment dans le texte
            text_position = 0
            for i in range(segment_index):
                text_position += len(self._segments[i].text) + 2  # +2 pour \n\n

            # Sélectionner et surligner
            cursor = self._text_edit.textCursor()
            cursor.setPosition(text_position)
            cursor.setPosition(text_position + len(self._segments[segment_index].text), QTextCursor.KeepAnchor)

            # Appliquer le surlignage
            fmt = QTextCharFormat()
            fmt.setBackground(QColor("#fffacd"))  # Jaune clair
            cursor.setCharFormat(fmt)

            # Scroller vers le segment
            self._text_edit.setTextCursor(cursor)
            self._text_edit.ensureCursorVisible()

    def _on_text_clicked(self, event):
        """
        Gère le clic sur le texte.

        Args:
            event: QMouseEvent
        """
        # Obtenir la position du clic
        cursor = self._text_edit.cursorForPosition(event.pos())
        position = cursor.position()

        # Sélectionner le mot
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText()

        if word.strip():
            # Émettre le signal
            self.word_clicked.emit(word, position)

    def clear(self):
        """Efface la transcription."""
        self._text_edit.clear()
        self._segments = []
        self._current_segment_index = None
