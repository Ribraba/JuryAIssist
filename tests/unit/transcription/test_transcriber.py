"""
Tests unitaires pour TranscriptionSegment et TranscriptionResult.
"""

import pytest

from src.transcription.transcriber import (
    TranscriptionResult,
    TranscriptionSegment,
    TranscriptionStatus,
)


# ============================================================================
# TESTS TranscriptionSegment
# ============================================================================


def test_segment_creation_valid():
    """Test création d'un segment valide."""
    seg = TranscriptionSegment(start=0.0, end=5.0, text="Bonjour")

    assert seg.start == 0.0
    assert seg.end == 5.0
    assert seg.text == "Bonjour"
    assert seg.confidence is None
    assert seg.duration == 5.0


def test_segment_with_confidence():
    """Test segment avec confiance."""
    seg = TranscriptionSegment(start=0.0, end=5.0, text="Test", confidence=0.95)

    assert seg.confidence == 0.95


def test_segment_invalid_start_negative():
    """Test segment avec start négatif."""
    with pytest.raises(ValueError, match="start doit être >= 0"):
        TranscriptionSegment(start=-1.0, end=5.0, text="Test")


def test_segment_invalid_end_before_start():
    """Test segment avec end <= start."""
    with pytest.raises(ValueError, match="end doit être > start"):
        TranscriptionSegment(start=5.0, end=3.0, text="Test")

    with pytest.raises(ValueError, match="end doit être > start"):
        TranscriptionSegment(start=5.0, end=5.0, text="Test")


def test_segment_invalid_confidence_out_of_range():
    """Test segment avec confiance hors limites."""
    with pytest.raises(ValueError, match="confidence doit être entre 0.0 et 1.0"):
        TranscriptionSegment(start=0.0, end=5.0, text="Test", confidence=1.5)

    with pytest.raises(ValueError, match="confidence doit être entre 0.0 et 1.0"):
        TranscriptionSegment(start=0.0, end=5.0, text="Test", confidence=-0.1)


def test_segment_duration():
    """Test calcul de durée."""
    seg = TranscriptionSegment(start=2.5, end=7.8, text="Test")
    assert seg.duration == pytest.approx(5.3, rel=0.01)


# ============================================================================
# TESTS TranscriptionResult
# ============================================================================


def test_result_creation_empty():
    """Test création d'un résultat vide."""
    result = TranscriptionResult(
        segments=[],
        full_text="",
        language="fr",
        status=TranscriptionStatus.IDLE,
    )

    assert result.segments == []
    assert result.full_text == ""
    assert result.language == "fr"
    assert result.status == TranscriptionStatus.IDLE
    assert result.error_message is None
    assert result.duration == 0.0
    assert result.word_count == 0


def test_result_with_segments():
    """Test résultat avec segments."""
    segments = [
        TranscriptionSegment(start=0.0, end=2.0, text="Bonjour"),
        TranscriptionSegment(start=2.0, end=5.0, text="comment allez-vous"),
    ]

    result = TranscriptionResult(
        segments=segments,
        full_text="Bonjour comment allez-vous",
        language="fr",
        status=TranscriptionStatus.COMPLETED,
    )

    assert len(result.segments) == 2
    assert result.full_text == "Bonjour comment allez-vous"
    assert result.duration == 5.0  # Fin du dernier segment
    assert result.word_count == 3


def test_result_with_error():
    """Test résultat avec erreur."""
    result = TranscriptionResult(
        segments=[],
        full_text="",
        language="unknown",
        status=TranscriptionStatus.ERROR,
        error_message="Fichier introuvable",
    )

    assert result.status == TranscriptionStatus.ERROR
    assert result.error_message == "Fichier introuvable"


def test_result_duration_multiple_segments():
    """Test durée avec plusieurs segments."""
    segments = [
        TranscriptionSegment(start=0.0, end=2.0, text="Un"),
        TranscriptionSegment(start=2.0, end=5.0, text="Deux"),
        TranscriptionSegment(start=5.0, end=10.5, text="Trois"),
    ]

    result = TranscriptionResult(
        segments=segments,
        full_text="Un Deux Trois",
        language="fr",
        status=TranscriptionStatus.COMPLETED,
    )

    assert result.duration == 10.5


def test_result_word_count():
    """Test comptage de mots."""
    result = TranscriptionResult(
        segments=[],
        full_text="Ceci est un test de comptage de mots",
        language="fr",
        status=TranscriptionStatus.COMPLETED,
    )

    assert result.word_count == 8


def test_result_word_count_empty():
    """Test comptage de mots vide."""
    result = TranscriptionResult(
        segments=[], full_text="", language="fr", status=TranscriptionStatus.IDLE
    )

    assert result.word_count == 0


# ============================================================================
# TESTS STATUTS
# ============================================================================


def test_transcription_statuses():
    """Test tous les statuts possibles."""
    assert TranscriptionStatus.IDLE.value == "idle"
    assert TranscriptionStatus.PROCESSING.value == "processing"
    assert TranscriptionStatus.COMPLETED.value == "completed"
    assert TranscriptionStatus.ERROR.value == "error"
