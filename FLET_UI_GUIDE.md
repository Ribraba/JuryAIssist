# Guide de la Nouvelle Interface Flet

## Vue d'ensemble

La nouvelle interface JuryAIssist a été complètement repensée avec **Flet** pour offrir une expérience moderne et minimaliste inspirée de macOS.

### Pourquoi Flet?

- **Moderne et cross-platform**: Fonctionne sur macOS, Windows et Linux avec le même code
- **Design fluide**: Interface responsive et animations fluides
- **Plus léger**: Moins de dépendances que PyQt5
- **Apple-like**: Design épuré et élégant

## Nouvelles fonctionnalités

### Design minimaliste

- **Palette de couleurs Apple**: Blanc cassé, gris doux, bleu système
- **Composants arrondis**: Bordures douces et ombres subtiles
- **Typographie claire**: Police system avec tailles cohérentes
- **Animations fluides**: Transitions et effets visuels agréables

### Interface

L'interface est divisée en zones claires:

1. **Sidebar gauche**
   - Logo et titre de l'application
   - Bouton d'import de fichiers audio
   - Liste des fichiers importés
   - Bouton paramètres

2. **Zone principale**
   - Badge de statut de la pédale (en haut)
   - Éditeur de transcription (zone principale)
   - Vue de transcription scrollable avec timestamps cliquables
   - Lecteur audio avec contrôles complets

3. **Lecteur audio**
   - Timeline interactive
   - Boutons de lecture (Reculer 5s, Play/Pause, Avancer 5s, Stop)
   - Contrôle de vitesse (0.5x à 2.0x)
   - Contrôle de volume

## Architecture technique

### Modules réutilisés

Tous les modules métier ont été conservés:
- `src/audio/`: Lecture audio avec VLC
- `src/transcription/`: Transcription avec Whisper
- `src/devices/`: Support pédale Olympus RS-31
- Tests unitaires: 134 tests toujours fonctionnels

### Nouvelle structure GUI

```
src/gui_flet/
├── __init__.py
├── theme.py                      # Thème et constantes de design
├── main_window.py                # Fenêtre principale et logique
└── components/
    ├── sidebar.py                # Sidebar avec navigation
    ├── audio_player.py           # Lecteur audio complet
    ├── editor_panel.py           # Éditeur de transcription
    └── transcription_view.py     # Vue segments avec timestamps
```

### Principes SOLID respectés

- **Single Responsibility**: Chaque composant a une responsabilité unique
- **Open/Closed**: Extensions possibles sans modification
- **Liskov Substitution**: Composants interchangeables
- **Interface Segregation**: Interfaces claires via callbacks
- **Dependency Inversion**: Injection de dépendances via callbacks

## Installation et utilisation

### Installation

```bash
# Se placer sur la branche Flet
git checkout feature/flet-ui

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement

```bash
# Lancer l'application
python -m src.main

# Ou directement
python src/main.py
```

## Comparaison des branches

### Branche `main` (PyQt5)
- Interface PyQt5 classique
- Plus de code (4898 lignes supprimées)
- Design basé sur Figma
- Nécessite PyQt5, PyQt5-Qt5, PyQt5-sip

### Branche `feature/flet-ui` (Flet)
- Interface Flet moderne
- Code simplifié (1710 nouvelles lignes)
- Design minimaliste Apple-like
- Nécessite seulement Flet

## Commandes Git utiles

### Voir les branches disponibles
```bash
git branch -a
```

### Basculer entre les branches

```bash
# Aller sur la branche principale (PyQt5)
git checkout main

# Aller sur la branche Flet
git checkout feature/flet-ui
```

### Comparer les branches

```bash
# Voir les différences entre les branches
git diff main feature/flet-ui

# Voir uniquement les fichiers modifiés
git diff --name-status main feature/flet-ui
```

### Fusionner la branche Flet dans main (quand prêt)

```bash
# Se placer sur main
git checkout main

# Fusionner Flet
git merge feature/flet-ui

# En cas de conflit, résoudre puis:
git add .
git commit
```

## Workflow de développement

### Tester la nouvelle interface

1. Basculer sur la branche Flet:
   ```bash
   git checkout feature/flet-ui
   ```

2. Installer les dépendances:
   ```bash
   pip install -r requirements.txt
   ```

3. Lancer l'application:
   ```bash
   python -m src.main
   ```

4. Tester les fonctionnalités:
   - Import de fichier audio
   - Transcription automatique
   - Lecture audio avec contrôles
   - Navigation par timestamps
   - Export TXT/DOCX
   - Support pédale (si disponible)

### Revenir à l'ancienne interface

```bash
# Revenir sur main
git checkout main

# Réinstaller les dépendances PyQt5
pip install -r requirements.txt

# Lancer
python -m src.main
```

## Fonctionnalités futures

### À implémenter

- [ ] Dialogue de paramètres complet
- [ ] Configuration des touches de pédale dans l'UI
- [ ] Thème dark mode
- [ ] Recherche dans la transcription
- [ ] Édition collaborative
- [ ] Sauvegarde automatique

### Améliorations possibles

- [ ] Animations plus fluides
- [ ] Raccourcis clavier personnalisables
- [ ] Templates d'export personnalisés
- [ ] Support multi-langues dans l'UI
- [ ] Mode plein écran
- [ ] Mini-player détachable

## Support et documentation

### Ressources Flet

- Documentation officielle: https://flet.dev
- Exemples: https://github.com/flet-dev/examples
- Galerie de composants: https://flet.dev/docs/controls

### Structure du projet

Consultez ces fichiers pour comprendre l'architecture:
- `src/gui_flet/theme.py`: Constantes de design et helpers
- `src/gui_flet/main_window.py`: Logique principale
- `src/gui_flet/components/`: Tous les composants réutilisables

## Contribution

Pour contribuer à l'interface Flet:

1. Créer une branche depuis `feature/flet-ui`:
   ```bash
   git checkout feature/flet-ui
   git checkout -b feature/my-new-feature
   ```

2. Faire vos modifications

3. Commiter avec un message clair:
   ```bash
   git commit -m "feat: add new feature"
   ```

4. Pousser et créer une PR:
   ```bash
   git push origin feature/my-new-feature
   ```

## Questions fréquentes

### Puis-je garder les deux interfaces?

Oui! C'est exactement l'intérêt des branches. Vous pouvez basculer entre les deux à tout moment.

### Laquelle choisir?

- **PyQt5 (main)**: Si vous préférez une interface classique et éprouvée
- **Flet (feature/flet-ui)**: Si vous voulez une interface moderne et légère

### Les tests fonctionnent toujours?

Oui! Tous les tests unitaires (134) continuent de fonctionner car seule la GUI a changé. Les modules métier sont intacts.

### Comment supprimer une branche?

```bash
# Supprimer une branche locale
git branch -d feature/branch-name

# Supprimer une branche distante
git push origin --delete feature/branch-name
```

---

**Note**: Cette interface est en développement actif. N'hésitez pas à suggérer des améliorations!
