# Prochaines Étapes - Refactoring SOLID

**État actuel**: Phase 3 terminée (40% du refactoring)
**Branche**: `refactoring/solid-architecture-phase1`
**Dernière mise à jour**: 2026-01-12

---

## ✅ Ce Qui Est Fait

### Phase 1: Nettoyage Legacy (100%)
- Suppression ~3,500 lignes de code Flet
- Fix bug blocage UI transcription
- Test E2E créé et validé

### Phases 2-3: Architecture Layered (100%)
- **Domain layer** (15 fichiers, 100% Qt-free)
  - Audio: interfaces, entities, events
  - Transcription: interfaces, entities, events
  - Devices: interfaces, entities, events
  - Common: TimeUtils

- **Infrastructure layer** (15 fichiers)
  - Copies des implémentations (VLC, Whisper, HID)
  - Imports mis à jour pour utiliser domain layer

**Commits**: 7 commits propres, branche pushée

---

## 🚧 Ce Qui Reste à Faire (60%)

### Phase 4: Domain Controllers Qt-Free

**Fichiers à créer** (3 fichiers, ~500 lignes):

#### 1. `src/domain/audio/controller.py`

Version Qt-free de `src/audio/controller.py`:

```python
"""
AudioController Qt-free pour le domain layer.
"""
from typing import Optional, Callable
from .interfaces import IAudioPlayer, IAudioSource
from .entities import PlayerState
from .events import AudioEvent, AudioEventType


class AudioController:
    """
    Contrôleur audio sans dépendance Qt.

    Utilise des callbacks au lieu de signaux Qt.
    """

    def __init__(
        self,
        player: IAudioPlayer,
        event_callback: Optional[Callable[[AudioEvent], None]] = None
    ):
        self._player = player
        self._event_callback = event_callback
        self._current_source: Optional[IAudioSource] = None
        self._current_speed = 1.0
        self._current_volume = 100

    def load_file(self, filepath: str) -> bool:
        """Charge un fichier et émet événement."""
        from src.infrastructure.audio.source import FileAudioSource
        source = FileAudioSource(filepath)

        if not source.is_available():
            self._emit_event(AudioEvent(
                type=AudioEventType.ERROR,
                message=f"File not found: {filepath}"
            ))
            return False

        success = self._player.load(source.get_uri())

        if success:
            self._current_source = source
            duration = self._player.get_duration()

            self._emit_event(AudioEvent(
                type=AudioEventType.SOURCE_LOADED,
                source_name=source.get_display_name(),
                duration=duration
            ))

            self._emit_event(AudioEvent(
                type=AudioEventType.STATE_CHANGED,
                state=self._player.get_state()
            ))

        return success

    def play(self) -> bool:
        """Démarre lecture."""
        success = self._player.play()
        if success:
            self._emit_event(AudioEvent(
                type=AudioEventType.STATE_CHANGED,
                state=PlayerState.PLAYING
            ))
        return success

    def pause(self) -> bool:
        """Met en pause."""
        success = self._player.pause()
        if success:
            self._emit_event(AudioEvent(
                type=AudioEventType.STATE_CHANGED,
                state=PlayerState.PAUSED
            ))
        return success

    def seek(self, position: float) -> bool:
        """Se déplace à une position."""
        success = self._player.seek(position)
        if success:
            self._emit_event(AudioEvent(
                type=AudioEventType.POSITION_CHANGED,
                position=position
            ))
        return success

    def set_speed(self, speed: float) -> bool:
        """Change vitesse."""
        success = self._player.set_speed(speed)
        if success:
            self._current_speed = speed
            self._emit_event(AudioEvent(
                type=AudioEventType.SPEED_CHANGED,
                speed=speed
            ))
        return success

    def set_volume(self, volume: int) -> bool:
        """Change volume."""
        success = self._player.set_volume(volume)
        if success:
            self._current_volume = volume
            self._emit_event(AudioEvent(
                type=AudioEventType.VOLUME_CHANGED,
                volume=volume
            ))
        return success

    def get_position(self) -> float:
        """Position actuelle."""
        return self._player.get_position()

    def get_duration(self) -> float:
        """Durée totale."""
        return self._player.get_duration()

    def get_state(self) -> PlayerState:
        """État actuel."""
        return self._player.get_state()

    def _emit_event(self, event: AudioEvent) -> None:
        """Émet un événement via callback."""
        if self._event_callback:
            self._event_callback(event)
```

**Source**: Adapter depuis `src/audio/controller.py` (lignes 1-400)

#### 2. `src/domain/devices/controller.py`

Version Qt-free de `src/devices/olympus_pedal.py`:

