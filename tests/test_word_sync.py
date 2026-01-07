"""
Tests unitaires pour le module word_sync.py.
"""

import pytest

from src.transcription.transcriber import TranscriptionSegment
from src.transcription.word_sync import WordSynchronizer, WordTimestamp


@pytest.fixture
def sample_segments():
    """Fixture de segments de test."""
    return [
        TranscriptionSegment(
            start=0.0,
            end=5.0,
            text="Bonjour tout le monde"
        ),
        TranscriptionSegment(
            start=5.0,
            end=10.0,
            text="Ceci est un test"
        ),
        TranscriptionSegment(
            start=10.0,
            end=15.0,
            text="Le mot test apparaît deux fois"
        )
    ]


@pytest.fixture
def synchronizer_with_data(sample_segments):
    """Fixture de synchroniseur avec données."""
    sync = WordSynchronizer()
    sync.build_index(sample_segments)
    return sync


class TestWordSynchronizer:
    """Tests pour WordSynchronizer."""

    def test_build_index_creates_word_timestamps(self, synchronizer_with_data):
        """Test que build_index crée les word timestamps."""
        words = synchronizer_with_data.get_all_words()

        # Doit avoir des mots
        assert len(words) > 0

        # Premier mot du premier segment
        assert words[0].word == "bonjour"
        assert words[0].start_time == 0.0
        assert words[0].segment_index == 0
        assert words[0].word_index == 0

    def test_find_timestamp_first_occurrence(self, synchronizer_with_data):
        """Test recherche du timestamp d'un mot (première occurrence)."""
        # Rechercher "test" (première occurrence dans segment 2)
        timestamp = synchronizer_with_data.find_timestamp("test", occurrence=0)

        assert timestamp is not None
        # Doit être dans le segment 2 (5.0 - 10.0)
        assert 5.0 <= timestamp < 10.0

    def test_find_timestamp_second_occurrence(self, synchronizer_with_data):
        """Test recherche du timestamp d'un mot (deuxième occurrence)."""
        # Rechercher "test" (deuxième occurrence dans segment 3)
        timestamp = synchronizer_with_data.find_timestamp("test", occurrence=1)

        assert timestamp is not None
        # Doit être dans le segment 3 (10.0 - 15.0)
        assert 10.0 <= timestamp < 15.0

    def test_find_timestamp_case_insensitive(self, synchronizer_with_data):
        """Test que la recherche est insensible à la casse."""
        timestamp1 = synchronizer_with_data.find_timestamp("BONJOUR")
        timestamp2 = synchronizer_with_data.find_timestamp("bonjour")
        timestamp3 = synchronizer_with_data.find_timestamp("Bonjour")

        assert timestamp1 == timestamp2 == timestamp3

    def test_find_timestamp_nonexistent_word(self, synchronizer_with_data):
        """Test recherche d'un mot inexistant."""
        timestamp = synchronizer_with_data.find_timestamp("inexistant")
        assert timestamp is None

    def test_find_timestamp_invalid_occurrence(self, synchronizer_with_data):
        """Test recherche d'une occurrence invalide."""
        # "test" apparaît 2 fois, occurrence 2 (3ème) n'existe pas
        timestamp = synchronizer_with_data.find_timestamp("test", occurrence=2)
        assert timestamp is None

    def test_linear_interpolation(self, synchronizer_with_data):
        """Test que l'interpolation linéaire fonctionne."""
        words = synchronizer_with_data.get_all_words()

        # Dans le premier segment (0.0 - 5.0) : "Bonjour tout le monde" (4 mots)
        # Chaque mot devrait avoir une durée de 5.0 / 4 = 1.25 secondes
        segment_0_words = [w for w in words if w.segment_index == 0]

        assert len(segment_0_words) == 4

        # Vérifier que les timestamps sont bien interpolés
        assert segment_0_words[0].start_time == pytest.approx(0.0, abs=0.01)
        assert segment_0_words[0].end_time == pytest.approx(1.25, abs=0.01)

        assert segment_0_words[1].start_time == pytest.approx(1.25, abs=0.01)
        assert segment_0_words[1].end_time == pytest.approx(2.5, abs=0.01)

    def test_get_all_words(self, synchronizer_with_data):
        """Test récupération de tous les mots."""
        words = synchronizer_with_data.get_all_words()

        # Segment 1: 4 mots, Segment 2: 4 mots, Segment 3: 6 mots
        assert len(words) == 14

    def test_get_words_in_range(self, synchronizer_with_data):
        """Test récupération des mots dans une plage de temps."""
        # Récupérer les mots entre 5.0 et 10.0 (segment 2)
        words = synchronizer_with_data.get_words_in_range(5.0, 10.0)

        # Doit contenir tous les mots du segment 2
        assert len(words) > 0
        assert all(5.0 <= w.start_time < 10.0 for w in words)
        assert all(w.end_time <= 10.0 for w in words)

    def test_word_index_tracking(self, synchronizer_with_data):
        """Test que word_index suit correctement l'ordre des mots."""
        words = synchronizer_with_data.get_all_words()

        # Vérifier que les word_index sont séquentiels dans chaque segment
        for segment_idx in range(3):
            segment_words = [w for w in words if w.segment_index == segment_idx]
            word_indices = [w.word_index for w in segment_words]

            assert word_indices == list(range(len(segment_words)))

    def test_empty_segments(self):
        """Test avec des segments vides."""
        sync = WordSynchronizer()
        sync.build_index([])

        words = sync.get_all_words()
        assert len(words) == 0

        timestamp = sync.find_timestamp("test")
        assert timestamp is None

    def test_segment_with_punctuation(self):
        """Test avec des segments contenant de la ponctuation."""
        segments = [
            TranscriptionSegment(
                start=0.0,
                end=5.0,
                text="Bonjour, comment allez-vous?"
            )
        ]

        sync = WordSynchronizer()
        sync.build_index(segments)

        # Doit extraire les mots sans la ponctuation
        timestamp = sync.find_timestamp("bonjour")
        assert timestamp is not None

        timestamp = sync.find_timestamp("comment")
        assert timestamp is not None

    def test_segment_with_apostrophe(self):
        """Test avec des mots contenant des apostrophes."""
        segments = [
            TranscriptionSegment(
                start=0.0,
                end=5.0,
                text="C'est l'heure du déjeuner"
            )
        ]

        sync = WordSynchronizer()
        sync.build_index(segments)

        # Les apostrophes devraient être conservées
        timestamp = sync.find_timestamp("c'est")
        assert timestamp is not None

        timestamp = sync.find_timestamp("l'heure")
        assert timestamp is not None

    def test_find_word_at_position_basic(self, synchronizer_with_data):
        """Test find_word_at_position trouve le bon mot."""
        # Le texte construit est: "Bonjour tout le monde\n\nCeci est un test\n\nLe mot test apparaît deux fois"
        # Position 0 = 'B' de "Bonjour"
        result = synchronizer_with_data.find_word_at_position(0)
        assert result is not None
        assert result.word == "bonjour"
        assert result.segment_index == 0

    def test_find_word_at_position_with_duplicates(self):
        """
        Test que find_word_at_position gère correctement les doublons.

        Ce test vérifie le bug corrigé: quand un mot apparaît plusieurs fois,
        cliquer sur la 2ème occurrence doit pointer vers la 2ème occurrence,
        pas la première.
        """
        # Créer des segments avec le mot "test" qui apparaît 3 fois
        segments = [
            TranscriptionSegment(
                start=0.0,
                end=5.0,
                text="Premier test ici"  # "test" à la position ~8
            ),
            TranscriptionSegment(
                start=5.0,
                end=10.0,
                text="Deuxième test là"  # "test" à la position ~32 (23 + 2 + 9)
            ),
            TranscriptionSegment(
                start=10.0,
                end=15.0,
                text="Troisième test final"  # "test" à la position ~58 (46 + 2 + 10)
            )
        ]

        sync = WordSynchronizer()
        sync.build_index(segments)

        # Texte construit: "Premier test ici\n\nDeuxième test là\n\nTroisième test final"
        # Positions approximatives:
        # Segment 1: "Premier test ici" (0-16)
        # "\n\n" (16-18)
        # Segment 2: "Deuxième test là" (18-34)
        # "\n\n" (34-36)
        # Segment 3: "Troisième test final" (36-56)

        # Trouver la position exacte du premier "test"
        text_segment_1 = "Premier test ici"
        first_test_pos = text_segment_1.find("test")  # ~8

        # Trouver la position exacte du deuxième "test"
        text_segment_2 = "Deuxième test là"
        second_test_pos = len(text_segment_1) + 2 + text_segment_2.find("test")  # ~27

        # Trouver la position exacte du troisième "test"
        text_segment_3 = "Troisième test final"
        third_test_pos = len(text_segment_1) + 2 + len(text_segment_2) + 2 + text_segment_3.find("test")  # ~47

        # Tester la première occurrence
        result1 = sync.find_word_at_position(first_test_pos)
        assert result1 is not None
        assert result1.word == "test"
        assert result1.segment_index == 0, "La première occurrence doit être dans le segment 0"
        assert 0.0 <= result1.start_time < 5.0, "Le timestamp doit être dans le premier segment"

        # Tester la deuxième occurrence
        result2 = sync.find_word_at_position(second_test_pos)
        assert result2 is not None
        assert result2.word == "test"
        assert result2.segment_index == 1, "La deuxième occurrence doit être dans le segment 1"
        assert 5.0 <= result2.start_time < 10.0, "Le timestamp doit être dans le deuxième segment"

        # Tester la troisième occurrence
        result3 = sync.find_word_at_position(third_test_pos)
        assert result3 is not None
        assert result3.word == "test"
        assert result3.segment_index == 2, "La troisième occurrence doit être dans le segment 2"
        assert 10.0 <= result3.start_time < 15.0, "Le timestamp doit être dans le troisième segment"

        # Vérifier que les timestamps sont différents
        assert result1.start_time != result2.start_time != result3.start_time, \
            "Chaque occurrence doit avoir un timestamp différent"

    def test_find_word_at_position_same_word_in_same_segment(self):
        """
        Test avec un mot qui apparaît plusieurs fois dans le MÊME segment.

        Ce cas est particulièrement difficile car les occurrences sont dans le même
        intervalle de temps mais doivent quand même avoir des positions distinctes.
        """
        segments = [
            TranscriptionSegment(
                start=0.0,
                end=10.0,
                text="Le chat et le chien jouent avec le ballon"
                # "le" apparaît 3 fois dans le même segment
            )
        ]

        sync = WordSynchronizer()
        sync.build_index(segments)

        text = "Le chat et le chien jouent avec le ballon"

        # Trouver les positions de chaque "le" / "Le"
        import re
        le_positions = [m.start() for m in re.finditer(r"\b[Ll]e\b", text)]

        # Doit y avoir 3 occurrences
        assert len(le_positions) == 3

        # Tester chaque occurrence
        results = []
        for i, pos in enumerate(le_positions):
            result = sync.find_word_at_position(pos)
            assert result is not None, f"L'occurrence {i} doit être trouvée"
            assert result.word == "le"
            assert result.segment_index == 0
            results.append(result)

        # Vérifier que chaque occurrence a un word_index différent
        word_indices = [r.word_index for r in results]
        assert len(word_indices) == len(set(word_indices)), \
            "Chaque occurrence doit avoir un word_index unique"

        # Vérifier que les timestamps sont différents
        timestamps = [r.start_time for r in results]
        assert len(timestamps) == len(set(timestamps)), \
            "Chaque occurrence doit avoir un timestamp unique"

    def test_word_timestamps_have_correct_attributes(self, synchronizer_with_data):
        """Test que les WordTimestamp ont tous les attributs corrects."""
        words = synchronizer_with_data.get_all_words()

        for word in words:
            assert isinstance(word.word, str)
            assert isinstance(word.start_time, float)
            assert isinstance(word.end_time, float)
            assert isinstance(word.segment_index, int)
            assert isinstance(word.word_index, int)

            # Les timestamps doivent être cohérents
            assert word.start_time < word.end_time
            assert word.segment_index >= 0
            assert word.word_index >= 0
