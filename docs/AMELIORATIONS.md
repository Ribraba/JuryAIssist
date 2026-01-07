# 🚀 Pistes d'Améliorations - JuryAIssist

**Date**: 2026-01-05
**Version actuelle**: 2.1.0
**Statut**: Application complète et fonctionnelle

---

## 📊 Vue d'ensemble

L'application JuryAIssist est **pleinement fonctionnelle** avec toutes les phases principales terminées (Phases 0-5). Les améliorations ci-dessous sont des optimisations et des fonctionnalités avancées optionnelles.

---

## 🎯 Améliorations Prioritaires

### 1. Configuration de la Pédale via Interface Graphique

**Statut**: Non implémenté
**Priorité**: HAUTE
**Temps estimé**: 2-3 jours

**Description**:
Actuellement, le mapping des boutons de la pédale est codé en dur. Ajouter une interface graphique pour:
- Configurer les actions de chaque bouton
- Tester les boutons en temps réel
- Sauvegarder/charger des profils de configuration

**Fichiers à créer**:
- `src/gui/dialogs/pedal_config_dialog.py`
- `src/devices/config_manager.py`

**Fonctionnalités**:
- Dialogue de configuration avec 4 dropdowns (un par bouton)
- Preview des actions en temps réel
- Sauvegarde dans `~/.juryaissist/pedal_config.json`
- Profils prédéfinis (Professionnel, Rapide, Personnalisé)

**Tests**:
- `tests/unit/gui/test_pedal_config_dialog.py`
- `tests/unit/devices/test_config_manager.py`

---

### 2. Packaging et Distribution ⚠️ CRITIQUE

**Statut**: Non commencé
**Priorité**: CRITIQUE (bloquant pour distribution)
**Temps estimé**: 1 semaine

**Contexte Critique**:
L'installation actuelle nécessite des connaissances techniques (terminal, venv, pip) **incompatibles avec la cible utilisateur** (assistantes juridiques non-techniques).

**Risques Majeurs**:
- ❌ Pas de `chmod +x` ou `venv` pour une secrétaire
- ❌ Dépendances PyTorch (2+ Go) peuvent échouer sur machines faibles
- ❌ VLC externe requis = problème compatibilité 32/64 bits
- ❌ Pédale nécessite configuration manuelle `/etc/udev/rules.d/` (Linux)

**Tâches**:

#### 2.1 Exécutable macOS (Standalone)
- Utiliser **PyInstaller** ou **Briefcase (BeeWare)** pour créer un `.app`
- Créer un installateur `.dmg` professionnel
- **Inclure libvlc** directement dans le bundle
- Pré-télécharger modèles Whisper (tiny/base)
- Script de permissions HID automatique à l'installation
- Signer l'application (optionnel mais recommandé)

**Commandes améliorées**:
```bash
# macOS - avec libvlc intégré
pyinstaller --onefile --windowed \
  --add-data "src:src" \
  --add-binary "/opt/homebrew/lib/libvlc.dylib:." \
  --add-data "models/whisper-base:models" \
  --icon resources/icon.icns \
  --name JuryAIssist \
  --osx-bundle-identifier com.juryaissist.app \
  src/main.py

# Créer DMG
hdiutil create -volname "JuryAIssist" -srcfolder dist/JuryAIssist.app -ov -format UDZO JuryAIssist.dmg
```

#### 2.2 Exécutable Windows (Standalone)
- Créer `.exe` avec PyInstaller
- Installateur avec **NSIS** ou **Inno Setup**
- Intégrer `libvlc.dll` et dépendances VLC
- Pré-inclure modèles Whisper
- Installation automatique pilotes HID si nécessaire

```bash
# Windows
pyinstaller --onefile --windowed \
  --add-data "src;src" \
  --add-binary "C:\Program Files\VideoLAN\VLC\libvlc.dll;." \
  --add-data "models\whisper-base;models" \
  --icon resources/icon.ico \
  --name JuryAIssist \
  src/main.py
```

#### 2.3 Gestion Automatique VLC (Fallback)
**Nouveau fichier**: `src/audio/player_factory.py`

**Problème**: Si VLC manquant ou incompatible, l'app crash

**Solution**: Système de fallback
```python
def create_audio_player() -> IAudioPlayer:
    """Factory avec fallback automatique."""
    try:
        return VLCAudioPlayer()
    except Exception as e:
        logger.warning(f"VLC non disponible: {e}")
        logger.info("Basculement sur lecteur de secours")
        return FallbackAudioPlayer()  # pygame.mixer ou miniaudio
```

