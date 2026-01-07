"""
Fenêtre principale du lecteur audio.

Interface graphique moderne, sobre et responsive.
"""

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

from src.audio.controller import AudioController
from src.audio.player import PlayerState
from src.audio.timeline import TimeUtils
from src.audio.vlc_player import VLCAudioPlayer
from src.gui.icons import Icons
from src.gui.styles import (
    get_app_style,
    get_card_style,
    get_file_info_style,
    get_icon_button_style,
    get_load_button_style,
    get_primary_button_style,
    get_secondary_button_style,
    get_slider_style,
    get_speed_badge_style,
    get_stop_button_style,
    get_time_label_style,
    get_title_style,
)


class AudioPlayerWindow(QMainWindow):
    """
    Fenêtre principale du lecteur audio.

    Interface minimaliste, moderne et responsive.
    """

    def __init__(self, controller: AudioController = None):
        """
        Initialise la fenêtre.

        Args:
            controller: Controller audio à utiliser (optionnel).
                       Si None, crée son propre controller.
                       Principe SOLID-D : Injection de dépendances.
        """
        super().__init__()

        # Injection de dépendances (SOLID-D)
        if controller is None:
            # Mode standalone : créer notre propre player et controller
            self._player = VLCAudioPlayer()
            self._controller = AudioController(self._player)
            self._owns_controller = True
        else:
            # Mode intégré : utiliser le controller fourni
            self._controller = controller
            self._player = controller._player
            self._owns_controller = False

        # État
        self._is_seeking = False

        # Configuration de la fenêtre
        self.setWindowTitle("JuryAIssist")
        self.setMinimumSize(700, 500)
        self.resize(800, 600)

        # Appliquer le style global
        self.setStyleSheet(get_app_style())

        # Créer l'interface
        self._create_ui()

        # Connecter les signaux
        self._connect_signals()

    def _create_ui(self):
        """Crée l'interface utilisateur."""
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        # Layout principal avec marges généreuses
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(32)

        # Titre
        title = QLabel("Lecteur Audio")
        title.setObjectName("title")
        title.setStyleSheet(get_title_style())
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Card principale
        card = self._create_card()
        main_layout.addWidget(card, 1)  # Prend tout l'espace disponible

    def _create_card(self) -> QFrame:
        """Crée la carte principale."""
        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(get_card_style())

        layout = QVBoxLayout(card)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(32)

        # Bouton de chargement
        load_btn = QPushButton("Ouvrir un fichier")
        load_btn.setObjectName("load")
        load_btn.setStyleSheet(get_load_button_style())
        load_btn.setCursor(Qt.PointingHandCursor)
        load_btn.clicked.connect(self._load_file)
        load_btn.setIcon(Icons.folder())
        layout.addWidget(load_btn)

        # Info fichier
        self._file_label = QLabel("Aucun fichier chargé")
        self._file_label.setObjectName("file_info")
        self._file_label.setStyleSheet(get_file_info_style())
        self._file_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._file_label)

        # Spacer
        layout.addSpacing(24)

        # Timeline
        timeline = self._create_timeline()
        layout.addLayout(timeline)

        # Spacer
        layout.addSpacing(16)

        # Contrôles principaux
        controls = self._create_main_controls()
        layout.addLayout(controls)

        # Spacer
        layout.addSpacing(16)

        # Contrôles secondaires
        secondary = self._create_secondary_controls()
        layout.addLayout(secondary)

        # Stretch en bas
        layout.addStretch()

        return card

    def _create_timeline(self) -> QVBoxLayout:
        """Crée la section timeline."""
        layout = QVBoxLayout()
        layout.setSpacing(16)

        # Slider
        self._slider = QSlider(Qt.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(1000)
        self._slider.setValue(0)
        self._slider.setStyleSheet(get_slider_style())
        self._slider.setCursor(Qt.PointingHandCursor)
        self._slider.sliderPressed.connect(self._on_slider_pressed)
        self._slider.sliderReleased.connect(self._on_slider_released)
        self._slider.valueChanged.connect(self._on_slider_moved)
        layout.addWidget(self._slider)

        # Labels de temps
        time_layout = QHBoxLayout()
        time_layout.setSpacing(0)

        self._current_time = QLabel("00:00")
        self._current_time.setObjectName("time")
        self._current_time.setStyleSheet(get_time_label_style())
        time_layout.addWidget(self._current_time)

        time_layout.addStretch()

        self._duration = QLabel("00:00")
        self._duration.setObjectName("time")
        self._duration.setStyleSheet(get_time_label_style())
        time_layout.addWidget(self._duration)

        layout.addLayout(time_layout)

        return layout

    def _create_main_controls(self) -> QHBoxLayout:
        """Crée les contrôles principaux."""
        layout = QHBoxLayout()
        layout.setSpacing(24)

        layout.addStretch()

        # Play/Pause
        self._play_btn = QPushButton()
        self._play_btn.setObjectName("primary")
        self._play_btn.setStyleSheet(get_primary_button_style())
        self._play_btn.setCursor(Qt.PointingHandCursor)
        self._play_btn.setIcon(Icons.play())
        self._play_btn.setIconSize(self._play_btn.size() * 0.4)
        self._play_btn.clicked.connect(self._toggle_play_pause)
        self._play_btn.setEnabled(False)
        layout.addWidget(self._play_btn)

        # Stop
        self._stop_btn = QPushButton()
        self._stop_btn.setObjectName("stop")
        self._stop_btn.setStyleSheet(get_stop_button_style())
        self._stop_btn.setCursor(Qt.PointingHandCursor)
        self._stop_btn.setIcon(Icons.stop())
        self._stop_btn.clicked.connect(self._stop)
        self._stop_btn.setEnabled(False)
        layout.addWidget(self._stop_btn)

        layout.addStretch()

        return layout

    def _create_secondary_controls(self) -> QHBoxLayout:
        """Crée les contrôles secondaires."""
        layout = QHBoxLayout()
        layout.setSpacing(16)

        # Skip backward
        self._skip_back_btn = QPushButton()
        self._skip_back_btn.setObjectName("icon_button")
        self._skip_back_btn.setStyleSheet(get_icon_button_style())
        self._skip_back_btn.setCursor(Qt.PointingHandCursor)
        self._skip_back_btn.setIcon(Icons.skip_back())
        self._skip_back_btn.setToolTip("Reculer de 5 secondes")
        self._skip_back_btn.clicked.connect(self._skip_backward)
        self._skip_back_btn.setEnabled(False)
        layout.addWidget(self._skip_back_btn)

        layout.addStretch()

        # Vitesse
        speed_layout = QHBoxLayout()
        speed_layout.setSpacing(12)

        self._speed_badge = QLabel("1.0x")
        self._speed_badge.setObjectName("speed_badge")
        self._speed_badge.setStyleSheet(get_speed_badge_style())
        self._speed_badge.setAlignment(Qt.AlignCenter)
        speed_layout.addWidget(self._speed_badge)

        self._speed_btn = QPushButton("Vitesse")
        self._speed_btn.setObjectName("secondary")
        self._speed_btn.setStyleSheet(get_secondary_button_style())
        self._speed_btn.setCursor(Qt.PointingHandCursor)
        self._speed_btn.setIcon(Icons.speed())
        self._speed_btn.clicked.connect(self._cycle_speed)
        self._speed_btn.setEnabled(False)
        speed_layout.addWidget(self._speed_btn)

        layout.addLayout(speed_layout)

        layout.addStretch()

        # Skip forward
        self._skip_forward_btn = QPushButton()
        self._skip_forward_btn.setObjectName("icon_button")
        self._skip_forward_btn.setStyleSheet(get_icon_button_style())
        self._skip_forward_btn.setCursor(Qt.PointingHandCursor)
        self._skip_forward_btn.setIcon(Icons.skip_forward())
        self._skip_forward_btn.setToolTip("Avancer de 5 secondes")
        self._skip_forward_btn.clicked.connect(self._skip_forward)
        self._skip_forward_btn.setEnabled(False)
        layout.addWidget(self._skip_forward_btn)

        return layout

    def _connect_signals(self):
        """Connecte les signaux du contrôleur."""
        self._controller.position_changed.connect(self._on_position_changed)
        self._controller.state_changed.connect(self._on_state_changed)
        self._controller.duration_changed.connect(self._on_duration_changed)
        self._controller.source_loaded.connect(self._on_source_loaded)
        self._controller.speed_changed.connect(self._on_speed_changed)
        self._controller.error_occurred.connect(self._on_error)

    # Slots UI

    def _load_file(self):
        """Charge un fichier audio."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un fichier audio",
            str(Path.home()),
            "Audio (*.mp3 *.wav *.m4a *.flac *.ogg *.dss);;Tous (*)",
        )

        if path:
            if self._controller.load_file(path):
                self._enable_controls()

    def _toggle_play_pause(self):
        """Bascule Play/Pause."""
        self._controller.toggle_play_pause()

    def _stop(self):
        """Arrête la lecture."""
        self._controller.stop()

    def _skip_backward(self):
        """Recule de 5s."""
        self._controller.skip_backward(5.0)

    def _skip_forward(self):
        """Avance de 5s."""
        self._controller.skip_forward(5.0)

    def _cycle_speed(self):
        """Change la vitesse."""
        self._controller.cycle_speed()

    def _enable_controls(self):
        """Active les contrôles."""
        self._play_btn.setEnabled(True)
        self._stop_btn.setEnabled(True)
        self._skip_back_btn.setEnabled(True)
        self._skip_forward_btn.setEnabled(True)
        self._speed_btn.setEnabled(True)

    # Slider

    def _on_slider_pressed(self):
        """Slider pressé."""
        self._is_seeking = True

    def _on_slider_released(self):
        """Slider relâché."""
        self._is_seeking = False
        duration = self._controller.get_duration()
        if duration > 0:
            pos = (self._slider.value() / 1000.0) * duration
            self._controller.seek(pos)

    def _on_slider_moved(self, value: int):
        """Slider bougé."""
        if self._is_seeking:
            duration = self._controller.get_duration()
            if duration > 0:
                pos = (value / 1000.0) * duration
                self._current_time.setText(TimeUtils.seconds_to_timestamp(pos))

    # Slots contrôleur

    def _on_position_changed(self, position: float):
        """Position changée."""
        self._current_time.setText(TimeUtils.seconds_to_timestamp(position))

        if not self._is_seeking:
            duration = self._controller.get_duration()
            if duration > 0:
                value = int((position / duration) * 1000)
                self._slider.setValue(value)

    def _on_state_changed(self, state: PlayerState):
        """État changé."""
        if state == PlayerState.PLAYING:
            self._play_btn.setIcon(Icons.pause())
        else:
            self._play_btn.setIcon(Icons.play())

    def _on_duration_changed(self, duration: float):
        """Durée changée."""
        self._duration.setText(TimeUtils.seconds_to_timestamp(duration))

    def _on_source_loaded(self, name: str):
        """Source chargée."""
        self._file_label.setText(name)

    def _on_speed_changed(self, speed: float):
        """Vitesse changée."""
        self._speed_badge.setText(f"{speed:.1f}x")

    def _on_error(self, message: str):
        """Erreur."""
        self._file_label.setText(f"Erreur: {message}")

    def closeEvent(self, event):
        """Fermeture."""
        # Libérer le controller seulement si on le possède
        if self._owns_controller:
            self._controller.release()
        event.accept()
