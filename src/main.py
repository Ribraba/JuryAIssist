"""
Point d'entrée de l'application JuryAIssist avec Flet.

Lance l'interface graphique moderne et minimaliste.
"""
import flet as ft
from src.gui_flet.main_window import MainWindow


def main(page: ft.Page):
    """
    Point d'entrée de l'application Flet.

    Args:
        page: Page Flet
    """
    # Créer la fenêtre principale
    app = MainWindow(page)

    # Gérer la fermeture propre
    def on_window_event(e):
        if e.data == "close":
            app.cleanup()

    page.on_window_event = on_window_event


if __name__ == "__main__":
    # Lancer l'application Flet
    ft.app(target=main, view=ft.AppView.FLET_APP)