#### 2.4 Migration vers faster-whisper (URGENT)
**Problème**: PyTorch = 2+ Go, crash sur machines faibles

**Solution**: Utiliser `faster-whisper` (GGML)
- 5x plus rapide que Whisper
- RAM divisée par 4
- Pas de GPU requis
- Installation simplifiée (~500 Mo vs 2+ Go)

**Migration recommandée**:
```python
# Nouvelle implémentation: src/transcription/faster_whisper_transcriber.py
from faster_whisper import WhisperModel

class FasterWhisperTranscriber(ITranscriber):
    def __init__(self, model_size: str = "base"):
        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"  # Quantification INT8
        )
```

**Dépendances à ajouter**:
```
# requirements.txt
faster-whisper>=0.10.0  # Au lieu de openai-whisper
```

#### 2.5 Permissions HID Automatiques
**Problème**: Assistante ne peut pas éditer `/etc/udev/rules.d/` (Linux) ou permissions HID (macOS)

**Solutions**:

**macOS**: Script d'installation dans le DMG
```bash
#!/bin/bash
# postinstall.sh (inclus dans le DMG)
echo "Configuration des permissions pour pédale USB..."
sudo chmod 666 /dev/hidraw* 2>/dev/null || true
```

**Linux**: Installation automatique via pkexec
```python
# src/devices/setup_permissions.py
def setup_udev_rules():
    """Configure udev rules automatiquement (Linux)."""
    rules_content = """
# Olympus RS-31 Pedal
SUBSYSTEM=="usb", ATTRS{idVendor}=="07b4", ATTRS{idProduct}=="025f", MODE="0666"
"""
    rules_path = "/etc/udev/rules.d/99-olympus-pedal.rules"

    try:
        # Demande privilèges admin graphiquement
        subprocess.run([
            "pkexec", "sh", "-c",
            f"echo '{rules_content}' > {rules_path}"
        ])
        subprocess.run(["sudo", "udevadm", "control", "--reload-rules"])
        print("✅ Permissions pédale configurées")
        return True
    except Exception as e:
        print(f"⚠️ Permissions manuelles requises: {e}")
        return False
```

