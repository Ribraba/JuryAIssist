"""
Module audio - Entités du domain layer (Qt-free).

Définit les entités et value objects du domaine audio.
"""

from enum import Enum


class PlayerState(Enum):
    """États possibles du lecteur audio."""

    STOPPED = "stopped"  # Arrêté, position à 0
    PLAYING = "playing"  # En cours de lecture
    PAUSED = "paused"  # En pause, position conservée
    ERROR = "error"  # Erreur (fichier invalide, codec manquant, etc.)
