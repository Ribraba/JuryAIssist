"""
Tests unitaires pour TimeUtils.

Ces tests vérifient les conversions de temps et formatages.
"""

import pytest

from src.audio.timeline import TimeUtils


# ============================================================================
# TESTS DE CONVERSION SECONDES → TIMESTAMP
# ============================================================================


def test_seconds_to_timestamp_under_minute():
    """Test conversion < 1 minute."""
    assert TimeUtils.seconds_to_timestamp(0) == "00:00"
    assert TimeUtils.seconds_to_timestamp(5) == "00:05"
    assert TimeUtils.seconds_to_timestamp(59) == "00:59"


def test_seconds_to_timestamp_under_hour():
    """Test conversion entre 1 minute et 1 heure."""
    assert TimeUtils.seconds_to_timestamp(60) == "01:00"
    assert TimeUtils.seconds_to_timestamp(65) == "01:05"
    assert TimeUtils.seconds_to_timestamp(125) == "02:05"
    assert TimeUtils.seconds_to_timestamp(3599) == "59:59"


def test_seconds_to_timestamp_over_hour():
    """Test conversion >= 1 heure."""
    assert TimeUtils.seconds_to_timestamp(3600) == "01:00:00"
    assert TimeUtils.seconds_to_timestamp(3665) == "01:01:05"
    assert TimeUtils.seconds_to_timestamp(7325) == "02:02:05"


def test_seconds_to_timestamp_with_decimals():
    """Test conversion avec décimales (arrondi inférieur)."""
    assert TimeUtils.seconds_to_timestamp(65.7) == "01:05"
    assert TimeUtils.seconds_to_timestamp(65.2) == "01:05"
    assert TimeUtils.seconds_to_timestamp(59.9) == "00:59"


def test_seconds_to_timestamp_negative():
    """Test conversion valeurs négatives (traitées comme 0)."""
    assert TimeUtils.seconds_to_timestamp(-10) == "00:00"
    assert TimeUtils.seconds_to_timestamp(-100) == "00:00"


# ============================================================================
# TESTS DE CONVERSION TIMESTAMP → SECONDES
# ============================================================================


def test_timestamp_to_seconds_mm_ss():
    """Test conversion format MM:SS."""
    assert TimeUtils.timestamp_to_seconds("00:00") == 0.0
    assert TimeUtils.timestamp_to_seconds("00:05") == 5.0
    assert TimeUtils.timestamp_to_seconds("01:00") == 60.0
    assert TimeUtils.timestamp_to_seconds("01:05") == 65.0
    assert TimeUtils.timestamp_to_seconds("59:59") == 3599.0


def test_timestamp_to_seconds_hh_mm_ss():
    """Test conversion format HH:MM:SS."""
    assert TimeUtils.timestamp_to_seconds("01:00:00") == 3600.0
    assert TimeUtils.timestamp_to_seconds("01:01:05") == 3665.0
    assert TimeUtils.timestamp_to_seconds("02:30:15") == 9015.0


def test_timestamp_to_seconds_with_whitespace():
    """Test conversion avec espaces."""
    assert TimeUtils.timestamp_to_seconds("  01:05  ") == 65.0
    assert TimeUtils.timestamp_to_seconds(" 01:01:05 ") == 3665.0


def test_timestamp_to_seconds_invalid_format():
    """Test conversion format invalide."""
    with pytest.raises(ValueError, match="Format timestamp invalide"):
        TimeUtils.timestamp_to_seconds("5")

    with pytest.raises(ValueError, match="Format timestamp invalide"):
        TimeUtils.timestamp_to_seconds("01:02:03:04")

    with pytest.raises(ValueError, match="Format MM:SS invalide"):
        TimeUtils.timestamp_to_seconds("aa:bb")

    with pytest.raises(ValueError, match="Format HH:MM:SS invalide"):
        TimeUtils.timestamp_to_seconds("aa:bb:cc")


# ============================================================================
# TESTS DE CONVERSION BIDIRECTIONNELLE
# ============================================================================


def test_seconds_timestamp_roundtrip():
    """Test aller-retour secondes → timestamp → secondes."""
    # Sous 1 heure
    assert TimeUtils.timestamp_to_seconds(TimeUtils.seconds_to_timestamp(65)) == 65.0
    assert TimeUtils.timestamp_to_seconds(TimeUtils.seconds_to_timestamp(125)) == 125.0

    # Au-dessus 1 heure
    assert (
        TimeUtils.timestamp_to_seconds(TimeUtils.seconds_to_timestamp(3665)) == 3665.0
    )


# ============================================================================
# TESTS DE CALCUL DE POURCENTAGE
# ============================================================================


def test_get_percentage_basic():
    """Test calcul de pourcentage basique."""
    assert TimeUtils.get_percentage(0, 100) == 0.0
    assert TimeUtils.get_percentage(50, 100) == 50.0
    assert TimeUtils.get_percentage(100, 100) == 100.0
    assert TimeUtils.get_percentage(25, 100) == 25.0


def test_get_percentage_decimal():
    """Test calcul avec décimales."""
    assert TimeUtils.get_percentage(33.33, 100) == 33.33
    assert TimeUtils.get_percentage(66.66, 100) == 66.66


