"""
Tests d'intégration pour WhisperTranscriber avec fichiers audio réels.
"""

import os
import pytest
from pathlib import Path

from src.transcription.whisper_transcriber import WhisperTranscriber
from src.transcription.transcriber import TranscriptionStatus


# Marquer tous les tests de ce fichier comme nécessitant whisper
pytestmark = pytest.mark.skipif(
    os.getenv("SKIP_WHISPER_TESTS", "false").lower() == "true",
    reason="Tests Whisper désactivés (SKIP_WHISPER_TESTS=true)"
)


@pytest.fixture
def audio_file():
    """Fixture pour le fichier audio de test."""
    test_file = Path("tests/data/Test_audio.m4a")
    if not test_file.exists():
        pytest.skip(f"Fichier audio de test non trouvé: {test_file}")
    return str(test_file)


@pytest.fixture
def transcriber():
    """Fixture pour le transcripteur Whisper."""
    try:
        # Utiliser le modèle tiny pour les tests (plus rapide)
        return WhisperTranscriber(model_size="tiny")
    except ImportError as e:
        pytest.skip(f"Whisper non disponible: {e}")


class TestWhisperIntegration:
    """Tests d'intégration pour WhisperTranscriber."""

    def test_transcribe_audio_file(self, transcriber, audio_file):
        """Test de transcription d'un fichier audio complet."""
        result = transcriber.transcribe(audio_file, language="fr")

        # Vérifier le statut
        assert result.status == TranscriptionStatus.COMPLETED
        assert result.error_message is None

        # Vérifier qu'il y a du contenu
        assert result.full_text
        assert len(result.full_text) > 0

        # Vérifier qu'il y a des segments
        assert len(result.segments) > 0

        # Vérifier la langue détectée
        assert result.language in ["fr", "en"]  # Peut détecter français ou anglais

        # Afficher le résultat pour inspection manuelle
        print(f"\n--- Résultat de la transcription ---")
        print(f"Langue détectée: {result.language}")
        print(f"Durée totale: {result.duration:.2f}s")
        print(f"Nombre de segments: {len(result.segments)}")
        print(f"Texte complet: {result.full_text}")
        print(f"\nSegments:")
        for i, seg in enumerate(result.segments, 1):
            print(f"  [{i}] {seg.start:.2f}s - {seg.end:.2f}s: {seg.text}")

    def test_transcribe_segment(self, transcriber, audio_file):
        """Test de transcription d'un segment spécifique."""
        # Transcrire les 5 premières secondes
        result = transcriber.transcribe_segment(audio_file, start=0.0, end=5.0, language="fr")

        assert result.status == TranscriptionStatus.COMPLETED
        assert result.full_text

        # Les segments doivent intersecte l'intervalle [0, 5]
        # C'est-à-dire: commencer avant 5s ET finir après 0s
        for seg in result.segments:
            assert seg.start < 5.0, f"Le segment commence après 5s: {seg.start}"
            assert seg.end > 0.0, f"Le segment finit avant 0s: {seg.end}"

        print(f"\n--- Segment [0-5s] ---")
        print(f"Texte: {result.full_text}")
        print(f"Segments trouvés: {len(result.segments)}")
        for seg in result.segments:
            print(f"  [{seg.start:.2f}s - {seg.end:.2f}s]: {seg.text}")

    def test_get_model_info(self, transcriber):
        """Test des informations du modèle."""
        info = transcriber.get_model_info()

        assert info["name"] == "whisper"
        assert info["size"] == "tiny"
        assert "version" in info
        assert "parameters" in info

        print(f"\n--- Info modèle ---")
        print(f"Nom: {info['name']}")
        print(f"Taille: {info['size']}")
        print(f"Version: {info['version']}")
        print(f"Paramètres: {info['parameters']}")

    def test_get_supported_languages(self, transcriber):
        """Test des langues supportées."""
        languages = transcriber.get_supported_languages()

        assert isinstance(languages, list)
        assert len(languages) > 0
        assert "fr" in languages
        assert "en" in languages

        print(f"\n--- Langues supportées ({len(languages)}) ---")
        print(", ".join(languages))

    def test_transcribe_nonexistent_file(self, transcriber):
        """Test avec un fichier inexistant."""
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe("/path/to/nonexistent/file.mp3")

    def test_transcribe_segment_invalid_range(self, transcriber, audio_file):
        """Test avec un segment invalide (start >= end)."""
        with pytest.raises(ValueError, match="start .* doit être < end"):
            transcriber.transcribe_segment(audio_file, start=5.0, end=2.0)


class TestWhisperComparison:
    """Tests pour comparer la transcription avec le texte attendu."""

    def test_compare_with_expected_text(self, transcriber, audio_file):
        """Compare la transcription avec le texte attendu."""
        # Lire le texte attendu
        expected_file = Path("tests/data/transcription.txt")
        if not expected_file.exists():
            pytest.skip("Fichier de transcription attendue non trouvé")

        with open(expected_file, "r", encoding="utf-8") as f:
            expected_lines = f.readlines()

        # Transcrire l'audio
        result = transcriber.transcribe(audio_file, language="fr")

        assert result.status == TranscriptionStatus.COMPLETED

        print(f"\n--- Comparaison avec texte attendu ---")
        print(f"Texte attendu ({len(expected_lines)} lignes):")
        for line in expected_lines:
            print(f"  {line.strip()}")

        print(f"\nTexte transcrit:")
        print(f"  {result.full_text}")

        # Note: On ne fait pas d'assertion stricte car Whisper peut varier
        # On vérifie juste que la transcription contient des mots clés
        text_lower = result.full_text.lower()

        # Mots-clés attendus basés sur transcription.txt
        keywords = ["test", "audio", "vlc"]
        found_keywords = [kw for kw in keywords if kw in text_lower]

        print(f"\nMots-clés trouvés: {found_keywords}/{len(keywords)}")

        # Au moins un mot-clé devrait être présent
        assert len(found_keywords) > 0, f"Aucun mot-clé trouvé dans: {result.full_text}"
