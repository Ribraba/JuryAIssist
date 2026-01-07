"""
Widgets personnalisés pour l'interface graphique.
"""

from src.gui.widgets.audio_controls_panel import AudioControlsPanel
from src.gui.widgets.editor import EditorPanel
from src.gui.widgets.transcript import TranscriptPanel
from src.gui.widgets.sidebar import SidebarWidget
from src.gui.widgets.scrolling_transcript_timeline import ScrollingTranscriptTimeline
from src.gui.widgets.pedal_status_badge import PedalStatusBadge

__all__ = [
    "AudioControlsPanel",
    "EditorPanel",
    "TranscriptPanel",
    "SidebarWidget",
    "ScrollingTranscriptTimeline",
    "PedalStatusBadge",
]
