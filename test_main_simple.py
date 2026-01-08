"""
Test de la version simplifiée de MainWindow.
"""
import flet as ft
from src.gui_flet.main_window_simple import MainWindowSimple

def main(page: ft.Page):
    print("🚀 Lancement de l'application simplifiée...")
    app = MainWindowSimple(page)
    print("✅ Application créée!")

if __name__ == "__main__":
    ft.app(target=main)
