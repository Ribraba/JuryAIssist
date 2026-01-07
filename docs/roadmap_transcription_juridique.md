# Roadmap - Logiciel de Transcription Audio pour Assistante Juridique

## Vue d'ensemble du projet

### Objectif
Développer une interface graphique en Python permettant à une assistante juridique de transcrire efficacement des enregistrements audio d'avocats avec synchronisation texte-audio et contrôle par pédale.

### Technologies principales
- **Langage** : Python 3.9+
- **GUI** : tkinter ou PyQt5/PyQt6
- **Audio** : python-vlc ou pygame
- **Pédale** : Bibliothèque HID (hidapi) pour Olympus
- **Tests** : pytest, unittest

---

## Phase 0 : Analyse et Préparation (2-3 jours)

### 0.1 Étude de faisabilité technique
**Objectif** : Valider les choix technologiques

#### Tâches
- [ ] **0.1.1** Rechercher et comparer les bibliothèques audio Python
  - python-vlc
  - pygame.mixer
  - pyaudio + pydub
  - Critères : contrôle précis de la timeline, performance, facilité d'intégration
  
- [ ] **0.1.2** Identifier le modèle exact de la pédale Olympus
  - RS-28, RS-31H, ou autre modèle
  - Rechercher la documentation technique
  - Vérifier la compatibilité HID
  
- [ ] **0.1.3** Choisir le framework GUI
  - tkinter : natif, simple, mais limité visuellement
  - PyQt5/6 : puissant, professionnel, courbe d'apprentissage
  - Recommandation : PyQt5 pour qualité professionnelle

- [ ] **0.1.4** Définir le format de synchronisation temps-texte
  - Option A : Format SRT (SubRip Subtitle)
  - Option B : JSON avec timestamps
  - Option C : SQLite pour grande échelle
  - Recommandation : SRT pour début, migration vers JSON/SQLite si nécessaire

**Livrables** :
- Document de décision technique (1 page)
- Liste des dépendances Python

---

## Phase 1 : Infrastructure de Base (1 semaine)

### 1.1 Configuration de l'environnement de développement

#### Tâches
- [ ] **1.1.1** Initialiser le projet
  ```
  projet-transcription/
  ├── src/
  │   ├── __init__.py
  │   ├── gui/
  │   ├── audio/
  │   ├── transcription/
  │   ├── devices/
  │   └── utils/
  ├── tests/
  │   ├── unit/
  │   └── integration/
  ├── resources/
  ├── docs/
  ├── requirements.txt
  └── README.md
  ```

- [ ] **1.1.2** Créer requirements.txt
  ```
  PyQt5>=5.15.0
  python-vlc>=3.0.0
  hidapi>=0.12.0
  pytest>=7.0.0
  pytest-qt>=4.0.0
  pytest-cov>=3.0.0
  ```

- [ ] **1.1.3** Configurer pytest et structure de tests
  - Créer pytest.ini
  - Définir conventions de nommage des tests
  - Configurer coverage minimum (80%)

**Tests** :
- Test d'importation de tous les modules
- Vérification de l'environnement virtuel

**Livrables** :
- Environnement de développement fonctionnel
- Structure de projet complète

---

### 1.2 Module de Lecture Audio (Core)

#### Architecture
```
src/audio/
├── __init__.py
├── player.py          # Classe AudioPlayer principale
├── controller.py      # Contrôle play/pause/seek
└── timeline.py        # Gestion de la timeline
```

#### Tâches

##### 1.2.1 Classe AudioPlayer de base
**Fichier** : `src/audio/player.py`

**Fonctionnalités** :
- Charger un fichier audio (MP3, WAV, M4A)
- Obtenir la durée totale
- Obtenir la position actuelle
- Gérer les états (stopped, playing, paused)

**Interface** :
```python
class AudioPlayer:
    def load(self, filepath: str) -> bool
    def get_duration(self) -> float  # en secondes
    def get_position(self) -> float  # en secondes
    def get_state(self) -> PlayerState  # Enum
```

