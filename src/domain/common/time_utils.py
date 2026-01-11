"""
Module common - Utilitaires temps (Qt-free).

Fonctions utilitaires pour la conversion et le formatage de temps.
"""


class TimeUtils:
    """Utilitaires statiques pour manipuler le temps."""

    @staticmethod
    def seconds_to_timestamp(seconds: float) -> str:
        """
        Convertit des secondes en timestamp formaté HH:MM:SS ou MM:SS.

        Args:
            seconds: Temps en secondes

        Returns:
            Timestamp formaté (ex: "1:23:45" ou "5:30")

        Examples:
            >>> TimeUtils.seconds_to_timestamp(65.5)
            '1:05'
            >>> TimeUtils.seconds_to_timestamp(3665.2)
            '1:01:05'
        """
        if seconds < 0:
            seconds = 0

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    @staticmethod
    def timestamp_to_seconds(timestamp: str) -> float:
        """
        Convertit un timestamp formaté en secondes.

        Args:
            timestamp: Timestamp formaté (HH:MM:SS, MM:SS, ou SS)

        Returns:
            Temps en secondes

        Examples:
            >>> TimeUtils.timestamp_to_seconds("1:05")
            65.0
            >>> TimeUtils.timestamp_to_seconds("1:01:05")
            3665.0
        """
        parts = timestamp.split(":")
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
        elif len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        elif len(parts) == 1:
            return float(parts[0])
        else:
            raise ValueError(f"Invalid timestamp format: {timestamp}")

    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Formate une durée de manière lisible.

        Args:
            seconds: Durée en secondes

        Returns:
            Durée formatée (ex: "1h 23m 45s", "5m 30s", "45s")
        """
        if seconds < 0:
            seconds = 0

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")

        return " ".join(parts)
