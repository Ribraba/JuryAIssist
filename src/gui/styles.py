"""
Styles Qt personnalisés pour l'interface graphique.

Design moderne flat inspiré de macOS Big Sur / Monterey :
- Thème sombre élégant
- Palette de couleurs épurée
- Espacement généreux
- Effets visuels subtils et modernes
- Bordures arrondies
- Flat design avec profondeur subtile
"""

# Palette de couleurs - Thème sombre moderne (inspiré macOS)
COLORS = {
    # Backgrounds - Thème sombre
    "bg_primary": "#1C1C1E",  # Noir Apple (fond principal)
    "bg_secondary": "#2C2C2E",  # Gris très foncé (cartes)
    "bg_tertiary": "#3A3A3C",  # Gris foncé (hover)
    "bg_elevated": "#48484A",  # Gris moyen foncé (éléments surélevés)

    # Textes
    "text_primary": "#FFFFFF",  # Blanc pur
    "text_secondary": "#AEAEB2",  # Gris clair
    "text_tertiary": "#8E8E93",  # Gris moyen

    # Accents Apple
    "accent_blue": "#0A84FF",  # Bleu Apple
    "accent_success": "#30D158",  # Vert Apple
    "accent_warning": "#FFD60A",  # Jaune Apple
    "accent_danger": "#FF453A",  # Rouge Apple

    # Bordures
    "border": "#48484A",  # Bordure subtile
    "divider": "#38383A",  # Séparateur

    # Shadow
    "shadow": "rgba(0, 0, 0, 0.3)",  # Ombre pour profondeur
    "shadow_light": "rgba(0, 0, 0, 0.15)",  # Ombre légère
}


def get_app_style() -> str:
    """Style global de l'application - Thème sombre moderne."""
    return f"""
        * {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        }}

        QMainWindow {{
            background-color: {COLORS['bg_primary']};
        }}

        QWidget {{
            color: {COLORS['text_primary']};
            font-size: 13px;
            background-color: transparent;
        }}

        /* Menu Bar moderne */
        QMenuBar {{
            background-color: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            border: none;
            padding: 4px;
        }}

        QMenuBar::item {{
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 6px;
        }}

        QMenuBar::item:selected {{
            background-color: {COLORS['bg_tertiary']};
        }}

        QMenuBar::item:pressed {{
            background-color: {COLORS['bg_elevated']};
        }}

        /* Menu déroulant */
        QMenu {{
            background-color: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 4px;
        }}

        QMenu::item {{
            padding: 8px 24px 8px 12px;
            border-radius: 4px;
        }}

        QMenu::item:selected {{
            background-color: {COLORS['accent_blue']};
            color: white;
        }}

        /* Dialogues */
        QDialog {{
            background-color: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
        }}

        QMessageBox {{
            background-color: {COLORS['bg_secondary']};
        }}

        QMessageBox QLabel {{
            color: {COLORS['text_primary']};
        }}

        QMessageBox QPushButton {{
            background-color: {COLORS['bg_tertiary']};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 80px;
        }}

        QMessageBox QPushButton:hover {{
            background-color: {COLORS['bg_elevated']};
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {COLORS['bg_secondary']};
            color: {COLORS['text_secondary']};
            border-top: 1px solid {COLORS['divider']};
            padding: 4px;
        }}

        /* Splitter */
        QSplitter::handle {{
            background-color: {COLORS['divider']};
        }}

        QSplitter::handle:horizontal {{
            width: 1px;
        }}

        QSplitter::handle:vertical {{
            height: 1px;
        }}
    """


def get_card_style() -> str:
    """Style des cartes/panneaux."""
    return f"""
        QFrame#card {{
            background-color: {COLORS['bg_secondary']};
            border-radius: 16px;
            border: none;
        }}
    """


def get_title_style() -> str:
    """Style du titre principal."""
    return f"""
        QLabel#title {{
            color: {COLORS['text_primary']};
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}
    """


def get_file_info_style() -> str:
    """Style de l'info fichier."""
    return f"""
        QLabel#file_info {{
            color: {COLORS['text_secondary']};
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
            background-color: {COLORS['bg_tertiary']};
            border-radius: 8px;
        }}
    """


def get_time_label_style() -> str:
    """Style des labels de temps."""
    return f"""
        QLabel#time {{
            color: {COLORS['text_primary']};
            font-size: 16px;
            font-weight: 600;
            font-family: "SF Mono", "Menlo", monospace;
            letter-spacing: 0.5px;
        }}
    """