**Tests unitaires** :
- `test_load_valid_audio()` : Charge un fichier valide
- `test_load_invalid_file()` : Gère erreur fichier inexistant
- `test_get_duration()` : Durée correcte d'un fichier connu
- `test_initial_state()` : État initial = STOPPED

---

##### 1.2.2 Contrôleur de lecture
**Fichier** : `src/audio/controller.py`

**Fonctionnalités** :
- Play/Pause
- Stop
- Seek (aller à une position précise)
- Skip forward/backward (5 secondes par défaut)
- Vitesse de lecture (0.5x à 2.0x)

**Interface** :
```python
class AudioController:
    def __init__(self, player: AudioPlayer)
    def play(self) -> None
    def pause(self) -> None
    def stop(self) -> None
    def seek(self, position: float) -> None
    def skip_forward(self, seconds: float = 5.0) -> None
    def skip_backward(self, seconds: float = 5.0) -> None
    def set_speed(self, speed: float) -> None  # 0.5 à 2.0
```

**Tests unitaires** :
- `test_play_pause_cycle()` : Play puis pause fonctionne
- `test_seek_to_position()` : Seek à 30s positionne correctement
- `test_skip_forward()` : Avance de 5s
- `test_skip_backward()` : Recule de 5s sans descendre sous 0
- `test_speed_change()` : Vitesse 1.5x fonctionne

---

##### 1.2.3 Gestion de la Timeline
**Fichier** : `src/audio/timeline.py`

**Fonctionnalités** :
- Convertir secondes ↔ format HH:MM:SS
- Calculer pourcentage de lecture
- Générer des marqueurs de temps

**Interface** :
```python
class Timeline:
    @staticmethod
    def seconds_to_timestamp(seconds: float) -> str
    @staticmethod
    def timestamp_to_seconds(timestamp: str) -> float
    @staticmethod
    def get_percentage(position: float, duration: float) -> float
```

**Tests unitaires** :
- `test_seconds_to_timestamp()` : 125.5s → "00:02:05.500"
- `test_timestamp_to_seconds()` : "00:02:05" → 125.0
- `test_get_percentage()` : 50s/100s → 50.0%

---

## Phase 2 : Module de Transcription (1 semaine)

### 2.1 Gestion des Transcriptions

#### Architecture
```
src/transcription/
├── __init__.py
├── models.py          # Classes de données
├── synchronizer.py    # Sync temps-texte
└── export.py          # Export TXT/SRT
```

#### Tâches

##### 2.1.1 Modèles de données
**Fichier** : `src/transcription/models.py`

**Classes** :
```python
@dataclass
class TranscriptSegment:
    start_time: float      # Début en secondes
    end_time: float        # Fin en secondes
    text: str              # Texte du segment
    speaker: Optional[str] # Intervenant (optionnel)

class Transcript:
    def __init__(self)
    def add_segment(self, segment: TranscriptSegment) -> None
    def get_segment_at_time(self, time: float) -> Optional[TranscriptSegment]
    def get_all_segments(self) -> List[TranscriptSegment]
    def update_segment(self, index: int, new_text: str) -> None
    def delete_segment(self, index: int) -> None
```

**Tests unitaires** :
- `test_add_segment()` : Ajoute un segment
- `test_get_segment_at_time()` : Trouve le bon segment à 45s
- `test_update_segment()` : Modifie le texte d'un segment
- `test_delete_segment()` : Supprime un segment

---

##### 2.1.2 Synchroniseur temps-texte
**Fichier** : `src/transcription/synchronizer.py`

**Fonctionnalités** :
- Charger/sauvegarder format SRT
- Trouver le timestamp d'un mot dans le texte
- Mise en cache pour performance

**Interface** :
```python
class Synchronizer:
    def __init__(self, transcript: Transcript)
    def load_from_srt(self, filepath: str) -> None
    def save_to_srt(self, filepath: str) -> None
    def find_word_timestamp(self, word: str, occurrence: int = 1) -> Optional[float]
    def get_text_at_time(self, time: float) -> str
```

