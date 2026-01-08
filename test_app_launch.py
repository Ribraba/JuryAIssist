"""
Test de lancement rapide de l'application pour vérifier les imports.
"""
import sys

try:
    print("1. Import de flet...")
    import flet as ft
    print("   ✓ Flet OK")

    print("\n2. Import des composants...")
    from src.gui_flet.main_window import MainWindow
    print("   ✓ MainWindow OK")

    print("\n3. Création d'une page de test...")
    def test_main(page: ft.Page):
        page.title = "Test"
        print("   ✓ Page créée")
        print("   ✓ Création de MainWindow...")
        try:
            app = MainWindow(page)
            print("   ✓ MainWindow créée avec succès!")
            print("\n✅ TOUS LES TESTS PASSENT!")
            print("\nVous pouvez maintenant lancer:")
            print("  python -m src.main")
        except Exception as e:
            print(f"   ✗ Erreur: {e}")
            import traceback
            traceback.print_exc()

    # Ne pas afficher la fenêtre
    print("\n4. Test de création...")
    ft.app(target=test_main, view=ft.AppView.FLET_APP_HIDDEN)

except KeyboardInterrupt:
    print("\n\n⚠ Test interrompu par l'utilisateur")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
