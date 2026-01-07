"""
Panneau d'édition selon Phase 3.1.3 de la roadmap.

Fonctionnalités :
- QTextEdit modifiable
- Sauvegarde auto toutes les 30 secondes
- Clic sur un mot → signal avec le mot cliqué
- Coloration syntaxique des timestamps (optionnel)
"""

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class EditorPanel(QWidget):
    """
    Panneau d'édition de texte modifiable.

    Permet d'éditer la transcription avec sauvegarde auto.
    """

    # Signaux
    text_changed = pyqtSignal(str)  # Texte modifié

    def __init__(self, parent=None):
        """Initialise le panneau."""
        super().__init__(parent)

        # État
        self._last_saved_text = ""
        self._autosave_enabled = False

        # Créer l'interface
        self._create_ui()

        # Timer pour sauvegarde automatique (30 secondes)
        self._autosave_timer = QTimer()
        self._autosave_timer.timeout.connect(self._autosave)
        self._autosave_timer.setInterval(30000)  # 30 secondes

    def _create_ui(self):
        """Crée l'interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Label
        label = QLabel("ÉDITEUR")
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

        # Zone de texte modifiable - Style moderne doux
        self._text_edit = QTextEdit()
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
            QTextEdit:focus {
                border: 1px solid #0A84FF;
            }
        """)
        self._text_edit.textChanged.connect(self._on_text_changed)
        layout.addWidget(self._text_edit)

    def set_text(self, text: str) -> None:
        """
        Définit le texte de l'éditeur.

        Args:
            text: Texte à afficher
        """
        self._text_edit.setPlainText(text)
        self._last_saved_text = text

    def get_text(self) -> str:
        """
        Récupère le texte de l'éditeur.

        Returns:
            Texte actuel
        """
        return self._text_edit.toPlainText()

    def highlight_word(self, word: str) -> None:
        """
        Surligne un mot dans le texte.

        Args:
            word: Mot à surligner
        """
        # Rechercher et surligner le mot
        cursor = self._text_edit.textCursor()
        self._text_edit.find(word)

    def enable_autosave(self, enabled: bool = True) -> None:
        """
        Active/désactive la sauvegarde automatique.

        Args:
            enabled: True pour activer
        """
        self._autosave_enabled = enabled
        if enabled:
            self._autosave_timer.start()
        else:
            self._autosave_timer.stop()

    def _on_text_changed(self):
        """Appelé quand le texte change."""
        current_text = self.get_text()
        if current_text != self._last_saved_text:
            self.text_changed.emit(current_text)

    def _autosave(self):
        """Sauvegarde automatique."""
        if self._autosave_enabled:
            current_text = self.get_text()
            if current_text != self._last_saved_text:
                self._last_saved_text = current_text
                # Note: La sauvegarde réelle serait gérée par le parent
                # qui écouterait le signal text_changed
