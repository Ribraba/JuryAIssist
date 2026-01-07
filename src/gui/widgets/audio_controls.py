"""
Widget de contrôles audio selon Phase 3.1.5 de la roadmap.

Fonctionnalités :
- Boutons : Play, Pause, Stop
- Boutons : Reculer 5s, Avancer 5s
- Slider de vitesse (0.5x à 2.0x)
- Affichage temps actuel / total
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
)

from src.gui.icons import Icons
from src.gui.styles import (
    get_primary_button_style,
    get_secondary_button_style,
    get_stop_button_style,
    get_icon_button_style,
)


class AudioControlsWidget(QWidget):
    """
    Widget de contrôles audio.

    Fournit tous les contrôles nécessaires pour la lecture audio.
    """

    # Signaux
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    skip_forward_clicked = pyqtSignal()
    skip_backward_clicked = pyqtSignal()
    speed_changed = pyqtSignal(float)  # Nouvelle vitesse
    volume_changed = pyqtSignal(int)  # Nouveau volume (0-100)

    def __init__(self, parent=None):
        """Initialise le widget."""
        super().__init__(parent)

        # État
        self._is_playing = False

        # Créer l'interface
        self._create_ui()

    def _create_ui(self):
        """Crée l'interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Contrôles principaux
        main_controls = self._create_main_controls()
        layout.addLayout(main_controls)

        # Contrôles secondaires (vitesse)
        speed_controls = self._create_speed_controls()
        layout.addLayout(speed_controls)

        # Contrôles de volume
        volume_controls = self._create_volume_controls()
        layout.addLayout(volume_controls)

    def _create_main_controls(self) -> QHBoxLayout:
        """Crée les contrôles principaux."""
        layout = QHBoxLayout()
        layout.setSpacing(12)

        layout.addStretch()

        # Reculer 5s
        self._skip_back_btn = QPushButton()
        self._skip_back_btn.setObjectName("icon_button")
        self._skip_back_btn.setStyleSheet(get_icon_button_style())
        self._skip_back_btn.setCursor(Qt.PointingHandCursor)
        self._skip_back_btn.setIcon(Icons.skip_back())
        self._skip_back_btn.setToolTip("Reculer de 5 secondes")
        self._skip_back_btn.clicked.connect(self.skip_backward_clicked.emit)
        self._skip_back_btn.setEnabled(False)
        layout.addWidget(self._skip_back_btn)

        # Play/Pause
        self._play_pause_btn = QPushButton()
        self._play_pause_btn.setObjectName("primary")
        self._play_pause_btn.setStyleSheet(get_primary_button_style())
        self._play_pause_btn.setCursor(Qt.PointingHandCursor)
        self._play_pause_btn.setIcon(Icons.play())
        self._play_pause_btn.setIconSize(self._play_pause_btn.size() * 0.4)
        self._play_pause_btn.clicked.connect(self._on_play_pause_clicked)
        self._play_pause_btn.setEnabled(False)
        layout.addWidget(self._play_pause_btn)

        # Stop
        self._stop_btn = QPushButton()
        self._stop_btn.setObjectName("stop")
        self._stop_btn.setStyleSheet(get_stop_button_style())
        self._stop_btn.setCursor(Qt.PointingHandCursor)
        self._stop_btn.setIcon(Icons.stop())
        self._stop_btn.clicked.connect(self.stop_clicked.emit)
        self._stop_btn.setEnabled(False)
        layout.addWidget(self._stop_btn)

        # Avancer 5s
        self._skip_forward_btn = QPushButton()
        self._skip_forward_btn.setObjectName("icon_button")
        self._skip_forward_btn.setStyleSheet(get_icon_button_style())
        self._skip_forward_btn.setCursor(Qt.PointingHandCursor)
        self._skip_forward_btn.setIcon(Icons.skip_forward())
        self._skip_forward_btn.setToolTip("Avancer de 5 secondes")
        self._skip_forward_btn.clicked.connect(self.skip_forward_clicked.emit)
        self._skip_forward_btn.setEnabled(False)
        layout.addWidget(self._skip_forward_btn)

        layout.addStretch()

        return layout

    def _create_speed_controls(self) -> QHBoxLayout:
        """Crée les contrôles de vitesse."""
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Label vitesse
        speed_label = QLabel("Vitesse:")
        speed_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        layout.addWidget(speed_label)

        # Slider de vitesse (0.5x à 2.0x)
        self._speed_slider = QSlider(Qt.Horizontal)
        self._speed_slider.setMinimum(5)  # 0.5x
        self._speed_slider.setMaximum(20)  # 2.0x
        self._speed_slider.setValue(10)  # 1.0x
        self._speed_slider.setTickPosition(QSlider.TicksBelow)
        self._speed_slider.setTickInterval(5)
        self._speed_slider.valueChanged.connect(self._on_speed_changed)
        self._speed_slider.setEnabled(False)
        layout.addWidget(self._speed_slider)

        # Affichage vitesse actuelle
        self._speed_label = QLabel("1.0x")
        self._speed_label.setStyleSheet("""
            QLabel {
                color: #4a9eff;
                font-size: 12px;
                font-weight: bold;
                min-width: 40px;
            }
        """)
        layout.addWidget(self._speed_label)

        return layout

    def _create_volume_controls(self) -> QHBoxLayout:
        """Crée les contrôles de volume."""
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Label volume
        volume_label = QLabel("Volume:")
        volume_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        layout.addWidget(volume_label)

        # Slider de volume (0 à 100)
        self._volume_slider = QSlider(Qt.Horizontal)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        self._volume_slider.setValue(100)  # Volume par défaut à 100%
        self._volume_slider.setTickPosition(QSlider.TicksBelow)
        self._volume_slider.setTickInterval(25)
        self._volume_slider.valueChanged.connect(self._on_volume_changed)
        self._volume_slider.setEnabled(False)
        layout.addWidget(self._volume_slider)

        # Affichage volume actuel
        self._volume_label = QLabel("100%")
        self._volume_label.setStyleSheet("""
            QLabel {
                color: #4a9eff;
                font-size: 12px;
                font-weight: bold;
                min-width: 40px;
            }
        """)
        layout.addWidget(self._volume_label)

        return layout

    def enable_controls(self, enabled: bool = True):
        """
        Active/désactive tous les contrôles.

        Args:
            enabled: True pour activer
        """
        self._play_pause_btn.setEnabled(enabled)
        self._stop_btn.setEnabled(enabled)
        self._skip_back_btn.setEnabled(enabled)
        self._skip_forward_btn.setEnabled(enabled)
        self._speed_slider.setEnabled(enabled)
        self._volume_slider.setEnabled(enabled)

    def set_playing_state(self, is_playing: bool):
        """
        Définit l'état de lecture (play/pause).

        Args:
            is_playing: True si en lecture
        """
        self._is_playing = is_playing
        if is_playing:
            self._play_pause_btn.setIcon(Icons.pause())
        else:
            self._play_pause_btn.setIcon(Icons.play())

    def _on_play_pause_clicked(self):
        """Appelé quand le bouton play/pause est cliqué."""
        # Désactiver temporairement le bouton pour éviter les clics multiples rapides
        self._play_pause_btn.setEnabled(False)

        if self._is_playing:
            self.pause_clicked.emit()
        else:
            self.play_clicked.emit()

        # Réactiver après un court délai
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(200, lambda: self._play_pause_btn.setEnabled(True))

    def _on_speed_changed(self, value: int):
        """Appelé quand le slider de vitesse change."""
        speed = value / 10.0  # Convertir en vitesse réelle
        self._speed_label.setText(f"{speed:.1f}x")
        self.speed_changed.emit(speed)

    def _on_volume_changed(self, value: int):
        """Appelé quand le slider de volume change."""
        self._volume_label.setText(f"{value}%")
        self.volume_changed.emit(value)
