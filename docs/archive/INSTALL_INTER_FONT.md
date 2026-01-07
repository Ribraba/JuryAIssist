# Installation de la police Inter

La nouvelle interface Figma utilise la police **Inter** pour une fidélité maximale au design.

## Option 1 : Installation système (Recommandé)

### macOS

1. Télécharger Inter : https://fonts.google.com/specimen/Inter
2. Cliquer sur "Download family"
3. Décompresser le fichier ZIP
4. Ouvrir le dossier `static/`
5. Double-cliquer sur chaque fichier `.ttf`
6. Cliquer sur "Installer la police"

Ou via Homebrew :
```bash
brew tap homebrew/cask-fonts
brew install font-inter
```

### Windows

1. Télécharger Inter : https://fonts.google.com/specimen/Inter
2. Extraire le ZIP
3. Aller dans `static/`
4. Sélectionner tous les fichiers `.ttf`
5. Clic droit → Installer

### Linux (Ubuntu/Debian)

```bash
# Créer le dossier fonts local
mkdir -p ~/.local/share/fonts

# Télécharger et installer
cd ~/.local/share/fonts
wget https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip
unzip Inter-4.0.zip
fc-cache -f -v
```

## Option 2 : Installation locale dans l'application

Si vous ne pouvez pas installer Inter au niveau système, placez les fichiers de police dans le dossier de l'application :

```bash
# Créer le dossier (déjà existant)
mkdir -p src/gui/fonts

# Télécharger Inter
curl -L -o /tmp/Inter.zip "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip"

# Extraire
cd /tmp
unzip Inter.zip

# Copier les fichiers nécessaires
cp Inter Desktop/static/*.ttf /path/to/JuryAIssist/src/gui/fonts/

# Nettoyer
rm -rf /tmp/Inter*
```

Les fichiers seront chargés automatiquement par `figma_resources.py`.

## Vérification

Pour vérifier que la police est installée :

### macOS
1. Ouvrir "Livre des polices"
2. Rechercher "Inter"
3. Vérifier que toutes les variantes sont présentes

### Windows
1. Ouvrir "Panneau de configuration" → "Polices"
2. Rechercher "Inter"

### Linux
```bash
fc-list | grep -i inter
```

### Dans l'application

Lancez l'interface et vérifiez dans la console :

```bash
python launch_figma_ui.py
```

Si Inter est chargée, vous verrez :
```
✓ Loaded font: Inter-Regular.ttf (Inter)
✓ Loaded font: Inter-Medium.ttf (Inter)
✓ Loaded font: Inter-SemiBold.ttf (Inter)
```

## Fallback

Si Inter n'est pas disponible, l'application utilisera automatiquement :
- **macOS** : SF Pro (Apple system font)
- **Windows** : Segoe UI
- **Linux** : System sans-serif

L'interface fonctionnera parfaitement, mais avec une typographie légèrement différente.

## Variantes nécessaires

Pour l'interface JuryAIssist, ces variantes sont utilisées :

| Poids | Utilisation |
|-------|-------------|
| Regular (400) | Texte standard, sous-titres |
| Medium (500) | Items de menu, texte transcription |
| SemiBold (600) | Titres, headers, texte important |

## Fichiers de police recommandés

Si vous installez manuellement, ces fichiers sont les plus importants :

```
Inter-Regular.ttf       # Poids 400
Inter-Medium.ttf        # Poids 500
Inter-SemiBold.ttf      # Poids 600
```

Les autres variantes (Thin, Light, Bold, etc.) ne sont pas utilisées dans l'interface actuelle.

## Taille du téléchargement

- **Fichier ZIP complet** : ~20 MB (toutes les variantes)
- **Fichiers nécessaires uniquement** : ~600 KB (3 fichiers .ttf)

## Liens utiles

- Site officiel Inter : https://rsms.me/inter/
- Google Fonts : https://fonts.google.com/specimen/Inter
- GitHub : https://github.com/rsms/inter
- Documentation : https://rsms.me/inter/docs/

---

**Note** : La police Inter est libre d'utilisation (SIL Open Font License 1.1)
