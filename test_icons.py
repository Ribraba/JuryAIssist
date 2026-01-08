"""
Test rapide des icônes utilisées dans l'application.
"""
import flet as ft

# Liste des icônes utilisées
icons_to_test = [
    "GAVEL_ROUNDED",
    "ADD_CIRCLE_OUTLINE_ROUNDED",
    "SETTINGS_OUTLINED",
    "AUDIOTRACK_ROUNDED",
    "DESCRIPTION_OUTLINED",
    "TEXT_SNIPPET_OUTLINED",
    "ARTICLE_OUTLINED",
    "REPLAY_5_ROUNDED",
    "FORWARD_5_ROUNDED",
    "STOP_ROUNDED",
    "SPEED_ROUNDED",
    "VOLUME_UP_ROUNDED",
    "PLAY_ARROW_ROUNDED",
    "PAUSE_ROUNDED",
    "CHECK_CIRCLE",
    "CIRCLE_OUTLINED",
]

print("Test des icônes Flet:")
print("-" * 50)

for icon_name in icons_to_test:
    try:
        icon_value = getattr(ft.icons, icon_name)
        print(f"✓ {icon_name}: {icon_value}")
    except AttributeError:
        print(f"✗ {icon_name}: NON DISPONIBLE")

print("-" * 50)
print("\nTest terminé!")
