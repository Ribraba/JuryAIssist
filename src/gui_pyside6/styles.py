"""
Styles modernes pour l'interface PySide6 JuryAIssist.
Basé sur le design Figma avec la police Inter et la palette de couleurs exacte.
"""

from .design_tokens import (
    FigmaColors,
    FigmaTypography,
    FigmaSpacing,
    FigmaBorderRadius,
    FigmaDimensions
)

# Raccourcis pour faciliter l'accès
COLORS = {
    "bg_primary": FigmaColors.BG_PRIMARY,
    "bg_sidebar": FigmaColors.BG_SIDEBAR,
    "bg_timeline": FigmaColors.BG_TIMELINE,
    "bg_hover": FigmaColors.BG_HOVER,
    "text_primary": FigmaColors.TEXT_PRIMARY,
    "text_secondary": FigmaColors.TEXT_SECONDARY,
    "text_tertiary": FigmaColors.TEXT_TERTIARY,
    "accent_primary": FigmaColors.ACCENT_PRIMARY,
    "accent_blue": FigmaColors.ACCENT_BLUE,
    "border_light": FigmaColors.BORDER_LIGHT,
    "border_medium": FigmaColors.BORDER_MEDIUM,
    "status_connected": FigmaColors.STATUS_CONNECTED,
    "status_disconnected": FigmaColors.STATUS_DISCONNECTED,
}

