"""
Panneau de transcription brute selon Phase 3.1.4 de la roadmap.

Fonctionnalités :
- QTextEdit en lecture seule
- Scroll automatique vers segment actuel
- Surlignage du segment en cours de lecture
- Clic sur segment → retour à ce timestamp
"""

from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class TranscriptPanel(QWidget):
    """
    Panneau de transcription brute en lecture seule.

    Affiche la transcription avec surlignage du segment actuel.
    """

    # Signaux
    segment_clicked = pyqtSignal(float)  # Timestamp du segment
    word_clicked = pyqtSignal(str, int)  # Mot cliqué et position dans le texte

    def __init__(self, parent=None):
        """Initialise le panneau."""
        super().__init__(parent)

        # État
        self._segments = []  # Liste de tuples (start, end, text)
        self._current_segment_index = -1

        # Créer l'interface
        self._create_ui()

    def _create_ui(self):
        """Crée l'interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        label = QLabel("TRANSCRIPTION BRUTE")
        label.setObjectName("section_title")
        label.setStyleSheet("""
            QLabel {
                color: #AEAEB2;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                padding: 8px 12px;
            }
        """)
        layout.addWidget(label)

        # Zone de texte en lecture seule - Style moderne doux
        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setFont(QFont("-apple-system, SF Pro Text", 13))
        self._text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2C2C2E;
                color: #E5E5E7;
                border: 1px solid #38383A;
                border-radius: 8px;
                padding: 16px;
                line-height: 1.6;
                selection-background-color: #0A84FF;
                selection-color: white;
            }
        """)
        # Connecter au clic de souris pour la navigation mot-à-mot
        self._text_edit.mouseReleaseEvent = self._on_mouse_click
        layout.addWidget(self._text_edit)

    def set_transcript_text(self, text: str) -> None:
        """
        Définit le texte de la transcription.

        Args:
            text: Texte à afficher
        """
        self._text_edit.setPlainText(text)

    def set_transcript_segments(self, segments):
        """
        Définit les segments de la transcription.

        Args:
            segments: Liste de segments (objets avec start_time, end_time, text)
        """
        self._segments = segments

        # Construire le texte sans timestamps (selon demande utilisateur)
        text_lines = []
        for seg in segments:
            text_lines.append(seg.text)

        self._text_edit.setPlainText("\n\n".join(text_lines))

    def highlight_segment_at_time(self, time: float) -> None:
        """
        Surligne le segment correspondant au temps donné.

        Args:
            time: Temps en secondes
        """
        # Trouver le segment correspondant
        segment_index = -1
        for i, seg in enumerate(self._segments):
            if seg.start <= time < seg.end:
                segment_index = i
                break

        if segment_index != self._current_segment_index:
            self._current_segment_index = segment_index
            self._highlight_current_segment()

    def _highlight_current_segment(self):
        """Surligne le segment actuel."""
        if self._current_segment_index < 0 or self._current_segment_index >= len(self._segments):
            return

        # Réinitialiser le format
        cursor = self._text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        normal_format = QTextCharFormat()
        normal_format.setBackground(QColor("#2C2C2E"))
        cursor.setCharFormat(normal_format)

        # Calculer la position du segment dans le texte
        # Chaque segment est séparé par 2 lignes vides (sans timestamps)
        segment_start_pos = 0
        for i in range(self._current_segment_index):
            segment_text = self._segments[i].text
            segment_start_pos += len(segment_text) + 2  # +2 pour "\n\n"

        # Obtenir le texte du segment actuel
        current_seg = self._segments[self._current_segment_index]
        segment_text = current_seg.text

        # Surligner
        cursor.setPosition(segment_start_pos)
        cursor.setPosition(segment_start_pos + len(segment_text), QTextCursor.KeepAnchor)

        highlight_format = QTextCharFormat()
        highlight_format.setBackground(QColor("#3a3a3a"))
        cursor.setCharFormat(highlight_format)

        # Scroll vers le segment
        self._text_edit.setTextCursor(cursor)
        self._text_edit.ensureCursorVisible()

    def _on_mouse_click(self, event):
        """Appelé quand l'utilisateur clique dans le texte."""
        # Laisser le QTextEdit gérer l'événement normalement
        from PyQt5.QtWidgets import QTextEdit
        QTextEdit.mouseReleaseEvent(self._text_edit, event)

        # Récupérer le mot sous le curseur
        cursor = self._text_edit.textCursor()

        # Sélectionner le mot sous le curseur
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText()

        # Obtenir la position de début du mot sélectionné
        word_start_position = cursor.selectionStart()

        if word:
            # Émettre le mot et sa position pour synchronisation
            self.word_clicked.emit(word, word_start_position)

    def _format_timestamp(self, seconds: float) -> str:
        """
        Formate un timestamp.

        Args:
            seconds: Temps en secondes

        Returns:
            Timestamp formaté (MM:SS)
        """
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
