"""
Tests unitaires pour les composants de l'interface Flet.

Teste les composants: Sidebar, AudioPlayer, EditorPanel, TranscriptionView.
"""
import pytest
import flet as ft

from src.gui_flet.components.sidebar import Sidebar
from src.gui_flet.components.audio_player import AudioPlayer
from src.gui_flet.components.editor_panel import EditorPanel
from src.gui_flet.components.transcription_view import TranscriptionView
from src.transcription.transcriber import TranscriptionSegment


class TestSidebar:
    """Tests pour le composant Sidebar."""

    def test_sidebar_creation(self):
        """Vérifie que la sidebar peut être créée."""
        sidebar = Sidebar()
        assert sidebar is not None
        assert isinstance(sidebar, ft.Container)

    def test_sidebar_has_fixed_width(self):
        """Vérifie que la sidebar a une largeur fixe."""
        sidebar = Sidebar()
        assert sidebar.width == 280

    def test_sidebar_callbacks_are_optional(self):
        """Vérifie que les callbacks sont optionnels."""
        sidebar = Sidebar()  # Sans callbacks
        assert sidebar.on_import_clicked is None
        assert sidebar.on_settings_clicked is None
        assert sidebar.on_file_selected is None

    def test_sidebar_accepts_callbacks(self):
        """Vérifie que les callbacks peuvent être fournis."""
        def import_cb():
            pass

        def settings_cb():
            pass

        def file_cb(filename):
            pass

        sidebar = Sidebar(
            on_import_clicked=import_cb,
            on_settings_clicked=settings_cb,
            on_file_selected=file_cb,
        )
        assert sidebar.on_import_clicked == import_cb
        assert sidebar.on_settings_clicked == settings_cb
        assert sidebar.on_file_selected == file_cb

    def test_add_file(self):
        """Vérifie qu'on peut ajouter un fichier."""
        sidebar = Sidebar()
        initial_count = len(sidebar.files_list.controls)
        sidebar.add_file("test.mp3")
        assert len(sidebar.files_list.controls) == initial_count + 1

    def test_clear_files(self):
        """Vérifie qu'on peut vider la liste des fichiers."""
        sidebar = Sidebar()
        sidebar.add_file("test1.mp3")
        sidebar.add_file("test2.mp3")
        sidebar.clear_files()
        assert len(sidebar.files_list.controls) == 0


class TestAudioPlayer:
    """Tests pour le composant AudioPlayer."""

    def test_audio_player_creation(self):
        """Vérifie que le lecteur audio peut être créé."""
        player = AudioPlayer()
        assert player is not None
        assert isinstance(player, ft.Container)

    def test_initial_state(self):
        """Vérifie l'état initial du lecteur."""
        player = AudioPlayer()
        assert player.is_playing is False
        assert player.current_position == 0.0
        assert player.total_duration == 0.0
        assert player.current_speed == 1.0
        assert player.current_volume == 70

    def test_callbacks_are_optional(self):
        """Vérifie que les callbacks sont optionnels."""
        player = AudioPlayer()  # Sans callbacks
        assert player.on_play is None
        assert player.on_pause is None

    def test_set_position(self):
        """Vérifie qu'on peut définir la position."""
        player = AudioPlayer()
        player.set_duration(100.0)
        player.set_position(50.0)
        assert player.current_position == 50.0

    def test_set_duration(self):
        """Vérifie qu'on peut définir la durée."""
        player = AudioPlayer()
        player.set_duration(120.0)
        assert player.total_duration == 120.0

    def test_set_playing_state(self):
        """Vérifie qu'on peut changer l'état de lecture."""
        player = AudioPlayer()
        player.set_playing_state(True)
        assert player.is_playing is True
        player.set_playing_state(False)
        assert player.is_playing is False