**Format SRT exemple** :
```
1
00:00:00,000 --> 00:00:05,000
Bonjour, je suis l'avocat Dupont.

2
00:00:05,000 --> 00:00:10,000
Concernant le dossier numéro 12345...
```

**Tests unitaires** :
- `test_load_srt()` : Charge un fichier SRT valide
- `test_save_srt()` : Sauvegarde et recharge identique
- `test_find_word_timestamp()` : Trouve "avocat" à 2.5s
- `test_get_text_at_time()` : Texte correct à 7s

---

##### 2.1.3 Module d'export
**Fichier** : `src/transcription/export.py`

**Fonctionnalités** :
- Export en TXT simple (sans timestamps)
- Export en TXT avec timestamps
- Export en SRT
- Export en DOCX (optionnel, phase ultérieure)

**Interface** :
```python
class Exporter:
    def __init__(self, transcript: Transcript)
    def to_txt(self, filepath: str, include_timestamps: bool = False) -> None
    def to_srt(self, filepath: str) -> None
    def to_docx(self, filepath: str) -> None  # Optionnel
```

**Tests unitaires** :
- `test_export_txt_simple()` : TXT sans timestamps
- `test_export_txt_with_timestamps()` : TXT avec [00:02:30]
- `test_export_srt()` : SRT valide

---

## Phase 3 : Interface Graphique (2 semaines)

### 3.1 Architecture GUI (PyQt5)

#### Structure
```
src/gui/
├── __init__.py
├── main_window.py     # Fenêtre principale
├── widgets/
│   ├── audio_controls.py   # Boutons play/pause/etc
│   ├── timeline_widget.py  # Timeline graphique
│   ├── editor_panel.py     # Panneau édition
│   └── transcript_panel.py # Panneau transcription brute
└── dialogs/
    ├── export_dialog.py
    └── settings_dialog.py
```

#### Tâches

##### 3.1.1 Fenêtre principale
**Fichier** : `src/gui/main_window.py`

**Layout** :
```
+------------------------------------------+
|  Menu: Fichier | Edition | Aide         |
+------------------------------------------+
|  [Timeline avec curseur de lecture]      |
|  [Play] [Pause] [<<] [>>] [Vitesse]     |
+------------------------------------------+
|  Éditeur        |  Transcription Brute   |
|  (modifiable)   |  (lecture seule)       |
|                 |                         |
|                 |                         |
+------------------------------------------+
|  Status: Position 00:02:35 / 01:23:45    |
+------------------------------------------+
```

**Fonctionnalités** :
- Splitter horizontal entre les deux panneaux
- Menu avec Fichier (Ouvrir, Exporter, Quitter)
- Barre de status avec position actuelle
- Raccourcis clavier (Space=Play/Pause, etc.)

**Tests** :
- Test d'intégration : Interface se lance sans crash
- Test : Menu "Fichier" contient les bonnes options

---

##### 3.1.2 Widget Timeline
**Fichier** : `src/gui/widgets/timeline_widget.py`

**Fonctionnalités** :
- Barre de progression visuelle
- Curseur de position actuelle
- Clic pour se déplacer dans l'audio
- Marqueurs pour segments de transcription
- Affichage du temps actuel et total

**Interface Qt** :
```python
class TimelineWidget(QWidget):
    position_changed = pyqtSignal(float)  # Émet la nouvelle position
    
    def set_duration(self, duration: float) -> None
    def set_position(self, position: float) -> None
    def add_marker(self, position: float, label: str) -> None
```

**Tests** :
- `test_timeline_render()` : S'affiche correctement
- `test_click_to_seek()` : Clic émet signal avec bonne position
- `test_markers_displayed()` : Marqueurs visibles

---

##### 3.1.3 Panneau d'édition
**Fichier** : `src/gui/widgets/editor_panel.py`

