"""
Worker Qt pour la transcription asynchrone.

Permet d'exécuter la transcription dans un thread séparé
pour ne pas bloquer l'interface utilisateur.

Principe SOLID:
- Single Responsibility: Gère uniquement la transcription async
- Interface Segregation: Signaux clairs et ciblés
"""

from PyQt5.QtCore import QThread, pyqtSignal

from src.transcription.whisper_transcriber import WhisperTranscriber
from src.transcription.transcriber import TranscriptionStatus


class TranscriptionWorker(QThread):
    """
    Worker thread pour transcription asynchrone.

    Signaux:
        finished: Émis avec la liste des segments quand terminé
        progress: Émis avec le pourcentage (0-100)
        error: Émis avec un message d'erreur en cas de problème
    """

    finished = pyqtSignal(list)  # List[TranscriptionSegment]
    progress = pyqtSignal(int)  # Pourcentage de progression
    error = pyqtSignal(str)  # Message d'erreur

    def __init__(self, audio_path: str, model_size: str = "base", language: str = "fr"):
        """
        Initialise le worker.

        Args:
            audio_path: Chemin vers le fichier audio
            model_size: Taille du modèle Whisper (tiny, base, small, medium, large)
            language: Code de langue (fr, en, etc.)
        """
        super().__init__()
        self._audio_path = audio_path
        self._model_size = model_size
        self._language = language
        self._is_stopped = False

    def run(self):
        """Exécute la transcription dans le thread."""
        try:
            self.progress.emit(10)
            transcriber = WhisperTranscriber(model_size=self._model_size)

            if self._is_stopped:
                return

            self.progress.emit(30)
            result = transcriber.transcribe(self._audio_path, language=self._language)

            if self._is_stopped:
                transcriber.release()
                return

            self.progress.emit(90)
            transcriber.release()

            # Convertir le résultat en liste de segments
            segments = result.segments if result.status == TranscriptionStatus.COMPLETED else []
            self.progress.emit(100)
            self.finished.emit(segments)

        except Exception as e:
            self.error.emit(f"Erreur: {str(e)}")

    def stop(self):
        """Arrête le worker proprement."""
        self._is_stopped = True
