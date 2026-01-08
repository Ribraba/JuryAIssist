"""
Panneau d'édition de transcription - Style minimaliste.

Affiche:
- Titre du fichier en cours d'édition
- Zone de texte éditable avec la transcription
- Boutons d'export (TXT, DOCX)
"""
import flet as ft
from typing import Callable, Optional

from src.gui_flet.theme import (
    AppColors,
    AppSpacing,
    AppBorderRadius,
    AppFonts,
    create_card,
)


class EditorPanel(ft.Container):
    """
    Panneau d'édition de la transcription.

    Permet de visualiser et éditer le texte transcrit.
    """

    def __init__(
        self,
        on_export_txt: Optional[Callable[[str], None]] = None,
        on_export_docx: Optional[Callable[[str], None]] = None,
    ):
        """
        Initialise le panneau d'édition.

        Args:
            on_export_txt: Callback pour l'export TXT
            on_export_docx: Callback pour l'export DOCX
        """
        self.on_export_txt = on_export_txt
        self.on_export_docx = on_export_docx

        # État
        self.current_filename = "Aucun fichier"

        # Widgets
        self.filename_label = ft.Text(
            self.current_filename,
            size=AppFonts.H3,
            weight=ft.FontWeight.W_600,
            color=AppColors.TEXT_PRIMARY,
        )

        self.editor = ft.TextField(
            multiline=True,
            min_lines=20,
            max_lines=None,
            border_color=AppColors.BORDER,
            focused_border_color=AppColors.PRIMARY,
            text_size=AppFonts.BODY,
            hint_text="La transcription apparaîtra ici...\n\nVous pourrez ensuite l'éditer librement.",
            hint_style=ft.TextStyle(
                color=AppColors.TEXT_TERTIARY,
                size=AppFonts.BODY,
            ),
        )

        super().__init__(
            content=self._build_content(),
            expand=True,
        )

    def _build_content(self) -> ft.Column:
        """Construit le contenu du panneau."""
        return ft.Column(
            [
                # En-tête avec titre et boutons d'export
                ft.Row(
                    [
                        # Icône de fichier + nom
                        ft.Row(
                            [
                                ft.Icon(
                                    "description",
                                    size=28,
                                    color=AppColors.PRIMARY,
                                ),
                                self.filename_label,
                            ],
                            spacing=AppSpacing.SM,
                        ),

                        # Spacer
                        ft.Container(expand=True),

                        # Boutons d'export
                        self._create_export_button(
                            "TXT",
                            "text_snippet",
                            lambda _: self.on_export_txt(self.get_text()) if self.on_export_txt else None,
                        ),
                        self._create_export_button(
                            "DOCX",
                            "article",
                            lambda _: self.on_export_docx(self.get_text()) if self.on_export_docx else None,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                ft.Container(height=AppSpacing.SM),

                # Éditeur de texte
                ft.Container(
                    content=self.editor,
                    expand=True,
                    border_radius=AppBorderRadius.MD,
                    border=ft.border.all(1, AppColors.BORDER),
                    padding=AppSpacing.SM,
                    bgcolor=AppColors.SURFACE,
                ),
            ],
            spacing=0,
            expand=True,
        )

    def _create_export_button(
        self,
        label: str,
        icon: str,
        on_click: Callable,
    ) -> ft.Container:
        """
        Crée un bouton d'export.

        Args:
            label: Label du bouton
            icon: Icône Material
            on_click: Callback au clic

        Returns:
            Container stylisé comme un bouton
        """
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=18, color=AppColors.TEXT_PRIMARY),
                    ft.Text(
                        label,
                        size=AppFonts.BODY_SM,
                        weight=ft.FontWeight.W_500,
                        color=AppColors.TEXT_PRIMARY,
                    ),
                ],
                spacing=AppSpacing.XS,
            ),
            padding=ft.padding.symmetric(
                horizontal=AppSpacing.MD,
                vertical=AppSpacing.SM,
            ),
            border_radius=AppBorderRadius.SM,
            bgcolor=AppColors.SURFACE,
            border=ft.border.all(1, AppColors.BORDER),
            ink=True,
            on_click=on_click,
        )

    def set_filename(self, filename: str):
        """
        Met à jour le nom du fichier affiché.

        Args:
            filename: Nouveau nom de fichier
        """
        self.current_filename = filename
        self.filename_label.value = filename
        if self.page:
            self.page.update()

    def set_text(self, text: str):
        """
        Met à jour le texte de l'éditeur.

        Args:
            text: Nouveau texte
        """
        self.editor.value = text
        if self.page:
            self.page.update()

    def get_text(self) -> str:
        """
        Récupère le texte de l'éditeur.

        Returns:
            Texte actuel
        """
        return self.editor.value or ""