**Fonctionnalités** :
- QTextEdit modifiable
- Sauvegarde auto toutes les 30 secondes
- Coloration syntaxique des timestamps (optionnel)
- Clic sur un mot → signal avec le mot cliqué

**Interface** :
```python
class EditorPanel(QWidget):
    word_clicked = pyqtSignal(str, int)  # Mot et position dans texte
    text_changed = pyqtSignal(str)
    
    def set_text(self, text: str) -> None
    def get_text(self) -> str
    def highlight_word(self, word: str) -> None
```

**Tests** :
- `test_text_edit()` : Texte modifiable
- `test_word_click_detection()` : Détecte mot cliqué
- `test_highlight()` : Surlignage fonctionne

---

##### 3.1.4 Panneau transcription brute
**Fichier** : `src/gui/widgets/transcript_panel.py`

**Fonctionnalités** :
- QTextEdit en lecture seule
- Scroll automatique vers segment actuel
- Surlignage du segment en cours de lecture
- Clic sur segment → retour à ce timestamp

**Interface** :
```python
class TranscriptPanel(QWidget):
    segment_clicked = pyqtSignal(float)  # Timestamp du segment
    
    def set_transcript(self, transcript: Transcript) -> None
    def highlight_segment_at_time(self, time: float) -> None
```

**Tests** :
- `test_display_transcript()` : Affiche correctement
- `test_segment_highlight()` : Surligne le bon segment
- `test_segment_click()` : Clic émet bon timestamp

---

##### 3.1.5 Contrôles audio
**Fichier** : `src/gui/widgets/audio_controls.py`

**Fonctionnalités** :
- Boutons : Play, Pause, Stop
- Boutons : Reculer 5s, Avancer 5s
- Slider de vitesse (0.5x à 2.0x)
- Affichage temps actuel / total

**Interface** :
```python
class AudioControlsWidget(QWidget):
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    skip_forward_clicked = pyqtSignal()
    skip_backward_clicked = pyqtSignal()
    speed_changed = pyqtSignal(float)
```

**Tests** :
- `test_buttons_emit_signals()` : Boutons émettent signaux
- `test_speed_slider()` : Slider émet valeur correcte

---

## Phase 4 : Support de la Pédale Olympus (1 semaine)

### 4.1 Reverse Engineering de la Pédale

#### Tâches

##### 4.1.1 Identification du périphérique
**Fichier** : `src/devices/pedal_detector.py`

**Objectifs** :
- Détecter la pédale USB Olympus connectée
- Identifier le Vendor ID et Product ID
- Lister les endpoints HID

**Outils nécessaires** :
- Linux : `lsusb`, `evtest`
- Windows : Device Manager, HID API
- Python : `hidapi`, `pyusb`

**Code de test** :
```python
import hid

def list_hid_devices():
    for device in hid.enumerate():
        print(f"Vendor ID: {device['vendor_id']:04x}")
        print(f"Product ID: {device['product_id']:04x}")
        print(f"Manufacturer: {device['manufacturer_string']}")
        print(f"Product: {device['product_string']}")
```

**Tests** :
- `test_detect_pedal()` : Détecte la pédale si connectée
- `test_no_pedal()` : Gère absence de pédale gracieusement

---

##### 4.1.2 Décodage des événements
**Fichier** : `src/devices/pedal_events.py`

**Objectifs** :
- Capturer les événements bruts de la pédale
- Identifier quels bytes correspondent à quelle pédale
- Mapper les actions (play, pause, forward, backward)

**Process** :
1. Capturer événements bruts pendant appui sur chaque pédale
2. Analyser les patterns de bytes
3. Créer mapping événement → action

**Exemple de mapping** :
```python
@dataclass
class PedalEvent:
    pedal_id: int  # 1, 2, ou 3
    pressed: bool  # True si appuyé, False si relâché

PEDAL_ACTIONS = {
    1: "play_pause",
    2: "skip_backward",
    3: "skip_forward"
}
```

**Tests** :
- `test_parse_event()` : Parse correctement un événement brut
- `test_pedal_mapping()` : Mapping correct pour chaque pédale

