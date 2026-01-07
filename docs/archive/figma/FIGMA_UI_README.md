# Interface Figma - JuryAIssist

## Vue d'ensemble

Nouvelle interface utilisateur moderne basée sur le design Figma, créée en parallèle de l'interface actuelle.

## Lancement

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer la nouvelle interface Figma
python launch_figma_ui.py

# Lancer l'ancienne interface (pour comparaison)
python -m src.main
```

## Fonctionnalités

### ✅ Implémenté

1. **Sidebar de navigation**
   - Logo "JuryAIssist"
   - Barre de recherche (visuel uniquement pour l'instant)
   - Liste des transcriptions avec sélection
   - Boutons "Nouvel import" et "Paramètres"

2. **Timeline avec transcription défilante**
   - Texte horizontal défilant au-dessus de la timeline
   - Opacité progressive (100% pour le mot actuel, dégradé pour avant/après)
   - Synchronisation en temps réel avec la lecture
   - Clic sur la timeline pour naviguer

3. **Panneau de transcription brute**
   - En-tête "Transcription brute" / "Lecture"
   - Affichage lecture seule
   - Surlignage du segment actuel
   - Clic sur mot pour navigation

4. **Panneau d'édition**
   - En-tête avec nom du fichier / "Édition"
   - Zone de texte éditable
   - Grande police (24px) pour confort de lecture

5. **Contrôles audio**
   - Boutons Play/Pause, Skip, Stop
   - Slider de volume
   - Indicateur de temps (00:15 / 02:45:30)
   - Indicateur de vitesse (1.0x) cliquable

6. **Badge de statut de pédale**
   - Indicateur visuel en haut à droite
   - Vert si connecté, gris sinon
   - Affiche le modèle (RS-31)

### 🎨 Design

- **Police**: Inter (avec fallback système)
- **Couleurs**:
  - Background: #ffffff (blanc)
  - Timeline: #eeeeee (gris clair)
  - Accent: #477ed8 (bleu)
  - Texte principal: #000000
  - Texte secondaire: #444444
- **Spacing**: Système cohérent (4px, 8px, 16px, 24px)

### 📐 Principes SOLID appliqués

Chaque composant respecte les principes SOLID + Tell, Don't Ask:

- **Single Responsibility**: Chaque widget a une responsabilité unique
- **Open/Closed**: Extensible sans modification
- **Liskov Substitution**: Interfaces cohérentes
- **Interface Segregation**: Signaux et méthodes minimales
- **Dependency Inversion**: Injection de dépendances

## Structure des fichiers

```
src/gui/
├── figma_resources.py          # Gestion des icônes et polices
├── figma_styles.py              # Styles QSS et design tokens
├── design_tokens.py             # Tokens extraits de Figma
├── main_window_figma.py         # Fenêtre principale Figma
└── widgets/
    ├── sidebar.py               # Navigation latérale
    ├── scrolling_transcript_timeline.py  # Timeline innovante
    ├── figma_transcript_panel.py         # Transcription lecture seule
    ├── figma_editor_panel.py             # Éditeur
    ├── figma_audio_controls.py           # Contrôles audio
    └── pedal_status_badge.py             # Badge pédale
```

## Icônes

Les icônes SVG sont dans `src/gui/icons_figma/`:
- `loupe.svg` - Recherche
- `radio.svg` - Sélection de fichier
- `dossier.svg` - Import
- `engrenage.svg` - Paramètres
- `play.svg` - Lecture
- `stop.svg` - Arrêt
- `skip_backward.svg` / `skip_forward.svg` - Navigation
- `mute.svg` - Volume
- `pedale.svg` - Indicateur de pédale

## Fonctionnalités à venir

### En développement

- [ ] Fonctionnalité de recherche dans la sidebar
- [ ] Export TXT/DOCX
- [ ] Raccourcis clavier
- [ ] Configuration de la transcription (modèle, langue)
- [ ] Gestion persistante de la liste des fichiers
- [ ] Icône Pause (actuellement utilise Play)

### Améliorations prévues

- [ ] Thème sombre
- [ ] Animation de transition
- [ ] Sauvegarde automatique
- [ ] Historique des modifications
- [ ] Marqueurs de temps personnalisés

## Différences avec l'interface actuelle

### Ajouté

1. **Sidebar** - Navigation latérale moderne
2. **Timeline avec transcription défilante** - Innovation majeure pour la navigation
3. **Badge de pédale** - Indicateur visuel permanent
4. **Design moderne** - Interface épurée et professionnelle

### Modifié

1. **Pas de barre de menu traditionnelle** - Remplacée par boutons dans sidebar
2. **Layout repensé** - Sidebar + contenu plutôt que layout traditionnel
3. **Contrôles audio compacts** - Design horizontal optimisé
4. **Typographie** - Polices et tailles revues pour meilleure lisibilité

### Conservé

1. **Toutes les fonctionnalités principales**
2. **Support de la pédale**
3. **Transcription Whisper**
4. **Édition de texte**
5. **Export de fichiers**

## Migration

Une fois validé, pour migrer complètement vers la nouvelle interface :

1. Renommer `src/gui/main_window.py` → `src/gui/main_window_old.py`
2. Renommer `src/gui/main_window_figma.py` → `src/gui/main_window.py`
3. Mettre à jour `src/main.py` pour utiliser la nouvelle interface
4. Supprimer les anciens widgets non utilisés
5. Mettre à jour les tests

## Notes techniques

### Police Inter

La police Inter est chargée depuis le dossier `src/gui/fonts/` si disponible.
Sinon, un fallback système est utilisé :
- macOS: SF Pro
- Windows: Segoe UI
- Linux: System sans-serif

Pour installer Inter manuellement:
1. Télécharger depuis https://fonts.google.com/specimen/Inter
2. Placer les fichiers .ttf dans `src/gui/fonts/`

### Performances

- Les icônes SVG sont mises en cache
- La timeline utilise un rendu optimisé
- Le surlignage de transcription ne redessine que ce qui est nécessaire

## Tests

```bash
# Tester l'interface
python launch_figma_ui.py

# Tester avec un fichier audio
# 1. Lancer l'interface
# 2. Cliquer sur "Nouvel import" ou sidebar
# 3. Sélectionner un fichier audio
# 4. Tester la transcription et la navigation
```

## Problèmes connus

- L'icône de pause n'est pas encore disponible (utilise play pour l'instant)
- La recherche dans la sidebar est visuelle uniquement
- Les fichiers de la liste ne sont pas persistants entre les sessions

## Contribution

Pour ajouter de nouvelles fonctionnalités :

1. Créer un nouveau widget dans `src/gui/widgets/`
2. Suivre les principes SOLID
3. Utiliser les design tokens de `figma_styles.py`
4. Documenter les signaux et méthodes
5. Tester avec la nouvelle interface

---

**Version**: 1.0.0
**Date**: 2026-01-06
**Design Figma**: https://www.figma.com/design/0ieFrBWSvz46jv5zOYcW4e/JuryAIssist
