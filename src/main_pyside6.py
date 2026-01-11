"""
Point d'entrée de l'application JuryAIssist avec PySide6.

Lance l'interface graphique moderne avec Qt6.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from src.gui_pyside6.main_window_modern import ModernMainWindow


def load_inter_font(app: QApplication):
    """
    Charge la police Inter si disponible dans assets/fonts.

    Args:
        app: L'application Qt

    Returns:
        bool: True si la police a été chargée avec succès
    """
    # Chemin vers le dossier fonts
    fonts_dir = Path(__file__).parent.parent / "assets" / "fonts"

    # Essayer de charger les différentes variations de Inter
    inter_variants = [
        "Inter-Regular.ttf",
        "Inter-Medium.ttf",
        "Inter-SemiBold.ttf",
        "Inter-Bold.ttf"
    ]

    loaded = False
    for variant in inter_variants:
        font_path = fonts_dir / variant
        if font_path.exists():
            font_id = QFontDatabase.addApplicationFont(str(font_path))
            if font_id != -1:
                loaded = True
                print(f"✓ Police chargée: {variant}")

    if loaded:
        # Définir Inter comme police par défaut de l'application
        app.setFont(QFont("Inter", 14))
        print("✓ Police Inter définie comme police par défaut")
    else:
        print("⚠ Police Inter non trouvée, utilisation de la police système")

    return loaded


def main():
    """Point d'entrée de l'application."""
    app = QApplication(sys.argv)

    # Configuration de l'application
    app.setApplicationName("JuryAIssist")
    app.setOrganizationName("JuryAIssist")
    app.setApplicationVersion("2.0.0")

    # Style moderne
    app.setStyle("Fusion")

    # Charger la police Inter
    load_inter_font(app)

    # Créer et afficher la fenêtre principale
    window = ModernMainWindow()
    window.show()

    # Lancer la boucle d'événements
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