#### 2.6 Documentation utilisateur
- Guide d'installation complet (non-technique)
- **Vidéo de démonstration** (5-10 min)
- FAQ et troubleshooting
- Section "🔒 Confidentialité et RGPD" (voir amélioration #21)

---

### 3. Tests d'Intégration Automatisés

**Statut**: Tests manuels OK, automatisation manquante
**Priorité**: MOYENNE
**Temps estimé**: 2-3 jours

**Description**:
Ajouter des tests end-to-end automatisés pour valider les workflows complets.

**Tests à créer**:
- `tests/integration/test_full_workflow.py`
  - Charger audio
  - Transcrire
  - Éditer transcription
  - Clic mot → seek audio
  - Export TXT/DOCX

- `tests/integration/test_pedal_workflow.py`
  - Connecter pédale
  - Contrôler lecture
  - Déconnexion/reconnexion

- `tests/integration/test_performance.py`
  - Latence < 50ms pour actions pédale
  - Chargement fichier 2h < 5 secondes
  - Utilisation mémoire < 500 MB

**Outils**:
- pytest-qt pour GUI
- pytest-benchmark pour performance
- pytest-timeout pour robustesse

---

## 💡 Fonctionnalités Avancées

### 4. Support d'Autres Modèles de Pédales

**Statut**: Architecture extensible prête
**Priorité**: BASSE
**Temps estimé**: 1-2 jours

**Description**:
Supporter d'autres modèles de pédales Olympus (RS-28, RS-31H) ou autres marques.

**Architecture existante**:
- Interface `IEventParser` déjà en place
- `GenericHIDParser` déjà implémenté
- Ajout d'un parser = nouveau fichier, pas de modification du code existant

**Nouveau parser exemple**:
```python
class RS28EventParser(IEventParser):
    """Parser pour pédale RS-28 (3 boutons)."""

    BUTTON_MASKS = {
        1: (2, 0x01),
        2: (2, 0x02),
        3: (2, 0x04),
    }

    def parse(self, raw_data: bytes) -> List[ButtonEvent]:
        # Implémentation spécifique RS-28
        pass
```

---

### 5. Détection Automatique des Appuis Longs

**Statut**: Infrastructure prête (ButtonConfig.on_long_press existe)
**Priorité**: BASSE
**Temps estimé**: 1 jour

**Description**:
Différencier appuis courts et longs pour plus d'actions.

**Exemple d'usage**:
- Bouton 3 court: Avancer 5s
- Bouton 3 long: Avancer 30s
- Bouton 4 court: Stop
- Bouton 4 long: Retour à 0s

**Code existant**:
```python
# Déjà dans action_mapper.py
ButtonConfig(
    on_press=AudioAction.SKIP_FORWARD,
    on_long_press=AudioAction.SKIP_FORWARD_30S,  # À implémenter
    long_press_duration=1.0
)
```

**À faire**:
- Ajouter actions dans `PedalAction` enum
- Implémenter dans `AudioController`
- Tests unitaires

---

### 6. Thèmes d'Interface (Clair/Sombre)

**Statut**: Non implémenté
**Priorité**: BASSE
**Temps estimé**: 1-2 jours

**Description**:
Ajouter un système de thèmes pour l'interface.

**Fichiers à créer**:
- `src/gui/themes/light_theme.py`
- `src/gui/themes/dark_theme.py`
- `src/gui/themes/theme_manager.py`

**Fonctionnalités**:
- Switch rapide via menu Affichage
- Détection du thème système (macOS/Windows)
- Sauvegarde du choix dans préférences

**Exemple**:
```python
class ThemeManager:
    THEMES = {
        'light': LightTheme(),
        'dark': DarkTheme(),
        'auto': AutoTheme(),  # Suit le système
    }

    def apply_theme(self, app: QApplication, theme_name: str):
        theme = self.THEMES[theme_name]
        app.setStyleSheet(theme.get_stylesheet())
```

---

### 7. Raccourcis Clavier Configurables

**Statut**: Raccourcis hardcodés (Space, Ctrl+O, etc.)
**Priorité**: BASSE
**Temps estimé**: 1-2 jours

**Description**:
Permettre à l'utilisateur de personnaliser les raccourcis clavier.

**Fonctionnalités**:
- Dialogue de configuration des raccourcis
- Détection de conflits
- Profils prédéfinis (Standard, Vim-like, Emacs-like)
- Export/Import de profils

**Fichiers**:
- `src/gui/dialogs/shortcuts_dialog.py`
- `src/utils/shortcut_manager.py`
- `~/.juryaissist/shortcuts.json`

---

### 8. Historique d'Édition Amélioré (Undo/Redo)

**Statut**: Undo/Redo basique de Qt
**Priorité**: BASSE
**Temps estimé**: 1 jour

**Description**:
Améliorer le système d'undo/redo avec:
- Historique persistant entre sessions
- Timeline visuelle des modifications
- Annotations des changements

**Fichiers**:
- `src/transcription/edit_history.py`
- Sauvegarde dans fichier projet

---

### 9. Détection Automatique des Locuteurs

**Statut**: Non implémenté
**Priorité**: BASSE (fonctionnalité avancée)
**Temps estimé**: 3-5 jours

**Description**:
Utiliser un modèle de diarisation pour identifier les différents intervenants.

**Technologies**:
- pyannote.audio (diarisation)
- Whisper (déjà utilisé) peut aussi aider

**Workflow**:
1. Transcrire avec Whisper
2. Diariser avec pyannote
3. Fusionner les résultats
4. Permettre correction manuelle

**Exemple**:
```
[Avocat 1 - 00:00:00]
Bonjour, je représente le demandeur.

[Juge - 00:00:15]
Très bien, poursuivez.

[Avocat 2 - 00:00:20]
De notre côté, nous contestons...
```

---

### 10. Export Avancé (DOCX avec Mise en Forme)

**Statut**: Export basique TXT/DOCX implémenté
**Priorité**: BASSE
**Temps estimé**: 2 jours

**Description**:
Améliorer l'export DOCX avec:
- Formatage professionnel
- En-têtes/pieds de page personnalisables
- Table des matières automatique
- Numérotation des paragraphes
- Différentes polices/tailles selon le locuteur

**Bibliothèque**:
- python-docx (déjà utilisé)
- Créer templates personnalisables

**Templates**:
- Standard (simple)
- Juridique (avec numéros de lignes)
- Rapport (avec table des matières)

---

## 🔧 Optimisations Techniques

### 11. Optimisation des Performances

**Statut**: Performances OK, optimisations possibles
**Priorité**: BASSE
**Temps estimé**: 2-3 jours

**Optimisations possibles**:

#### 11.1 Chargement Paresseux (Lazy Loading)
- Ne charger Whisper que si transcription demandée
- Réduire temps de démarrage

#### 11.2 Cache des Positions de Mots
- Sauvegarder l'index mot→timestamp dans fichier
- Recalculer seulement si transcription modifiée

#### 11.3 Optimisation Timeline
- Redessiner seulement la zone visible
- Throttling des mises à jour (max 30 FPS)

#### 11.4 Threading Amélioré
- Pool de threads pour exports multiples
- Transcription en tâche de fond sans bloquer UI

**Mesures**:
- Profiling avec cProfile
- Memory profiling avec memory_profiler
- Benchmarks automatisés

---

### 12. Système de Logging Avancé

**Statut**: Logging basique (print)
**Priorité**: MOYENNE
**Temps estimé**: 1 jour

**Description**:
Implémenter un système de logging professionnel.

**Fichiers**:
- `src/utils/logger.py`
- Logs dans `~/.juryaissist/logs/`

**Fonctionnalités**:
- Niveaux: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Rotation automatique des fichiers (max 10 MB par fichier)
- Format: timestamp, niveau, module, message
- Logs d'erreurs envoyés dans fichier séparé

**Exemple**:
```python
# src/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Handler fichier
    handler = RotatingFileHandler(
        '~/.juryaissist/logs/app.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```

---

### 13. CI/CD avec GitHub Actions

**Statut**: Non configuré
**Priorité**: MOYENNE (pour projet collaboratif)
**Temps estimé**: 1 jour

**Description**:
Automatiser les tests et les builds.

**Pipeline**:
1. **Tests** (sur chaque push)
   - Linter (black, pylint, mypy)
   - Tests unitaires
   - Tests d'intégration
   - Rapport de couverture

2. **Build** (sur tag de version)
   - Build exécutables (macOS, Windows, Linux)
   - Création des installateurs
   - Upload vers GitHub Releases

**Fichier**: `.github/workflows/ci.yml`

```yaml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.13
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run linters
        run: |
          black --check src/ tests/
          pylint src/
          mypy src/
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 📱 Nouvelles Fonctionnalités

### 14. Support Multi-fichiers (Playlist)

**Statut**: Non implémenté
**Priorité**: BASSE
**Temps estimé**: 2-3 jours

**Description**:
Gérer plusieurs fichiers audio dans une session.

**Fonctionnalités**:
- Charger plusieurs fichiers
- Navigation entre fichiers (Précédent/Suivant)
- Transcription batch (tous les fichiers)
- Export consolidé

**Interface**:
- Panneau latéral avec liste de fichiers
- Indicateur du fichier actif
- Progression globale

---

### 15. Correction Orthographique Intégrée

**Statut**: Non implémenté
**Priorité**: BASSE
**Temps estimé**: 2 jours

**Description**:
Ajouter vérification orthographique dans l'éditeur.

**Bibliothèque**:
- pyspellchecker ou language-tool-python
- Dictionnaire juridique français personnalisé

**Fonctionnalités**:
- Soulignement en rouge des fautes
- Suggestions au clic droit
- Ajout au dictionnaire personnel
- Support multi-langues

---

### 16. Cloud Backup et Synchronisation

**Statut**: Non implémenté
**Priorité**: BASSE (nécessite backend)
**Temps estimé**: 1-2 semaines

**Description**:
Synchroniser les projets dans le cloud.

**Fonctionnalités**:
- Sauvegarde automatique (Google Drive, Dropbox, S3)
- Synchronisation entre machines
- Historique de versions
- Partage de projets

**Architecture**:
- Backend REST API (Flask/FastAPI)
- Base de données (PostgreSQL)
- Stockage fichiers (S3)
- Authentification (OAuth2)

**Note**: Nécessite développement backend séparé

---

## 🐛 Corrections et Robustesse

### 17. Gestion d'Erreurs Améliorée

**Statut**: Gestion basique en place
**Priorité**: MOYENNE
**Temps estimé**: 1-2 jours

**Améliorations**:
- Dialogues d'erreur plus informatifs
- Récupération automatique en cas d'erreur
- Rapport de bugs automatique (optionnel)
- Mode "safe" en cas de crash répété

**Exemple**:
```python
class ErrorDialog(QDialog):
    """Dialogue d'erreur avancé."""

    def __init__(self, error: Exception):
        # Affichage message utilisateur
        # Détails techniques en mode expandable
        # Boutons: Réessayer, Ignorer, Rapporter, Quitter
```

---

### 18. Tests de Robustesse

**Statut**: Non implémenté
**Priorité**: MOYENNE
**Temps estimé**: 2 jours

**Tests à ajouter**:
- Déconnexion pédale pendant lecture
- Fichier audio corrompu
- Transcription très longue (>3h)
- Mémoire limitée (simulation)
- Disque plein lors de l'export

**Fichier**: `tests/robustness/test_edge_cases.py`

---

## 📊 Métriques et Analytics (Optionnel)

### 19. Statistiques d'Utilisation

**Statut**: Non implémenté
**Priorité**: TRÈS BASSE
**Temps estimé**: 2-3 jours

**Description**:
Collecter des statistiques anonymes d'utilisation (avec consentement).

**Métriques**:
- Temps moyen de transcription
- Formats audio les plus utilisés
- Actions pédale les plus fréquentes
- Temps passé dans l'application

**Privacy**:
- Opt-in explicite
- Données anonymisées
- Conformité RGPD
- Stockage local uniquement (option)

---

## 🎓 Documentation Avancée

### 20. Guide Vidéo et Tutoriels

**Statut**: Non créé
**Priorité**: MOYENNE (pour adoption)
**Temps estimé**: 3-4 jours

**Contenu**:
1. **Vidéo de présentation** (2 min)
   - Fonctionnalités principales
   - Cas d'usage

2. **Tutoriel de démarrage** (5 min)
   - Installation
   - Premier audio
   - Première transcription

3. **Tutoriel avancé** (10 min)
   - Configuration pédale
   - Workflows optimisés
   - Export professionnel

**Format**:
- Vidéos screencast avec voix off
- Sous-titres français/anglais
- Publication sur YouTube/Vimeo

---

## 🔐 Sécurité et Confidentialité (NOUVELLES PRIORITÉS)

### 21. Sécurité Juridique RGPD ⚠️ OBLIGATION LÉGALE

**Statut**: Non vérifié
**Priorité**: HAUTE (obligation légale)
**Temps estimé**: 2-3 jours

**Contexte**:
Les cabinets d'avocats sont soumis au **Secret Professionnel** et au **RGPD**.
Toute fuite de données audio/texte = sanctions graves.

#### 21.1 Garantie Transcription 100% Locale

**À faire**:
1. **Audit du code**: Vérifier qu'aucune connexion réseau n'est faite
2. **Documentation**: Section "🔒 Confidentialité et RGPD" dans README
3. **Verrouillage technique** (optionnel): Désactiver connexions réseau pendant transcription

**Documentation à ajouter au README**:
```markdown
## 🔒 Confidentialité et RGPD

JuryAIssist garantit une **transcription 100% locale** :
- ✅ Aucun audio ne quitte votre machine
- ✅ Aucune connexion Internet requise pour la transcription
- ✅ Modèle Whisper stocké localement
- ✅ Conformité RGPD et Secret Professionnel

**Audit technique** :
- Aucun appel API externe
- Traitement entièrement en mémoire
- Fichiers temporaires sécurisés (voir ci-dessous)
```

#### 21.2 Gestion Sécurisée des Fichiers Temporaires

**Risque**: Whisper peut créer des fichiers temporaires sur disque

**Solutions**:
1. **Utiliser io.BytesIO**: Tout en RAM
2. **Chiffrement**: Si disque nécessaire, AES-256
3. **Suppression sécurisée**: Écrasement avant suppression

**Code à implémenter**:
```python
# src/transcription/secure_transcriber.py
import io
from cryptography.fernet import Fernet

class SecureTranscriber:
    """Transcriber avec gestion sécurisée de la mémoire."""

    def __init__(self):
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)

    def transcribe_secure(self, audio_path: str):
        # Charger en mémoire (pas de fichier temporaire)
        with open(audio_path, 'rb') as f:
            audio_data = f.read()

        # Transcrire depuis BytesIO
        audio_stream = io.BytesIO(audio_data)
        result = self.whisper_model.transcribe(audio_stream)

        # Effacer la mémoire de manière sécurisée
        del audio_data
        import gc
        gc.collect()

        return result
