"""
Styles PyQt5 basés sur le design Figma.

Principe SOLID:
- Single Responsibility: Gère uniquement les styles et le thème
- Open/Closed: Extensible via composition de styles
"""
from src.gui.design_tokens import COLORS, TYPOGRAPHY, SPACING


# === COULEURS ===

class FigmaColors:
    """Palette de couleurs du design Figma."""

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

    # Page background (optionnel, si dark mode plus tard)
    BG_PAGE = COLORS["#ffffff"]["hex"]


class FigmaSpacing:
    """Espacements du design Figma."""

    XS = int(SPACING[0])   # 4px
    SM = int(SPACING[1])   # 8px
    MD = int(SPACING[2])   # 16px
    LG = int(SPACING[3])   # 24px


class FigmaTypography:
    """Styles typographiques du design Figma."""

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


# === STYLES QSS ===

def get_figma_stylesheet() -> str:
    """
    Retourne le stylesheet QSS complet basé sur le design Figma.

    Returns:
        QString contenant tout le CSS
    """
    return f"""
    /* === GLOBAL === */
    * {{
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    QMainWindow {{
        background-color: {FigmaColors.BG_PRIMARY};
    }}

    /* === SIDEBAR === */
    #sidebar {{
        background-color: {FigmaColors.BG_SIDEBAR};
        border-right: 1px solid {FigmaColors.BG_TIMELINE};
    }}

    #sidebarTitle {{
        color: {FigmaColors.TEXT_PRIMARY};
        font-size: 20px;
        font-weight: 600;
        padding: {FigmaSpacing.MD}px;
    }}

    /* Search bar */
    #searchBar {{
        background-color: {FigmaColors.BG_PRIMARY};
        border: 1px solid {FigmaColors.BG_TIMELINE};
        border-radius: 8px;
        padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
        font-size: 16px;
        color: {FigmaColors.TEXT_PRIMARY};
    }}

    #searchBar:focus {{
        border: 1px solid {FigmaColors.ACCENT_BLUE};
    }}

    /* Menu items */
    .menuItem {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
        text-align: left;
        font-size: 16px;
        font-weight: 500;
        color: {FigmaColors.TEXT_PRIMARY};
    }}

    .menuItem:hover {{
        background-color: {FigmaColors.BG_ITEM_HOVER};
    }}

    .menuItem:checked {{
        background-color: {FigmaColors.BG_ITEM_SELECTED};
    }}

    .menuSectionTitle {{
        color: {FigmaColors.TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 600;
        padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
    }}

    /* === SECTION HEADERS === */
    .sectionHeader {{
        background-color: transparent;
    }}

    .sectionTitle {{
        color: {FigmaColors.TEXT_PRIMARY};
        font-size: 34px;
        font-weight: 600;
        letter-spacing: -0.68px;
    }}

    .sectionSubtitle {{
        color: {FigmaColors.TEXT_SECONDARY};
        font-size: 16px;
        font-weight: 400;
    }}

    /* === TRANSCRIPT PANEL === */
    #transcriptPanel {{
        background-color: {FigmaColors.BG_PRIMARY};
        border: none;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: -0.4px;
        color: {FigmaColors.TEXT_PRIMARY};
        padding: {FigmaSpacing.MD}px;
    }}

    /* === EDITOR PANEL === */
    #editorPanel {{
        background-color: {FigmaColors.BG_PRIMARY};
        border: none;
        font-size: 24px;
        font-weight: 500;
        letter-spacing: -0.48px;
        color: {FigmaColors.TEXT_PRIMARY};
        padding: {FigmaSpacing.MD}px;
    }}

    /* === TIMELINE === */
    #timeline {{
        background-color: {FigmaColors.BG_TIMELINE};
        border-radius: 4px;
    }}

    QSlider::groove:horizontal {{
        background-color: {FigmaColors.BG_TIMELINE};
        height: 8px;
        border-radius: 4px;
    }}

    QSlider::handle:horizontal {{
        background-color: {FigmaColors.ACCENT_BLUE};
        width: 16px;
        height: 16px;
        margin: -4px 0;
        border-radius: 8px;
    }}

    QSlider::sub-page:horizontal {{
        background-color: {FigmaColors.ACCENT_BLUE};
        border-radius: 4px;
    }}

    /* === AUDIO CONTROLS === */
    #playButton {{
        background-color: transparent;
        border: none;
        border-radius: 25px;
    }}

    #playButton:hover {{
        background-color: {FigmaColors.BG_ITEM_HOVER};
    }}

    .controlButton {{
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }}

    .controlButton:hover {{
        background-color: {FigmaColors.BG_ITEM_HOVER};
    }}

    #timeLabel {{
        color: {FigmaColors.TEXT_SECONDARY};
        font-size: 15px;
        font-weight: 400;
    }}

    #speedLabel {{
        color: {FigmaColors.TEXT_PRIMARY};
        font-size: 16px;
        font-weight: 400;
    }}

    /* Volume slider */
    #volumeSlider::groove:horizontal {{
        background-color: {FigmaColors.BG_TIMELINE};
        height: 9px;
        border-radius: 4px;
    }}

    #volumeSlider::handle:horizontal {{
        background-color: {FigmaColors.ACCENT_BLUE};
        width: 18px;
        height: 18px;
        margin: -4px 0;
        border-radius: 9px;
    }}

    #volumeSlider::sub-page:horizontal {{
        background-color: {FigmaColors.ACCENT_BLUE};
        border-radius: 4px;
    }}

    /* === PEDAL STATUS BADGE === */
    #pedalBadge {{
        background-color: transparent;
        padding: {FigmaSpacing.XS}px {FigmaSpacing.SM}px;
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
        background-color: {FigmaColors.TEXT_PRIMARY};
        color: {FigmaColors.TEXT_ON_DARK};
        border: none;
        border-radius: 8px;
        padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
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
    """Style pour les en-têtes de section."""
    return f"""
        QWidget {{
            background-color: transparent;
        }}
    """