```python
"""
PedalController Qt-free pour le domain layer.
"""
from typing import Optional, Callable
from .interfaces import IPedalDetector, IEventParser, IActionMapper, IPedalReader
from .entities import ButtonEvent, PedalAction, PedalInfo
from .events import PedalEvent, PedalEventType


class PedalController:
    """
    Contrôleur pédale sans dépendance Qt.
    """

    def __init__(
        self,
        detector: IPedalDetector,
        parser: IEventParser,
        mapper: IActionMapper,
        event_callback: Optional[Callable[[PedalEvent], None]] = None
    ):
        self._detector = detector
        self._parser = parser
        self._mapper = mapper
        self._event_callback = event_callback

        self._pedal_info: Optional[PedalInfo] = None
        self._reader: Optional[IPedalReader] = None

    def detect(self) -> bool:
        """Détecte pédale."""
        try:
            self._pedal_info = self._detector.detect()

            if self._pedal_info is None:
                self._emit_event(PedalEvent(
                    type=PedalEventType.ERROR,
                    message="No pedal detected"
                ))
                return False

            return True
        except Exception as e:
            self._emit_event(PedalEvent(
                type=PedalEventType.ERROR,
                message=str(e)
            ))
            return False

    def connect(self) -> bool:
        """Connecte à la pédale."""
        if self._pedal_info is None:
            if not self.detect():
                return False

        try:
            from src.infrastructure.devices.hid_reader import HIDReader

            # Créer reader avec callback
            self._reader = HIDReader(
                pedal_info=self._pedal_info,
                event_parser=self._parser,
                event_callback=self._on_button_event
            )

            if self._reader.start():
                self._emit_event(PedalEvent(type=PedalEventType.CONNECTED))
                return True

            return False

        except Exception as e:
            self._emit_event(PedalEvent(
                type=PedalEventType.ERROR,
                message=str(e)
            ))
            return False

    def disconnect(self) -> None:
        """Déconnecte pédale."""
        if self._reader:
            self._reader.stop()
            self._reader = None

        self._emit_event(PedalEvent(type=PedalEventType.DISCONNECTED))

    def _on_button_event(self, event: ButtonEvent) -> None:
        """Gère événement bouton."""
        if event.pressed:
            self._emit_event(PedalEvent(
                type=PedalEventType.BUTTON_PRESSED,
                button_number=event.button_number
            ))

            action = self._mapper.get_action(event.button_number)
            if action != PedalAction.UNKNOWN:
                self._emit_event(PedalEvent(
                    type=PedalEventType.ACTION_TRIGGERED,
                    action=action
                ))
        else:
            self._emit_event(PedalEvent(
                type=PedalEventType.BUTTON_RELEASED,
                button_number=event.button_number
            ))

    def _emit_event(self, event: PedalEvent) -> None:
        """Émet événement."""
        if self._event_callback:
            self._event_callback(event)
```

**Source**: Adapter depuis `src/devices/olympus_pedal.py`

#### 3. `src/domain/transcription/service.py`

Nouveau service avec progress callbacks:

```python
"""
TranscriptionService pour le domain layer.
"""
from typing import Callable, Optional
from .interfaces import ITranscriber
from .entities import TranscriptionResult, TranscriptionStatus
from .events import TranscriptionEvent, TranscriptionEventType


class TranscriptionService:
    """Service de transcription avec progress."""

    def __init__(
        self,
        transcriber: ITranscriber,
        event_callback: Optional[Callable[[TranscriptionEvent], None]] = None
    ):
        self._transcriber = transcriber
        self._event_callback = event_callback

    def transcribe_with_progress(
        self,
        audio_path: str,
        language: Optional[str] = None
    ) -> TranscriptionResult:
        """Transcrit avec émission de progress."""
        self._emit_event(TranscriptionEvent(
            type=TranscriptionEventType.STARTED,
            message="Starting transcription..."
        ))

        try:
            # Progress 0%
            self._emit_event(TranscriptionEvent(
                type=TranscriptionEventType.PROGRESS,
                progress_percent=0
            ))

            # Transcription (TODO: hook into Whisper progress)
            result = self._transcriber.transcribe(audio_path, language)

            # Progress 100%
            self._emit_event(TranscriptionEvent(
                type=TranscriptionEventType.PROGRESS,
                progress_percent=100
            ))

            if result.status == TranscriptionStatus.COMPLETED:
                self._emit_event(TranscriptionEvent(
                    type=TranscriptionEventType.COMPLETED,
                    result=result
                ))
            else:
                self._emit_event(TranscriptionEvent(
                    type=TranscriptionEventType.ERROR,
                    message=result.error_message
                ))

            return result

        except Exception as e:
            self._emit_event(TranscriptionEvent(
                type=TranscriptionEventType.ERROR,
                message=str(e)
            ))
            raise

    def _emit_event(self, event: TranscriptionEvent) -> None:
        """Émet événement."""
        if self._event_callback:
            self._event_callback(event)
```

