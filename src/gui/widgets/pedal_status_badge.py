"""
Widget de badge de statut de pédale selon le design Figma.

Affiche l'état de connexion de la pédale avec une icône et un texte.

Principes SOLID:
- Single Responsibility: Affiche uniquement le statut de la pédale
- Open/Closed: Extensible via configuration des couleurs
- Tell, Don't Ask: Commande l'affichage plutôt que d'exposer l'état
"""
from typing import Optional
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from src.gui.resources import get_icon, get_font
from src.gui.theme import AppSpacing


class PedalStatusBadge(QWidget):
    """
    Badge affichant le statut de connexion de la pédale.

    Design Figma:
    - Icône de pédale
    - Texte "Pédale connectée (RS-31)" ou "Pédale déconnectée"
    - Couleur verte si connectée, grise sinon
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialise le badge.

        Args:
            parent: Widget parent
        """
        super().__init__(parent)

        self.setObjectName("pedalBadge")

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            AppSpacing.SM,
            AppSpacing.XS,
            AppSpacing.SM,
            AppSpacing.XS
        )
        layout.setSpacing(AppSpacing.XS)

        # Icône
        self._icon_label = QLabel()
        icon = get_icon("pedale")
        if not icon.isNull():
            # Redimensionner l'icône à une taille appropriée
            self._icon_label.setPixmap(icon.pixmap(QSize(16, 16)))
        layout.addWidget(self._icon_label)

        # Texte
        self._text_label = QLabel()
        self._text_label.setObjectName("pedalBadgeText")
        self._text_label.setFont(get_font(11, 400))
        layout.addWidget(self._text_label)

        # État initial: déconnecté
        self.set_connected(False, "RS-31")

    def set_connected(self, connected: bool, pedal_model: str = ""):
        """
        Définit l'état de connexion de la pédale.

        Args:
            connected: True si connectée
            pedal_model: Modèle de la pédale (ex: "RS-31")
        """
        if connected:
            text = f"Pédale connectée ({pedal_model})" if pedal_model else "Pédale connectée"
            self._text_label.setText(text)
            self.setStyleSheet("""
                #pedalBadge {
                    background-color: rgba(48, 209, 88, 0.15);
                    border-radius: 6px;
                }
                #pedalBadgeText {
                    color: #30D158;
                    font-size: 11px;
                    font-weight: 400;
                }
            """)
        else:
            self._text_label.setText("Pédale déconnectée")
            self.setStyleSheet("""
                #pedalBadge {
                    background-color: transparent;
                    border-radius: 6px;
                }
                #pedalBadgeText {
                    color: #8E8E93;
                    font-size: 11px;
                    font-weight: 400;
                }
            """)
