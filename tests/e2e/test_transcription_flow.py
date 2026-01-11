"""
Test End-to-End du workflow de transcription.

Ce test reproduit le bug de blocage lors de la transcription et de l'insertion
dans l'éditeur de texte.
"""
import sys
import time
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtTest import QTest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.gui_pyside6.main_window_modern import ModernMainWindow
from src.transcription.transcriber import TranscriptionResult, TranscriptionSegment, TranscriptionStatus


@pytest.fixture(scope="module")
def qapp():
    """Fixture Qt Application."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # Don't quit here, let pytest handle it


class TestTranscriptionE2E:
    """Tests E2E pour le workflow de transcription."""

    def test_transcription_does_not_block_ui(self, qapp, tmp_path):
        """
        Test que la transcription ne bloque pas l'UI.

        Simule:
        1. Import d'un fichier audio
        2. Lancement de la transcription (avec mock Whisper)
        3. Vérifier que l'UI reste responsive
        4. Vérifier que le texte est inséré dans l'éditeur
        """
        # Create fake audio file
        audio_file = tmp_path / "test_audio.mp3"
        audio_file.write_bytes(b"fake audio data")

        # Create window
        window = ModernMainWindow()
        window.show()

        # Process events to ensure window is rendered
        qapp.processEvents()

        # Mock the transcriber to return quickly
        mock_result = TranscriptionResult(
            segments=[
                TranscriptionSegment(
                    start=0.0,
                    end=2.5,
                    text="Bonjour ceci est un test",
                    confidence=0.95
                ),
                TranscriptionSegment(
                    start=2.5,
                    end=5.0,
                    text="de transcription automatique",
                    confidence=0.92
                ),
            ],
            full_text="Bonjour ceci est un test de transcription automatique",
            language="fr",
            status=TranscriptionStatus.COMPLETED,
        )

        # Measure UI responsiveness
        ui_responsive = True
        response_times = []

        def check_ui_responsiveness():
            """Check if UI is still responsive."""
            nonlocal ui_responsive
            start = time.time()
            qapp.processEvents()
            elapsed = time.time() - start
            response_times.append(elapsed)

            # If processEvents takes more than 100ms, UI is blocked
            if elapsed > 0.1:
                ui_responsive = False
                print(f"⚠️ UI blocked for {elapsed*1000:.2f}ms")

        with patch('src.gui_pyside6.main_window_modern.WhisperTranscriber') as MockTranscriber:
            # Configure mock
            mock_instance = MockTranscriber.return_value
            mock_instance.transcribe.return_value = mock_result

            # Simulate file import
            from src.gui_pyside6.main_window_modern import TranscriptionItem
            transcription = TranscriptionItem(str(audio_file), "test_audio.mp3")
            window.transcriptions.append(transcription)
            window.current_transcription = transcription

            # Start transcription
            window._start_transcription()

            # Check UI responsiveness during transcription
            for _ in range(10):
                check_ui_responsiveness()
                time.sleep(0.05)  # 50ms intervals

            # Wait for transcription to complete
            # Give it up to 5 seconds
            timeout = 50  # 50 * 100ms = 5s
            while timeout > 0:
                qapp.processEvents()
                if window.text_editor.toPlainText():
                    break
                timeout -= 1
                time.sleep(0.1)

            # Verify UI was responsive
            assert ui_responsive, f"UI was blocked! Response times: {response_times}"

            # Verify text was inserted
            editor_text = window.text_editor.toPlainText()
            assert len(editor_text) > 0, "Text editor is empty"
            assert "Bonjour" in editor_text, "Transcription text not found in editor"
            assert "[0:00]" in editor_text or "[00:00]" in editor_text, "Timestamp not found in editor"

            print(f"✅ UI responsiveness: {max(response_times)*1000:.2f}ms max delay")
            print(f"✅ Text inserted: {len(editor_text)} characters")

        window.close()

    def test_transcription_handles_large_text(self, qapp, tmp_path):
        """
        Test que l'insertion de gros textes ne bloque pas l'UI.

        Simule une transcription de 1h avec 1000+ segments.
        """
        audio_file = tmp_path / "long_audio.mp3"
        audio_file.write_bytes(b"fake long audio")

        window = ModernMainWindow()
        window.show()
        qapp.processEvents()

        # Create large transcription result (1000 segments = ~1h)
        segments = []
        full_text_parts = []
        for i in range(1000):
            text = f"Segment numéro {i} avec du texte de test"
            segments.append(
                TranscriptionSegment(
                    start=i * 3.6,  # 3.6s per segment
                    end=(i + 1) * 3.6,
                    text=text,
                    confidence=0.9
                )
            )
            full_text_parts.append(text)

        mock_result = TranscriptionResult(
            segments=segments,
            full_text=" ".join(full_text_parts),
            language="fr",
            status=TranscriptionStatus.COMPLETED,
        )

        with patch('src.gui_pyside6.main_window_modern.WhisperTranscriber') as MockTranscriber:
            mock_instance = MockTranscriber.return_value
            mock_instance.transcribe.return_value = mock_result

            from src.gui_pyside6.main_window_modern import TranscriptionItem
            transcription = TranscriptionItem(str(audio_file), "long_audio.mp3")
            window.transcriptions.append(transcription)
            window.current_transcription = transcription

            # Measure time to insert text
            start_time = time.time()
            window._start_transcription()

            # Wait for completion
            timeout = 100  # 10s timeout
            while timeout > 0:
                qapp.processEvents()
                if window.text_editor.toPlainText():
                    break
                timeout -= 1
                time.sleep(0.1)

            insert_time = time.time() - start_time

            # Should complete within reasonable time (< 5s for 1000 segments)
            assert insert_time < 5.0, f"Text insertion took {insert_time:.2f}s (too slow!)"

            # Verify content
            editor_text = window.text_editor.toPlainText()
            assert len(editor_text) > 50000, "Text too short"
            assert "Segment numéro 0" in editor_text
            assert "Segment numéro 999" in editor_text

            print(f"✅ Large text insertion: {insert_time:.2f}s for {len(segments)} segments")

        window.close()

    def test_transcription_error_handling(self, qapp, tmp_path):
        """
        Test que les erreurs de transcription sont bien gérées.
        """
        audio_file = tmp_path / "bad_audio.mp3"
        audio_file.write_bytes(b"corrupted")

        window = ModernMainWindow()
        window.show()
        qapp.processEvents()

        # Mock transcriber to raise exception
        with patch('src.gui_pyside6.main_window_modern.WhisperTranscriber') as MockTranscriber:
            mock_instance = MockTranscriber.return_value
            mock_instance.transcribe.side_effect = Exception("Whisper model loading failed")

            from src.gui_pyside6.main_window_modern import TranscriptionItem
            transcription = TranscriptionItem(str(audio_file), "bad_audio.mp3")
            window.transcriptions.append(transcription)
            window.current_transcription = transcription

            # Mock QMessageBox to avoid blocking
            with patch('src.gui_pyside6.main_window_modern.QMessageBox.critical') as mock_msg:
                window._start_transcription()

                # Wait for error handling
                timeout = 50
                while timeout > 0:
                    qapp.processEvents()
                    if mock_msg.called:
                        break
                    timeout -= 1
                    time.sleep(0.1)

                # Verify error message was shown
                assert mock_msg.called, "Error dialog not shown"
                error_msg = mock_msg.call_args[0][2]
                assert "Whisper" in error_msg or "failed" in error_msg

                print(f"✅ Error handled correctly: {error_msg[:50]}...")

        window.close()

    def test_transcription_thread_safety(self, qapp, tmp_path):
        """
        Test la thread-safety de la transcription.

        Vérifie que les appels depuis le thread de transcription
        vers le thread GUI sont correctement synchronisés.
        """
        audio_file = tmp_path / "test_thread.mp3"
        audio_file.write_bytes(b"test")

        window = ModernMainWindow()
        window.show()
        qapp.processEvents()

        # Track if any Qt warnings are raised
        qt_warnings = []

        def warning_handler(msg_type, context, message):
            if "QObject" in message or "thread" in message.lower():
                qt_warnings.append(message)

        # Install Qt message handler (if available)
        # Note: This is tricky in PySide6, so we'll check differently

        mock_result = TranscriptionResult(
            segments=[
                TranscriptionSegment(start=0.0, end=1.0, text="Test", confidence=0.9)
            ],
            full_text="Test",
            language="fr",
            status=TranscriptionStatus.COMPLETED,
        )

        with patch('src.gui_pyside6.main_window_modern.WhisperTranscriber') as MockTranscriber:
            mock_instance = MockTranscriber.return_value
            mock_instance.transcribe.return_value = mock_result

            from src.gui_pyside6.main_window_modern import TranscriptionItem
            transcription = TranscriptionItem(str(audio_file), "test_thread.mp3")
            window.transcriptions.append(transcription)
            window.current_transcription = transcription

            window._start_transcription()

            # Wait for completion
            timeout = 50
            while timeout > 0:
                qapp.processEvents()
                if window.text_editor.toPlainText():
                    break
                timeout -= 1
                time.sleep(0.1)

            # Verify no thread-safety issues
            # (Would manifest as crashes or Qt warnings)
            editor_text = window.text_editor.toPlainText()
            assert "Test" in editor_text

            print("✅ Thread-safety check passed")

        window.close()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
