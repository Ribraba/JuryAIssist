"""
Dialog de configuration de l'application.

Permet de modifier:
- Modèle Whisper
- Langue de transcription
- Configuration pédale
- Mode sombre

Principe SOLID:
- Single Responsibility: Gère uniquement l'édition des paramètres
- Tell, Don't Ask: Émet un signal quand les settings changent
"""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QSpinBox,
    QDoubleSpinBox,
    QFormLayout,
)

from src.config import get_settings
from src.devices.pedal import PedalAction


class SettingsDialog(QDialog):
    """
    Dialog de configuration de l'application.

    Signals:
        settings_changed: Émis quand les paramètres sont sauvegardés
    """

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = get_settings()
        self._setup_ui()
        self._load_current_settings()

    def _setup_ui(self):
        """Configure l'interface."""
        self.setWindowTitle("Paramètres")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        # === TRANSCRIPTION ===
        transcription_group = QGroupBox("Transcription")
        transcription_layout = QFormLayout()

        # Modèle Whisper
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.model_combo.setToolTip(
            "tiny: Rapide, moins précis\n"
            "base: Bon compromis (recommandé)\n"
            "small: Plus lent, plus précis\n"
            "medium: Très lent, très précis\n"
            "large: Extrêmement lent, maximum de précision"
        )
        transcription_layout.addRow("Modèle Whisper:", self.model_combo)

        # Langue
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "fr - Français",
            "en - English",
            "es - Español",
            "de - Deutsch",
            "it - Italiano",
            "pt - Português",
            "nl - Nederlands",
            "pl - Polski",
            "ru - Русский",
            "zh - 中文",
            "ja - 日本語",
            "ko - 한국어",
            "ar - العربية",
            "hi - हिन्दी",
        ])
        transcription_layout.addRow("Langue:", self.language_combo)

        transcription_group.setLayout(transcription_layout)
        layout.addWidget(transcription_group)

        # === PÉDALE ===
        pedal_group = QGroupBox("Configuration Pédale")
        pedal_layout = QFormLayout()

        self.button_combos = {}
        actions = [
            ("play_pause", "Play/Pause"),
            ("stop", "Stop"),
            ("skip_forward", "Avancer 5s"),
            ("skip_backward", "Reculer 5s"),
            ("cycle_speed", "Changer vitesse"),
        ]

        for button_num in range(1, 5):
            combo = QComboBox()
            for action_key, action_label in actions:
                combo.addItem(action_label, action_key)
            pedal_layout.addRow(f"Bouton {button_num}:", combo)
            self.button_combos[button_num] = combo

        pedal_group.setLayout(pedal_layout)
        layout.addWidget(pedal_group)

        # === INTERFACE ===
        ui_group = QGroupBox("Interface")
        ui_layout = QFormLayout()

        # Mode sombre
        self.dark_mode_checkbox = QCheckBox("Activer le mode sombre")
        self.dark_mode_checkbox.setToolTip("Redémarrage de l'application requis")
        ui_layout.addRow("", self.dark_mode_checkbox)

        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)

        # === BOUTONS ===
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Sauvegarder")
        self.save_button.clicked.connect(self._save_settings)
        self.save_button.setDefault(True)
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

    def _load_current_settings(self):
        """Charge les paramètres actuels dans l'interface."""
        # Modèle Whisper
        model = self.settings.get("preferred_model", "base")
        index = self.model_combo.findText(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)

        # Langue
        lang = self.settings.get("preferred_language", "fr")
        for i in range(self.language_combo.count()):
            if self.language_combo.itemText(i).startswith(lang):
                self.language_combo.setCurrentIndex(i)
                break

        # Configuration pédale
        for button_num, combo in self.button_combos.items():
            action = self.settings.get(f"pedal_button_{button_num}", "")
            for i in range(combo.count()):
                if combo.itemData(i) == action:
                    combo.setCurrentIndex(i)
                    break

        # Mode sombre
        dark_mode = self.settings.get("dark_mode", False)
        self.dark_mode_checkbox.setChecked(dark_mode)

    def _save_settings(self):
        """Sauvegarde les paramètres modifiés."""
        # Modèle Whisper
        self.settings.set("preferred_model", self.model_combo.currentText())

        # Langue (extraire le code)
        lang_text = self.language_combo.currentText()
        lang_code = lang_text.split(" - ")[0]
        self.settings.set("preferred_language", lang_code)

        # Configuration pédale
        for button_num, combo in self.button_combos.items():
            action = combo.currentData()
            self.settings.set(f"pedal_button_{button_num}", action)

        # Mode sombre
        self.settings.set("dark_mode", self.dark_mode_checkbox.isChecked())

        # Sauvegarder sur disque
        if self.settings.save():
            self.settings_changed.emit()
            self.accept()
        else:
            # TODO: Afficher un message d'erreur
            pass
