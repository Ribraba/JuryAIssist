"""
Fenêtre principale de l'application Flet - Version fonctionnelle simplifiée.
"""
import flet as ft
from src.gui_flet.theme import AppColors, AppSpacing

class MainWindow:
    """Fenêtre principale de l'application."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self._build_ui_simple()

    def _setup_page(self):
        """Configure la page."""
        self.page.title = "JuryAIssist - Test Simple"
        self.page.bgcolor = AppColors.BACKGROUND

    def _build_ui_simple(self):
        """Construit une UI ultra-simple."""
        print("🔍 Début construction UI...")

        # Test 1: Sidebar simple
        sidebar = ft.Container(
            content=ft.Column([
                ft.Text("JuryAIssist", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Transcription audio", size=12),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text("Importer un fichier", size=14),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=10,
                    border_radius=8,
                ),
            ]),
            width=280,
            bgcolor=ft.Colors.WHITE,
            padding=20,
            expand=False,  # Ne pas étendre verticalement
        )
        print("✓ Sidebar créée")

        # Test 2: Zone de contenu simple
        content = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Zone de contenu", size=20),
                    ft.Container(
                        content=ft.TextField(
                            multiline=True,
                            min_lines=10,
                            hint_text="La transcription apparaîtra ici...",
                            border_color=ft.Colors.GREY_300,
                            expand=True,  # Prend toute la largeur
                        ),
                        bgcolor=ft.Colors.WHITE,
                        padding=20,
                        border_radius=12,
                        expand=True,  # Prend tout l'espace vertical disponible
                    ),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Row([
                            ft.Text("⏮️", size=24),
                            ft.Text("▶️", size=32),
                            ft.Text("⏭️", size=24),
                            ft.Text("⏹️", size=24),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.WHITE,
                        padding=20,
                        border_radius=12,
                        height=80,
                    ),
                ],
                expand=True,  # La colonne prend toute la hauteur
            ),
            padding=20,
            expand=True,  # Prend tout l'espace horizontal disponible
        )
        print("✓ Content créé")

        # Test 3: Row principal
        main_row = ft.Row(
            [sidebar, content],
            spacing=0,
            expand=True,  # Prend toute la hauteur de la page
        )
        print("✓ Main row créé")

        # Ajouter à la page
        self.page.add(main_row)
        print("✓ Ajouté à la page")

        # Update explicite
        self.page.update()
        print("✓ Page.update() appelé")

        print("✅ Construction UI terminée!")
