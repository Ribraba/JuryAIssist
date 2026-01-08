"""
Sidebar moderne avec navigation - Style minimaliste Apple.

La sidebar contient:
- Logo/titre de l'application
- Liste des fichiers audio importés
- Actions: Importer, Paramètres
"""
import flet as ft
from typing import Callable, Optional

from src.gui_flet.theme import (
    AppColors,
    AppSpacing,
    AppBorderRadius,
    AppFonts,
)


class Sidebar(ft.Container):
    """
    Sidebar gauche de l'application.

    Affiche la liste des fichiers et les actions principales.
    """

    def __init__(
        self,
        on_import_clicked: Optional[Callable] = None,
        on_settings_clicked: Optional[Callable] = None,
        on_file_selected: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialise la sidebar.

        Args:
            on_import_clicked: Callback lors du clic sur Importer
            on_settings_clicked: Callback lors du clic sur Paramètres
            on_file_selected: Callback lors de la sélection d'un fichier
        """
        self.on_import_clicked = on_import_clicked
        self.on_settings_clicked = on_settings_clicked
        self.on_file_selected = on_file_selected

        # Liste des fichiers
        self.files_list = ft.Column(
            spacing=AppSpacing.XS,
            scroll=ft.ScrollMode.AUTO,
        )

        super().__init__(
            content=self._build_content(),
            width=280,
            bgcolor=AppColors.SURFACE,
            border=ft.border.only(right=ft.BorderSide(1, AppColors.BORDER)),
            padding=AppSpacing.MD,
        )

    def _build_content(self) -> ft.Column:
        """Construit le contenu de la sidebar."""
        return ft.Column(
            [
                # En-tête avec logo/titre
                self._build_header(),

                ft.Divider(height=AppSpacing.LG, color=AppColors.BORDER),

                # Bouton Importer
                self._build_import_button(),

                ft.Container(height=AppSpacing.SM),

                # Label "Fichiers"
                ft.Text(
                    "Fichiers",
                    size=AppFonts.CAPTION,
                    weight=ft.FontWeight.W_600,
                    color=AppColors.TEXT_TERTIARY,
                ),

                ft.Container(height=AppSpacing.XS),

                # Liste des fichiers
                ft.Container(
                    content=self.files_list,
                    expand=True,
                ),

                ft.Divider(height=AppSpacing.LG, color=AppColors.BORDER),

                # Bouton Paramètres
                self._build_settings_button(),
            ],
            spacing=0,
            expand=True,
        )

    def _build_header(self) -> ft.Container:
        """Construit l'en-tête de la sidebar."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        "gavel",
                        size=32,
                        color=AppColors.PRIMARY,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                "JuryAIssist",
                                size=AppFonts.H4,
                                weight=ft.FontWeight.W_600,
                                color=AppColors.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Transcription audio",
                                size=AppFonts.CAPTION,
                                color=AppColors.TEXT_SECONDARY,
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=AppSpacing.SM,
            ),
            padding=AppSpacing.SM,
        )

    def _build_import_button(self) -> ft.Container:
        """Construit le bouton d'import."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        "add_circle_outline",
                        size=20,
                        color=AppColors.PRIMARY,
                    ),
                    ft.Text(
                        "Importer un fichier",
                        size=AppFonts.BODY,
                        weight=ft.FontWeight.W_500,
                        color=AppColors.PRIMARY,
                    ),
                ],
                spacing=AppSpacing.SM,
            ),
            padding=AppSpacing.SM,
            border_radius=AppBorderRadius.SM,
            bgcolor=ft.Colors.BLUE_50,
            ink=True,
            on_click=lambda _: self.on_import_clicked() if self.on_import_clicked else None,
        )

    def _build_settings_button(self) -> ft.Container:
        """Construit le bouton des paramètres."""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        "settings",
                        size=20,
                        color=AppColors.TEXT_SECONDARY,
                    ),
                    ft.Text(
                        "Paramètres",
                        size=AppFonts.BODY,
                        color=AppColors.TEXT_SECONDARY,
                    ),
                ],
                spacing=AppSpacing.SM,
            ),
            padding=AppSpacing.SM,
            border_radius=AppBorderRadius.SM,
            ink=True,
            on_click=lambda _: self.on_settings_clicked() if self.on_settings_clicked else None,
        )

    def add_file(self, filename: str, selected: bool = False):
        """
        Ajoute un fichier à la liste.

        Args:
            filename: Nom du fichier
            selected: Si True, marque le fichier comme sélectionné
        """
        file_item = self._create_file_item(filename, selected)
        self.files_list.controls.append(file_item)
        if self.page:
            self.page.update()

    def clear_files(self):
        """Vide la liste des fichiers."""
        self.files_list.controls.clear()
        if self.page:
            self.page.update()

    def _create_file_item(self, filename: str, selected: bool) -> ft.Container:
        """
        Crée un élément de fichier.

        Args:
            filename: Nom du fichier
            selected: Si True, affiche comme sélectionné

        Returns:
            Container représentant le fichier
        """
        bg_color = ft.Colors.BLUE_50 if selected else None
        text_color = AppColors.PRIMARY if selected else AppColors.TEXT_PRIMARY
        icon_color = AppColors.PRIMARY if selected else AppColors.TEXT_SECONDARY

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(
                        "audiotrack",
                        size=18,
                        color=icon_color,
                    ),
                    ft.Text(
                        filename,
                        size=AppFonts.BODY_SM,
                        color=text_color,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        expand=True,
                    ),
                ],
                spacing=AppSpacing.SM,
            ),
            padding=AppSpacing.SM,
            border_radius=AppBorderRadius.SM,
            bgcolor=bg_color,
            ink=True,
            on_click=lambda _: self.on_file_selected(filename) if self.on_file_selected else None,
        )