---

### Phase 5: Qt Adapters (Presentation Layer)

**Fichiers à créer** (3 fichiers, ~400 lignes):

#### 1. `src/presentation/adapters/audio_adapter.py`

```python
"""Qt adapter for AudioController."""
from PySide6.QtCore import QObject, QTimer, Signal
from src.domain.audio.controller import AudioController
from src.domain.audio.events import AudioEvent, AudioEventType


class AudioControllerAdapter(QObject):
    """Convertit domain events → Qt signals."""

    position_changed = Signal(float)
    state_changed = Signal(object)
    duration_changed = Signal(float)
    source_loaded = Signal(str)
    speed_changed = Signal(float)
    volume_changed = Signal(int)
    error_occurred = Signal(str)

    def __init__(self, controller: AudioController, update_interval: int = 100):
        super().__init__()
        self._controller = controller
        self._controller._event_callback = self._on_controller_event

        # Position timer
        self._position_timer = QTimer()
        self._position_timer.setInterval(update_interval)
        self._position_timer.timeout.connect(self._update_position)

    def _on_controller_event(self, event: AudioEvent):
        """Convertit événements domain en signaux Qt."""
        if event.type == AudioEventType.POSITION_CHANGED:
            self.position_changed.emit(event.position)
        elif event.type == AudioEventType.STATE_CHANGED:
            self.state_changed.emit(event.state)
            # Start/stop timer based on state
            from src.domain.audio.entities import PlayerState
            if event.state == PlayerState.PLAYING:
                self._position_timer.start()
            else:
                self._position_timer.stop()
        elif event.type == AudioEventType.DURATION_CHANGED:
            self.duration_changed.emit(event.duration)
        elif event.type == AudioEventType.SOURCE_LOADED:
            self.source_loaded.emit(event.source_name)
        elif event.type == AudioEventType.SPEED_CHANGED:
            self.speed_changed.emit(event.speed)
        elif event.type == AudioEventType.VOLUME_CHANGED:
            self.volume_changed.emit(event.volume)
        elif event.type == AudioEventType.ERROR:
            self.error_occurred.emit(event.message)

    def _update_position(self):
        """Update position periodically."""
        position = self._controller.get_position()
        self.position_changed.emit(position)

    # Delegate methods
    def load_file(self, filepath: str) -> bool:
        return self._controller.load_file(filepath)

    def play(self) -> bool:
        return self._controller.play()

    def pause(self) -> bool:
        return self._controller.pause()

    # ... autres méthodes
```

#### 2. `src/presentation/adapters/pedal_adapter.py`
#### 3. `src/presentation/adapters/transcription_adapter.py`

Voir `REFACTORING_STATUS.md` pour templates complets.

---

### Phase 6: DI Container

**Fichier**: `src/application/container.py` (~200 lignes)

Voir `REFACTORING_STATUS.md` section Phase 5.

---

### Phase 7: Entry Point

**Fichier**: `src/application/main.py` (~80 lignes)

Voir `REFACTORING_STATUS.md` section Phase 6.

---

### Phases 8-10: Migration GUI, Cleanup, Tests

Voir `REFACTORING_STATUS.md` et `REFACTORING_PROGRESS.md`.

---

## 🎯 Pour Reprendre

```bash
# Vérifier branche
git checkout refactoring/solid-architecture-phase1
git pull origin refactoring/solid-architecture-phase1

# Créer Phase 4 fichiers
# 1. src/domain/audio/controller.py
# 2. src/domain/devices/controller.py
# 3. src/domain/transcription/service.py

# Commit
git add src/domain/
git commit -m "feat(domain): add Qt-free controllers and service"

# Continuer Phase 5...
```

---

## 📚 Documentation Complète

- `REFACTORING_STATUS.md` - Roadmap détaillée avec templates de code
- `REFACTORING_PROGRESS.md` - Tracking détaillé
- `test_transcription_blocking.py` - Test E2E du fix transcription

---

## ⏱️ Estimation Temps Restant

| Phase | Temps | Complexité |
|-------|-------|------------|
| 4 (controllers) | 2h | Moyenne |
| 5 (adapters) | 2h | Moyenne |
| 6-7 (DI + entry) | 1.5h | Moyenne |
| 8 (GUI migration) | 1h | Moyenne |
| 9-10 (cleanup + tests) | 2h | Faible-Moyenne |
| **TOTAL** | **~8.5h** | |

**Progression actuelle**: 40%
