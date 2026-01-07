"""
Module de synchronisation mot ↔ timestamp selon Phase 5.1.2 de la roadmap.

Fonctionnalités :
- Découpage de segments en mots
- Interpolation linéaire des timestamps de chaque mot
- Index inversé : mot → liste de timestamps
- Recherche de timestamp par mot et occurrence
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import re

from src.transcription.transcriber import TranscriptionSegment


@dataclass
class WordTimestamp:
    """Représente un mot avec son timestamp."""

    word: str
    start_time: float
    end_time: float
    segment_index: int  # Index du segment d'origine
    word_index: int  # Index du mot dans le segment


class IWordSynchronizer:
    """Interface pour la synchronisation mot-timestamp."""

    def build_index(self, segments: List[TranscriptionSegment]) -> None:
        """
        Construit l'index de synchronisation.

        Args:
            segments: Liste de segments de transcription
        """
        raise NotImplementedError

    def find_timestamp(self, word: str, occurrence: int = 0) -> Optional[float]:
        """
        Trouve le timestamp d'un mot.

        Args:
            word: Mot à rechercher
            occurrence: Numéro d'occurrence (0 = première occurrence)

        Returns:
            Timestamp de début du mot, ou None si non trouvé
        """
        raise NotImplementedError

    def find_word_at_position(self, text_position: int) -> Optional[WordTimestamp]:
        """
        Trouve le mot à une position donnée dans le texte.

        Args:
            text_position: Position du caractère dans le texte complet

        Returns:
            WordTimestamp ou None si non trouvé
        """
        raise NotImplementedError


class WordSynchronizer(IWordSynchronizer):
    """
    Synchroniseur mot-timestamp avec interpolation linéaire.

    Découpe chaque segment en mots et interpole linéairement
    le timestamp de chaque mot en fonction de sa position dans le segment.
    """

    def __init__(self):
        """Initialise le synchroniseur."""
        self._word_timestamps: List[WordTimestamp] = []
        self._word_index: Dict[str, List[int]] = {}  # mot → liste d'indices dans _word_timestamps
        self._position_map: List[Tuple[int, int, int]] = []  # (char_start, char_end, word_timestamp_index)
        self._segments: List[TranscriptionSegment] = []

    def build_index(self, segments: List[TranscriptionSegment]) -> None:
        """
        Construit l'index de synchronisation.

        Args:
            segments: Liste de segments de transcription
        """
        self._segments = segments
        self._word_timestamps = []
        self._word_index = {}
        self._position_map = []

        # Position dans le texte de l'éditeur (sans timestamps)
        char_position = 0

        for seg_idx, segment in enumerate(segments):
            # Découper le segment en mots
            words = self._extract_words(segment.text)

            if not words:
                # Même sans mots, compter les caractères du segment vide
                char_position += len(segment.text) + 2  # +2 pour "\n\n"
                continue

            # Calculer la durée du segment
            segment_duration = segment.end - segment.start

            # Trouver les positions exactes des mots dans le texte du segment
            # en utilisant la regex pour matcher les positions réelles
            segment_text = segment.text
            word_positions_in_segment = []

            # Utiliser la même regex que _extract_words pour trouver les positions
            for match in re.finditer(r"\b[\w']+\b", segment_text):
                word_positions_in_segment.append(match.start())

            # Interpoler les timestamps pour chaque mot
            for word_idx, word in enumerate(words):
                # Interpolation linéaire du timestamp
                word_start_ratio = word_idx / len(words)
                word_end_ratio = (word_idx + 1) / len(words)

                word_start_time = segment.start + (segment_duration * word_start_ratio)
                word_end_time = segment.start + (segment_duration * word_end_ratio)

                # Créer le WordTimestamp
                word_timestamp = WordTimestamp(
                    word=word.lower(),
                    start_time=word_start_time,
                    end_time=word_end_time,
                    segment_index=seg_idx,
                    word_index=word_idx
                )

                word_ts_index = len(self._word_timestamps)
                self._word_timestamps.append(word_timestamp)

                # Ajouter à l'index inversé
                word_lower = word.lower()
                if word_lower not in self._word_index:
                    self._word_index[word_lower] = []
                self._word_index[word_lower].append(word_ts_index)

                # Calculer la position du mot dans le texte de l'éditeur
                # Le texte de l'éditeur est construit comme: "segment1.text\n\nsegment2.text\n\n..."
                word_char_start = char_position + word_positions_in_segment[word_idx]
                word_char_end = word_char_start + len(word)

                self._position_map.append((word_char_start, word_char_end, word_ts_index))

            # Mettre à jour la position pour le prochain segment
            # Format de l'éditeur : "text\n\n"
            char_position += len(segment.text) + 2  # +2 pour "\n\n"

    def find_timestamp(self, word: str, occurrence: int = 0) -> Optional[float]:
        """
        Trouve le timestamp d'un mot.

        Args:
            word: Mot à rechercher
            occurrence: Numéro d'occurrence (0 = première occurrence)

        Returns:
            Timestamp de début du mot, ou None si non trouvé
        """
        word_lower = word.lower()

        if word_lower not in self._word_index:
            return None

        occurrences = self._word_index[word_lower]

        if occurrence >= len(occurrences):
            return None

        word_ts_index = occurrences[occurrence]
        word_timestamp = self._word_timestamps[word_ts_index]

        return word_timestamp.start_time

    def find_word_at_position(self, text_position: int) -> Optional[WordTimestamp]:
        """
        Trouve le mot à une position donnée dans le texte.

        Args:
            text_position: Position du caractère dans le texte complet

        Returns:
            WordTimestamp ou None si non trouvé
        """
        for char_start, char_end, word_ts_index in self._position_map:
            if char_start <= text_position < char_end:
                return self._word_timestamps[word_ts_index]

        return None

    def get_all_words(self) -> List[WordTimestamp]:
        """
        Récupère tous les mots avec leurs timestamps.

        Returns:
            Liste de tous les WordTimestamp
        """
        return self._word_timestamps.copy()

    def get_words_in_range(self, start_time: float, end_time: float) -> List[WordTimestamp]:
        """
        Récupère tous les mots dans une plage de temps.

        Args:
            start_time: Début de la plage (secondes)
            end_time: Fin de la plage (secondes)

        Returns:
            Liste de WordTimestamp dans la plage
        """
        return [
            wt for wt in self._word_timestamps
            if wt.start_time >= start_time and wt.end_time <= end_time
        ]

    def _extract_words(self, text: str) -> List[str]:
        """
        Extrait les mots d'un texte.

        Args:
            text: Texte à découper

        Returns:
            Liste de mots
        """
        # Utiliser une regex pour extraire les mots (lettres, chiffres, apostrophes)
        words = re.findall(r"\b[\w']+\b", text)
        return words

    def _format_timestamp(self, seconds: float) -> str:
        """
        Formate un timestamp.

        Args:
            seconds: Temps en secondes

        Returns:
            Timestamp formaté (MM:SS)
        """
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