```

---

## ✨ Nouvelles Fonctionnalités Avancées

### 22. Nettoyage Post-Transcription avec LLM

**Statut**: Non implémenté
**Priorité**: HAUTE (qualité transcription)
**Temps estimé**: 1 semaine

**Problème**:
Whisper produit du texte brut avec:
- Hésitations ("euh", "hmm", "ben")
- Répétitions ("je je je pense")
- Bégaiements
- Ponctuation approximative
- Erreurs sur jargon juridique

**Solution**: Pipeline de nettoyage avec petit LLM local

#### 22.1 Choix du Modèle LLM

**Comparatif des Small Language Models (SLM)** :

| Modèle | Taille | Performance | Français | Vitesse |
|--------|--------|-------------|----------|---------|
| **Qwen3-0.6B** ⭐ | 600 MB | Excellente | ✅ Parfait | Ultra-rapide |
| **Phi-4 Mini-Flash** | 800 MB | Très bonne | ✅ Bon | Rapide |
| **Gemma-3n-2B** | 2 GB | Supérieure | ✅ Excellent | Moyenne |

**Recommandation**: **Qwen3-0.6B** (Alibaba)
- Minuscule (600 MB)
- Parfait pour français juridique
- Peut tourner en arrière-plan sur CPU

#### 22.2 Architecture du Post-Processor

**Fichier à créer**: `src/transcription/text_cleaner.py`

**Interface SOLID**:
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

class ITextProcessor(ABC):
    @abstractmethod
    def process(self, raw_text: str) -> CleanedText:
        """Nettoie le texte brut."""
        pass

@dataclass
class CleanedText:
    original: str           # Texte original (JAMAIS supprimé)
    cleaned: str            # Texte nettoyé
    changes: List[Change]   # Liste des modifications

@dataclass
class Change:
    position: int           # Position dans l'original
    original_text: str      # Texte supprimé/modifié
    new_text: str          # Texte remplacé (ou "" si suppression)
    reason: str            # "disfluence", "repetition", "punctuation"
```

