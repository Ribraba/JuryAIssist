"""
Script pour récupérer et analyser le design Figma.
"""
import requests
import json
from pathlib import Path

# Configuration
FIGMA_TOKEN = "figd_KAg1rQM6CsQmpSkulCL8avCSZBcj0d09tWqDHAxh"
FILE_KEY = "0ieFrBWSvz46jv5zOYcW4e"

# Headers pour l'API
headers = {
    "X-Figma-Token": FIGMA_TOKEN
}

def fetch_figma_file():
    """Récupère les données du fichier Figma."""
    url = f"https://api.figma.com/v1/files/{FILE_KEY}"

    print(f"Fetching Figma file: {FILE_KEY}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Sauvegarder les données brutes
        output_file = Path("figma_design.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Design saved to {output_file}")
        return data
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
        return None

def analyze_design(data):
    """Analyse les données du design."""
    if not data:
        return

    print("\n" + "="*60)
    print("FIGMA DESIGN ANALYSIS")
    print("="*60)

    # Informations générales
    document = data.get('document', {})
    print(f"\nFile name: {data.get('name')}")
    print(f"Last modified: {data.get('lastModified')}")

    # Parcourir les pages
    if 'children' in document:
        print(f"\nPages found: {len(document['children'])}")
        for page in document['children']:
            print(f"\n  Page: {page.get('name')}")
            analyze_node(page, indent=4)

    # Styles
    styles = data.get('styles', {})
    if styles:
        print(f"\nStyles defined: {len(styles)}")

    # Composants
    components = data.get('components', {})
    if components:
        print(f"Components defined: {len(components)}")

def analyze_node(node, indent=0):
    """Analyse récursivement un nœud."""
    prefix = " " * indent
    node_type = node.get('type', 'UNKNOWN')
    node_name = node.get('name', 'Unnamed')

    # Afficher les informations importantes
    if node_type in ['FRAME', 'GROUP', 'COMPONENT', 'INSTANCE', 'RECTANGLE', 'TEXT']:
        print(f"{prefix}├─ [{node_type}] {node_name}")

        # Dimensions
        if 'absoluteBoundingBox' in node:
            bbox = node['absoluteBoundingBox']
            w, h = bbox.get('width', 0), bbox.get('height', 0)
            print(f"{prefix}   Size: {w:.0f}x{h:.0f}")

        # Couleurs de fond
        if 'backgroundColor' in node:
            bg = node['backgroundColor']
            print(f"{prefix}   BG: rgba({bg.get('r',0)*255:.0f}, {bg.get('g',0)*255:.0f}, {bg.get('b',0)*255:.0f}, {bg.get('a',1):.2f})")

        # Texte
        if node_type == 'TEXT' and 'characters' in node:
            text = node['characters'][:50]
            print(f"{prefix}   Text: \"{text}...\"")

            if 'style' in node:
                style = node['style']
                print(f"{prefix}   Font: {style.get('fontFamily', 'Unknown')} {style.get('fontSize', 0)}px")

    # Récursion sur les enfants
    if 'children' in node:
        for child in node['children']:
            analyze_node(child, indent + 2)

def extract_colors(data):
    """Extrait toutes les couleurs utilisées."""
    colors = set()

    def traverse(node):
        # Couleur de fond
        if 'backgroundColor' in node:
            bg = node['backgroundColor']
            colors.add((
                int(bg.get('r', 0) * 255),
                int(bg.get('g', 0) * 255),
                int(bg.get('b', 0) * 255),
                bg.get('a', 1)
            ))

        # Couleurs de remplissage
        if 'fills' in node:
            for fill in node['fills']:
                if fill.get('type') == 'SOLID' and 'color' in fill:
                    c = fill['color']
                    colors.add((
                        int(c.get('r', 0) * 255),
                        int(c.get('g', 0) * 255),
                        int(c.get('b', 0) * 255),
                        fill.get('opacity', 1)
                    ))

        # Récursion
        if 'children' in node:
            for child in node['children']:
                traverse(child)

    traverse(data.get('document', {}))

    print("\n" + "="*60)
    print("COLOR PALETTE")
    print("="*60)
    for r, g, b, a in sorted(colors):
        print(f"rgba({r}, {g}, {b}, {a:.2f}) | #{r:02x}{g:02x}{b:02x}")

if __name__ == "__main__":
    # Récupérer le design
    data = fetch_figma_file()

    # Analyser
    if data:
        analyze_design(data)
        extract_colors(data)