---

##### 4.1.3 Lecteur d'événements pédale
**Fichier** : `src/devices/pedal_reader.py`

**Fonctionnalités** :
- Thread séparé pour lecture continue
- Queue d'événements thread-safe
- Gestion reconnexion si déconnexion

**Interface** :
```python
class PedalReader(QThread):
    pedal_event = pyqtSignal(PedalEvent)
    
    def __init__(self, vendor_id: int, product_id: int)
    def run(self) -> None
    def stop(self) -> None
```

**Tests** :
- `test_pedal_reader_thread()` : Thread démarre et s'arrête
- `test_event_emission()` : Événements émis correctement
- Mock de la pédale pour tests automatisés

---

## Phase 5 : Intégration et Fonctionnalités Avancées (1 semaine)

### 5.1 Intégration complète

#### Tâches

##### 5.1.1 Chef d'orchestre (Coordinator)
**Fichier** : `src/coordinator.py`

**Rôle** : Connecter tous les modules ensemble

**Fonctionnalités** :
- Initialiser AudioController, Synchronizer, GUI
- Connecter signaux Qt entre composants
- Gérer le workflow complet :
  1. Charger audio
  2. Charger/créer transcription
  3. Synchroniser lecture et affichage
  4. Gérer pédale
  5. Exporter

**Connexions clés** :
```python
class ApplicationCoordinator:
    def setup_connections(self):
        # Audio → GUI
        self.audio.position_changed.connect(self.gui.timeline.set_position)
        
        # GUI → Audio
        self.gui.controls.play_clicked.connect(self.audio.play)
        self.gui.timeline.position_changed.connect(self.audio.seek)
        
        # Pédale → Audio
        self.pedal.pedal_event.connect(self.handle_pedal_action)
        
        # Transcription → GUI
        self.sync.segment_changed.connect(self.gui.transcript.highlight_segment)
        
        # GUI → Transcription (clic sur mot)
        self.gui.editor.word_clicked.connect(self.seek_to_word)
```

**Tests d'intégration** :
- `test_load_audio_updates_gui()` : Charger audio met à jour timeline
- `test_pedal_controls_audio()` : Pédale contrôle lecture
- `test_word_click_seeks()` : Clic mot va au timestamp
- `test_export_workflow()` : Workflow complet d'export

---

##### 5.1.2 Synchronisation mot ↔ timestamp
**Fichier** : `src/transcription/word_sync.py`

**Algorithme** :
1. Découper chaque segment en mots
2. Interpoler linéairement le timestamp de chaque mot
3. Créer index inversé : mot → liste de timestamps

**Exemple** :
```
Segment: 00:00:00 → 00:00:10
Texte: "Bonjour je suis avocat"
4 mots en 10 secondes

Timestamps estimés:
- "Bonjour" → 0.0s
- "je" → 2.5s
- "suis" → 5.0s
- "avocat" → 7.5s
```

**Interface** :
```python
class WordSynchronizer:
    def __init__(self, transcript: Transcript)
    def build_word_index(self) -> None
    def find_timestamp(self, word: str, occurrence: int = 1) -> Optional[float]
    def find_word_at_position(self, char_position: int) -> Tuple[str, float]
```

**Tests** :
- `test_word_interpolation()` : Timestamps interpolés correctement
- `test_find_word()` : Trouve le bon timestamp
- `test_multiple_occurrences()` : Gère plusieurs occurrences du même mot

---

##### 5.1.3 Surlignage et navigation
**Fichier** : `src/gui/highlighter.py`

**Fonctionnalités** :
- Surligner un mot dans l'éditeur
- Surligner le segment actuel dans transcription brute
- Scroll automatique vers le texte en cours

**Interface Qt** :
```python
class TextHighlighter:
    def __init__(self, text_edit: QTextEdit)
    def highlight_word(self, word: str, occurrence: int = 1) -> None
    def highlight_range(self, start_pos: int, end_pos: int) -> None
    def clear_highlight(self) -> None
    def scroll_to_position(self, position: int) -> None
```