**Implémentation avec Qwen**:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

class LegalTextCleaner(ITextProcessor):
    """Nettoyeur de texte juridique avec Qwen 0.6B."""

    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-0.6B-Instruct"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="cpu"
        )

    def process(self, raw_text: str) -> CleanedText:
        prompt = f"""Tu es un assistant de transcription juridique.

Nettoie le texte suivant :
- Enlève les hésitations (euh, hmm, ben)
- Enlève les répétitions
- Corrige la ponctuation
- NE CHANGE AUCUN MOT JURIDIQUE OU TECHNIQUE
- Conserve TOUS les faits, noms, dates

Texte original :
{raw_text}

Texte nettoyé :"""

        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=512)
        cleaned = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extraire seulement la partie après "Texte nettoyé :"
        cleaned = cleaned.split("Texte nettoyé :")[1].strip()

        # Détecter changements (algorithme de diff)
        changes = self._detect_changes(raw_text, cleaned)

        return CleanedText(
            original=raw_text,
            cleaned=cleaned,
            changes=changes
        )
```

#### 22.3 Alternative Sans LLM (Plus Performante)

**Pour nettoyage simple**: Utiliser un modèle de classification de tokens

```python
from deepmultilingualpunctuation import PunctuationModel
import re

class SimpleCleaner(ITextProcessor):
    """Nettoyeur simple sans LLM (plus rapide)."""

    def __init__(self):
        self.punct_model = PunctuationModel()
        self.disfluences = {"euh", "hmm", "ben", "voilà", "donc", "alors"}

    def process(self, raw_text: str) -> CleanedText:
        # 1. Enlever disfluences
        words = raw_text.split()
        cleaned_words = [w for w in words if w.lower().strip('.,!?') not in self.disfluences]

        # 2. Enlever répétitions
        cleaned_words = self._remove_repetitions(cleaned_words)

        # 3. Corriger ponctuation
        text = " ".join(cleaned_words)
        text = self.punct_model.restore_punctuation(text)

        changes = []  # À implémenter si besoin
        return CleanedText(original=raw_text, cleaned=text, changes=changes)

    def _remove_repetitions(self, words: List[str]) -> List[str]:
        """Enlève les répétitions consécutives."""
        result = []
        prev = None
        for word in words:
            if word.lower() != prev:
                result.append(word)
            prev = word.lower()
        return result
