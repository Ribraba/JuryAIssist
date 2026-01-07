"""
Fenêtre principale de l'application avec onglets.

Combine le lecteur audio et la transcription.
"""

from pathlib import Path
from typing import Optional

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.audio.controller import AudioController
from src.audio.vlc_player import VLCAudioPlayer
from src.gui.audio_player_window import AudioPlayerWindow
from src.gui.transcription_panel import TranscriptionPanel
from src.gui.icons import Icons
from src.gui.styles import (
    get_app_style,
    get_load_button_style,
    get_title_style,
    COLORS,
)
from src.devices.olympus_pedal import OlympusPedal
from src.devices.pedal import PedalAction


class MainWindow(QMainWindow):
    """
    Fenêtre principale avec onglets.

    Combine lecteur audio et panneau de transcription.
    """

    def __init__(self):
        """Initialise la fenêtre."""
        super().__init__()

        # État
        self._current_audio_file: Optional[str] = None

        # Créer le player et le contrôleur (partagés)
        self._player = VLCAudioPlayer()
        self._controller = AudioController(self._player)

        # Pédale Olympus (optionnelle)
        self._pedal: Optional[OlympusPedal] = None
        self._pedal_connected = False

        # Timer pour détecter la pédale périodiquement
        self._pedal_detect_timer = QTimer()
        self._pedal_detect_timer.timeout.connect(self._check_pedal_connection)
        self._pedal_detect_timer.setInterval(2000)  # Vérifier toutes les 2 secondes

        # Configuration de la fenêtre
        self.setWindowTitle("JuryAIssist - Transcription Audio Juridique")
        self.setMinimumSize(900, 700)
        self.resize(1100, 800)

        # Appliquer le style global
        self.setStyleSheet(get_app_style())

        # Créer l'interface
        self._create_ui()

        # Connecter les signaux du controller aux widgets de l'interface
        self._connect_audio_signals()

        # Tenter de connecter la pédale au démarrage
        self._init_pedal()

        # Démarrer le timer de détection de pédale
        self._pedal_detect_timer.start()

    def _create_ui(self):
        """Crée l'interface utilisateur."""
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        # Layout principal
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(24)

        # En-tête avec titre et bouton de chargement
        header = self._create_header()
        main_layout.addLayout(header)

        # Onglets
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background: transparent;
            }}
            QTabBar::tab {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                padding: 12px 24px;
                border: 1px solid {COLORS['border']};
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 4px;
            }}
            QTabBar::tab:selected {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                font-weight: 600;
                border-bottom: 2px solid {COLORS['text_primary']};
            }}
            QTabBar::tab:hover {{
                background: {COLORS['bg_tertiary']};
            }}
        """)

        # Créer les onglets
        self._create_tabs()

        main_layout.addWidget(self._tabs)

    def _create_header(self) -> QHBoxLayout:
        """Crée l'en-tête avec titre et bouton."""
        layout = QHBoxLayout()
        layout.setSpacing(16)

        # Titre
        title = QLabel("JuryAIssist")
        title.setObjectName("title")
        title.setStyleSheet(get_title_style())
        layout.addWidget(title)

        # Indicateur de pédale
        self._pedal_indicator = QLabel("⚪ Pédale non détectée")
        self._pedal_indicator.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 12px;
                padding: 4px 8px;
                border-radius: 4px;
                background: {COLORS['bg_secondary']};
            }}
        """)
        layout.addWidget(self._pedal_indicator)

        layout.addStretch()

        # Bouton de chargement de fichier
        self._load_btn = QPushButton("Ouvrir un fichier audio")
        self._load_btn.setObjectName("load")
        self._load_btn.setStyleSheet(get_load_button_style())
        self._load_btn.setCursor(Qt.PointingHandCursor)
        self._load_btn.setIcon(Icons.folder())
        self._load_btn.clicked.connect(self._load_file)
        layout.addWidget(self._load_btn)

        return layout

    def _create_tabs(self):
        """Crée les onglets."""
        # Onglet 1 : Lecteur Audio
        self._audio_tab = self._create_audio_tab()
        self._tabs.addTab(self._audio_tab, "Lecteur Audio")

        # Onglet 2 : Transcription
        self._transcription_panel = TranscriptionPanel()
        self._tabs.addTab(self._transcription_panel, "Transcription")

    def _create_audio_tab(self) -> QWidget:
        """
        Crée l'onglet lecteur audio.

        Principe SOLID-D : Injection de dépendances
        On passe notre controller à AudioPlayerWindow au lieu d'en créer un nouveau.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 16, 0, 0)

        from src.gui.audio_player_window import AudioPlayerWindow

        # Injection de dépendances (SOLID-D)
        # AudioPlayerWindow utilise notre controller au lieu d'en créer un nouveau
        self._audio_window_ref = AudioPlayerWindow(controller=self._controller)

        # Récupérer la card créée par AudioPlayerWindow
        card = self._audio_window_ref.centralWidget().layout().itemAt(1).widget()

        # Enlever le bouton "Ouvrir un fichier" et récupérer le label
        card_layout = card.layout()
        if card_layout and card_layout.count() > 0:
            first_widget = card_layout.itemAt(0).widget()
            if isinstance(first_widget, QPushButton):
                first_widget.setVisible(False)
            if card_layout.count() > 1:
                second_widget = card_layout.itemAt(1).widget()
                if isinstance(second_widget, QLabel):
                    self._file_label = second_widget

        # Ajouter seulement la card (pas toute la fenêtre)
        layout.addWidget(card)

        return widget

    def _load_file(self):
        """Charge un fichier audio."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un fichier audio",
            str(Path.home()),
            "Audio (*.mp3 *.wav *.m4a *.flac *.ogg *.dss);;Tous (*)",
        )

        if path:
            self._current_audio_file = path

            # Charger dans le contrôleur audio
            if self._controller.load_file(path):
                # Activer les contrôles
                if hasattr(self, '_audio_window_ref'):
                    self._audio_window_ref._enable_controls()

                # Mettre à jour le label de fichier
                if hasattr(self, '_file_label'):
                    filename = Path(path).name
                    self._file_label.setText(f"🎵 {filename}")

                # Passer le fichier au panneau de transcription
                self._transcription_panel.set_audio_file(path)

    def _connect_audio_signals(self):
        """Connecte les signaux du controller audio aux widgets."""
        # Cette méthode sera appelée après la création de l'interface
        # Les signaux de l'audio sont déjà gérés par AudioPlayerWindow
        # Pas besoin de connexions supplémentaires ici
        pass

    def _check_pedal_connection(self):
        """Vérifie périodiquement si une pédale est connectée."""
        # Si déjà connectée, vérifier qu'elle est toujours là
        if self._pedal_connected and self._pedal:
            if not self._pedal.is_connected():
                print("⚠️ Pédale déconnectée")
                self._pedal_connected = False
                self._pedal = None
                self._update_pedal_indicator(False)
                # Continuer à chercher une nouvelle connexion

        # Si pas connectée, essayer de détecter
        if not self._pedal_connected:
            self._init_pedal()

    def _init_pedal(self):
        """Initialise et connecte la pédale Olympus (si disponible)."""
        # Ne rien faire si déjà connectée
        if self._pedal_connected and self._pedal and self._pedal.is_connected():
            return

        try:
            # Créer une nouvelle instance
            pedal = OlympusPedal()

            # Détecter la pédale
            if pedal.detect():
                pedal_info = pedal.get_pedal_info()
                print(f"✅ Pédale détectée: {pedal_info}")

                # Se connecter
                if pedal.connect():
                    # Déconnecter l'ancienne si elle existe
                    if self._pedal:
                        self._pedal.disconnect()

                    self._pedal = pedal
                    self._pedal_connected = True
                    print("✅ Pédale connectée avec succès")

                    # Mettre à jour l'indicateur
                    self._update_pedal_indicator(True)

                    # Connecter les signaux aux actions audio
                    self._connect_pedal_signals()
                else:
                    print("⚠️ Échec de connexion à la pédale")

        except ImportError:
            # Module hidapi non disponible - arrêter le timer
            if self._pedal_detect_timer.isActive():
                self._pedal_detect_timer.stop()
                print("ℹ️ Module hidapi non disponible - pédale désactivée")
        except Exception as e:
            # Erreur temporaire, on réessayera au prochain tick
            pass

    def _update_pedal_indicator(self, connected: bool):
        """
        Met à jour l'indicateur visuel de la pédale.

        Args:
            connected: True si connectée, False sinon
        """
        if connected:
            self._pedal_indicator.setText("🟢 Pédale connectée")
            self._pedal_indicator.setStyleSheet(f"""
                QLabel {{
                    color: #10b981;
                    font-size: 12px;
                    font-weight: 600;
                    padding: 4px 8px;
                    border-radius: 4px;
                    background: {COLORS['bg_secondary']};
                }}
            """)
        else:
            self._pedal_indicator.setText("⚪ Pédale non détectée")
            self._pedal_indicator.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_secondary']};
                    font-size: 12px;
                    padding: 4px 8px;
                    border-radius: 4px;
                    background: {COLORS['bg_secondary']};
                }}
            """)

    def _connect_pedal_signals(self):
        """Connecte les signaux de la pédale aux actions audio."""
        if not self._pedal:
            return

        # Connecter les actions de la pédale au contrôleur audio
        self._pedal.action_triggered.connect(self._on_pedal_action)

        # Connecter les signaux d'état
        self._pedal.connected.connect(lambda: print("🔌 Pédale connectée"))
        self._pedal.disconnected.connect(lambda: print("🔌 Pédale déconnectée"))
        self._pedal.error.connect(lambda err: print(f"❌ Erreur pédale: {err}"))

    def _on_pedal_action(self, action: PedalAction):
        """
        Gère les actions de la pédale.

        Args:
            action: Action détectée par la pédale
        """
        if action == PedalAction.PLAY_PAUSE:
            self._controller.toggle_play_pause()
            print("🎮 Pédale: Play/Pause")

        elif action == PedalAction.SKIP_FORWARD:
            self._controller.skip_forward()
            print("🎮 Pédale: Avancer 5s")

        elif action == PedalAction.SKIP_BACKWARD:
            self._controller.skip_backward()
            print("🎮 Pédale: Reculer 5s")

        elif action == PedalAction.STOP:
            self._controller.stop()
            print("🎮 Pédale: Stop")

        elif action == PedalAction.CYCLE_SPEED:
            self._controller.cycle_speed()
            print("🎮 Pédale: Cycle vitesse")

    def closeEvent(self, event):
        """Appelé à la fermeture de la fenêtre."""
        # Arrêter le timer de détection
        if self._pedal_detect_timer.isActive():
            self._pedal_detect_timer.stop()

        # Déconnecter la pédale
        if self._pedal:
            self._pedal.disconnect()

        # Libérer les ressources audio
        self._controller.release()

        event.accept()