**Tests** :
- `test_highlight_word()` : Mot surligné visuellement
- `test_clear_highlight()` : Surlignage effacé
- `test_scroll_to()` : Scroll vers la bonne position

---

### 5.2 Sauvegarde et Persistance

#### Tâches

##### 5.2.1 Auto-sauvegarde
**Fichier** : `src/utils/autosave.py`

**Fonctionnalités** :
- Sauvegarde automatique toutes les X secondes (configurable)
- Fichier de sauvegarde temporaire
- Récupération en cas de crash

**Interface** :
```python
class AutoSaver(QTimer):
    def __init__(self, save_callback: Callable, interval: int = 30)
    def start_autosave(self) -> None
    def stop_autosave(self) -> None
    def force_save(self) -> None
```

**Tests** :
- `test_autosave_triggers()` : Sauvegarde après délai
- `test_crash_recovery()` : Récupère fichier temporaire

---

##### 5.2.2 Gestion de projet
**Fichier** : `src/project/project_manager.py`

**Format de projet** (JSON) :
```json
{
  "audio_file": "/path/to/audio.mp3",
  "transcript_file": "/path/to/transcript.srt",
  "edited_text_file": "/path/to/edited.txt",
  "last_position": 125.5,
  "speed": 1.0,
  "metadata": {
    "avocat": "Me Dupont",
    "dossier": "12345",
    "date": "2025-01-03"
  }
}
```

**Interface** :
```python
class ProjectManager:
    def create_project(self, audio_path: str) -> Project
    def load_project(self, project_path: str) -> Project
    def save_project(self, project: Project, path: str) -> None
    def get_recent_projects(self) -> List[str]
```

**Tests** :
- `test_create_project()` : Crée structure complète
- `test_save_load_project()` : Sauvegarde et recharge identique

---

## Phase 6 : Tests et Qualité (1 semaine)

### 6.1 Suite de tests complète

#### Catégories de tests

##### 6.1.1 Tests unitaires
**Localisation** : `tests/unit/`

**Modules à tester** :
- `test_audio_player.py` : Toutes fonctions AudioPlayer
- `test_audio_controller.py` : Contrôles audio
- `test_timeline.py` : Conversions temps
- `test_transcript_models.py` : Classes de données
- `test_synchronizer.py` : Sync temps-texte
- `test_exporter.py` : Exports
- `test_word_sync.py` : Synchronisation mots

**Couverture cible** : 80% minimum

**Commande** :
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

---

##### 6.1.2 Tests d'intégration
**Localisation** : `tests/integration/`

**Scénarios** :
- `test_audio_gui_integration.py` : Audio contrôlé par GUI
- `test_transcription_sync.py` : Sync transcription-audio
- `test_pedal_integration.py` : Pédale contrôle l'application
- `test_export_workflow.py` : Workflow complet d'export

---

##### 6.1.3 Tests de l'interface (GUI)
**Outil** : pytest-qt

**Scénarios** :
- `test_main_window.py` : Fenêtre se lance et est réactive
- `test_timeline_interaction.py` : Interactions timeline
- `test_panel_synchronization.py` : Panneaux synchronisés
- `test_keyboard_shortcuts.py` : Raccourcis fonctionnent

---

### 6.2 Assurance qualité

#### Outils

##### 6.2.1 Linting et formatage
**Outils** :
- `black` : Formatage automatique
- `pylint` : Analyse statique
- `mypy` : Vérification types

**Configuration** : `pyproject.toml`
```toml
[tool.black]
line-length = 100

[tool.pylint]
max-line-length = 100
disable = ["C0111"]  # Missing docstring

[tool.mypy]
python_version = "3.9"
warn_return_any = true
```

---

##### 6.2.2 CI/CD (optionnel)
**GitHub Actions** : `.github/workflows/tests.yml`