def test_get_percentage_zero_duration():
    """Test calcul avec durée nulle."""
    assert TimeUtils.get_percentage(50, 0) == 0.0
    assert TimeUtils.get_percentage(0, 0) == 0.0


def test_get_percentage_clamping():
    """Test clamping 0-100."""
    # Position > durée
    assert TimeUtils.get_percentage(150, 100) == 100.0

    # Position négative
    assert TimeUtils.get_percentage(-10, 100) == 0.0


# ============================================================================
# TESTS DE FORMATAGE COMPACT
# ============================================================================


def test_format_duration_compact_seconds_only():
    """Test formatage compact < 1 minute."""
    assert TimeUtils.format_duration_compact(0) == "0s"
    assert TimeUtils.format_duration_compact(5) == "5s"
    assert TimeUtils.format_duration_compact(59) == "59s"


def test_format_duration_compact_minutes():
    """Test formatage compact avec minutes."""
    assert TimeUtils.format_duration_compact(60) == "1m"
    assert TimeUtils.format_duration_compact(65) == "1m 5s"
    assert TimeUtils.format_duration_compact(125) == "2m 5s"


def test_format_duration_compact_hours():
    """Test formatage compact avec heures."""
    assert TimeUtils.format_duration_compact(3600) == "1h"
    assert TimeUtils.format_duration_compact(3660) == "1h 1m"
    assert TimeUtils.format_duration_compact(3665) == "1h 1m 5s"
    assert TimeUtils.format_duration_compact(7325) == "2h 2m 5s"


def test_format_duration_compact_negative():
    """Test formatage compact valeurs négatives."""
    assert TimeUtils.format_duration_compact(-10) == "0s"


# ============================================================================
# TESTS DE PARSING DE COMPOSANTES
# ============================================================================


def test_parse_time_components_basic():
    """Test parsing composantes basique."""
    assert TimeUtils.parse_time_components(0) == (0, 0, 0)
    assert TimeUtils.parse_time_components(5) == (0, 0, 5)
    assert TimeUtils.parse_time_components(65) == (0, 1, 5)
    assert TimeUtils.parse_time_components(3665) == (1, 1, 5)


def test_parse_time_components_exact_boundaries():
    """Test parsing aux limites exactes."""
    assert TimeUtils.parse_time_components(60) == (0, 1, 0)
    assert TimeUtils.parse_time_components(3600) == (1, 0, 0)


def test_parse_time_components_negative():
    """Test parsing valeurs négatives."""
    assert TimeUtils.parse_time_components(-10) == (0, 0, 0)


# ============================================================================
# TESTS DE FORMATAGE DU TEMPS RESTANT
# ============================================================================


def test_format_remaining_time_basic():
    """Test formatage temps restant."""
    assert TimeUtils.format_remaining_time(30, 100) == "-01:10"
    assert TimeUtils.format_remaining_time(0, 100) == "-01:40"
    assert TimeUtils.format_remaining_time(100, 100) == "-00:00"


def test_format_remaining_time_over_hour():
    """Test formatage temps restant > 1h."""
    assert TimeUtils.format_remaining_time(0, 3665) == "-01:01:05"
    assert TimeUtils.format_remaining_time(3600, 3665) == "-01:05"


def test_format_remaining_time_negative():
    """Test formatage temps restant négatif (position > durée)."""
    # Si position dépasse durée, temps restant = 0
    assert TimeUtils.format_remaining_time(150, 100) == "-00:00"


# ============================================================================
# TESTS D'INTÉGRATION
# ============================================================================


def test_real_world_scenario():
    """Test scénario réel d'affichage."""
    # Audio de 11.669 secondes (comme Test_audio.m4a)
    duration = 11.669

    # Position à 5 secondes
    position = 5.0

    # Timestamp position
    pos_timestamp = TimeUtils.seconds_to_timestamp(position)
    assert pos_timestamp == "00:05"

    # Timestamp durée
    dur_timestamp = TimeUtils.seconds_to_timestamp(duration)
    assert dur_timestamp == "00:11"

    # Pourcentage
    percentage = TimeUtils.get_percentage(position, duration)
    assert 42.0 < percentage < 43.0  # ~42.8%

    # Temps restant
    remaining = TimeUtils.format_remaining_time(position, duration)
    assert remaining == "-00:06"

    # Format compact
    compact = TimeUtils.format_duration_compact(duration)
    assert compact == "11s"


def test_long_audio_scenario():
    """Test scénario avec audio long (> 1h)."""
    # Audio de 1h 30m 45s
    duration = 5445.0

    # Position à 30m
    position = 1800.0

    # Timestamps
    pos_timestamp = TimeUtils.seconds_to_timestamp(position)
    assert pos_timestamp == "30:00"

    dur_timestamp = TimeUtils.seconds_to_timestamp(duration)
    assert dur_timestamp == "01:30:45"

    # Pourcentage
    percentage = TimeUtils.get_percentage(position, duration)
    assert 33.0 < percentage < 34.0  # ~33.05%

    # Format compact
    compact = TimeUtils.format_duration_compact(duration)
    assert compact == "1h 30m 45s"
