"""
Système de thème pour l'application JuryAIssist.

Ce module centralise tous les aspects visuels de l'application:
- Design tokens (couleurs, typographie, espacements)
- Classes d'accès aux tokens
- Fonctions de génération de stylesheets Qt
- Support futur pour le mode sombre

Principe SOLID:
- Single Responsibility: Gère uniquement les styles et le thème
- Open/Closed: Extensible via composition de styles (dark mode à venir)
"""

# ============================================================================
# DESIGN TOKENS
# ============================================================================

# Couleurs extraites du design
COLORS = {
    "#000000": {  # Used in: Transcription brute, Playlist section title, Rechercher
        "hex": "#000000",
    },
    "#1e1e1e": {  # Used in: Page 1 (bg)
        "hex": "#1e1e1e",
    },
    "#444444": {  # Used in: Édition, Pédale connectée (RS-31), Lecture
        "hex": "#444444",
    },
    "#477ed8": {  # Used in: Rectangle 12 (accent blue)
        "hex": "#477ed8",
    },
    "#eeeeee": {  # Used in: Timeline brouillon (bg), Timeline brouillon
        "hex": "#eeeeee",
    },
    "#f7f7f7": {  # Used in: Menu item, Menu item (bg)
        "hex": "#f7f7f7",
    },
    "#ffffff": {  # Used in: Home Page (bg), Home Page, Sidebar
        "hex": "#ffffff",
    },
}

# Typographie
TYPOGRAPHY = {
    "Inter_11_0px_400": {
        "family": "Inter",
        "size": 11.0,
        "weight": 400,
        # Used for: Pédale connectée (RS-31)
    },
    "Inter_15_0px_400": {
        "family": "Inter",
        "size": 15.0,
        "weight": 400,
        # Used for: 00:15 / 02:45:30
    },
    "Inter_16_0px_400": {
        "family": "Inter",
        "size": 16.0,
        "weight": 400,
        # Used for: Lecture
    },
    "Inter_16_0px_500": {
        "family": "Inter",
        "size": 16.0,
        "weight": 500,
        # Used for: Rechercher
    },
    "Inter_16_0px_600": {
        "family": "Inter",
        "size": 16.0,
        "weight": 600,
        # Used for: Transcriptions
    },
    "Inter_20_0px_500": {
        "family": "Inter",
        "size": 20.0,
        "weight": 500,
        "letterSpacing": -0.4,
        # Used for: Transcript text
    },
    "Inter_20_0px_600": {
        "family": "Inter",
        "size": 20.0,
        "weight": 600,
        "letterSpacing": -0.2,
        # Used for: Title
    },
    "Inter_24_0px_500": {
        "family": "Inter",
        "size": 24.0,
        "weight": 500,
        "letterSpacing": -0.48,
        # Used for: Editor text
    },
    "Inter_34_0px_600": {
        "family": "Inter",
        "size": 34.0,
        "weight": 600,
        "letterSpacing": -0.68,
        # Used for: Transcription brute (section titles)
    },
}

# Espacements (système de grille)
SPACING = [4.0, 8.0, 16.0, 24.0]


# ============================================================================
# CLASSES D'ACCÈS AUX TOKENS
# ============================================================================

class AppColors:
    """
    Palette de couleurs de l'application.

    Cette classe fournit un accès sémantique aux couleurs,
    facilitant la maintenance et l'ajout futur d'un mode sombre.
    """

    # Backgrounds
    BG_PRIMARY = COLORS["#ffffff"]["hex"]
    BG_SIDEBAR = COLORS["#ffffff"]["hex"]
    BG_TIMELINE = COLORS["#eeeeee"]["hex"]
    BG_ITEM_HOVER = COLORS["#f7f7f7"]["hex"]
    BG_ITEM_SELECTED = COLORS["#f7f7f7"]["hex"]

    # Accents
    ACCENT_BLUE = COLORS["#477ed8"]["hex"]

    # Texte
    TEXT_PRIMARY = COLORS["#000000"]["hex"]
    TEXT_SECONDARY = COLORS["#444444"]["hex"]
    TEXT_ON_DARK = COLORS["#ffffff"]["hex"]

    # Page background (pour le dark mode futur)
    BG_PAGE = COLORS["#ffffff"]["hex"]


