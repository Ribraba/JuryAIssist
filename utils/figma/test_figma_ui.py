"""
Test rapide de l'interface Figma sans lancer la GUI complète.
"""
import sys
sys.path.insert(0, '/Users/ibrahim/Documents/Projets/JuryAIssist')

print("🧪 Test de l'interface Figma...")
print()

# Test imports
print("1️⃣ Test des imports...")
try:
    from src.gui.figma_styles import FigmaColors, FigmaSpacing, FigmaTypography
    print("   ✅ figma_styles")
except Exception as e:
    print(f"   ❌ figma_styles: {e}")

try:
    from src.gui.figma_resources import get_icon, get_font
    print("   ✅ figma_resources")
except Exception as e:
    print(f"   ❌ figma_resources: {e}")

try:
    from src.gui.widgets.sidebar import SidebarWidget
    print("   ✅ sidebar")
except Exception as e:
    print(f"   ❌ sidebar: {e}")

try:
    from src.gui.widgets.scrolling_transcript_timeline import ScrollingTranscriptTimeline
    print("   ✅ scrolling_transcript_timeline")
except Exception as e:
    print(f"   ❌ scrolling_transcript_timeline: {e}")

try:
    from src.gui.widgets.figma_transcript_panel import FigmaTranscriptPanel
    print("   ✅ figma_transcript_panel")
except Exception as e:
    print(f"   ❌ figma_transcript_panel: {e}")

try:
    from src.gui.widgets.figma_editor_panel import FigmaEditorPanel
    print("   ✅ figma_editor_panel")
except Exception as e:
    print(f"   ❌ figma_editor_panel: {e}")

try:
    from src.gui.widgets.figma_audio_controls import FigmaAudioControls
    print("   ✅ figma_audio_controls")
except Exception as e:
    print(f"   ❌ figma_audio_controls: {e}")

try:
    from src.gui.widgets.pedal_status_badge import PedalStatusBadge
    print("   ✅ pedal_status_badge")
except Exception as e:
    print(f"   ❌ pedal_status_badge: {e}")

try:
    from src.gui.main_window_figma import MainWindowFigma
    print("   ✅ main_window_figma")
except Exception as e:
    print(f"   ❌ main_window_figma: {e}")

print()
print("2️⃣ Test des design tokens...")
print(f"   Couleurs: {len(FigmaColors.__dict__)} définies")
print(f"   Spacing: {len(FigmaSpacing.__dict__)} valeurs")
print(f"   Typography: {len(FigmaTypography.__dict__)} styles")

print()
print("3️⃣ Test des icônes...")
import os
icons_dir = "/Users/ibrahim/Documents/Projets/JuryAIssist/src/gui/icons_figma"
if os.path.exists(icons_dir):
    icons = [f for f in os.listdir(icons_dir) if f.endswith('.svg')]
    print(f"   ✅ {len(icons)} icônes SVG trouvées:")
    for icon in sorted(icons):
        print(f"      - {icon}")
else:
    print("   ❌ Dossier icons_figma introuvable")

print()
print("✅ Tests terminés !")
print()
print("Pour lancer l'interface complète:")
print("   python launch_figma_ui.py")
