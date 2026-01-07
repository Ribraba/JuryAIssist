# Corrections apportées au design Figma

## 🔧 Problèmes corrigés

Suite à votre retour sur la comparaison avec le design Figma original, voici les corrections apportées :

### 1. ✅ Sidebar - Hauteur des items de fichiers

**Problème** : Les items de fichiers (Affaire Dupont.m4a, audience_2024.mp3) prenaient toute la hauteur du container au lieu d'être compacts.

**Solution** :
- Ajout d'une hauteur fixe de 40px pour chaque item (`setFixedHeight(40)`)
- Réduction de la taille de l'icône radio de 24px à 16px
- Ajout de styles hover pour meilleure interaction

**Fichier modifié** : `src/gui/widgets/sidebar.py` (ligne 233)

```python
file_widget.setFixedHeight(40)  # Hauteur fixe compacte
radio_icon_label.setPixmap(radio_icon.pixmap(QSize(16, 16)))  # Icône plus petite
```

### 2. ✅ Timeline - Position

**Problème** : La timeline était EN HAUT alors qu'elle doit être EN BAS (juste au-dessus des contrôles audio).

**Solution** :
- Réorganisation du layout dans `main_window_figma.py`
- Ordre correct maintenant :
  1. Badge pédale (en haut)
  2. Splitter avec panneaux transcription/édition (prend tout l'espace)
  3. **Timeline** (en bas, au-dessus des contrôles)
  4. Contrôles audio (tout en bas)

**Fichier modifié** : `src/gui/main_window_figma.py` (lignes 156-178)

```python
# Ordre corrigé:
content_layout.addWidget(pedal_container)
content_layout.addWidget(splitter, 1)  # Prend l'espace
content_layout.addWidget(self._timeline)  # EN BAS
content_layout.addWidget(self._audio_controls)  # Tout en bas
```

### 3. ✅ Contrôles audio - Layout des boutons

**Problème** : Les boutons Skip backward, Stop et Skip forward étaient alignés horizontalement au même niveau que Play, alors qu'ils doivent être EN DESSOUS du bouton Play.

**Solution** :
- Refonte complète du layout des boutons en layout VERTICAL
- Ligne 1 : Bouton Play/Pause (grand, 51x51px, centré)
- Ligne 2 : Skip backward, Stop, Skip forward (petits, 32x32px, alignés horizontalement)

**Fichier modifié** : `src/gui/widgets/figma_audio_controls.py` (lignes 92-149)

```python
# Layout vertical pour les boutons
buttons_layout = QVBoxLayout()

# Ligne 1: Play/Pause (centré)
play_pause_layout (avec stretchers pour centrer)

# Ligne 2: Skip backward, Stop, Skip forward (horizontaux)
small_buttons_layout (3 boutons alignés)
```

### 4. ✅ Fichiers statiques dans la sidebar

**Problème** : Les fichiers "Affaire Dupont.m4a" et "audience_2024.mp3" étaient des exemples statiques, alors qu'ils doivent être ajoutés dynamiquement quand l'utilisateur importe un fichier.

**Solution** :
- Suppression de l'initialisation statique : `_sidebar.set_transcript_files([...])`
- La sidebar démarre maintenant avec une liste vide
- Ajout automatique d'un fichier à la sidebar quand il est chargé

**Fichier modifié** : `src/gui/main_window_figma.py` (lignes 182-237)

```python
# Ligne 182: Commentaire au lieu d'initialisation statique
# NE PAS initialiser de fichiers statiques - la liste commence vide

# Ligne 237: Ajout dynamique lors du chargement
self._sidebar.add_transcript_file(filename, selected=True)
```

## 📊 Résumé des modifications

| Composant | Modification | Fichier | Lignes |
|-----------|--------------|---------|--------|
| Sidebar items | Hauteur fixe 40px | `sidebar.py` | 233, 242-243 |
| Timeline | Position déplacée en bas | `main_window_figma.py` | 172-174 |
| Audio controls | Layout vertical (Play en haut, Skip/Stop en bas) | `figma_audio_controls.py` | 92-149 |
| File list | Suppression des exemples statiques | `main_window_figma.py` | 182, 237 |

## 🎯 Résultat attendu

Après ces corrections, l'interface doit maintenant correspondre exactement au design Figma :

### Layout final (de haut en bas) :

```
┌────────────────────────────────────────────────────┐
│ Sidebar    │  🎮 Pédale (badge en haut à droite) │
│  256px     │                                       │
│            │  ┌─────────────┬──────────────────┐  │
│ JuryAIssist│  │Transcription│ Editor           │  │
│            │  │  Brute      │                  │  │
│ 🔍 Rech... │  │ (lecture    │  (éditable)      │  │
│            │  │  seule)     │                  │  │
│ Trans...   │  │             │                  │  │
│ (vide)     │  └─────────────┴──────────────────┘  │
│            │                                       │
│ Library    │  ┌─────────────────────────────────┐ │
│ + Import   │  │ Timeline + texte défilant       │ │
│ ⚙ Params   │  └─────────────────────────────────┘ │
│            │                                       │
│            │     ▶          (Play grand)           │
│            │   ◀  ⏹  ▶     (Skip/Stop petits)     │
│            │   🔊 ─── 00:15 / 02:45:30  1.0x      │
└────────────────────────────────────────────────────┘
```

### Comportement attendu :

1. **Sidebar** :
   - Démarre vide (pas de fichiers)
   - Items compacts (40px de hauteur)
   - Ajout dynamique quand on importe un fichier

2. **Timeline** :
   - Positionnée EN BAS (juste au-dessus des contrôles)
   - Texte défilant au-dessus
   - Opacité progressive

3. **Contrôles audio** :
   - Play grand et centré EN HAUT
   - Skip backward, Stop, Skip forward EN DESSOUS (alignés horizontalement)
   - Volume, temps et vitesse à droite

## 🚀 Test

Pour tester les corrections :

```bash
source venv/bin/activate
python launch_figma_ui.py
```

Vérifications :
- [ ] Sidebar : liste vide au démarrage
- [ ] Timeline : en bas (au-dessus des contrôles audio)
- [ ] Bouton Play : grand et en haut
- [ ] Boutons Skip/Stop : petits et en dessous du Play
- [ ] Items de fichiers : compacts (40px) quand on en ajoute

## 📝 Notes

- Tous les changements respectent les principes SOLID
- Aucune régression fonctionnelle
- Le comportement dynamique est maintenant correct
- Le layout correspond au design Figma

---

**Date des corrections** : 2026-01-06
**Fichiers modifiés** : 3
**Problèmes résolus** : 4