```

#### 22.4 Interface Graphique "Double Vue" ⚠️ CRITIQUE JURIDIQUE

**IMPORTANT**: Ne JAMAIS supprimer définitivement le texte original

**Fichier**: `src/gui/widgets/dual_editor.py`

**Interface avec onglets**:
```python
class DualEditorPanel(QWidget):
    """Éditeur avec vue double (original + nettoyé)."""

    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()

        # Onglet 1: Texte nettoyé (par défaut, éditable)
        self.cleaned_editor = QTextEdit()
        self.cleaned_editor.setPlaceholderText("Texte nettoyé (modifiable)")

        # Onglet 2: Texte original (lecture seule, archivage)
        self.original_editor = QTextEdit()
        self.original_editor.setReadOnly(True)
        self.original_editor.setStyleSheet("background-color: #f0f0f0;")

        # Onglet 3: Vue Diff (surlignage des changements)
        self.diff_viewer = QTextEdit()
        self.diff_viewer.setReadOnly(True)

        self.tab_widget.addTab(self.cleaned_editor, "✅ Nettoyé")
        self.tab_widget.addTab(self.original_editor, "📄 Original")
        self.tab_widget.addTab(self.diff_viewer, "🔍 Différences")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def set_cleaned_text(self, cleaned: CleanedText):
        """Charge le texte nettoyé et l'original."""
        self.cleaned_editor.setPlainText(cleaned.cleaned)
        self.original_editor.setPlainText(cleaned.original)
        self._show_diff(cleaned)

    def _show_diff(self, cleaned: CleanedText):
        """Affiche les différences avec couleurs."""
        html = "<style>"
        html += "del { background-color: #ffcccc; text-decoration: line-through; }"
        html += "ins { background-color: #ccffcc; }"
        html += "</style>"

        # Algorithme de diff simplifié
        import difflib
        diff = difflib.ndiff(
            cleaned.original.split(),
            cleaned.cleaned.split()
        )

        for item in diff:
            if item.startswith('- '):
                html += f"<del>{item[2:]}</del> "
            elif item.startswith('+ '):
                html += f"<ins>{item[2:]}</ins> "
            elif item.startswith('  '):
                html += f"{item[2:]} "

        self.diff_viewer.setHtml(html)
