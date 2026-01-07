"""
Analyse détaillée du design Figma pour créer les design tokens.
"""
import json
from pathlib import Path
from collections import defaultdict

def load_design():
    """Charge le fichier JSON du design."""
    with open('figma_design.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_design_tokens(data):
    """Extrait les design tokens (couleurs, typographie, spacing)."""

    tokens = {
        'colors': defaultdict(list),
        'typography': defaultdict(list),
        'spacing': set(),
        'layout': {}
    }

    def traverse(node, path=""):
        # Couleurs
        if 'fills' in node:
            for fill in node['fills']:
                if fill.get('type') == 'SOLID' and 'color' in fill:
                    c = fill['color']
                    color_hex = f"#{int(c['r']*255):02x}{int(c['g']*255):02x}{int(c['b']*255):02x}"
                    opacity = fill.get('opacity', c.get('a', 1))
                    tokens['colors'][color_hex].append({
                        'opacity': opacity,
                        'context': node.get('name', 'unnamed'),
                        'path': path
                    })

        if 'backgroundColor' in node:
            bg = node['backgroundColor']
            if bg.get('a', 0) > 0:  # Seulement si visible
                color_hex = f"#{int(bg['r']*255):02x}{int(bg['g']*255):02x}{int(bg['b']*255):02x}"
                tokens['colors'][color_hex].append({
                    'opacity': bg.get('a', 1),
                    'context': f"{node.get('name', 'unnamed')} (bg)",
                    'path': path
                })

        # Typographie
        if node.get('type') == 'TEXT' and 'style' in node:
            style = node['style']
            font_key = f"{style.get('fontFamily', 'Unknown')}-{style.get('fontSize', 0)}px-{style.get('fontWeight', 400)}"
            tokens['typography'][font_key].append({
                'family': style.get('fontFamily'),
                'size': style.get('fontSize'),
                'weight': style.get('fontWeight'),
                'letterSpacing': style.get('letterSpacing', 0),
                'lineHeight': style.get('lineHeightPx', 0),
                'text': node.get('characters', '')[:50],
                'context': node.get('name'),
                'path': path
            })

        # Spacing (padding, gaps)
        if 'itemSpacing' in node:
            tokens['spacing'].add(node['itemSpacing'])
        if 'paddingLeft' in node:
            tokens['spacing'].add(node['paddingLeft'])
        if 'paddingRight' in node:
            tokens['spacing'].add(node['paddingRight'])
        if 'paddingTop' in node:
            tokens['spacing'].add(node['paddingTop'])
        if 'paddingBottom' in node:
            tokens['spacing'].add(node['paddingBottom'])

        # Récursion
        if 'children' in node:
            for i, child in enumerate(node['children']):
                child_path = f"{path}/{child.get('name', f'child-{i}')}"
                traverse(child, child_path)

    traverse(data.get('document', {}))
    return tokens

def analyze_layout_structure(data):
    """Analyse la structure du layout principal."""

    structure = {
        'sidebar': None,
        'main_content': None,
        'audio_controls': None,
        'transcript_panel': None,
        'editor_panel': None
    }

    def find_components(node, depth=0):
        name = node.get('name', '').lower()

        # Identifier les composants principaux
        if 'sidebar' in name:
            structure['sidebar'] = {
                'name': node.get('name'),
                'width': node.get('absoluteBoundingBox', {}).get('width'),
                'height': node.get('absoluteBoundingBox', {}).get('height'),
                'backgroundColor': node.get('backgroundColor', {}),
                'children_count': len(node.get('children', []))
            }

        if 'transcription brute' in name or 'transcript' in name:
            structure['transcript_panel'] = {
                'name': node.get('name'),
                'bbox': node.get('absoluteBoundingBox', {})
            }

        if 'édition' in name or 'editor' in name or 'bloc édition' in name:
            structure['editor_panel'] = {
                'name': node.get('name'),
                'bbox': node.get('absoluteBoundingBox', {})
            }

        # Récursion
        if 'children' in node:
            for child in node['children']:
                find_components(child, depth + 1)

    find_components(data.get('document', {}))
    return structure

def generate_design_tokens_file(tokens):
    """Génère un fichier Python avec les design tokens."""

    output = ['"""', 'Design tokens extraits du design Figma.', '"""', '']

    # Couleurs
    output.append('# === COLORS ===')
    output.append('COLORS = {')
    for color, usages in sorted(tokens['colors'].items()):
        contexts = ', '.join(set(u['context'] for u in usages[:3]))
        output.append(f'    "{color}": {{  # Used in: {contexts}')
        output.append(f'        "hex": "{color}",')
        if usages[0]['opacity'] < 1:
            output.append(f'        "opacity": {usages[0]["opacity"]},')
        output.append('    },')
    output.append('}')
    output.append('')

    # Typographie
    output.append('# === TYPOGRAPHY ===')
    output.append('TYPOGRAPHY = {')
    for font_key, usages in sorted(tokens['typography'].items()):
        usage = usages[0]
        safe_key = font_key.replace('-', '_').replace('.', '_')
        output.append(f'    "{safe_key}": {{')
        output.append(f'        "family": "{usage["family"]}",')
        output.append(f'        "size": {usage["size"]},')
        output.append(f'        "weight": {usage["weight"]},')
        if usage['letterSpacing'] != 0:
            output.append(f'        "letterSpacing": {usage["letterSpacing"]},')
        output.append(f'        # Used for: {usage["context"]}')
        output.append('    },')
    output.append('}')
    output.append('')

    # Spacing
    output.append('# === SPACING ===')
    output.append(f'SPACING = {sorted(tokens["spacing"])}')
    output.append('')

    return '\n'.join(output)

def main():
    print("Analyzing Figma design...")
    data = load_design()

    # Extraire les tokens
    print("\n1. Extracting design tokens...")
    tokens = extract_design_tokens(data)

    print(f"   - Found {len(tokens['colors'])} unique colors")
    print(f"   - Found {len(tokens['typography'])} typography styles")
    print(f"   - Found {len(tokens['spacing'])} spacing values")

    # Analyser la structure
    print("\n2. Analyzing layout structure...")
    structure = analyze_layout_structure(data)

    print("\nLayout components found:")
    for key, value in structure.items():
        if value:
            print(f"   ✓ {key}: {value.get('name', 'Found')}")

    # Générer le fichier de tokens
    print("\n3. Generating design tokens file...")
    tokens_content = generate_design_tokens_file(tokens)

    with open('src/gui/design_tokens.py', 'w', encoding='utf-8') as f:
        f.write(tokens_content)

    print("   ✓ Design tokens saved to src/gui/design_tokens.py")

    # Générer un rapport détaillé
    print("\n4. Generating detailed report...")

    report = []
    report.append("# Figma Design Analysis Report")
    report.append("")
    report.append("## Color Palette")
    report.append("")
    for color, usages in sorted(tokens['colors'].items()):
        report.append(f"### {color}")
        for usage in usages[:5]:  # Top 5 usages
            report.append(f"- {usage['context']} (opacity: {usage['opacity']})")
        report.append("")

    report.append("## Typography Styles")
    report.append("")
    for font_key, usages in sorted(tokens['typography'].items()):
        usage = usages[0]
        report.append(f"### {usage['family']} {usage['size']}px (Weight: {usage['weight']})")
        report.append(f"- Used in: {usage['context']}")
        report.append(f"- Example: \"{usage['text']}\"")
        report.append("")

    report.append("## Layout Structure")
    report.append("")
    for key, value in structure.items():
        if value:
            report.append(f"### {key.replace('_', ' ').title()}")
            report.append(f"```")
            report.append(json.dumps(value, indent=2))
            report.append(f"```")
            report.append("")

    with open('figma_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print("   ✓ Report saved to figma_analysis_report.md")

    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