# Stylesheet principal avec design Figma
MAIN_STYLE = f"""
/* ===== FENÊTRE PRINCIPALE ===== */
QMainWindow {{
    background-color: {COLORS['bg_primary']};
}}

/* ===== SIDEBAR ===== */
#sidebar {{
    background-color: {COLORS['bg_sidebar']};
    border-right: 1px solid {COLORS['border_light']};
}}

#sidebar_title {{
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.TITLE_MEDIUM['size']}px;
    font-weight: {FigmaTypography.TITLE_MEDIUM['weight']};
    padding: {FigmaSpacing.LG}px;
}}

/* ===== BOUTONS ===== */
QPushButton {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.MEDIUM}px;
    padding: 12px {FigmaSpacing.MD}px;
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.BODY_REGULAR['size']}px;
    font-weight: {FigmaTypography.BODY_REGULAR['weight']};
    min-height: {FigmaDimensions.BUTTON_HEIGHT}px;
}}

QPushButton:hover {{
    background-color: {COLORS['bg_hover']};
    border: 1px solid {COLORS['border_medium']};
}}

QPushButton:pressed {{
    background-color: {COLORS['bg_sidebar']};
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_sidebar']};
    color: {COLORS['text_tertiary']};
    border: 1px solid {COLORS['border_light']};
}}

QPushButton#primary_button {{
    background-color: {COLORS['accent_primary']};
    color: white;
    border: none;
    font-weight: 600;
}}

QPushButton#primary_button:hover {{
    background-color: #1A1A1A;
}}

QPushButton#primary_button:pressed {{
    background-color: #333333;
}}

QPushButton#white_button {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border_light']};
    font-weight: 500;
    border-radius: {FigmaBorderRadius.MEDIUM}px;
}}

QPushButton#white_button:hover {{
    background-color: {COLORS['bg_hover']};
    border: 1px solid {COLORS['border_medium']};
}}

QPushButton#white_button:pressed {{
    background-color: {COLORS['bg_sidebar']};
}}

QPushButton#black_button {{
    background-color: {COLORS['accent_primary']};
    color: white;
    border: none;
    font-weight: 600;
    font-size: 14px;
    border-radius: {FigmaBorderRadius.MEDIUM}px;
}}

QPushButton#black_button:hover {{
    background-color: #1A1A1A;
}}

QPushButton#black_button:pressed {{
    background-color: #333333;
}}

/* ===== LISTE DES TRANSCRIPTIONS ===== */
QListWidget {{
    background-color: transparent;
    border: none;
    outline: none;
    padding: {FigmaSpacing.SM}px;
}}

QListWidget::item {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.MEDIUM}px;
    padding: {FigmaSpacing.MD}px;
    margin-bottom: {FigmaSpacing.SM}px;
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.BODY_REGULAR['size']}px;
}}

QListWidget::item:hover {{
    background-color: {COLORS['bg_hover']};
    border: 1px solid {COLORS['border_medium']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent_primary']};
    color: white;
    border: 1px solid {COLORS['accent_primary']};
}}

/* ===== ÉDITEUR DE TEXTE ===== */
QTextEdit {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.LARGE}px;
    padding: {FigmaSpacing.LG}px;
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: 18px;
    font-weight: 400;
    line-height: 1.6;
    selection-background-color: {COLORS['accent_primary']};
    selection-color: white;
}}

QTextEdit:focus {{
    border: 2px solid {COLORS['accent_primary']};
    padding: {FigmaSpacing.LG - 1}px;
}}

/* ===== SLIDER (Timeline + Volume) ===== */
QSlider::groove:horizontal {{
    background: {COLORS['bg_timeline']};
    height: {FigmaDimensions.SLIDER_HEIGHT}px;
    border-radius: {FigmaDimensions.SLIDER_HEIGHT // 2}px;
}}

QSlider::handle:horizontal {{
    background: {COLORS['accent_primary']};
    width: {FigmaDimensions.SLIDER_HANDLE_SIZE}px;
    height: {FigmaDimensions.SLIDER_HANDLE_SIZE}px;
    border-radius: {FigmaDimensions.SLIDER_HANDLE_SIZE // 2}px;
    margin: -{(FigmaDimensions.SLIDER_HANDLE_SIZE - FigmaDimensions.SLIDER_HEIGHT) // 2}px 0;
}}

QSlider::handle:horizontal:hover {{
    background: #1A1A1A;
    width: 18px;
    height: 18px;
    border-radius: 9px;
    margin: -6px 0;
}}

QSlider::sub-page:horizontal {{
    background: {COLORS['accent_primary']};
    border-radius: {FigmaDimensions.SLIDER_HEIGHT // 2}px;
}}

/* ===== LABELS ===== */
QLabel {{
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.BODY_REGULAR['size']}px;
}}

QLabel#secondary_label {{
    color: {COLORS['text_secondary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.LABEL_REGULAR['size']}px;
    font-weight: {FigmaTypography.LABEL_REGULAR['weight']};
}}

QLabel#title_label {{
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.TITLE_MEDIUM['size']}px;
    font-weight: {FigmaTypography.TITLE_MEDIUM['weight']};
}}

QLabel#header_label {{
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.TITLE_LARGE['size']}px;
    font-weight: {FigmaTypography.TITLE_LARGE['weight']};
}}

QLabel#title_large {{
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.56px;
}}

/* ===== COMBO BOX ===== */
QComboBox {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.MEDIUM}px;
    padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.BODY_REGULAR['size']}px;
    min-height: {FigmaDimensions.BUTTON_SMALL_HEIGHT}px;
}}

QComboBox:hover {{
    border: 1px solid {COLORS['border_medium']};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: {FigmaSpacing.SM}px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {COLORS['text_secondary']};
    margin-right: 5px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.MEDIUM}px;
    padding: {FigmaSpacing.XS}px;
    selection-background-color: {COLORS['accent_primary']};
    selection-color: white;
}}

/* ===== SPIN BOX ===== */
QSpinBox {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.MEDIUM}px;
    padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.BODY_REGULAR['size']}px;
    min-height: {FigmaDimensions.BUTTON_SMALL_HEIGHT}px;
}}

QSpinBox:hover {{
    border: 1px solid {COLORS['border_medium']};
}}

QSpinBox:focus {{
    border: 2px solid {COLORS['accent_primary']};
    padding: {FigmaSpacing.SM - 1}px {FigmaSpacing.MD - 1}px;
}}

/* ===== FRAME TIMELINE ===== */
#timeline_frame {{
    background-color: {COLORS['bg_sidebar']};
    border-top: 1px solid {COLORS['border_light']};
    padding: {FigmaSpacing.MD}px;
}}

/* ===== BADGE PÉDALE ===== */
#pedal_badge {{
    background-color: {COLORS['bg_sidebar']};
    border-radius: {FigmaBorderRadius.LARGE}px;
    padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: {FigmaTypography.LABEL_SMALL['size']}px;
    font-weight: {FigmaTypography.LABEL_SMALL['weight']};
}}

#pedal_badge[connected="true"] {{
    background-color: #D7F5E0;
    color: {COLORS['status_connected']};
}}

#pedal_badge[connected="false"] {{
    background-color: {COLORS['bg_sidebar']};
    color: {COLORS['status_disconnected']};
}}

/* ===== SCROLL BARS ===== */
QScrollBar:vertical {{
    background: transparent;
    width: 12px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['border_medium']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS['text_tertiary']};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {{
    background: transparent;
    border: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 12px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS['border_medium']};
    border-radius: 6px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS['text_tertiary']};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {{
    background: transparent;
    border: none;
}}

/* ===== MENU BAR ===== */
QMenuBar {{
    background-color: {COLORS['bg_primary']};
    border-bottom: 1px solid {COLORS['border_light']};
    padding: {FigmaSpacing.XS}px;
}}

QMenuBar::item {{
    padding: {FigmaSpacing.SM}px {FigmaSpacing.MD}px;
    border-radius: {FigmaBorderRadius.SMALL}px;
    color: {COLORS['text_primary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
}}

QMenuBar::item:selected {{
    background-color: {COLORS['bg_hover']};
}}

QMenu {{
    background-color: {COLORS['bg_primary']};
    border: 1px solid {COLORS['border_light']};
    border-radius: {FigmaBorderRadius.MEDIUM}px;
    padding: {FigmaSpacing.XS}px;
}}

QMenu::item {{
    padding: {FigmaSpacing.SM}px {FigmaSpacing.LG}px;
    border-radius: {FigmaBorderRadius.SMALL}px;
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
}}

QMenu::item:selected {{
    background-color: {COLORS['bg_hover']};
}}

/* ===== STATUS BAR ===== */
QStatusBar {{
    background-color: {COLORS['bg_primary']};
    border-top: 1px solid {COLORS['border_light']};
    color: {COLORS['text_secondary']};
    font-family: "{FigmaTypography.FONT_FAMILY}", {FigmaTypography.FONT_FAMILY_FALLBACK};
    font-size: 12px;
}}

/* ===== DIALOG ===== */
QDialog {{
    background-color: {COLORS['bg_primary']};
}}

QDialogButtonBox QPushButton {{
    min-width: 80px;
}}

/* ===== PROGRESS DIALOG ===== */
QProgressDialog {{
    background-color: {COLORS['bg_primary']};
}}
"""
