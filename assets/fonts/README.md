# Polices Personnalisées

## Police Inter pour JuryAIssist (PySide6)

La police **Inter** est utilisée dans le design Figma de JuryAIssist. Pour une fidélité maximale au design, veuillez télécharger et installer cette police.

### Téléchargement

1. Visitez: https://fonts.google.com/specimen/Inter
2. Cliquez sur "Download family"
3. Extrayez le fichier ZIP

### Installation pour PySide6

Copiez les fichiers suivants dans ce dossier (`assets/fonts/`):

- `Inter-Regular.ttf`
- `Inter-Medium.ttf`
- `Inter-SemiBold.ttf`
- `Inter-Bold.ttf`

### Structure attendue

```
assets/fonts/
├── Inter-Regular.ttf
├── Inter-Medium.ttf
├── Inter-SemiBold.ttf
├── Inter-Bold.ttf
└── README.md (ce fichier)
```

### Fallback

Si la police Inter n'est pas disponible, l'application utilisera automatiquement une police système de substitution:
- macOS: SF Pro Display
- Windows: Segoe UI
- Linux: Police sans-serif système

### Vérification

Lorsque vous lancez l'application PySide6, vous devriez voir dans la console:

```
✓ Police chargée: Inter-Regular.ttf
✓ Police chargée: Inter-Medium.ttf
✓ Police chargée: Inter-SemiBold.ttf
✓ Police chargée: Inter-Bold.ttf
✓ Police Inter définie comme police par défaut
```

Si vous voyez `⚠ Police Inter non trouvée`, cela signifie que les fichiers de police ne sont pas dans le bon dossier.

---

## Configuration Flet (ancienne interface)

Les polices sont configurées dans `src/main.py` pour l'interface Flet:

```python
page.fonts = {
    "SF Pro Display": "assets/fonts/SF-Pro-Display-Regular.otf",
    "SF Pro Display Bold": "assets/fonts/SF-Pro-Display-Bold.otf",
}
```

## Polices recommandées

- **Inter** : https://fonts.google.com/specimen/Inter (utilisée dans Figma)
- **SF Pro** : https://developer.apple.com/fonts/ (style Apple)
- **Roboto** : https://fonts.google.com/specimen/Roboto (alternative Google)

## Licence

Inter est sous licence SIL Open Font License 1.1, ce qui permet une utilisation libre dans les projets open source et commerciaux.

Licence complète: https://github.com/rsms/inter/blob/master/LICENSE.txt
