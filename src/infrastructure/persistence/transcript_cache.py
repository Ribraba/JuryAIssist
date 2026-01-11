"""
Système de cache pour sauvegarder automatiquement les transcriptions.

Principe SOLID:
- Single Responsibility: Gère uniquement la persistence des transcriptions
- Open/Closed: Extensible pour d'autres formats
- Dependency Inversion: Interface abstraite pour le stockage

Fichiers de cache: ~/.juryaissist/cache/transcripts/
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.domain.transcription.entities import TranscriptionSegment


class TranscriptCache:
    """
    Gestionnaire de cache pour les transcriptions.

    Responsabilités:
    - Sauvegarder automatiquement les transcriptions
    - Charger les transcriptions depuis le cache
    - Gérer l'expiration du cache
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialise le gestionnaire de cache.

        Args:
            cache_dir: Répertoire de cache
                      Par défaut:
                      - macOS/Linux: ~/.juryaissist/cache/transcripts
                      - Windows: ~/JuryAIssist/cache/transcripts
        """
        if cache_dir is None:
            import sys
            # Sur Windows, éviter le point au début pour compatibilité
            if sys.platform == 'win32':
                self.cache_dir = Path.home() / "JuryAIssist" / "cache" / "transcripts"
            else:
                self.cache_dir = Path.home() / ".juryaissist" / "cache" / "transcripts"
        else:
            self.cache_dir = cache_dir

        # Créer le répertoire si nécessaire
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, audio_path: str, model: str, language: str) -> str:
        """
        Génère une clé de cache unique basée sur le fichier audio et les paramètres.

        Args:
            audio_path: Chemin vers le fichier audio
            model: Modèle Whisper utilisé
            language: Langue de transcription

        Returns:
            Clé de cache unique
        """
        # Créer un hash unique basé sur le chemin + modification time + paramètres
        try:
            audio_file = Path(audio_path)
            if audio_file.exists():
                mtime = audio_file.stat().st_mtime
                unique_str = f"{audio_path}_{mtime}_{model}_{language}"
            else:
                unique_str = f"{audio_path}_{model}_{language}"

            # Générer un hash SHA256
            return hashlib.sha256(unique_str.encode()).hexdigest()
        except Exception:
            # Fallback si erreur
            return hashlib.sha256(f"{audio_path}_{model}_{language}".encode()).hexdigest()

    def save_transcript(
        self,
        audio_path: str,
        segments: List[TranscriptionSegment],
        model: str,
        language: str,
        edited_text: Optional[str] = None
    ) -> bool:
        """
        Sauvegarde une transcription dans le cache.

        Args:
            audio_path: Chemin vers le fichier audio
            segments: Liste des segments de transcription
            model: Modèle Whisper utilisé
            language: Langue de transcription
            edited_text: Texte édité par l'utilisateur (optionnel)

        Returns:
            True si sauvegarde réussie, False sinon
        """
        try:
            cache_key = self._get_cache_key(audio_path, model, language)
            cache_file = self.cache_dir / f"{cache_key}.json"

            # Convertir les segments en dictionnaires
            segments_data = [
                {
                    "text": seg.text,
                    "start": seg.start,
                    "end": seg.end,
                    "confidence": seg.confidence,
                }
                for seg in segments
            ]

            # Créer les métadonnées
            cache_data = {
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "audio_path": str(audio_path),
                "model": model,
                "language": language,
                "segments": segments_data,
                "edited_text": edited_text,
            }

            # Sauvegarder
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde du cache: {e}")
            return False

    def load_transcript(
        self, audio_path: str, model: str, language: str
    ) -> Optional[Dict[str, Any]]:
        """
        Charge une transcription depuis le cache.

        Args:
            audio_path: Chemin vers le fichier audio
            model: Modèle Whisper utilisé
            language: Langue de transcription

        Returns:
            Dictionnaire avec segments et edited_text, ou None si non trouvé
        """
        try:
            cache_key = self._get_cache_key(audio_path, model, language)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if not cache_file.exists():
                return None

            # Charger
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Recréer les segments
            segments = [
                TranscriptionSegment(
                    text=seg["text"],
                    start=seg["start"],
                    end=seg["end"],
                    confidence=seg.get("confidence"),
                )
                for seg in cache_data.get("segments", [])
            ]

            return {
                "segments": segments,
                "edited_text": cache_data.get("edited_text"),
                "timestamp": cache_data.get("timestamp"),
            }

        except Exception as e:
            print(f"⚠️ Erreur lors du chargement du cache: {e}")
            return None

    def save_edited_text(self, audio_path: str, model: str, language: str, text: str) -> bool:
        """
        Sauvegarde uniquement le texte édité (mise à jour rapide).

        Args:
            audio_path: Chemin vers le fichier audio
            model: Modèle Whisper utilisé
            language: Langue de transcription
            text: Texte édité

        Returns:
            True si sauvegarde réussie, False sinon
        """
        try:
            cache_key = self._get_cache_key(audio_path, model, language)
            cache_file = self.cache_dir / f"{cache_key}.json"

            if not cache_file.exists():
                return False

            # Charger les données existantes
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Mettre à jour le texte édité et le timestamp
            cache_data["edited_text"] = text
            cache_data["last_edit"] = datetime.now().isoformat()

            # Sauvegarder
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde du texte édité: {e}")
            return False

    def clear_cache(self, max_age_days: Optional[int] = None) -> int:
        """
        Nettoie le cache.

        Args:
            max_age_days: Si spécifié, supprime les fichiers plus vieux que N jours
                         Si None, supprime tout

        Returns:
            Nombre de fichiers supprimés
        """
        count = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                should_delete = False

                if max_age_days is None:
                    should_delete = True
                else:
                    # Vérifier l'âge du fichier
                    file_age = datetime.now().timestamp() - cache_file.stat().st_mtime
                    if file_age > (max_age_days * 86400):  # Convertir jours en secondes
                        should_delete = True

                if should_delete:
                    cache_file.unlink()
                    count += 1

            return count

        except Exception as e:
            print(f"⚠️ Erreur lors du nettoyage du cache: {e}")
            return count


# Instance globale (singleton)
_transcript_cache: Optional[TranscriptCache] = None


def get_transcript_cache() -> TranscriptCache:
    """
    Retourne l'instance unique du cache de transcription.

    Returns:
        TranscriptCache singleton
    """
    global _transcript_cache
    if _transcript_cache is None:
        _transcript_cache = TranscriptCache()
    return _transcript_cache