**Pipeline** :
1. Installer dépendances
2. Lancer linters
3. Lancer tests unitaires
4. Lancer tests d'intégration
5. Générer rapport de couverture
6. Build exécutable (PyInstaller)

---

## Phase 7 : Documentation et Déploiement (3 jours)

### 7.1 Documentation

#### Types de documentation

##### 7.1.1 Documentation utilisateur
**Fichier** : `docs/USER_GUIDE.md`

**Contenu** :
- Installation
- Premier lancement
- Charger un audio
- Charger/créer une transcription
- Utiliser la pédale
- Éditer le texte
- Naviguer par clic sur mots
- Exporter le résultat
- Raccourcis clavier
- Dépannage

---

##### 7.1.2 Documentation technique
**Fichier** : `docs/TECHNICAL.md`

**Contenu** :
- Architecture globale
- Diagrammes de classes
- Flux de données
- Format des fichiers (SRT, projet JSON)
- API des modules principaux
- Ajout de nouvelles fonctionnalités

---

##### 7.1.3 Documentation développeur
**Fichier** : `docs/DEVELOPER.md`

**Contenu** :
- Setup environnement
- Conventions de code
- Lancer les tests
- Créer un build
- Contribuer au projet

---

### 7.2 Packaging et distribution

#### Tâches

##### 7.2.1 Création d'exécutable
**Outil** : PyInstaller

**Script** : `build.py`
```python
# Création d'un exécutable standalone
# Windows: .exe
# Linux: binaire
# macOS: .app
```

**Configuration** : `transcription.spec`

**Tests** :
- Exécutable se lance sur machine vierge
- Toutes fonctionnalités opérationnelles
- Taille raisonnable (<100 MB)

---

##### 7.2.2 Installateur
**Windows** : Inno Setup
**Linux** : .deb ou AppImage
**macOS** : .dmg

---

## Phase 8 : Optimisations et Fonctionnalités Bonus (Optionnel)

### 8.1 Performance

- Chargement paresseux de gros fichiers audio
- Cache des positions de mots
- Optimisation de l'affichage timeline (pas de redessins inutiles)

### 8.2 Fonctionnalités avancées

- Import/export DOCX avec formatage
- Détection automatique de locuteurs
- Raccourcis pédale configurables
- Thèmes d'interface (clair/sombre)
- Gestion de multiples fichiers audio (playlist)
- Transcription automatique (via API Whisper)
- Correction orthographique intégrée
- Historique d'édition (undo/redo amélioré)

---

## Estimation Temporelle Globale

| Phase | Durée | Dépendances |
|-------|-------|-------------|
| Phase 0 : Analyse | 2-3 jours | Aucune |
| Phase 1 : Infrastructure | 1 semaine | Phase 0 |
| Phase 2 : Transcription | 1 semaine | Phase 1 |
| Phase 3 : GUI | 2 semaines | Phase 1, 2 |
| Phase 4 : Pédale | 1 semaine | Phase 1 |
| Phase 5 : Intégration | 1 semaine | Phases 1-4 |
| Phase 6 : Tests/QA | 1 semaine | Phase 5 |
| Phase 7 : Documentation | 3 jours | Phase 6 |
| **TOTAL** | **7-8 semaines** | |

---

## Risques et Mitigation

### Risque 1 : Pédale Olympus incompatible
**Probabilité** : Moyenne
**Impact** : Élevé
**Mitigation** :
- Tester détection pédale dès Phase 0
- Plan B : Utiliser clavier comme alternative
- Contacter Olympus pour documentation

### Risque 2 : Performance avec gros fichiers audio
**Probabilité** : Faible
**Impact** : Moyen
**Mitigation** :
- Tester avec fichiers de 2h+ dès Phase 1
- Utiliser streaming audio si nécessaire
- Optimiser mémoire

### Risque 3 : Synchronisation imprécise mot-timestamp
**Probabilité** : Moyenne
**Impact** : Moyen
**Mitigation** :
- Utiliser vraie transcription avec timestamps si disponible
- Permettre correction manuelle des timestamps
- Utiliser API de reconnaissance vocale (Whisper)