```

---

### 23. Réduction de Bruit Audio (Pré-Processing)

**Statut**: Non implémenté
**Priorité**: MOYENNE
**Temps estimé**: 2 jours

**Problème**:
Dictaphones juridiques bas de gamme = bruit de fond, souffle

**Solution**: Filtre audio avant transcription

**Bibliothèque**: `noisereduce`

```python
# src/transcription/audio_preprocessor.py
import noisereduce as nr
import soundfile as sf

class AudioPreprocessor:
    """Pré-traitement audio avant transcription."""

    def reduce_noise(self, audio_path: str) -> str:
        """Réduit le bruit d'un fichier audio."""
        # Charger audio
        data, rate = sf.read(audio_path)

        # Réduire bruit
        reduced_noise = nr.reduce_noise(y=data, sr=rate)

        # Sauvegarder temporairement
        temp_path = audio_path.replace(".mp3", "_cleaned.wav")
        sf.write(temp_path, reduced_noise, rate)

        return temp_path
```

**Intégration dans WhisperTranscriber**:
```python
# Dans src/transcription/whisper_transcriber.py
def transcribe(self, audio_source: IAudioSource) -> Transcript:
    # 1. Pré-traitement (optionnel via paramètre)
    if self.enable_noise_reduction:
        cleaned_path = self.preprocessor.reduce_noise(audio_source.file_path)
    else:
        cleaned_path = audio_source.file_path

    # 2. Transcription
    result = self.model.transcribe(cleaned_path)

    # 3. Nettoyage fichier temporaire
    if self.enable_noise_reduction:
        os.remove(cleaned_path)

    return result
```

**Option dans GUI**:
- Checkbox "Réduire le bruit" dans panneau de transcription
- Sauvegardée dans les préférences utilisateur

---

### 24. Migration STT vers Modèles 2026 (Optionnel)

**Statut**: Whisper fonctionne bien
**Priorité**: BASSE (optimisation)
**Temps estimé**: 2-3 jours

**Contexte**:
Whisper (OpenAI) reste la référence, mais nouveaux modèles 2026 sont plus rapides.

**Comparatif STT Local (Janvier 2026)**:

| Modèle | Vitesse vs Whisper | Précision (WER) | Taille | Point Fort |
|--------|-------------------|-----------------|--------|------------|
| **Whisper (faster-whisper)** | Baseline | Excellente | 1.5-3 GB | Standard, très stable |
| **NVIDIA Parakeet TDT 0.6B** ⚡ | **5x plus rapide** | Très bonne | 1.2 GB | Temps réel, GPU-friendly |
| **Canary Qwen 2.5B** | 3x plus rapide | **Supérieure** | 2.5 GB | Top benchmarks 2026 |
| **Moonshine (Tiny)** | 10x plus rapide | Correcte | **500 MB** | MacBook Air, CPU-only |

**Recommandation**:
- **Garder Whisper (faster-whisper)** par défaut (robustesse juridique)
- **Ajouter Parakeet TDT** en option si utilisatrices se plaignent de lenteur
- **Interface**: Dropdown de choix de moteur dans paramètres

**Architecture extensible avec Factory Pattern**:
```python
# src/transcription/transcriber_factory.py
def create_transcriber(engine: str, model_size: str = "base") -> ITranscriber:
    """Factory pour créer le bon transcriber."""
    if engine == "whisper":
        return WhisperTranscriber(model_size)
    elif engine == "faster-whisper":
        return FasterWhisperTranscriber(model_size)
    elif engine == "parakeet":
        return ParakeetTranscriber(model_size)
    elif engine == "moonshine":
        return MoonshineTranscriber(model_size)
    else:
        raise ValueError(f"Moteur inconnu: {engine}")
