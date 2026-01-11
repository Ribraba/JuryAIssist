"""
Implémentation de ITranscriber avec OpenAI Whisper.

Utilise le modèle Whisper pour transcription audio multilingue.
"""

import os
from pathlib import Path
from typing import List, Optional

try:
    import whisper
except ImportError:
    whisper = None

from src.transcription.transcriber import (
    ITranscriber,
    TranscriptionResult,
    TranscriptionSegment,
    TranscriptionStatus,
)


class WhisperTranscriber(ITranscriber):
    """
    Transcripteur utilisant OpenAI Whisper.

    Supporte plusieurs tailles de modèle (tiny, base, small, medium, large).
    """

    # Langues supportées par Whisper (principales)
    SUPPORTED_LANGUAGES = [
        "fr",
        "en",
        "es",
        "de",
        "it",
        "pt",
        "nl",
        "pl",
        "ru",
        "zh",
        "ja",
        "ko",
        "ar",
        "hi",
    ]

    def __init__(self, model_size: str = "base", device: Optional[str] = None):
        """
        Initialise le transcripteur Whisper.

        Args:
            model_size: Taille du modèle ("tiny", "base", "small", "medium", "large")
            device: Device à utiliser ("cpu", "cuda"), None pour auto-détection

        Raises:
            ImportError: Si whisper n'est pas installé
            ValueError: Si model_size invalide
        """
        if whisper is None:
            raise ImportError(
                "Le package 'openai-whisper' n'est pas installé. "
                "Installez-le avec : pip install openai-whisper"
            )

        valid_sizes = ["tiny", "base", "small", "medium", "large"]
        if model_size not in valid_sizes:
            raise ValueError(
                f"model_size doit être dans {valid_sizes}, reçu: {model_size}"
            )

        self._model_size = model_size
        self._device = device
        self._model = None  # Chargement lazy

    def _ensure_model_loaded(self):
        """Charge le modèle si nécessaire (lazy loading)."""
        if self._model is None:
            self._model = whisper.load_model(self._model_size, device=self._device)

    def transcribe(
        self, audio_path: str, language: Optional[str] = None
    ) -> TranscriptionResult:
        """
        Transcrit un fichier audio complet.

        Args:
            audio_path: Chemin vers le fichier audio
            language: Code langue (ex: "fr"), None pour détection auto

        Returns:
            TranscriptionResult avec segments et texte complet

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            RuntimeError: Si la transcription échoue
        """
        # Vérifier que le fichier existe
        if not os.path.isfile(audio_path):
            raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

        # Charger le modèle
        self._ensure_model_loaded()

        try:
            # Options de transcription
            options = {
                "language": language,
                "task": "transcribe",
                "verbose": False,
            }

            # Transcription
            result = self._model.transcribe(audio_path, **options)

            # Extraire les segments
            segments = []
            for seg in result.get("segments", []):
                segment = TranscriptionSegment(
                    start=seg["start"],
                    end=seg["end"],
                    text=seg["text"].strip(),
                    confidence=seg.get("confidence"),  # Pas toujours disponible
                )
                segments.append(segment)

            # Texte complet
            full_text = result.get("text", "").strip()

            # Langue détectée
            detected_language = result.get("language", language or "unknown")

            return TranscriptionResult(
                segments=segments,
                full_text=full_text,
                language=detected_language,
                status=TranscriptionStatus.COMPLETED,
            )

        except Exception as e:
            return TranscriptionResult(
                segments=[],
                full_text="",
                language=language or "unknown",
                status=TranscriptionStatus.ERROR,
                error_message=str(e),
            )

    def transcribe_segment(
        self, audio_path: str, start: float, end: float, language: Optional[str] = None
    ) -> TranscriptionResult:
        """
        Transcrit une portion spécifique d'un fichier audio.

        Note: Whisper ne supporte pas nativement la transcription de segments.
        Cette méthode transcrit tout le fichier puis filtre les segments.

        Args:
            audio_path: Chemin vers le fichier audio
            start: Début du segment en secondes
            end: Fin du segment en secondes
            language: Code langue, None pour détection auto

        Returns:
            TranscriptionResult du segment filtré

        Raises:
            FileNotFoundError: Si le fichier n'existe pas
            ValueError: Si start >= end
        """
        if start >= end:
            raise ValueError(f"start ({start}) doit être < end ({end})")

        # Transcrire le fichier complet
        full_result = self.transcribe(audio_path, language)

        if full_result.status == TranscriptionStatus.ERROR:
            return full_result

        # Filtrer les segments qui intersectent l'intervalle [start, end]
        # Un segment intersecte si: seg.start < end ET seg.end > start
        filtered_segments = [
            seg
            for seg in full_result.segments
            if seg.start < end and seg.end > start
        ]

        # Reconstruire le texte complet des segments filtrés
        filtered_text = " ".join(seg.text for seg in filtered_segments)

        return TranscriptionResult(
            segments=filtered_segments,
            full_text=filtered_text,
            language=full_result.language,
            status=TranscriptionStatus.COMPLETED,
        )

    def get_supported_languages(self) -> List[str]:
        """
        Retourne la liste des langues supportées par Whisper.

        Returns:
            Liste des codes ISO de langues
        """
        return self.SUPPORTED_LANGUAGES.copy()

    def get_model_info(self) -> dict:
        """
        Retourne les informations sur le modèle Whisper utilisé.

        Returns:
            Dictionnaire avec nom, taille, paramètres
        """
        # Nombre de paramètres par taille de modèle
        params = {
            "tiny": "39M",
            "base": "74M",
            "small": "244M",
            "medium": "769M",
            "large": "1550M",
        }

        return {
            "name": "whisper",
            "size": self._model_size,
            "version": whisper.__version__ if whisper else "unknown",
            "parameters": params.get(self._model_size, "unknown"),
            "device": self._device or "auto",
        }

    def release(self):
        """Libère les ressources du modèle."""
        if self._model is not None:
            del self._model
            self._model = None
