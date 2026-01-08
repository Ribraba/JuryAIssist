"""
Composant lecteur audio moderne - Style minimaliste.

Affiche:
- Timeline de lecture avec position actuelle
- Contrôles: Play/Pause, Skip, Stop
- Contrôles de vitesse et volume
- Durée actuelle / totale
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
from src.audio.timeline import TimeUtils


class AudioPlayer(ft.Container):
    """
    Lecteur audio avec contrôles et timeline.

    Design minimaliste avec boutons ronds et timeline élégante.
    """

    def __init__(
        self,
        on_play: Optional[Callable] = None,
        on_pause: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        on_skip_forward: Optional[Callable] = None,
        on_skip_backward: Optional[Callable] = None,
        on_seek: Optional[Callable[[float], None]] = None,
        on_speed_change: Optional[Callable[[float], None]] = None,
        on_volume_change: Optional[Callable[[int], None]] = None,
    ):
        """
        Initialise le lecteur audio.

        Args:
            on_play: Callback lecture
            on_pause: Callback pause
            on_stop: Callback stop
            on_skip_forward: Callback avancer
            on_skip_backward: Callback reculer
            on_seek: Callback changement de position
            on_speed_change: Callback changement de vitesse
            on_volume_change: Callback changement de volume
        """
        self.on_play = on_play
        self.on_pause = on_pause
        self.on_stop = on_stop
        self.on_skip_forward = on_skip_forward
        self.on_skip_backward = on_skip_backward
        self.on_seek = on_seek
        self.on_speed_change = on_speed_change
        self.on_volume_change = on_volume_change

        # État
        self.is_playing = False
        self.current_position = 0.0
        self.total_duration = 0.0
        self.current_speed = 1.0
        self.current_volume = 70

        # Widgets
        self.play_pause_btn = self._create_play_pause_button()
        self.time_label = ft.Text(
            "00:00 / 00:00",
            size=AppFonts.BODY_SM,
            color=AppColors.TEXT_SECONDARY,
        )
        self.timeline_slider = ft.Slider(
            min=0,
            max=100,
            value=0,
            on_change=self._on_slider_change,
            active_color=AppColors.PRIMARY,
            inactive_color=AppColors.BORDER,
        )
        self.speed_dropdown = ft.Dropdown(
            width=100,
            value="1.0x",
            options=[
                ft.dropdown.Option("0.5x"),
                ft.dropdown.Option("0.75x"),
                ft.dropdown.Option("1.0x"),
                ft.dropdown.Option("1.25x"),
                ft.dropdown.Option("1.5x"),
                ft.dropdown.Option("2.0x"),
            ],
            on_select=self._on_speed_change,
            text_size=AppFonts.BODY_SM,
        )
        self.volume_slider = ft.Slider(
            min=0,
            max=100,
            value=self.current_volume,
            width=120,
            on_change=self._on_volume_change,
            active_color=AppColors.PRIMARY,
            inactive_color=AppColors.BORDER,
        )

        super().__init__(
            content=self._build_content(),
            padding=AppSpacing.MD,
        )

    def _build_content(self) -> ft.Column:
        """Construit le contenu du lecteur."""
        return ft.Column(
            [
                # Timeline et temps
                ft.Column(
                    [
                        self.timeline_slider,
                        self.time_label,
                    ],
                    spacing=AppSpacing.XS,
                ),

                ft.Container(height=AppSpacing.SM),

                # Contrôles principaux
                ft.Row(
                    [
                        # Boutons de lecture
                        ft.Row(
                            [
                                self._create_control_button(
                                    "replay_5",
                                    lambda _: self.on_skip_backward() if self.on_skip_backward else None,
                                    "Reculer 5s",
                                ),
                                self.play_pause_btn,
                                self._create_control_button(
                                    "forward_5",
                                    lambda _: self.on_skip_forward() if self.on_skip_forward else None,
                                    "Avancer 5s",
                                ),
                                self._create_control_button(
                                    "stop",
                                    lambda _: self.on_stop() if self.on_stop else None,
                                    "Stop",
                                ),
                            ],
                            spacing=AppSpacing.SM,
                        ),

                        # Spacer
                        ft.Container(expand=True),

                        # Vitesse
                        ft.Row(
                            [
                                ft.Icon(
                                    "speed",
                                    size=20,
                                    color=AppColors.TEXT_SECONDARY,
                                ),
                                self.speed_dropdown,
                            ],
                            spacing=AppSpacing.XS,
                        ),

                        # Volume
                        ft.Row(
                            [
                                ft.Icon(
                                    "volume_up",
                                    size=20,
                                    color=AppColors.TEXT_SECONDARY,
                                ),
                                self.volume_slider,
                            ],
                            spacing=AppSpacing.XS,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=0,
        )

    def _create_play_pause_button(self) -> ft.Container:
        """Crée le bouton Play/Pause principal."""
        return ft.Container(
            content=ft.Icon(
                "play_arrow",
                size=32,
                color=AppColors.SURFACE,
            ),
            width=56,
            height=56,
            border_radius=AppBorderRadius.FULL,
            bgcolor=AppColors.PRIMARY,
            alignment=ft.alignment.Alignment(0, 0),
            ink=True,
            on_click=self._on_play_pause_click,
        )

    def _create_control_button(
        self,
        icon: str,
        on_click: Callable,
        tooltip: str,
    ) -> ft.Container:
        """
        Crée un bouton de contrôle secondaire.

        Args:
            icon: Icône Material
            on_click: Callback au clic
            tooltip: Info-bulle

        Returns:
            Container stylisé comme un bouton
        """
        return ft.Container(
            content=ft.Icon(
                icon,
                size=24,
                color=AppColors.TEXT_PRIMARY,
            ),
            width=48,
            height=48,
            border_radius=AppBorderRadius.FULL,
            bgcolor=AppColors.SURFACE,
            border=ft.border.all(1, AppColors.BORDER),
            alignment=ft.alignment.Alignment(0, 0),
            ink=True,
            on_click=on_click,
            tooltip=tooltip,
        )

    def _on_play_pause_click(self, e):
        """Gère le clic sur Play/Pause."""
        self.is_playing = not self.is_playing
        self._update_play_pause_icon()

        if self.is_playing and self.on_play:
            self.on_play()
        elif not self.is_playing and self.on_pause:
            self.on_pause()

    def _update_play_pause_icon(self):
        """Met à jour l'icône Play/Pause."""
        icon_name = "pause" if self.is_playing else "play_arrow"
        self.play_pause_btn.content = ft.Icon(
            icon_name,
            size=32,
            color=AppColors.SURFACE,
        )
        if self.page:
            self.page.update()

    def _on_slider_change(self, e):
        """Gère le changement de position via le slider."""
        if self.on_seek:
            position = (e.control.value / 100) * self.total_duration
            self.on_seek(position)

    def _on_speed_change(self, e):
        """Gère le changement de vitesse."""
        speed_str = e.control.value.replace("x", "")
        speed = float(speed_str)
        self.current_speed = speed
        if self.on_speed_change:
            self.on_speed_change(speed)

    def _on_volume_change(self, e):
        """Gère le changement de volume."""
        volume = int(e.control.value)
        self.current_volume = volume
        if self.on_volume_change:
            self.on_volume_change(volume)

    def set_position(self, position: float):
        """
        Met à jour la position actuelle.

        Args:
            position: Position en secondes
        """
        self.current_position = position
        if self.total_duration > 0:
            self.timeline_slider.value = (position / self.total_duration) * 100
        self._update_time_label()
        if self.page:
            self.page.update()

    def set_duration(self, duration: float):
        """
        Met à jour la durée totale.

        Args:
            duration: Durée en secondes
        """
        self.total_duration = duration
        self._update_time_label()
        if self.page:
            self.page.update()

    def set_playing_state(self, playing: bool):
        """
        Met à jour l'état de lecture.

        Args:
            playing: True si en lecture
        """
        self.is_playing = playing
        self._update_play_pause_icon()

    def _update_time_label(self):
        """Met à jour le label de temps."""
        current = TimeUtils.format_time(self.current_position)
        total = TimeUtils.format_time(self.total_duration)
        self.time_label.value = f"{current} / {total}"