```

---

## 📝 Résumé des Priorités ACTUALISÉ

### 🔴 Haute Priorité CRITIQUE (1-2 semaines)
1. **Packaging et distribution** (#2) - BLOQUANT POUR DISTRIBUTION
   - Exécutables standalone (macOS/Windows)
   - Migration faster-whisper (réduction taille)
   - Permissions HID automatiques
   - Fallback VLC

2. **Sécurité Juridique RGPD** (#21) - OBLIGATION LÉGALE
   - Documentation confidentialité
   - Fichiers temporaires sécurisés
   - Audit code (zéro connexion réseau)

3. **Nettoyage Post-Transcription LLM** (#22) - QUALITÉ
   - Qwen3-0.6B ou SimpleCleaner
   - Interface "Double Vue" (original + nettoyé)
   - Diff viewer

### 🟡 Haute Priorité (2-3 semaines)
4. Configuration pédale via GUI (#1)
5. Tests d'intégration automatisés (#3)
6. Réduction de bruit audio (#23)
7. Documentation utilisateur complète

### 🟢 Moyenne Priorité (optionnel)
8. Système de logging avancé (#12)
9. Gestion d'erreurs améliorée (#17)
10. Guide vidéo (#20)
11. Migration STT 2026 (#24)

### ⚪ Basse Priorité (fonctionnalités avancées)
12. Support autres pédales (#4)
13. Appuis longs (#5)
14. Thèmes d'interface (#6)
15. Raccourcis configurables (#7)
16. Détection locuteurs (#9)
17. Export DOCX avancé (#10)
18. Optimisations performance (#11)
19. Multi-fichiers (#14)
20. Correction orthographique (#15)
21. Cloud backup (#16)

---

## 🚀 Recommandation MISE À JOUR

Pour la **prochaine phase de développement**, ordre de priorité CRITIQUE:

### Semaine 1-2: Bloquants Distribution
1. **Packaging Standalone** (#2) - URGENT
   - PyInstaller/Briefcase pour .app/.exe
   - Intégration libvlc
   - Migration faster-whisper (divise taille par 4)
   - Permissions HID automatiques (Linux/macOS)

2. **Sécurité RGPD** (#21) - LÉGAL
   - Documentation confidentialité dans README
   - Audit code (pas de connexions réseau)
   - Fichiers temporaires en RAM (io.BytesIO)

### Semaine 3: Qualité Transcription
3. **Nettoyage LLM** (#22) - VALEUR AJOUTÉE
   - Implémentation Qwen3-0.6B ou SimpleCleaner
   - Interface "Double Vue" avec onglets
   - Diff viewer (crucial pour juridique)

4. **Réduction Bruit** (#23) - BONUS
   - noisereduce pour dictaphones bas de gamme
   - Option activable dans GUI

### Semaine 4: Finitions
5. **Configuration Pédale GUI** (#1)
6. **Tests automatisés** (#3)
7. **Documentation** (#20)

**Ces améliorations** rendront l'application **prête pour distribution professionnelle** avec:
- ✅ Installation facile (non-technique)
- ✅ Conformité RGPD/Secret Professionnel
- ✅ Qualité transcription améliorée (nettoyage LLM)
- ✅ Performance optimisée (faster-whisper)

---

**Document mis à jour le**: 2026-01-06
**Version application**: 2.1.0
**Auteur**: Analyse du projet JuryAIssist + Pistes critiques pour utilisateurs non-techniques
