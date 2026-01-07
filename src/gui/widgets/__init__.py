"""
Widgets personnalisés pour l'interface graphique.

Widgets selon Phase 3 de la roadmap.
"""

from src.gui.widgets.timeline_widget import TimelineWidget
from src.gui.widgets.audio_controls import AudioControlsWidget
from src.gui.widgets.editor_panel import EditorPanel
from src.gui.widgets.transcript_panel import TranscriptPanel

__all__ = [
    "TimelineWidget",
    "AudioControlsWidget",
    "EditorPanel",
    "TranscriptPanel",
]
