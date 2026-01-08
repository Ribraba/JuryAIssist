"""
Script pour corriger les icônes dans les fichiers Flet.
Les icônes Material dans Flet utilisent des chaînes de caractères, pas des constantes.
"""
import re
from pathlib import Path

# Mapping des icônes utilisées
ICON_MAPPING = {
    "ft.icons.GAVEL": '"gavel"',
    "ft.icons.ADD_CIRCLE_OUTLINE": '"add_circle_outline"',
    "ft.icons.SETTINGS": '"settings"',
    "ft.icons.AUDIOTRACK": '"audiotrack"',
    "ft.icons.DESCRIPTION": '"description"',
    "ft.icons.TEXT_SNIPPET": '"text_snippet"',
    "ft.icons.ARTICLE": '"article"',
    "ft.icons.REPLAY_5": '"replay_5"',
    "ft.icons.FORWARD_5": '"forward_5"',
    "ft.icons.STOP": '"stop"',
    "ft.icons.SPEED": '"speed"',
    "ft.icons.VOLUME_UP": '"volume_up"',
    "ft.icons.PLAY_ARROW": '"play_arrow"',
    "ft.icons.PAUSE": '"pause"',
    "ft.icons.CHECK_CIRCLE": '"check_circle"',
    "ft.icons.CIRCLE": '"circle"',
}

def fix_icons_in_file(file_path: Path):
    """Corrige les icônes dans un fichier."""
    content = file_path.read_text()
    original = content

    for old, new in ICON_MAPPING.items():
        content = content.replace(old, new)

    if content != original:
        file_path.write_text(content)
        print(f"✓ Corrigé: {file_path}")
        return True
    return False

# Trouver tous les fichiers Python dans src/gui_flet
gui_flet_dir = Path("src/gui_flet")
python_files = list(gui_flet_dir.rglob("*.py"))

print(f"Correction des icônes dans {len(python_files)} fichiers...")
print("-" * 50)

fixed_count = 0
for py_file in python_files:
    if fix_icons_in_file(py_file):
        fixed_count += 1

print("-" * 50)
print(f"\n✅ {fixed_count} fichier(s) corrigé(s)")
