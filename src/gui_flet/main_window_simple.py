"""
Version simplifiée de MainWindow pour déboguer.
"""
import flet as ft
from src.gui_flet.theme import AppColors, AppSpacing

class MainWindowSimple:
    """Version simplifiée pour déboguer."""

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
        )
        print("✓ Sidebar créée")

        # Test 2: Zone de contenu simple
        content = ft.Container(
            content=ft.Column([
                ft.Text("Zone de contenu", size=20),
                ft.Container(
                    content=ft.Text("Éditeur de transcription", size=14),
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    border_radius=12,
                    height=200,
                ),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Text("Lecteur audio", size=14),
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    border_radius=12,
                    height=100,
                ),
            ]),
            padding=20,
            expand=True,
        )
        print("✓ Content créé")

        # Test 3: Row principal
        main_row = ft.Row(
            [sidebar, content],
            spacing=0,
        )
        print("✓ Main row créé")

        # Ajouter à la page
        self.page.add(main_row)
        print("✓ Ajouté à la page")

        # Update explicite
        self.page.update()
        print("✓ Page.update() appelé")

        print("✅ Construction UI terminée!")
