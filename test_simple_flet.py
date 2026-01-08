"""
Test ultra-simple pour vérifier que Flet fonctionne.
"""
import flet as ft

def main(page: ft.Page):
    page.title = "Test Simple"
    page.bgcolor = "#F9FAFB"

    # Créer des éléments simples
    text = ft.Text("Hello Flet!", size=30, color="blue")
    button = ft.ElevatedButton("Click me", on_click=lambda e: print("Clicked!"))

    # Ajouter à la page
    page.add(text)
    page.add(button)

if __name__ == "__main__":
    ft.app(target=main)
