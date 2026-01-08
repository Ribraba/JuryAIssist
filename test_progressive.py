"""
Test progressif pour déboguer l'interface.
"""
import flet as ft

def main(page: ft.Page):
    page.title = "Test Progressif"
    page.bgcolor = "#F9FAFB"

    print("1. Page créée")

    # Test 1: Texte simple
    text = ft.Text("Étape 1: Texte simple", size=20)
    page.add(text)
    print("2. Texte ajouté")

    # Test 2: Container avec couleur
    container = ft.Container(
        content=ft.Text("Étape 2: Container avec couleur", color="white"),
        bgcolor="blue",
        padding=20,
        width=300,
        height=100,
    )
    page.add(container)
    print("3. Container ajouté")

    # Test 3: Row avec plusieurs éléments
    row = ft.Row([
        ft.Container(
            content=ft.Text("Sidebar", color="white"),
            bgcolor="green",
            width=200,
            height=400,
        ),
        ft.Container(
            content=ft.Text("Content", color="white"),
            bgcolor="orange",
            width=400,
            height=400,
        ),
    ])
    page.add(row)
    print("4. Row ajoutée")

    # Test 4: Column avec expand
    try:
        col = ft.Column(
            [
                ft.Text("Column avec expand"),
                ft.Container(bgcolor="red", height=50, width=200),
            ],
            expand=True,
        )
        page.add(col)
        print("5. Column avec expand ajoutée")
    except Exception as e:
        print(f"5. Erreur avec Column expand: {e}")

    print("✅ Tous les tests passés!")

if __name__ == "__main__":
    ft.app(target=main)
