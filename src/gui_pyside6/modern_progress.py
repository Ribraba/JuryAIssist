"""
Dialogue de progression moderne pour JuryAIssist.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from .styles import COLORS


class ModernProgressDialog(QDialog):
    """Dialogue de progression moderne avec design épuré."""

    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(150)

        # Supprimer le bouton de fermeture
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Message
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 16px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(self.message_label)

        # Barre de progression moderne
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)  # Mode indéterminé
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['bg_timeline']};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['accent_primary']};
                border-radius: 2px;
            }}
        """)
        layout.addWidget(self.progress_bar)

        # Label de statut
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 13px;
            }}
        """)
        layout.addWidget(self.status_label)

        layout.addStretch()

        self.setLayout(layout)

        # Style du dialogue
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_primary']};
                border-radius: 12px;
            }}
        """)

    def set_message(self, message: str):
        """Met à jour le message."""
        self.message_label.setText(message)

    def set_status(self, status: str):
        """Met à jour le statut."""
        self.status_label.setText(status)

    def set_progress(self, value: int, maximum: int = 100):
        """
        Définit la progression.

        Args:
            value: Valeur actuelle (0-maximum)
            maximum: Valeur maximale
        """
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(value)

    def set_indeterminate(self, indeterminate: bool = True):
        """
        Active/désactive le mode indéterminé.

        Args:
            indeterminate: True pour mode indéterminé
        """
        if indeterminate:
            self.progress_bar.setMaximum(0)
            self.progress_bar.setMinimum(0)
        else:
            self.progress_bar.setMaximum(100)
            self.progress_bar.setMinimum(0)
