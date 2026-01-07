"""
Panneau de contrôles audio de l'application.

Layout:
- Bouton Play/Pause (grand, circulaire) en HAUT
- Boutons Skip backward, Stop, Skip forward en BAS (horizontalement alignés)
- Volume, temps et vitesse à droite

Principes SOLID:
- Single Responsibility: Gère uniquement les contrôles audio
- Interface Segregation: Signaux ciblés pour chaque action
- Dependency Inversion: Ne dépend pas d'implémentations concrètes
- Tell, Don't Ask: Commande les actions via signaux
"""
from typing import Optional
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
)
from PyQt5.QtGui import QIcon

from src.gui.resources import get_icon, get_font
from src.gui.theme import AppSpacing, AppColors


class AudioControlsPanel(QWidget):
    """
    Contrôles audio selon le design Figma.

    Signals:
        play_clicked: Émis quand Play est cliqué
        pause_clicked: Émis quand Pause est cliqué
        stop_clicked: Émis quand Stop est cliqué
        skip_forward_clicked: Émis quand Skip forward est cliqué
        skip_backward_clicked: Émis quand Skip backward est cliqué
        volume_changed: Émis quand le volume change (0-100)
        speed_changed: Émis quand la vitesse change (0.5-2.0)
    """

    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    skip_forward_clicked = pyqtSignal()
    skip_backward_clicked = pyqtSignal()
    volume_changed = pyqtSignal(int)
    speed_changed = pyqtSignal(float)

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialise les contrôles.

        Args:
            parent: Widget parent
        """
        super().__init__(parent)

        # État
        self._is_playing = False
        self._current_speed = 1.0

        # Layout principal (horizontal)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(AppSpacing.MD, AppSpacing.SM, AppSpacing.MD, AppSpacing.SM)
        main_layout.setSpacing(AppSpacing.LG)

        # 1. Boutons de contrôle (gauche) - Layout vertical
        self._create_control_buttons(main_layout)

        # Spacer
        main_layout.addStretch()

        # 2. Volume control (centre-gauche)
        self._create_volume_control(main_layout)

        # Spacer
        main_layout.addSpacing(AppSpacing.LG)

        # 3. Temps (centre)
        self._create_time_display(main_layout)

        # Spacer
        main_layout.addSpacing(AppSpacing.LG)

        # 4. Vitesse (droite)
        self._create_speed_control(main_layout)

    def _create_control_buttons(self, layout: QHBoxLayout):
        """
        Crée les boutons de contrôle selon le design Figma.

        Layout vertical:
        - Play/Pause en haut (grand)
        - Skip backward, Stop, Skip forward en bas (petit, horizontaux)

        Args:
            layout: Layout parent
        """
        # Container vertical pour tous les boutons
        buttons_container = QWidget()
        buttons_layout = QVBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(AppSpacing.XS)

        # Ligne 1: Bouton Play/Pause (grand, centré)
        play_pause_container = QWidget()
        play_pause_layout = QHBoxLayout(play_pause_container)
        play_pause_layout.setContentsMargins(0, 0, 0, 0)
        play_pause_layout.addStretch()

        self._play_pause_btn = QPushButton()
        self._play_pause_btn.setObjectName("playButton")
        self._play_pause_btn.setFixedSize(51, 51)
        self._play_pause_btn.setCursor(Qt.PointingHandCursor)
        self._play_pause_btn.clicked.connect(self._on_play_pause_clicked)
        self._update_play_pause_icon()
        play_pause_layout.addWidget(self._play_pause_btn)

        play_pause_layout.addStretch()
        buttons_layout.addWidget(play_pause_container)

        # Ligne 2: Skip backward, Stop, Skip forward (petits, horizontaux)
        small_buttons_container = QWidget()
        small_buttons_layout = QHBoxLayout(small_buttons_container)
        small_buttons_layout.setContentsMargins(0, 0, 0, 0)
        small_buttons_layout.setSpacing(AppSpacing.XS)

        # Skip backward
        self._skip_back_btn = self._create_icon_button("skip_backward", 16)
        self._skip_back_btn.clicked.connect(self.skip_backward_clicked.emit)
        small_buttons_layout.addWidget(self._skip_back_btn)

        # Stop
        self._stop_btn = self._create_icon_button("stop", 16)
        self._stop_btn.clicked.connect(self.stop_clicked.emit)
        small_buttons_layout.addWidget(self._stop_btn)

        # Skip forward
        self._skip_forward_btn = self._create_icon_button("skip_forward", 16)
        self._skip_forward_btn.clicked.connect(self.skip_forward_clicked.emit)
        small_buttons_layout.addWidget(self._skip_forward_btn)

        buttons_layout.addWidget(small_buttons_container)

        layout.addWidget(buttons_container)

    def _create_icon_button(self, icon_name: str, size: int) -> QPushButton:
        """
        Crée un bouton avec icône.

        Args:
            icon_name: Nom de l'icône
            size: Taille de l'icône

        Returns:
            QPushButton configuré
        """
        btn = QPushButton()
        btn.setObjectName("controlButton")
        btn.setFlat(True)
        btn.setCursor(Qt.PointingHandCursor)

        icon = get_icon(icon_name)
        if not icon.isNull():
            btn.setIcon(icon)
            btn.setIconSize(QSize(size, size))

        btn.setFixedSize(32, 32)

        return btn

    def _create_volume_control(self, layout: QHBoxLayout):
        """
        Crée le contrôle de volume.

        Args:
            layout: Layout parent
        """
        volume_layout = QHBoxLayout()
        volume_layout.setSpacing(AppSpacing.SM)

        # Icône volume
        volume_icon_btn = QPushButton()
        volume_icon_btn.setObjectName("controlButton")
        volume_icon_btn.setFlat(True)
        volume_icon_btn.setCursor(Qt.PointingHandCursor)

        icon = get_icon("mute")
        if not icon.isNull():
            volume_icon_btn.setIcon(icon)
            volume_icon_btn.setIconSize(QSize(40, 40))  # Taille augmentée pour meilleure visibilité

        volume_icon_btn.setFixedSize(40, 40)
        volume_layout.addWidget(volume_icon_btn)

        # Slider volume
        self._volume_slider = QSlider(Qt.Horizontal)
        self._volume_slider.setObjectName("volumeSlider")
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        self._volume_slider.setValue(100)
        self._volume_slider.setFixedWidth(111)
        self._volume_slider.valueChanged.connect(self.volume_changed.emit)
        volume_layout.addWidget(self._volume_slider)

        layout.addLayout(volume_layout)

    def _create_time_display(self, layout: QHBoxLayout):
        """
        Crée l'affichage du temps.

        Args:
            layout: Layout parent
        """
        self._time_label = QLabel("00:00 / 00:00")
        self._time_label.setObjectName("timeLabel")
        self._time_label.setFont(get_font(15, 400))
        self._time_label.setStyleSheet(f"color: {AppColors.TEXT_SECONDARY};")
        layout.addWidget(self._time_label)

    def _create_speed_control(self, layout: QHBoxLayout):
        """
        Crée le contrôle de vitesse.

        Args:
            layout: Layout parent
        """
        self._speed_label = QLabel("1.0x")
        self._speed_label.setObjectName("speedLabel")
        self._speed_label.setFont(get_font(16, 400))
        self._speed_label.setStyleSheet(f"color: {AppColors.TEXT_PRIMARY};")
        self._speed_label.setCursor(Qt.PointingHandCursor)
        self._speed_label.mousePressEvent = self._on_speed_clicked
        layout.addWidget(self._speed_label)

    def _update_play_pause_icon(self):
        """Met à jour l'icône du bouton Play/Pause."""
        icon_name = "play" if not self._is_playing else "play"  # TODO: ajouter icône pause
        icon = get_icon(icon_name)
        if not icon.isNull():
            self._play_pause_btn.setIcon(icon)
            self._play_pause_btn.setIconSize(QSize(51, 51))

    def _on_play_pause_clicked(self):
        """Gère le clic sur Play/Pause."""
        # Désactiver temporairement le bouton pour éviter les clics multiples rapides
        self._play_pause_btn.setEnabled(False)

        if self._is_playing:
            self.pause_clicked.emit()
        else:
            self.play_clicked.emit()

        # Réactiver après un court délai
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(200, lambda: self._play_pause_btn.setEnabled(True))

    def _on_speed_clicked(self, event):
        """
        Gère le clic sur la vitesse pour cycler entre les valeurs.

        Args:
            event: QMouseEvent
        """
        # Cycler entre 0.5x, 0.75x, 1.0x, 1.25x, 1.5x, 2.0x
        speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]

        # Trouver l'index actuel
        current_index = speeds.index(self._current_speed) if self._current_speed in speeds else 2

        # Passer au suivant (avec boucle)
        next_index = (current_index + 1) % len(speeds)
        new_speed = speeds[next_index]

        self.set_speed(new_speed)
        self.speed_changed.emit(new_speed)

    def set_playing_state(self, is_playing: bool):
        """
        Définit l'état de lecture.

        Args:
            is_playing: True si en cours de lecture
        """
        self._is_playing = is_playing
        self._update_play_pause_icon()

    def set_time(self, position: float, duration: float):
        """
        Définit le temps affiché.

        Args:
            position: Position actuelle en secondes
            duration: Durée totale en secondes
        """
        pos_str = self._format_time(position)
        dur_str = self._format_time(duration)
        self._time_label.setText(f"{pos_str} / {dur_str}")

    def set_speed(self, speed: float):
        """
        Définit la vitesse affichée.

        Args:
            speed: Vitesse (0.5 à 2.0)
        """
        self._current_speed = speed
        # Formater la vitesse avec 1 ou 2 décimales selon le besoin
        speed_str = f"{speed:.2f}".rstrip('0').rstrip('.')
        self._speed_label.setText(f"{speed_str}x")

    def set_volume(self, volume: int):
        """
        Définit le volume.

        Args:
            volume: Volume (0-100)
        """
        self._volume_slider.setValue(volume)

    def enable_controls(self, enabled: bool):
        """
        Active/désactive les contrôles.

        Args:
            enabled: True pour activer
        """
        self._play_pause_btn.setEnabled(enabled)
        self._skip_back_btn.setEnabled(enabled)
        self._skip_forward_btn.setEnabled(enabled)
        self._stop_btn.setEnabled(enabled)
        self._volume_slider.setEnabled(enabled)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Formate un temps en secondes en HH:MM:SS ou MM:SS.

        Args:
            seconds: Temps en secondes

        Returns:
            Chaîne formatée
        """
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
