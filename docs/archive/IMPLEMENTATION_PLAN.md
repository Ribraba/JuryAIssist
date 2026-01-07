# Plan d'implémentation - Interface Figma → PyQt5

## Vue d'ensemble

Remplacement de l'interface actuelle de JuryAIssist par le design Figma.

## Analyse du design Figma

### Structure du layout
```
┌─────────────────────────────────────────────────────┐
│ [Sidebar 256px]  │  [Main Content Area]            │
│                  │                                   │
│ JuryAIssist      │  Transcription brute    Édition  │
│                  │  ───────────────────────────────  │
│ 🔍 Rechercher    │                                   │
│                  │  [Transcription]  [Bloc édition]  │
│ Transcriptions   │  (lecture seule)  (éditable)     │
│ ● Dupont.m4a     │                                   │
│ ○ audience.mp3   │                                   │
│                  │  ───────────────────────────────  │
│ Library          │  [Timeline + Controls]            │
│ + Import         │  ▶ ⏸ ⏹ ◀ ▶  🔊 ───  1.0x         │
│ ⚙ Paramètres     │  00:15 / 02:45:30                 │
│                  │                                   │
│                  │  [Pédale: 🎮 RS-31 connectée]     │
└─────────────────────────────────────────────────────┘
```

### Design Tokens

**Couleurs :**
- Background principal: `#ffffff`
- Background timeline: `#eeeeee`
- Item hover/sélectionné: `#f7f7f7`
- Accent (bleu): `#477ed8`
- Texte principal: `#000000`
- Texte secondaire: `#444444`

**Typographie (Inter) :**
- Titre app: 20px, weight 600
- Section heading: 34px, weight 600
- Sous-titre: 16px, weight 400
- Menu items: 16px, weight 500-600
- Transcription: 20px, weight 500
- Éditeur: 24px, weight 500
- Status pédale: 11px, weight 400
- Temps: 15px, weight 400

**Spacing :**
- 4px, 8px, 16px, 24px (système de spacing cohérent)

## Changements majeurs par rapport à l'interface actuelle

### 1. Ajout d'une Sidebar (NOUVEAU)
- **Largeur fixe :** 256px
- **Sections :**
  - Logo/Titre "JuryAIssist"
  - Barre de recherche
  - Liste des transcriptions (avec radio buttons)
  - Section "Library" avec :
    - Bouton "Nouvel import"
    - Bouton "Paramètres"

### 2. Réorganisation du contenu principal
- **Layout horizontal avec 2 panneaux :**
  - Gauche : Transcription brute (lecture seule)
  - Droite : Bloc édition (éditable)
- **Titres au-dessus de chaque panneau :**
  - "Transcription brute" + "Lecture"
  - Nom du fichier + "Édition"

### 3. Contrôles audio redessinés
- **Layout plus compact et moderne**
- **Éléments :**
  - Bouton Play/Pause (grand, circulaire)
  - Boutons Skip backward/forward
  - Bouton Stop
  - Timeline (barre de progression grise #eeeeee)
  - Volume control avec slider
  - Indicateur de vitesse (1.0x)
  - Temps (00:15 / 02:45:30)

### 4. Indicateur de pédale repositionné
- **Nouvelle position :** En haut à droite
- **Style :** Badge compact avec icône 🎮
- **Texte :** "Pédale connectée (RS-31)"

### 5. Suppression de la barre de menu traditionnelle
- Remplacée par des boutons dans la sidebar
- Menu actions intégrées dans les boutons d'action

## Plan d'implémentation

### Phase 1 : Mise à jour des styles
- [x] Extraire les design tokens depuis Figma
- [ ] Créer un nouveau fichier de styles PyQt5 (QSS)
- [ ] Intégrer la police Inter
- [ ] Définir les couleurs, typographies, spacing

### Phase 2 : Créer les nouveaux widgets
- [ ] `SidebarWidget` - Navigation et liste des fichiers
- [ ] `TranscriptPanelWidget` - Version redessinée
- [ ] `EditorPanelWidget` - Version redessinée
- [ ] `AudioControlsWidget` - Redesign complet
- [ ] `TimelineWidget` - Mise à jour visuelle
- [ ] `PedalStatusBadge` - Nouveau widget pour status pédale

### Phase 3 : Refactoriser MainWindow
- [ ] Supprimer la menubar traditionnelle
- [ ] Implémenter le layout avec sidebar + main content
- [ ] Intégrer tous les nouveaux widgets
- [ ] Connecter les signaux

### Phase 4 : Tests et ajustements
- [ ] Tester toutes les fonctionnalités
- [ ] Vérifier la responsivité
- [ ] Ajuster les espacements et alignements
- [ ] Tester avec la pédale

## Mapping Figma → PyQt5

| Composant Figma | Widget PyQt5 | Fichier |
|-----------------|--------------|---------|
| Sidebar | QFrame + QVBoxLayout | `src/gui/widgets/sidebar.py` |
| Titre section | QLabel (styled) | Intégré dans les widgets |
| Menu item | QPushButton (flat) | Intégré dans sidebar |
| Radio button | QRadioButton (custom style) | Intégré dans sidebar |
| Transcription brute | QTextEdit (readonly) | `src/gui/widgets/transcript_panel.py` |
| Bloc édition | QTextEdit | `src/gui/widgets/editor_panel.py` |
| Timeline | QSlider + QWidget custom | `src/gui/widgets/timeline_widget.py` |
| Play button | QPushButton (rond, styled) | `src/gui/widgets/audio_controls.py` |
| Volume slider | QSlider (horizontal) | `src/gui/widgets/audio_controls.py` |
| Badge pédale | QLabel (styled) | `src/gui/widgets/pedal_badge.py` |

## Notes techniques

### Police Inter
- La police Inter doit être installée ou intégrée comme ressource Qt
- Alternative : Utiliser "Segoe UI" (Windows) ou "SF Pro" (macOS) comme fallback

### Icônes
- Extraire les icônes de Figma en SVG
- Convertir en QIcon ou utiliser des caractères Unicode

### Responsivité
- La sidebar reste fixe à 256px
- Le contenu principal utilise un QSplitter pour les deux panneaux
- Les contrôles audio s'adaptent à la largeur

## Étapes suivantes

1. ✅ Analyser le design Figma
2. ✅ Extraire les design tokens
3. → Créer le nouveau fichier de styles
4. → Implémenter les widgets un par un
5. → Intégrer dans MainWindow
6. → Tests finaux