---

## Checklist de Livraison Finale

### Fonctionnalités
- [ ] Lecture audio (MP3, WAV, M4A)
- [ ] Contrôles : Play, Pause, Avancer, Reculer
- [ ] Timeline interactive avec curseur
- [ ] Deux panneaux : Éditeur + Transcription brute
- [ ] Synchronisation mot cliqué → timestamp
- [ ] Support pédale Olympus
- [ ] Export TXT
- [ ] Auto-sauvegarde
- [ ] Projet persistant

### Qualité
- [ ] Couverture tests > 80%
- [ ] Tous tests passent
- [ ] Pas de warning pylint critique
- [ ] Types vérifiés avec mypy
- [ ] Documentation complète
- [ ] Exécutable fonctionnel

### User Experience
- [ ] Interface intuitive
- [ ] Temps de réponse < 100ms pour interactions
- [ ] Aucun crash sur utilisation normale
- [ ] Messages d'erreur clairs
- [ ] Guide utilisateur clair

---

## Priorités pour MVP (Version Minimale)

Si délai réduit, se concentrer sur :

1. **Phase 1.2** : Lecture audio basique
2. **Phase 2** : Gestion transcription SRT
3. **Phase 3.1-3.4** : Interface GUI minimale
4. **Phase 5.1.2** : Synchronisation mot-timestamp
5. **Phase 2.1.3** : Export TXT

**Reporter pour v2.0** :
- Support pédale (utiliser clavier temporairement)
- Tests d'intégration avancés
- Fonctionnalités bonus
- Packaging avancé

---

## Notes Complémentaires

### Conventions de Code

**Nommage** :
- Classes : `PascalCase`
- Fonctions/méthodes : `snake_case`
- Constantes : `UPPER_SNAKE_CASE`
- Fichiers : `snake_case.py`

**Docstrings** :
```python
def function_example(param1: str, param2: int) -> bool:
    """Brève description de la fonction.
    
    Description plus détaillée si nécessaire.
    
    Args:
        param1: Description du paramètre 1
        param2: Description du paramètre 2
        
    Returns:
        Description de la valeur de retour
        
    Raises:
        ValueError: Quand param2 < 0
    """
    pass
```

### Git Workflow

**Branches** :
- `main` : Code stable en production
- `develop` : Code en développement
- `feature/nom-feature` : Nouvelles fonctionnalités
- `bugfix/nom-bug` : Corrections de bugs

**Commits** :
```
type(scope): description courte

Description détaillée si nécessaire

Types: feat, fix, docs, test, refactor, style
```

---

## Ressources et Références

### Documentation
- PyQt5 : https://doc.qt.io/qtforpython/
- python-vlc : https://wiki.videolan.org/Python_bindings
- hidapi : https://github.com/libusb/hidapi
- Format SRT : https://en.wikipedia.org/wiki/SubRip

### Outils Recommandés
- IDE : PyCharm ou VSCode avec Python extension
- Gestion dépendances : poetry ou pip + venv
- Débogage GUI : Qt Creator
- Profiling : cProfile, line_profiler

### Communauté
- Stack Overflow pour questions techniques
- GitHub Discussions pour fonctionnalités
- Reddit r/Python pour conseils généraux

---

## Conclusion

Cette roadmap fournit un plan structuré et détaillé pour développer le logiciel de transcription juridique. Chaque phase est décomposée en tâches spécifiques avec des tests unitaires associés, garantissant une qualité de code élevée.

**Points clés** :
✅ Architecture modulaire et testable
✅ Développement incrémental par phases
✅ Couverture de tests > 80%
✅ Documentation complète
✅ Qualité professionnelle

**Prochaines étapes** :
1. Valider cette roadmap avec l'équipe
2. Commencer Phase 0 : Analyse technique
3. Setup environnement de développement
4. Premier commit : Structure du projet

Bonne chance pour le développement ! 🚀
