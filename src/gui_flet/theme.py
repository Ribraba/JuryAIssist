"""
Thème et constantes de design - Style minimaliste Apple-like.

Palette de couleurs inspirée de macOS:
- Blanc cassé pour les fonds
- Gris doux pour les bordures et le texte secondaire
- Bleu système pour les actions primaires
- Vert subtil pour les états positifs
- Rouge doux pour les états d'erreur
"""
import flet as ft


class AppColors:
    """Palette de couleurs minimaliste."""

    # Couleurs de base
    BACKGROUND = "#F9FAFB"  # Blanc cassé
    SURFACE = "#FFFFFF"     # Blanc pur

    # Texte
    TEXT_PRIMARY = "#1F2937"    # Gris foncé
    TEXT_SECONDARY = "#6B7280"  # Gris moyen
    TEXT_TERTIARY = "#9CA3AF"   # Gris clair

    # Bordures
    BORDER = "#E5E7EB"          # Gris très clair
    BORDER_HOVER = "#D1D5DB"    # Gris clair

    # Actions
    PRIMARY = "#007AFF"         # Bleu système Apple
    PRIMARY_HOVER = "#0051D5"   # Bleu foncé

    # États
    SUCCESS = "#34C759"         # Vert Apple
    WARNING = "#FF9500"         # Orange Apple
    ERROR = "#FF3B30"           # Rouge Apple

    # Overlay
    SHADOW = "rgba(0, 0, 0, 0.05)"
    SHADOW_HOVER = "rgba(0, 0, 0, 0.1)"


class AppSpacing:
    """Espacements cohérents."""

    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48


class AppBorderRadius:
    """Rayons de bordure."""

    SM = 8
    MD = 12
    LG = 16
    XL = 24
    FULL = 9999


class AppFonts:
    """Tailles de police."""

    # Titres
    H1 = 32
    H2 = 24
    H3 = 20
    H4 = 18

    # Corps
    BODY_LG = 16
    BODY = 14
    BODY_SM = 12

    # Détails
    CAPTION = 11
    TINY = 10


def get_theme() -> ft.Theme:
    """
    Retourne le thème Flet personnalisé.

    Returns:
        Theme Flet configuré avec les couleurs minimalistes
    """
    return ft.Theme(
        color_scheme_seed=AppColors.PRIMARY,
        use_material3=True,
    )


def create_card(
    content: ft.Control,
    padding: int = AppSpacing.MD,
    border_radius: int = AppBorderRadius.MD,
) -> ft.Container:
    """
    Crée une carte avec l'esthétique Apple.

    Args:
        content: Contenu de la carte
        padding: Espacement interne
        border_radius: Rayon de bordure

    Returns:
        Container stylisé comme une carte
    """
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=border_radius,
        bgcolor=AppColors.SURFACE,
        border=ft.border.all(1, AppColors.BORDER),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=AppColors.SHADOW,
            offset=ft.Offset(0, 2),
        ),
    )


def create_button(
    text: str,
    on_click=None,
    icon: str = None,
    primary: bool = True,
    width: int = None,
) -> ft.Container:
    """
    Crée un bouton avec le style Apple.

    Args:
        text: Texte du bouton
        on_click: Callback au clic
        icon: Icône optionnelle (Material Icons)
        primary: Si True, style primaire (bleu), sinon secondaire
        width: Largeur personnalisée

    Returns:
        Container stylisé comme un bouton
    """
    bg_color = AppColors.PRIMARY if primary else AppColors.SURFACE
    text_color = AppColors.SURFACE if primary else AppColors.TEXT_PRIMARY
    border_color = None if primary else AppColors.BORDER

    content_controls = []
    if icon:
        content_controls.append(
            ft.Icon(icon, size=20, color=text_color)
        )
    content_controls.append(
        ft.Text(
            text,
            size=AppFonts.BODY,
            weight=ft.FontWeight.W_500,
            color=text_color,
        )
    )

    return ft.Container(
        content=ft.Row(
            content_controls,
            spacing=AppSpacing.SM,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=AppSpacing.LG, vertical=AppSpacing.SM),
        border_radius=AppBorderRadius.SM,
        bgcolor=bg_color,
        border=ft.border.all(1, border_color) if border_color else None,
        ink=True,
        on_click=on_click,
        width=width,
    )
