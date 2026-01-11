#!/usr/bin/env python3
"""
Test standalone pour reproduire le bug de blocage lors de la transcription.

Ce script ne nécessite pas pytest et peut être exécuté directement.
"""
import sys
import time
import threading
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

from src.gui_pyside6.main_window_modern import ModernMainWindow, TranscriptionItem
from src.transcription.transcriber import (
    TranscriptionResult,
    TranscriptionSegment,
    TranscriptionStatus,
)


def test_transcription_blocking():
    """Test que la transcription ne bloque pas l'UI."""
    print("\n" + "=" * 70)
    print("TEST: Blocage de l'UI pendant la transcription")
    print("=" * 70)

    app = QApplication.instance() or QApplication(sys.argv)

    # Create window
    window = ModernMainWindow()
    window.show()
    app.processEvents()

    print("✓ Fenêtre créée")

    # Create mock transcription result
    mock_result = TranscriptionResult(
        segments=[
            TranscriptionSegment(
                start=0.0, end=2.5, text="Bonjour ceci est un test", confidence=0.95
            ),
            TranscriptionSegment(
                start=2.5,
                end=5.0,
                text="de transcription automatique",
                confidence=0.92,
            ),
            TranscriptionSegment(
                start=5.0, end=8.0, text="avec PySide6 et Whisper", confidence=0.93
            ),
        ],
        full_text="Bonjour ceci est un test de transcription automatique avec PySide6 et Whisper",
        language="fr",
        status=TranscriptionStatus.COMPLETED,
    )

    print(f"✓ Résultat mock créé: {len(mock_result.segments)} segments")

    # Measure UI responsiveness
    ui_response_times = []
    max_blocking_time = 0

    def check_ui_responsiveness():
        """Vérifie si l'UI est responsive."""
        start = time.time()
        app.processEvents()
        elapsed = time.time() - start
        ui_response_times.append(elapsed)
        return elapsed

    # Mock WhisperTranscriber
    with patch("src.gui_pyside6.main_window_modern.WhisperTranscriber") as MockTranscriber:
        mock_instance = MockTranscriber.return_value

        # Simulate slow transcription (1 second delay)
        def slow_transcribe(*args, **kwargs):
            print("  → Simulation transcription (1s)...")
            time.sleep(1.0)
            return mock_result

        mock_instance.transcribe = slow_transcribe

        # Mock QMessageBox to avoid blocking
        with patch.object(QMessageBox, "information") as mock_info, \
             patch.object(QMessageBox, "critical") as mock_critical:

            # Create fake audio file
            transcription = TranscriptionItem("fake_audio.mp3", "fake_audio.mp3")
            window.transcriptions.append(transcription)
            window.current_transcription = transcription

            print("✓ Transcription item créé")

            # Start transcription
            print("\n→ Lancement de la transcription...")
            window._start_transcription()

            # Check UI responsiveness during transcription
            print("\n→ Vérification de la réactivité de l'UI...")
            for i in range(20):  # Check for 2 seconds (20 * 100ms)
                elapsed = check_ui_responsiveness()
                max_blocking_time = max(max_blocking_time, elapsed)

                if elapsed > 0.1:
                    print(
                        f"  ⚠️  Temps de réponse élevé: {elapsed*1000:.2f}ms (iteration {i})"
                    )

                time.sleep(0.1)

            # Wait for transcription to complete
            print("\n→ Attente de la complétion...")
            timeout = 50  # 5 seconds
            completed = False
            while timeout > 0:
                app.processEvents()
                editor_text = window.text_editor.toPlainText()
                if editor_text and len(editor_text) > 0:
                    completed = True
                    print(f"✓ Texte inséré dans l'éditeur ({len(editor_text)} caractères)")
                    break
                timeout -= 1
                time.sleep(0.1)

            # Results
            print("\n" + "=" * 70)
            print("RÉSULTATS")
            print("=" * 70)

            if not completed:
                print("❌ ÉCHEC: La transcription n'a pas complété dans le temps imparti")
                window.close()
                return False

            # Check UI responsiveness
            avg_response = sum(ui_response_times) / len(ui_response_times)
            print(f"Temps de réponse UI moyen: {avg_response*1000:.2f}ms")
            print(f"Temps de réponse UI max: {max_blocking_time*1000:.2f}ms")

            # UI should respond within 100ms
            if max_blocking_time > 0.15:
                print(
                    f"⚠️  AVERTISSEMENT: UI bloquée pendant {max_blocking_time*1000:.2f}ms"
                )
                ui_blocked = True
            else:
                print("✓ UI est restée réactive")
                ui_blocked = False

            # Check if text was inserted
            editor_text = window.text_editor.toPlainText()
            text_inserted = (
                len(editor_text) > 0
                and "Bonjour" in editor_text
                and "[" in editor_text  # Timestamp
            )

            if text_inserted:
                print(f"✓ Texte correctement inséré: {len(editor_text)} caractères")
                print(f"  Extraits: {editor_text[:80]}...")
            else:
                print(f"❌ ÉCHEC: Texte non inséré ou incorrect")
                print(f"  Contenu éditeur: {editor_text[:200]}")

            # Check if success message was shown
            if mock_info.called:
                print("✓ Message de succès affiché")
            else:
                print("⚠️  Message de succès non affiché")

            # Final verdict
            print("\n" + "=" * 70)
            if text_inserted and not ui_blocked:
                print("✅ TEST RÉUSSI: Transcription fonctionne sans bloquer l'UI")
                success = True
            elif text_inserted and ui_blocked:
                print("⚠️  TEST PARTIEL: Transcription OK mais UI bloquée")
                success = False
            else:
                print("❌ TEST ÉCHOUÉ: Problème de transcription")
                success = False
            print("=" * 70 + "\n")

            window.close()
            return success


