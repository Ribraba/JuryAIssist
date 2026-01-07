# Pédale Olympus RS-31 - Mapping HID

Date : 2026-01-03
Pédale testée : Serial 206122002

---

## 🔍 Identification HID

```
Vendor ID:  0x07b4 (OLYMPUS CORPORATION)
Product ID: 0x025f
Modèle:     HID FootSwitch RS Series (RS-31)
```

---

## 🎮 Mapping des Boutons

### Format des Données HID

La pédale envoie des paquets de 64 bytes. Seuls les 4 premiers bytes sont utilisés :

```
[byte0, byte1, byte2, byte3, ...]
```

### Événements Capturés

| Bouton | Pattern | byte[2] | byte[3] | Description |
|--------|---------|---------|---------|-------------|
| **Bouton 1** | `[0, 0, 1, 0]` | `0x01` | `0x00` | Reculer 5s |
| **Bouton 2** | `[0, 0, 2, 0]` | `0x02` | `0x00` | Play/Pause |
| **Bouton 3** | `[0, 0, 4, 0]` | `0x04` | `0x00` | Avancer 5s |
| **Bouton 4** | `[0, 0, 0, 2]` | `0x00` | `0x02` | À définir |
| **Repos** | `[0, 0, 0, 0]` | `0x00` | `0x00` | Aucun bouton |

### Masques de Bits

```python
BUTTON_MASKS = {
    1: (2, 0x01),  # byte[2], bit 0
    2: (2, 0x02),  # byte[2], bit 1
    3: (2, 0x04),  # byte[2], bit 2
    4: (3, 0x02),  # byte[3], bit 1
}
```

---

## 🔄 Séquence d'Événements

Chaque appui de bouton génère **2 événements** :

1. **Pressed** : Bouton enfoncé (pattern avec bits à 1)
2. **Released** : Bouton relâché (pattern `[0, 0, 0, 0]`)

### Exemple - Bouton 2

```
Appui → [0, 0, 2, 0]  (pressed)
Relâché → [0, 0, 0, 0]  (released)
```

---

## 📊 Données de Test

### Capture Réelle

```
Événement  | Pattern           | Action
-----------|-------------------|------------------
1          | [0, 0, 4, 0]     | Bouton 3 pressed
2          | [0, 0, 0, 0]     | Released
3          | [0, 0, 2, 0]     | Bouton 2 pressed
4          | [0, 0, 0, 0]     | Released
5          | [0, 0, 1, 0]     | Bouton 1 pressed
6          | [0, 0, 0, 0]     | Released
7          | [0, 0, 0, 2]     | Bouton 4 pressed
8          | [0, 0, 0, 0]     | Released
```

---

## 🎯 Configuration Proposée

### Mode Toggle (Validé)

| Bouton | Action par Défaut | Comportement |
|--------|------------------|--------------|
| **1** | Reculer 5s | Recule dans l'audio |
| **2** | Play/Pause (Toggle) | Bascule lecture/pause |
| **3** | Avancer 5s | Avance dans l'audio |
| **4** | Stop | Arrête et remet à 0 |

### Alternative Bouton 4

- **Option A** : Stop (simple et clair)
- **Option B** : Vitesse cycle (1.0x → 1.5x → 2.0x → 1.0x)
- **Option C** : Marqueur de position
- **Option D** : Configurable par l'utilisateur

---

## 💻 Implémentation

### Classe de Parsing

```python
class RS31EventParser:
    """Parse les événements de la pédale RS-31."""

    BUTTON_MASKS = {
        1: (2, 0x01),  # (byte_index, mask)
        2: (2, 0x02),
        3: (2, 0x04),
        4: (3, 0x02),
    }

    def parse(self, raw_data: bytes) -> List[ButtonEvent]:
        """
        Parse les données brutes HID.

        Args:
            raw_data: Paquet de 64 bytes de la pédale

        Returns:
            Liste d'événements (pressed/released)
        """
        events = []

        for button_num, (byte_idx, mask) in self.BUTTON_MASKS.items():
            if len(raw_data) > byte_idx:
                is_pressed = bool(raw_data[byte_idx] & mask)
                # Créer événement si changement d'état
                # ...

        return events
```

---

## 🧪 Tests

### Test de Détection

```bash
python -m src.utils.test_pedale
# Option 2 : Rechercher pédale Olympus
```

### Test de Capture

```bash
python -m src.utils.test_pedale
# Option 3 : Capturer événements (60s)
```

---

## 📝 Notes

- La pédale fonctionne en **mode Toggle** (pas Hold)
- Les appuis sont instantanés (< 50ms de latence)
- Pas d'appuis longs détectés dans cette version
- Format HID standard, compatible macOS/Linux/Windows

---

**Status** : ✅ Mapping complet et validé