class AppSpacing:
    """
    Espacements de l'application.

    Utilise un système de grille cohérent pour tous les éléments UI.
    """

    XS = int(SPACING[0])   # 4px
    SM = int(SPACING[1])   # 8px
    MD = int(SPACING[2])   # 16px
    LG = int(SPACING[3])   # 24px


class AppTypography:
    """
    Styles typographiques de l'application.

    Référence tous les styles de texte utilisés dans l'UI.
    """

    # Titre de l'application
    APP_TITLE = TYPOGRAPHY["Inter_20_0px_600"]

    # Section headings (gros titres)
    SECTION_HEADING = TYPOGRAPHY["Inter_34_0px_600"]

    # Sous-titres
    SUBTITLE = TYPOGRAPHY["Inter_16_0px_400"]

    # Menu items
    MENU_ITEM = TYPOGRAPHY["Inter_16_0px_500"]
    MENU_ITEM_BOLD = TYPOGRAPHY["Inter_16_0px_600"]

    # Contenu transcription
    TRANSCRIPT_TEXT = TYPOGRAPHY["Inter_20_0px_500"]

    # Éditeur
    EDITOR_TEXT = TYPOGRAPHY["Inter_24_0px_500"]

    # Status pédale
    PEDAL_STATUS = TYPOGRAPHY["Inter_11_0px_400"]

    # Temps audio
    TIME_TEXT = TYPOGRAPHY["Inter_15_0px_400"]

    # Vitesse
    SPEED_TEXT = TYPOGRAPHY["Inter_16_0px_400"]


# ============================================================================
# FONCTIONS DE GÉNÉRATION DE STYLESHEETS
# ============================================================================

