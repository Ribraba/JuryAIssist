"""
Utilitaires de gestion du temps pour l'audio.

Fournit des fonctions de conversion et de formatage du temps
pour l'affichage dans l'interface graphique.

Architecture SOLID :
- Single Responsibility : Conversion et formatage du temps uniquement
- Stateless : Fonctions pures sans état
"""

from typing import Tuple


class TimeUtils:
    """
    Utilitaires statiques pour conversion et formatage du temps.

    Toutes les méthodes sont statiques car elles ne dépendent pas d'un état.
    """

    @staticmethod
    def seconds_to_timestamp(seconds: float) -> str:
        """
        Convertit des secondes en format HH:MM:SS ou MM:SS.

        Args:
            seconds: Temps en secondes (peut être float)

        Returns:
            Chaîne formatée (HH:MM:SS si >= 1h, sinon MM:SS)

        Examples:
            >>> TimeUtils.seconds_to_timestamp(65.5)
            '01:05'
            >>> TimeUtils.seconds_to_timestamp(3665.2)
            '01:01:05'
            >>> TimeUtils.seconds_to_timestamp(0)
            '00:00'
        """
        # Gérer les valeurs négatives
        if seconds < 0:
            seconds = 0

        # Convertir en entier (arrondi inférieur)
        total_seconds = int(seconds)

        # Extraire heures, minutes, secondes
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        # Format avec ou sans heures
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def timestamp_to_seconds(timestamp: str) -> float:
        """
        Convertit un timestamp HH:MM:SS ou MM:SS en secondes.

        Args:
            timestamp: Chaîne au format HH:MM:SS ou MM:SS

        Returns:
            Temps en secondes (float)

        Raises:
            ValueError: Si le format est invalide

        Examples:
            >>> TimeUtils.timestamp_to_seconds("01:05")
            65.0
            >>> TimeUtils.timestamp_to_seconds("01:01:05")
            3665.0
            >>> TimeUtils.timestamp_to_seconds("00:00")
            0.0
        """
        parts = timestamp.strip().split(":")

        if len(parts) == 2:
            # Format MM:SS
            try:
                minutes = int(parts[0])
                seconds = int(parts[1])
                return float(minutes * 60 + seconds)
            except ValueError as e:
                raise ValueError(f"Format MM:SS invalide: {timestamp}") from e

        elif len(parts) == 3:
            # Format HH:MM:SS
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return float(hours * 3600 + minutes * 60 + seconds)
            except ValueError as e:
                raise ValueError(f"Format HH:MM:SS invalide: {timestamp}") from e

        else:
            raise ValueError(
                f"Format timestamp invalide: {timestamp}. "
                f"Attendu: MM:SS ou HH:MM:SS"
            )

    @staticmethod
    def get_percentage(position: float, duration: float) -> float:
        """
        Calcule le pourcentage de progression.

        Args:
            position: Position actuelle en secondes
            duration: Durée totale en secondes

        Returns:
            Pourcentage (0.0 à 100.0)

        Examples:
            >>> TimeUtils.get_percentage(30, 100)
            30.0
            >>> TimeUtils.get_percentage(0, 100)
            0.0
            >>> TimeUtils.get_percentage(100, 100)
            100.0
            >>> TimeUtils.get_percentage(50, 0)  # Durée nulle
            0.0
        """
        if duration <= 0:
            return 0.0

        percentage = (position / duration) * 100.0

        # Clamping 0-100
        return max(0.0, min(100.0, percentage))

    @staticmethod
    def format_duration_compact(seconds: float) -> str:
        """
        Formate une durée de manière compacte pour l'affichage.

        Args:
            seconds: Durée en secondes

        Returns:
            Chaîne formatée compacte (ex: "1h 5m", "45s", "2h 30m 15s")

        Examples:
            >>> TimeUtils.format_duration_compact(65)
            '1m 5s'
            >>> TimeUtils.format_duration_compact(3665)
            '1h 1m 5s'
            >>> TimeUtils.format_duration_compact(45)
            '45s'
            >>> TimeUtils.format_duration_compact(3600)
            '1h'
        """
        if seconds < 0:
            seconds = 0

        total_seconds = int(seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        parts = []

        if hours > 0:
            parts.append(f"{hours}h")

        if minutes > 0:
            parts.append(f"{minutes}m")

        if secs > 0 or not parts:  # Afficher "0s" si durée = 0
            parts.append(f"{secs}s")

        return " ".join(parts)

    @staticmethod
    def parse_time_components(seconds: float) -> Tuple[int, int, int]:
        """
        Décompose un temps en composantes (heures, minutes, secondes).

        Args:
            seconds: Temps en secondes

        Returns:
            Tuple (heures, minutes, secondes)

        Examples:
            >>> TimeUtils.parse_time_components(3665)
            (1, 1, 5)
            >>> TimeUtils.parse_time_components(65)
            (0, 1, 5)
        """
        if seconds < 0:
            seconds = 0

        total_seconds = int(seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        return (hours, minutes, secs)

    @staticmethod
    def format_remaining_time(position: float, duration: float) -> str:
        """
        Formate le temps restant.

        Args:
            position: Position actuelle en secondes
            duration: Durée totale en secondes

        Returns:
            Temps restant formaté (ex: "-05:30" pour 5min 30s restantes)

        Examples:
            >>> TimeUtils.format_remaining_time(30, 100)
            '-01:10'
            >>> TimeUtils.format_remaining_time(100, 100)
            '-00:00'
        """
        remaining = duration - position

        if remaining < 0:
            remaining = 0

        # Format avec signe moins
        timestamp = TimeUtils.seconds_to_timestamp(remaining)
        return f"-{timestamp}"
