"""
Dialog "À propos" de l'application.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class AboutDialog(QDialog):
    """Dialog "À propos" avec informations sur l'application."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface."""
        self.setWindowTitle("À propos de JuryAIssist")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Titre
        title = QLabel("<h2>JuryAIssist</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description
        description = QLabel(
            "<p>Application d'assistance à la transcription et à l'édition "
            "d'enregistrements audio pour juristes.</p>"
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        # Informations
        info = QLabel(
            "<p><b>Version:</b> 2.0</p>"
            "<p><b>Interface:</b> Moderne et intuitive</p>"
            "<p>Développé avec PyQt5 et les principes SOLID</p>"
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        layout.addStretch()

        # Bouton OK
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)
