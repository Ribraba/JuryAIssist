# Scripts utilitaires Figma

Ce dossier contient les scripts utilisés lors de l'intégration du design Figma dans l'application.

## Scripts disponibles

### `fetch_figma_design.py`
Récupère le design depuis l'API Figma et le sauvegarde en JSON.

**Usage:**
```bash
python utils/figma/fetch_figma_design.py
```

### `analyze_figma_design.py`
Analyse le fichier JSON du design Figma et génère un rapport.

**Usage:**
```bash
python utils/figma/analyze_figma_design.py
```

### `download_inter_font.py`
Télécharge et installe la police Inter utilisée dans le design.

**Usage:**
```bash
python utils/figma/download_inter_font.py
```

### `launch_figma_ui.py`
Lanceur pour tester l'interface Figma (version de développement).

**Usage:**
```bash
python utils/figma/launch_figma_ui.py
```

### `test_figma_ui.py`
Tests manuels pour l'interface Figma.

**Usage:**
```bash
python utils/figma/test_figma_ui.py
```

## Fichiers de données

### `figma_design.json`
Export JSON du design Figma original, utilisé comme référence.

---

**Note:** Ces scripts sont conservés pour référence et maintenance future. L'interface Figma est maintenant intégrée dans `src/gui/main_window.py`.
