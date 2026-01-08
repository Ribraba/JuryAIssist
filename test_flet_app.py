"""
Test simple de l'application Flet pour diagnostiquer les erreurs.
"""
import sys
import traceback

try:
    print("1. Import de flet...")
    import flet as ft
    print("✓ Flet importé")

    print("\n2. Import des modules métier...")
    from src.audio.controller import AudioController
    from src.audio.vlc_player import VLCAudioPlayer
    print("✓ Modules audio importés")

    from src.transcription.whisper_transcriber import WhisperTranscriber
    print("✓ Modules transcription importés")

    try:
        from src.devices.olympus_pedal import OlympusPedal
        print("✓ Modules devices importés")
    except Exception as e:
        print(f"⚠ Devices non disponibles (normal si pédale absente): {e}")

    print("\n3. Import de l'interface Flet...")
    from src.gui_flet.main_window import MainWindow
    print("✓ Interface Flet importée")

    print("\n4. Tentative de création de l'app...")
    def test_app(page: ft.Page):
        try:
            print("   - Configuration de la page...")
            page.title = "Test"
            print("   ✓ Page configurée")

            print("   - Création de la MainWindow...")
            app = MainWindow(page)
            print("   ✓ MainWindow créée")

            print("\n✅ TOUT FONCTIONNE!")

        except Exception as e:
            print(f"\n❌ ERREUR dans test_app:")
            print(f"   {type(e).__name__}: {e}")
            traceback.print_exc()

    print("\n5. Lancement de Flet...")
    print("   (Fermez la fenêtre pour terminer)\n")
    ft.app(target=test_app)

except Exception as e:
    print(f"\n❌ ERREUR FATALE:")
    print(f"   {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
