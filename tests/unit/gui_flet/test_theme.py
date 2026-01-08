"""
Tests unitaires pour le module theme de l'interface Flet.

Teste les constantes de design, la palette de couleurs, et les helpers.
"""
import pytest
import flet as ft

from src.gui_flet.theme import (
    AppColors,
    AppSpacing,
    AppBorderRadius,
    AppFonts,
    get_theme,
    create_card,
    create_button,
)


class TestAppColors:
    """Tests pour la palette de couleurs."""

    def test_background_color_defined(self):
        """Vérifie que la couleur de fond est définie."""
        assert AppColors.BACKGROUND is not None
        assert isinstance(AppColors.BACKGROUND, str)
        assert AppColors.BACKGROUND.startswith("#")

    def test_primary_color_defined(self):
        """Vérifie que la couleur primaire est définie."""
        assert AppColors.PRIMARY == "#007AFF"  # Bleu système Apple

    def test_text_colors_defined(self):
        """Vérifie que toutes les couleurs de texte sont définies."""
        assert AppColors.TEXT_PRIMARY is not None
        assert AppColors.TEXT_SECONDARY is not None
        assert AppColors.TEXT_TERTIARY is not None

    def test_state_colors_defined(self):
        """Vérifie que les couleurs d'état sont définies."""
        assert AppColors.SUCCESS == "#34C759"  # Vert Apple
        assert AppColors.ERROR == "#FF3B30"    # Rouge Apple


class TestAppSpacing:
    """Tests pour les espacements."""

    def test_spacing_values_positive(self):
        """Vérifie que tous les espacements sont positifs."""
        assert AppSpacing.XS > 0
        assert AppSpacing.SM > 0
        assert AppSpacing.MD > 0
        assert AppSpacing.LG > 0
        assert AppSpacing.XL > 0

    def test_spacing_progression(self):
        """Vérifie que les espacements sont progressifs."""
        assert AppSpacing.XS < AppSpacing.SM
        assert AppSpacing.SM < AppSpacing.MD
        assert AppSpacing.MD < AppSpacing.LG
        assert AppSpacing.LG < AppSpacing.XL


class TestAppBorderRadius:
    """Tests pour les rayons de bordure."""

    def test_border_radius_values_positive(self):
        """Vérifie que tous les rayons sont positifs."""
        assert AppBorderRadius.SM > 0
        assert AppBorderRadius.MD > 0
        assert AppBorderRadius.LG > 0
        assert AppBorderRadius.XL > 0

    def test_border_radius_progression(self):
        """Vérifie que les rayons sont progressifs."""
        assert AppBorderRadius.SM < AppBorderRadius.MD
        assert AppBorderRadius.MD < AppBorderRadius.LG
        assert AppBorderRadius.LG < AppBorderRadius.XL

    def test_full_radius_is_very_large(self):
        """Vérifie que FULL est un très grand nombre."""
        assert AppBorderRadius.FULL > 1000


class TestAppFonts:
    """Tests pour les tailles de police."""

    def test_font_sizes_positive(self):
        """Vérifie que toutes les tailles sont positives."""
        assert AppFonts.H1 > 0
        assert AppFonts.BODY > 0
        assert AppFonts.CAPTION > 0

    def test_heading_hierarchy(self):
        """Vérifie la hiérarchie des titres."""
        assert AppFonts.H1 > AppFonts.H2
        assert AppFonts.H2 > AppFonts.H3
        assert AppFonts.H3 > AppFonts.H4

    def test_body_hierarchy(self):
        """Vérifie la hiérarchie du corps de texte."""
        assert AppFonts.BODY_LG > AppFonts.BODY
        assert AppFonts.BODY > AppFonts.BODY_SM


class TestGetTheme:
    """Tests pour la fonction get_theme."""

    def test_returns_theme_object(self):
        """Vérifie que get_theme retourne un objet Theme."""
        theme = get_theme()
        assert theme is not None
        assert isinstance(theme, ft.Theme)

    def test_theme_uses_primary_color(self):
        """Vérifie que le thème utilise la couleur primaire."""
        theme = get_theme()
        assert theme.color_scheme_seed == AppColors.PRIMARY

    def test_theme_uses_material3(self):
        """Vérifie que le thème utilise Material 3."""
        theme = get_theme()
        assert theme.use_material3 is True


class TestCreateCard:
    """Tests pour la fonction create_card."""

    def test_returns_container(self):
        """Vérifie que create_card retourne un Container."""
        content = ft.Text("Test")
        card = create_card(content)
        assert isinstance(card, ft.Container)

    def test_contains_provided_content(self):
        """Vérifie que la carte contient le contenu fourni."""
        content = ft.Text("Test Content")
        card = create_card(content)
        assert card.content == content

    def test_has_default_padding(self):
        """Vérifie que la carte a un padding par défaut."""
        content = ft.Text("Test")
        card = create_card(content)
        assert card.padding == AppSpacing.MD

    def test_respects_custom_padding(self):
        """Vérifie que le padding personnalisé est respecté."""
        content = ft.Text("Test")
        custom_padding = 24
        card = create_card(content, padding=custom_padding)
        assert card.padding == custom_padding

    def test_has_border(self):
        """Vérifie que la carte a une bordure."""
        content = ft.Text("Test")
        card = create_card(content)
        assert card.border is not None

    def test_has_shadow(self):
        """Vérifie que la carte a une ombre."""
        content = ft.Text("Test")
        card = create_card(content)
        assert card.shadow is not None


class TestCreateButton:
    """Tests pour la fonction create_button."""

    def test_returns_container(self):
        """Vérifie que create_button retourne un Container."""
        button = create_button("Test")
        assert isinstance(button, ft.Container)

    def test_has_text(self):
        """Vérifie que le bouton contient du texte."""
        button = create_button("Test Button")
        assert button.content is not None

    def test_primary_button_has_primary_color(self):
        """Vérifie que le bouton primaire a la couleur primaire."""
        button = create_button("Primary", primary=True)
        assert button.bgcolor == AppColors.PRIMARY

    def test_secondary_button_has_surface_color(self):
        """Vérifie que le bouton secondaire a la couleur de surface."""
        button = create_button("Secondary", primary=False)
        assert button.bgcolor == AppColors.SURFACE

    def test_respects_custom_width(self):
        """Vérifie que la largeur personnalisée est respectée."""
        custom_width = 200
        button = create_button("Test", width=custom_width)
        assert button.width == custom_width

    def test_has_on_click_callback(self):
        """Vérifie que le callback on_click est attaché."""
        callback_called = False

        def test_callback(e):
            nonlocal callback_called
            callback_called = True

        button = create_button("Test", on_click=test_callback)
        assert button.on_click == test_callback