class TestEditorPanel:
    """Tests pour le composant EditorPanel."""

    def test_editor_panel_creation(self):
        """Vérifie que le panneau d'édition peut être créé."""
        editor = EditorPanel()
        assert editor is not None
        assert isinstance(editor, ft.Container)

    def test_initial_filename(self):
        """Vérifie le nom de fichier initial."""
        editor = EditorPanel()
        assert editor.current_filename == "Aucun fichier"

    def test_set_filename(self):
        """Vérifie qu'on peut changer le nom du fichier."""
        editor = EditorPanel()
        editor.set_filename("test.mp3")
        assert editor.current_filename == "test.mp3"

    def test_set_text(self):
        """Vérifie qu'on peut définir le texte."""
        editor = EditorPanel()
        test_text = "Ceci est un test"
        editor.set_text(test_text)
        assert editor.editor.value == test_text

    def test_get_text(self):
        """Vérifie qu'on peut récupérer le texte."""
        editor = EditorPanel()
        test_text = "Test de récupération"
        editor.set_text(test_text)
        assert editor.get_text() == test_text

    def test_get_text_empty(self):
        """Vérifie que get_text retourne une chaîne vide si vide."""
        editor = EditorPanel()
        assert editor.get_text() == ""

    def test_callbacks_are_optional(self):
        """Vérifie que les callbacks sont optionnels."""
        editor = EditorPanel()
        assert editor.on_export_txt is None
        assert editor.on_export_docx is None


class TestTranscriptionView:
    """Tests pour le composant TranscriptionView."""

    def test_transcription_view_creation(self):
        """Vérifie que la vue de transcription peut être créée."""
        view = TranscriptionView()
        assert view is not None
        assert isinstance(view, ft.Container)

    def test_initial_state(self):
        """Vérifie l'état initial."""
        view = TranscriptionView()
        assert view.segments == []
        assert view.current_position == 0.0

    def test_set_segments_empty(self):
        """Vérifie qu'on peut définir une liste vide."""
        view = TranscriptionView()
        view.set_segments([])
        assert len(view.segments) == 0

    def test_set_segments_with_data(self):
        """Vérifie qu'on peut définir des segments."""
        view = TranscriptionView()
        segments = [
            TranscriptionSegment(
                id=0,
                start=0.0,
                end=5.0,
                text="Premier segment",
                words=[],
            ),
            TranscriptionSegment(
                id=1,
                start=5.0,
                end=10.0,
                text="Deuxième segment",
                words=[],
            ),
        ]
        view.set_segments(segments)
        assert len(view.segments) == 2
        assert view.segments[0].text == "Premier segment"

    def test_set_position(self):
        """Vérifie qu'on peut définir la position."""
        view = TranscriptionView()
        view.set_position(42.5)
        assert view.current_position == 42.5

    def test_callback_is_optional(self):
        """Vérifie que le callback est optionnel."""
        view = TranscriptionView()
        assert view.on_segment_click is None


# Tests d'intégration pour vérifier que les composants fonctionnent ensemble


class TestComponentsIntegration:
    """Tests d'intégration des composants."""

    def test_all_components_can_be_created_together(self):
        """Vérifie que tous les composants peuvent être créés ensemble."""
        sidebar = Sidebar()
        player = AudioPlayer()
        editor = EditorPanel()
        transcription = TranscriptionView()

        assert sidebar is not None
        assert player is not None
        assert editor is not None
        assert transcription is not None

    def test_transcription_to_editor_workflow(self):
        """Teste le workflow transcription → éditeur."""
        editor = EditorPanel()
        transcription = TranscriptionView()

        # Créer des segments
        segments = [
            TranscriptionSegment(
                id=0,
                start=0.0,
                end=5.0,
                text="Premier segment",
                words=[],
            ),
            TranscriptionSegment(
                id=1,
                start=5.0,
                end=10.0,
                text="Deuxième segment",
                words=[],
            ),
        ]

        # Mettre à jour la vue de transcription
        transcription.set_segments(segments)

        # Extraire le texte et le mettre dans l'éditeur
        text = "\n\n".join([seg.text for seg in segments])
        editor.set_text(text)

        assert editor.get_text() == "Premier segment\n\nDeuxième segment"