def get_app_stylesheet() -> str:
    """
    Retourne le stylesheet QSS complet de l'application.

    Ce stylesheet utilise les tokens de design pour assurer
    une cohérence visuelle dans toute l'application.

    Returns:
        str: Stylesheet Qt (QSS) complet

    Note:
        Pour ajouter le dark mode plus tard, créer une fonction
        get_app_stylesheet_dark() qui retourne un stylesheet
        avec des couleurs sombres.
    """
    return f"""
    /* === GLOBAL === */
    * {{
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    QMainWindow {{
        background-color: {AppColors.BG_PRIMARY};
    }}

    /* === SIDEBAR === */
    #sidebar {{
        background-color: {AppColors.BG_SIDEBAR};
        border-right: 1px solid {AppColors.BG_TIMELINE};
    }}

    #sidebarTitle {{
        color: {AppColors.TEXT_PRIMARY};
        font-size: 20px;
        font-weight: 600;
        padding: {AppSpacing.MD}px;
    }}

    /* Search bar */
    #searchBar {{
        background-color: {AppColors.BG_PRIMARY};
        border: 1px solid {AppColors.BG_TIMELINE};
        border-radius: 8px;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
        font-size: 16px;
        color: {AppColors.TEXT_PRIMARY};
    }}

    #searchBar:focus {{
        border: 1px solid {AppColors.ACCENT_BLUE};
    }}

    /* Menu items */
    .menuItem {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
        text-align: left;
        font-size: 16px;
        font-weight: 500;
        color: {AppColors.TEXT_PRIMARY};
    }}

    .menuItem:hover {{
        background-color: {AppColors.BG_ITEM_HOVER};
    }}

    .menuItem:checked {{
        background-color: {AppColors.BG_ITEM_SELECTED};
    }}

    .menuSectionTitle {{
        color: {AppColors.TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 600;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
    }}

    /* === SECTION HEADERS === */
    .sectionHeader {{
        background-color: transparent;
    }}

    .sectionTitle {{
        color: {AppColors.TEXT_PRIMARY};
        font-size: 34px;
        font-weight: 600;
        letter-spacing: -0.68px;
    }}

    .sectionSubtitle {{
        color: {AppColors.TEXT_SECONDARY};
        font-size: 16px;
        font-weight: 400;
    }}

    /* === TRANSCRIPT PANEL === */
    #transcriptPanel {{
        background-color: {AppColors.BG_PRIMARY};
        border: none;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: {AppColors.TEXT_PRIMARY};
        padding: {AppSpacing.MD}px;
    }}

    /* === EDITOR PANEL === */
    #editorPanel {{
        background-color: {AppColors.BG_PRIMARY};
        border: none;
        font-size: 24px;
        font-weight: 500;
        letter-spacing: -0.48px;
        color: {AppColors.TEXT_PRIMARY};
        padding: {AppSpacing.MD}px;
    }}

    /* === TIMELINE === */
    #timeline {{
        background-color: {AppColors.BG_TIMELINE};
        border-radius: 4px;
    }}

    QSlider::groove:horizontal {{
        background-color: {AppColors.BG_TIMELINE};
        height: 8px;
        border-radius: 4px;
    }}

    QSlider::handle:horizontal {{
        background-color: {AppColors.ACCENT_BLUE};
        width: 16px;
        height: 16px;
        margin: -4px 0;
        border-radius: 8px;
    }}

    QSlider::sub-page:horizontal {{
        background-color: {AppColors.ACCENT_BLUE};
        border-radius: 4px;
    }}

    /* === AUDIO CONTROLS === */
    #playButton {{
        background-color: transparent;
        border: none;
        border-radius: 25px;
    }}

    #playButton:hover {{
        background-color: {AppColors.BG_ITEM_HOVER};
    }}

    .controlButton {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }}

    .controlButton:hover {{
        background-color: {AppColors.BG_ITEM_HOVER};
    }}

    #timeLabel {{
        color: {AppColors.TEXT_SECONDARY};
        font-size: 15px;
        font-weight: 400;
    }}

    #speedLabel {{
        color: {AppColors.TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 400;
    }}

    /* Volume slider */
    #volumeSlider::groove:horizontal {{
        background-color: {AppColors.BG_TIMELINE};
        height: 9px;
        border-radius: 4px;
    }}

    #volumeSlider::handle:horizontal {{
        background-color: {AppColors.ACCENT_BLUE};
        width: 18px;
        height: 18px;
        margin: -4px 0;
        border-radius: 9px;
    }}

    #volumeSlider::sub-page:horizontal {{
        background-color: {AppColors.ACCENT_BLUE};
        border-radius: 4px;
    }}

    /* === PEDAL STATUS BADGE === */
    #pedalBadge {{
        background-color: transparent;
        padding: {AppSpacing.XS}px {AppSpacing.SM}px;
        border-radius: 6px;
    }}

    #pedalBadgeConnected {{
        color: #30D158;
        background-color: rgba(48, 209, 88, 0.15);
    }}

    #pedalBadgeDisconnected {{
        color: #8E8E93;
        background-color: transparent;
    }}

    #pedalBadgeText {{
        font-size: 11px;
        font-weight: 400;
    }}

    /* === SCROLLING TRANSCRIPT === */
    #scrollingTranscript {{
        background-color: transparent;
        border: none;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: -0.4px;
    }}

    /* === BUTTONS === */
    #actionButton {{
        background-color: {AppColors.TEXT_PRIMARY};
        color: {AppColors.TEXT_ON_DARK};
        border: none;
        border-radius: 8px;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
        font-size: 16px;
        font-weight: 500;
    }}

    #actionButton:hover {{
        background-color: #1e1e1e;
    }}

    #actionButton:pressed {{
        background-color: #000000;
    }}
    """


def get_section_header_style() -> str:
    """
    Style pour les en-têtes de section.

    Returns:
        str: Stylesheet pour les headers
    """
    return """
        QWidget {
            background-color: transparent;
        }
    """


# ============================================================================
# DARK MODE
# ============================================================================

class DarkColors:
    """
    Palette de couleurs pour le mode sombre.

    Inspiré des standards macOS Dark Mode et Material Design Dark Theme.
    """

    # Backgrounds
    BG_PRIMARY = "#1e1e1e"        # Fond principal
    BG_SIDEBAR = "#2d2d2d"        # Fond sidebar
    BG_TIMELINE = "#3a3a3a"       # Fond timeline
    BG_ITEM_HOVER = "#404040"     # Hover
    BG_ITEM_SELECTED = "#3d3d3d"  # Sélection

    # Accents
    ACCENT_BLUE = "#5a9eff"       # Bleu plus clair pour le dark mode

    # Texte
    TEXT_PRIMARY = "#e8e8e8"      # Texte principal
    TEXT_SECONDARY = "#b4b4b4"    # Texte secondaire
    TEXT_ON_DARK = "#ffffff"      # Texte sur fond sombre

    # Page background
    BG_PAGE = "#1e1e1e"


