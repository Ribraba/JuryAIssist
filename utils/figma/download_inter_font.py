"""
Télécharge la police Inter depuis Google Fonts.
"""
import urllib.request
import zipfile
from pathlib import Path

def download_inter_font():
    """Télécharge la police Inter."""
    font_dir = Path("src/gui/fonts")
    font_dir.mkdir(parents=True, exist_ok=True)

    print("Downloading Inter font from Google Fonts...")

    # URL de téléchargement direct de Inter depuis Google Fonts
    url = "https://fonts.google.com/download?family=Inter"

    zip_path = font_dir / "inter.zip"

    try:
        # Télécharger
        urllib.request.urlretrieve(url, zip_path)
        print(f"✓ Downloaded to {zip_path}")

        # Extraire
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(font_dir)
        print(f"✓ Extracted to {font_dir}")

        # Nettoyer le zip
        zip_path.unlink()
        print("✓ Cleaned up zip file")

        # Lister les fichiers extraits
        fonts = list(font_dir.glob("**/*.ttf"))
        print(f"\n✓ Found {len(fonts)} font files:")
        for font in fonts:
            print(f"  - {font.name}")

        return True

    except Exception as e:
        print(f"✗ Error downloading font: {e}")
        print("\n⚠️  Alternative: Download manually from https://fonts.google.com/specimen/Inter")
        print("   and place .ttf files in src/gui/fonts/")
        return False

if __name__ == "__main__":
    download_inter_font()