def test_large_transcription():
    """Test avec une grosse transcription (1000 segments)."""
    print("\n" + "=" * 70)
    print("TEST: Insertion de grosse transcription (1000 segments)")
    print("=" * 70)

    app = QApplication.instance() or QApplication(sys.argv)

    window = ModernMainWindow()
    window.show()
    app.processEvents()

    # Create large result
    segments = []
    for i in range(1000):
        segments.append(
            TranscriptionSegment(
                start=i * 3.6,
                end=(i + 1) * 3.6,
                text=f"Segment numéro {i} avec du texte de test pour simuler une longue transcription",
                confidence=0.9,
            )
        )

    mock_result = TranscriptionResult(
        segments=segments,
        full_text=" ".join([s.text for s in segments]),
        language="fr",
        status=TranscriptionStatus.COMPLETED,
    )

    print(f"✓ Résultat mock créé: {len(segments)} segments")

    with patch("src.gui_pyside6.main_window_modern.WhisperTranscriber") as MockTranscriber:
        mock_instance = MockTranscriber.return_value
        mock_instance.transcribe.return_value = mock_result

        with patch.object(QMessageBox, "information"), \
             patch.object(QMessageBox, "critical"):

            transcription = TranscriptionItem("long_audio.mp3", "long_audio.mp3")
            window.transcriptions.append(transcription)
            window.current_transcription = transcription

            # Measure insertion time
            print("\n→ Lancement transcription...")
            start_time = time.time()
            window._start_transcription()

            # Wait for completion
            timeout = 100
            completed = False
            while timeout > 0:
                app.processEvents()
                if window.text_editor.toPlainText():
                    completed = True
                    break
                timeout -= 1
                time.sleep(0.1)

            insertion_time = time.time() - start_time

            print("\n" + "=" * 70)
            print("RÉSULTATS")
            print("=" * 70)

            if not completed:
                print("❌ ÉCHEC: Transcription non complétée")
                window.close()
                return False

            editor_text = window.text_editor.toPlainText()
            print(f"Temps d'insertion: {insertion_time:.2f}s")
            print(f"Taille du texte: {len(editor_text)} caractères")
            print(f"Contient segment 0: {'✓' if 'Segment numéro 0' in editor_text else '❌'}")
            print(f"Contient segment 999: {'✓' if 'Segment numéro 999' in editor_text else '❌'}")

            # Should complete within 10 seconds
            if insertion_time < 10.0:
                print(f"✓ Temps d'insertion acceptable ({insertion_time:.2f}s)")
                success = True
            else:
                print(f"⚠️  Temps d'insertion trop long ({insertion_time:.2f}s)")
                success = False

            print("=" * 70 + "\n")

            window.close()
            return success


def main():
    """Run all tests."""
    print("\n" + "█" * 70)
    print("TEST E2E: WORKFLOW DE TRANSCRIPTION")
    print("█" * 70)

    results = []

    # Test 1: Basic transcription
    try:
        result1 = test_transcription_blocking()
        results.append(("Transcription basique", result1))
    except Exception as e:
        print(f"\n❌ ERREUR TEST 1: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Transcription basique", False))

    # Test 2: Large transcription
    try:
        result2 = test_large_transcription()
        results.append(("Grosse transcription", result2))
    except Exception as e:
        print(f"\n❌ ERREUR TEST 2: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Grosse transcription", False))

    # Summary
    print("\n" + "█" * 70)
    print("RÉSUMÉ DES TESTS")
    print("█" * 70)

    for test_name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{status}: {test_name}")

    all_passed = all(r[1] for r in results)
    if all_passed:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS 🎉\n")
        return 0
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ ⚠️\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