def get_slider_style() -> str:
    """Style du slider moderne."""
    return f"""
        QSlider::groove:horizontal {{
            background: {COLORS['divider']};
            height: 4px;
            border-radius: 2px;
        }}

        QSlider::sub-page:horizontal {{
            background: {COLORS['text_primary']};
            border-radius: 2px;
        }}

        QSlider::handle:horizontal {{
            background: {COLORS['bg_secondary']};
            border: 2px solid {COLORS['text_primary']};
            width: 18px;
            height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }}

        QSlider::handle:horizontal:hover {{
            background: {COLORS['text_primary']};
            border: 2px solid {COLORS['text_primary']};
            width: 20px;
            height: 20px;
            margin: -8px 0;
            border-radius: 10px;
        }}

        QSlider::handle:horizontal:pressed {{
            background: {COLORS['text_secondary']};
            border: 2px solid {COLORS['text_secondary']};
        }}
    """


def get_primary_button_style() -> str:
    """Style du bouton primaire (Play/Pause) - Moderne flat."""
    return f"""
        QPushButton#primary {{
            background: {COLORS['accent_blue']};
            color: white;
            border: none;
            border-radius: 32px;
            font-size: 16px;
            font-weight: 600;
            min-width: 64px;
            min-height: 64px;
            max-width: 64px;
            max-height: 64px;
        }}

        QPushButton#primary:hover {{
            background: #1E90FF;
        }}

        QPushButton#primary:pressed {{
            background: #0066CC;
        }}

        QPushButton#primary:disabled {{
            background: {COLORS['bg_elevated']};
            color: {COLORS['text_tertiary']};
        }}
    """


def get_secondary_button_style() -> str:
    """Style des boutons secondaires - Flat moderne."""
    return f"""
        QPushButton#secondary {{
            background: {COLORS['bg_tertiary']};
            color: {COLORS['text_primary']};
            border: none;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 500;
            padding: 10px 20px;
            min-height: 36px;
        }}

        QPushButton#secondary:hover {{
            background: {COLORS['bg_elevated']};
        }}

        QPushButton#secondary:pressed {{
            background: {COLORS['border']};
        }}

        QPushButton#secondary:disabled {{
            color: {COLORS['text_tertiary']};
            background: {COLORS['bg_secondary']};
        }}
    """


def get_icon_button_style() -> str:
    """Style des boutons icônes (Skip, Stop)."""
    return f"""
        QPushButton#icon_button {{
            background: transparent;
            border: none;
            border-radius: 24px;
            min-width: 48px;
            min-height: 48px;
            max-width: 48px;
            max-height: 48px;
        }}

        QPushButton#icon_button:hover {{
            background: {COLORS['bg_tertiary']};
        }}

        QPushButton#icon_button:pressed {{
            background: {COLORS['divider']};
        }}

        QPushButton#icon_button:disabled {{
            opacity: 0.3;
        }}
    """


def get_stop_button_style() -> str:
    """Style du bouton Stop."""
    return f"""
        QPushButton#stop {{
            background: transparent;
            border: 2px solid {COLORS['text_secondary']};
            border-radius: 24px;
            min-width: 48px;
            min-height: 48px;
            max-width: 48px;
            max-height: 48px;
        }}

        QPushButton#stop:hover {{
            background: {COLORS['text_secondary']};
        }}

        QPushButton#stop:pressed {{
            background: {COLORS['text_primary']};
            border: 2px solid {COLORS['text_primary']};
        }}

        QPushButton#stop:disabled {{
            border: 2px solid {COLORS['divider']};
            opacity: 0.3;
        }}
    """


def get_speed_badge_style() -> str:
    """Style du badge de vitesse."""
    return f"""
        QLabel#speed_badge {{
            background: {COLORS['text_primary']};
            color: white;
            font-size: 15px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 12px;
            min-width: 50px;
        }}
    """


def get_load_button_style() -> str:
    """Style du bouton de chargement."""
    return f"""
        QPushButton#load {{
            background: {COLORS['accent_blue']};
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            padding: 12px 24px;
            min-height: 44px;
        }}

        QPushButton#load:hover {{
            background: #1E90FF;
        }}

        QPushButton#load:pressed {{
            background: #0066CC;
        }}
    """


def get_text_edit_style() -> str:
    """Style moderne pour les zones de texte."""
    return f"""
        QTextEdit {{
            background-color: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['divider']};
            border-radius: 8px;
            padding: 12px;
            font-size: 13px;
            line-height: 1.6;
            selection-background-color: {COLORS['accent_blue']};
            selection-color: white;
        }}

        QTextEdit:focus {{
            border: 1px solid {COLORS['accent_blue']};
        }}
    """


def get_label_style() -> str:
    """Style pour les labels."""
    return f"""
        QLabel {{
            color: {COLORS['text_primary']};
            font-size: 13px;
        }}

        QLabel#section_title {{
            color: {COLORS['text_secondary']};
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 4px 0;
        }}
    """