def get_app_stylesheet_dark() -> str:
    """
    Retourne le stylesheet QSS pour le mode sombre.

    Returns:
        str: Stylesheet Qt (QSS) en mode sombre
    """
    return f"""
    /* === GLOBAL === */
    * {{
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    QMainWindow {{
        background-color: {DarkColors.BG_PRIMARY};
    }}

    /* === SIDEBAR === */
    #sidebar {{
        background-color: {DarkColors.BG_SIDEBAR};
        border-right: 1px solid {DarkColors.BG_TIMELINE};
    }}

    #sidebarTitle {{
        color: {DarkColors.TEXT_PRIMARY};
        font-size: 20px;
        font-weight: 600;
        padding: {AppSpacing.MD}px;
    }}

    /* Search bar */
    #searchBar {{
        background-color: {DarkColors.BG_PRIMARY};
        border: 1px solid {DarkColors.BG_TIMELINE};
        border-radius: 8px;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
        font-size: 16px;
        color: {DarkColors.TEXT_PRIMARY};
    }}

    #searchBar:focus {{
        border: 1px solid {DarkColors.ACCENT_BLUE};
    }}

    /* Menu items */
    .menuItem {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
        text-align: left;
        font-size: 16px;
        font-weight: 500;
        color: {DarkColors.TEXT_PRIMARY};
    }}

    .menuItem:hover {{
        background-color: {DarkColors.BG_ITEM_HOVER};
    }}

    .menuItem:checked {{
        background-color: {DarkColors.BG_ITEM_SELECTED};
    }}

    .menuSectionTitle {{
        color: {DarkColors.TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 600;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
    }}

    /* === SECTION HEADERS === */
    .sectionHeader {{
        background-color: transparent;
    }}

    .sectionTitle {{
        color: {DarkColors.TEXT_PRIMARY};
        font-size: 34px;
        font-weight: 600;
        letter-spacing: -0.68px;
    }}

    .sectionSubtitle {{
        color: {DarkColors.TEXT_SECONDARY};
        font-size: 16px;
        font-weight: 400;
    }}

    /* === TRANSCRIPT PANEL === */
    #transcriptPanel {{
        background-color: {DarkColors.BG_PRIMARY};
        border: none;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: {DarkColors.TEXT_PRIMARY};
        padding: {AppSpacing.MD}px;
    }}

    /* === EDITOR PANEL === */
    #editorPanel {{
        background-color: {DarkColors.BG_PRIMARY};
        border: none;
        font-size: 24px;
        font-weight: 500;
        letter-spacing: -0.48px;
        color: {DarkColors.TEXT_PRIMARY};
        padding: {AppSpacing.MD}px;
    }}

    /* === TIMELINE === */
    #timeline {{
        background-color: {DarkColors.BG_TIMELINE};
        border-radius: 4px;
    }}

    QSlider::groove:horizontal {{
        background-color: {DarkColors.BG_TIMELINE};
        height: 8px;
        border-radius: 4px;
    }}

    QSlider::handle:horizontal {{
        background-color: {DarkColors.ACCENT_BLUE};
        width: 16px;
        height: 16px;
        margin: -4px 0;
        border-radius: 8px;
    }}

    QSlider::sub-page:horizontal {{
        background-color: {DarkColors.ACCENT_BLUE};
        border-radius: 4px;
    }}

    /* === AUDIO CONTROLS === */
    #playButton {{
        background-color: transparent;
        border: none;
        border-radius: 25px;
    }}

    #playButton:hover {{
        background-color: {DarkColors.BG_ITEM_HOVER};
    }}

    .controlButton {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }}

    .controlButton:hover {{
        background-color: {DarkColors.BG_ITEM_HOVER};
    }}

    #timeLabel {{
        color: {DarkColors.TEXT_SECONDARY};
        font-size: 15px;
        font-weight: 400;
    }}

    #speedLabel {{
        color: {DarkColors.TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 400;
    }}

    /* Volume slider */
    #volumeSlider::groove:horizontal {{
        background-color: {DarkColors.BG_TIMELINE};
        height: 9px;
        border-radius: 4px;
    }}

    #volumeSlider::handle:horizontal {{
        background-color: {DarkColors.ACCENT_BLUE};
        width: 18px;
        height: 18px;
        margin: -4px 0;
        border-radius: 9px;
    }}

    #volumeSlider::sub-page:horizontal {{
        background-color: {DarkColors.ACCENT_BLUE};
        border-radius: 4px;
    }}

    /* === PEDAL STATUS BADGE === */
    #pedalBadge {{
        background-color: transparent;
        padding: {AppSpacing.XS}px {AppSpacing.SM}px;
        border-radius: 6px;
    }}

    #pedalBadgeConnected {{
        color: #30D158;
        background-color: rgba(48, 209, 88, 0.15);
    }}

    #pedalBadgeDisconnected {{
        color: #8E8E93;
        background-color: transparent;
    }}

    #pedalBadgeText {{
        font-size: 11px;
        font-weight: 400;
    }}

    /* === SCROLLING TRANSCRIPT === */
    #scrollingTranscript {{
        background-color: transparent;
        border: none;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: {DarkColors.TEXT_PRIMARY};
    }}

    /* === BUTTONS === */
    #actionButton {{
        background-color: {DarkColors.TEXT_PRIMARY};
        color: {DarkColors.BG_PRIMARY};
        border: none;
        border-radius: 8px;
        padding: {AppSpacing.SM}px {AppSpacing.MD}px;
        font-size: 16px;
        font-weight: 500;
    }}

    #actionButton:hover {{
        background-color: {DarkColors.TEXT_ON_DARK};
    }}

    #actionButton:pressed {{
        background-color: #d0d0d0;
    }}

    /* === LABELS === */
    #lectureLabel {{
        color: {DarkColors.TEXT_SECONDARY};
    }}

    /* === DIALOG STYLES === */
    QDialog {{
        background-color: {DarkColors.BG_PRIMARY};
        color: {DarkColors.TEXT_PRIMARY};
    }}

    QLabel {{
        color: {DarkColors.TEXT_PRIMARY};
    }}

    QGroupBox {{
        color: {DarkColors.TEXT_PRIMARY};
        border: 1px solid {DarkColors.BG_TIMELINE};
        border-radius: 8px;
        margin-top: 8px;
        padding-top: 16px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 8px;
        background-color: {DarkColors.BG_PRIMARY};
    }}

    QComboBox {{
        background-color: {DarkColors.BG_SIDEBAR};
        color: {DarkColors.TEXT_PRIMARY};
        border: 1px solid {DarkColors.BG_TIMELINE};
        border-radius: 4px;
        padding: 4px 8px;
    }}

    QComboBox:hover {{
        border: 1px solid {DarkColors.ACCENT_BLUE};
    }}

    QComboBox::drop-down {{
        border: none;
    }}

    QComboBox QAbstractItemView {{
        background-color: {DarkColors.BG_SIDEBAR};
        color: {DarkColors.TEXT_PRIMARY};
        selection-background-color: {DarkColors.BG_ITEM_SELECTED};
        border: 1px solid {DarkColors.BG_TIMELINE};
    }}

    QCheckBox {{
        color: {DarkColors.TEXT_PRIMARY};
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {DarkColors.BG_TIMELINE};
        border-radius: 4px;
        background-color: {DarkColors.BG_SIDEBAR};
    }}

    QCheckBox::indicator:checked {{
        background-color: {DarkColors.ACCENT_BLUE};
        border: 1px solid {DarkColors.ACCENT_BLUE};
    }}

    QPushButton {{
        background-color: {DarkColors.BG_SIDEBAR};
        color: {DarkColors.TEXT_PRIMARY};
        border: 1px solid {DarkColors.BG_TIMELINE};
        border-radius: 6px;
        padding: 6px 16px;
    }}

    QPushButton:hover {{
        background-color: {DarkColors.BG_ITEM_HOVER};
    }}

    QPushButton:pressed {{
        background-color: {DarkColors.BG_TIMELINE};
    }}

    QPushButton:default {{
        background-color: {DarkColors.ACCENT_BLUE};
        border: 1px solid {DarkColors.ACCENT_BLUE};
    }}

    QPushButton:default:hover {{
        background-color: #6aadff;
    }}
    """
