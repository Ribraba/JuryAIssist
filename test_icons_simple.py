"""
Trouve les icônes correctes dans Flet.
"""
import flet as ft

# Icônes à chercher (sans suffixes)
icons_needed = [
    "GAVEL", "BALANCE", "ACCOUNT_BALANCE",  # Justice
    "ADD_CIRCLE", "ADD_CIRCLE_OUTLINE",     # Ajout
    "SETTINGS", "SETTINGS_OUTLINE",         # Paramètres
    "AUDIOTRACK", "AUDIO_FILE",             # Audio
    "DESCRIPTION", "ARTICLE",               # Document
    "TEXT_SNIPPET", "NOTES",                # Texte
    "REPLAY_5", "FAST_REWIND",              # Reculer
    "FORWARD_5", "FAST_FORWARD",            # Avancer
    "STOP", "STOP_CIRCLE",                  # Stop
    "SPEED", "TUNE",                        # Vitesse
    "VOLUME_UP", "VOLUME_DOWN",             # Volume
    "PLAY_ARROW", "PLAY_CIRCLE",            # Play
    "PAUSE", "PAUSE_CIRCLE",                # Pause
    "CHECK_CIRCLE", "CIRCLE",               # Check
]

print("Icônes disponibles:")
for icon_name in icons_needed:
    if hasattr(ft.icons, icon_name):
        print(f"✓ {icon_name}")
