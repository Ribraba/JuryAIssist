"""
Panneau d'édition redesigné selon Figma.

Version éditable avec en-tête affichant le nom du fichier et "Édition".

Principes SOLID:
- Single Responsibility: Gère l'édition de la transcription
- Open/Closed: Extensible via héritage
- Interface Segregation: Méthodes minimales et ciblées
"""
from typing import Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from src.gui.figma_resources import get_font
from src.gui.figma_styles import FigmaSpacing, FigmaColors


class FigmaEditorPanel(QWidget):
    """
    Panneau d'édition selon le design Figma.

    Affiche:
    - En-tête avec nom du fichier et "Édition"
    - Zone de texte éditable
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialise le panneau.

        Args:
            parent: Widget parent
        """
        super().__init__(parent)

        # État
        self._filename = "Insérer un nouveau fichier audio"

        # Ajouter une ombre portée (comme dans Figma)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40))  # Ombre légère
        self.setGraphicsEffect(shadow)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(FigmaSpacing.MD)

        # En-tête
        self._create_header(main_layout)

        # Zone d'édition
        self._create_editor_area(main_layout)

    def _create_header(self, layout: QVBoxLayout):
        """
        Crée l'en-tête avec titres.

        Args:
            layout: Layout parent
        """
        header_widget = QWidget()
        header_widget.setObjectName("sectionHeader")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(FigmaSpacing.MD, FigmaSpacing.MD, FigmaSpacing.MD, 0)
        header_layout.setSpacing(FigmaSpacing.SM)

        # Titre principal (nom du fichier)
        self._title_label = QLabel(self._filename)
        self._title_label.setObjectName("sectionTitle")
        self._title_label.setFont(get_font(34, 600))
        self._title_label.setStyleSheet(f"""
            color: {FigmaColors.TEXT_PRIMARY};
            letter-spacing: -0.68px;
        """)
        header_layout.addWidget(self._title_label)

        # Sous-titre
        subtitle_label = QLabel("Édition")
        subtitle_label.setObjectName("sectionSubtitle")
        subtitle_label.setFont(get_font(16, 400))
        subtitle_label.setStyleSheet(f"color: {FigmaColors.TEXT_SECONDARY};")
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header_widget)

    def _create_editor_area(self, layout: QVBoxLayout):
        """
        Crée la zone d'édition.

        Args:
            layout: Layout parent
        """
        # Zone de texte éditable
        self._text_edit = QTextEdit()
        self._text_edit.setObjectName("editorPanel")
        self._text_edit.setFont(get_font(24, 500))
        self._text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {FigmaColors.BG_PRIMARY};
                border: none;
                color: {FigmaColors.TEXT_PRIMARY};
                letter-spacing: -0.48px;
                padding: {FigmaSpacing.MD}px;
            }}
        """)

        layout.addWidget(self._text_edit, 1)

    def set_text(self, text: str):
        """
        Définit le texte de l'éditeur.

        Args:
            text: Texte à afficher
        """
        self._text_edit.setPlainText(text)

    def get_text(self) -> str:
        """
        Retourne le texte de l'éditeur.

        Returns:
            Texte édité
        """
        return self._text_edit.toPlainText()

    def set_filename(self, filename: str):
        """
        Définit le nom du fichier affiché dans l'en-tête.

        Args:
            filename: Nom du fichier
        """
        self._filename = filename
        self._title_label.setText(filename)

    def clear(self):
        """Efface le contenu de l'éditeur."""
        self._text_edit.clear()
