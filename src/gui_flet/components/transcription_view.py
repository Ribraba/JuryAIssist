"""
Vue de transcription scrollable avec synchronisation - Style minimaliste.

Affiche les segments de transcription avec:
- Timestamps cliquables
- Surlignage du segment actuel
- Navigation par clic
"""
import flet as ft
from typing import Callable, Optional, List

from src.gui_flet.theme import (
    AppColors,
    AppSpacing,
    AppBorderRadius,
    AppFonts,
)
from src.transcription.transcriber import TranscriptionSegment
from src.audio.timeline import TimeUtils


class TranscriptionView(ft.Container):
    """
    Vue scrollable de la transcription avec synchronisation.

    Affiche les segments avec timestamps et permet la navigation.
    """

    def __init__(
        self,
        on_segment_click: Optional[Callable[[float], None]] = None,
    ):
        """
        Initialise la vue de transcription.

        Args:
            on_segment_click: Callback lors du clic sur un segment
        """
        self.on_segment_click = on_segment_click

        # État
        self.segments: List[TranscriptionSegment] = []
        self.current_position = 0.0

        # Liste des segments
        self.segments_list = ft.Column(
            spacing=AppSpacing.XS,
            scroll=ft.ScrollMode.AUTO,
        )

        super().__init__(
            content=self._build_content(),
            height=200,
            border_radius=AppBorderRadius.MD,
            border=ft.border.all(1, AppColors.BORDER),
            padding=AppSpacing.MD,
            bgcolor=AppColors.SURFACE,
        )

    def _build_content(self) -> ft.Column:
        """Construit le contenu de la vue."""
        return ft.Column(
            [
                # Label
                ft.Text(
                    "Transcription",
                    size=AppFonts.BODY,
                    weight=ft.FontWeight.W_600,
                    color=AppColors.TEXT_PRIMARY,
                ),

                ft.Container(height=AppSpacing.XS),

                # Liste scrollable des segments
                ft.Container(
                    content=self.segments_list,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

    def set_segments(self, segments: List[TranscriptionSegment]):
        """
        Met à jour les segments de transcription.

        Args:
            segments: Liste des segments
        """
        self.segments = segments
        self.segments_list.controls.clear()

        if not segments:
            # Message par défaut
            self.segments_list.controls.append(
                ft.Text(
                    "Aucune transcription disponible",
                    size=AppFonts.BODY_SM,
                    color=AppColors.TEXT_TERTIARY,
                    italic=True,
                )
            )
        else:
            for seg in segments:
                segment_item = self._create_segment_item(seg)
                self.segments_list.controls.append(segment_item)

        if self.page:
            self.page.update()

    def _create_segment_item(self, segment: TranscriptionSegment) -> ft.Container:
        """
        Crée un élément de segment.

        Args:
            segment: Segment de transcription

        Returns:
            Container représentant le segment
        """
        timestamp_str = TimeUtils.seconds_to_timestamp(segment.start)

        # Déterminer si c'est le segment actuel
        is_active = (
            segment.start <= self.current_position < segment.end
        )

        bg_color = ft.Colors.BLUE_50 if is_active else None
        text_color = AppColors.PRIMARY if is_active else AppColors.TEXT_PRIMARY

        return ft.Container(
            content=ft.Row(
                [
                    # Timestamp
                    ft.Container(
                        content=ft.Text(
                            timestamp_str,
                            size=AppFonts.CAPTION,
                            weight=ft.FontWeight.W_500,
                            color=AppColors.PRIMARY,
                        ),
                        width=60,
                    ),
                    # Texte
                    ft.Text(
                        segment.text,
                        size=AppFonts.BODY_SM,
                        color=text_color,
                        expand=True,
                    ),
                ],
                spacing=AppSpacing.SM,
            ),
            padding=AppSpacing.SM,
            border_radius=AppBorderRadius.SM,
            bgcolor=bg_color,
            ink=True,
            on_click=lambda _, s=segment: self._on_segment_clicked(s),
        )

    def _on_segment_clicked(self, segment: TranscriptionSegment):
        """
        Gère le clic sur un segment.

        Args:
            segment: Segment cliqué
        """
        if self.on_segment_click:
            self.on_segment_click(segment.start)

    def set_position(self, position: float):
        """
        Met à jour la position actuelle et surligne le segment correspondant.

        Args:
            position: Position en secondes
        """
        self.current_position = position

        # Reconstruire les segments avec le nouveau surlignage
        # (optimisation possible: ne reconstruire que le segment changé)
        self.set_segments(self.segments)
