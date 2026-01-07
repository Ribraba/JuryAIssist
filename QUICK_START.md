# 🚀 Guide de démarrage rapide - Interface Figma

## ⚡ Lancement en 3 étapes

### 1. Activer l'environnement

```bash
cd /Users/ibrahim/Documents/Projets/JuryAIssist
source venv/bin/activate
```

### 2. Lancer l'interface Figma

```bash
python launch_figma_ui.py
```

### 3. Tester !

L'interface s'ouvre avec :
- ✅ Sidebar de navigation à gauche
- ✅ Timeline avec texte défilant
- ✅ Panneaux de transcription et d'édition
- ✅ Contrôles audio en bas
- ✅ Badge de pédale en haut à droite

## 📋 Checklist de test

### Interface
- [ ] La sidebar s'affiche à gauche (256px)
- [ ] Le titre "JuryAIssist" est visible
- [ ] La barre de recherche est présente
- [ ] Les fichiers "Affaire Dupont.m4a" et "audience_2024.mp3" sont listés
- [ ] Les boutons "Nouvel import" et "Paramètres" sont visibles

### Timeline
- [ ] La barre de timeline est visible en haut
- [ ] La zone de texte défilant est au-dessus

### Panneaux
- [ ] Panneau gauche : "Transcription brute" / "Lecture"
- [ ] Panneau droit : Nom du fichier / "Édition"
- [ ] Les deux panneaux sont redimensionnables (splitter)

### Contrôles audio
- [ ] Boutons Play, Stop, Skip visible
- [ ] Slider de volume présent
- [ ] Temps affiché (00:00 / 00:00)
- [ ] Vitesse affichée (1.0x)

### Pédale
- [ ] Badge visible en haut à droite
- [ ] État affiché (connectée ou déconnectée)

## 🎯 Premier test fonctionnel

### 1. Charger un fichier audio

1. Cliquez sur **"Nouvel import"** dans la sidebar
2. Sélectionnez un fichier audio (.mp3, .m4a, .wav, etc.)
3. Confirmez la transcription quand demandé

### 2. Observer la transcription

Une fois transcrite, vous devriez voir :
- ✅ Le texte dans le panneau de transcription (gauche)
- ✅ Le texte dans l'éditeur (droite)
- ✅ Le texte dans la timeline (en haut)

### 3. Tester la navigation

- **Timeline** : Cliquez sur la barre pour sauter à un moment
- **Transcription** : Cliquez sur un mot pour y naviguer
- **Audio** : Utilisez Play/Pause/Skip

### 4. Observer le texte défilant

Pendant la lecture :
- ✅ Le texte défile horizontalement
- ✅ Le mot actuel est opaque (100%)
- ✅ Les mots avant/après sont plus transparents
- ✅ L'effet suit la lecture en temps réel

## 🎨 Comparaison avec Figma

Ouvrez le design Figma pour comparer :
https://www.figma.com/design/0ieFrBWSvz46jv5zOYcW4e/JuryAIssist

Vérifiez :
- [ ] Couleurs identiques
- [ ] Espacements cohérents
- [ ] Typographie similaire (si Inter installée)
- [ ] Layout respecté
- [ ] Icônes correctes

## 🐛 Dépannage rapide

### L'interface ne se lance pas

```bash
# Vérifier l'environnement
which python
# Devrait afficher: .../venv/bin/python

# Réinstaller les dépendances si besoin
pip install -r requirements.txt
```

### Les icônes ne s'affichent pas

```bash
# Vérifier que les icônes sont présentes
ls src/gui/icons_figma/
# Devrait lister 10 fichiers .svg
```

### La police ne ressemble pas à Figma

C'est normal si Inter n'est pas installée.

Pour l'installer : voir `INSTALL_INTER_FONT.md`

Sans Inter, l'app utilise :
- **macOS** : SF Pro (très proche)
- **Windows** : Segoe UI
- **Linux** : Sans-serif système

### La pédale ne se connecte pas

C'est normal si :
- Vous n'avez pas de pédale Olympus RS-31
- La pédale n'est pas branchée
- Les drivers hidapi ne sont pas installés

L'interface fonctionne parfaitement sans pédale !

## 📝 Commandes utiles

```bash
# Lancer l'interface Figma
python launch_figma_ui.py

# Lancer l'ancienne interface (comparaison)
python -m src.main

# Tester les imports (sans GUI)
python test_figma_ui.py

# Lister les icônes
ls -la src/gui/icons_figma/

# Vérifier les design tokens
cat src/gui/design_tokens.py
```

## 📚 Documentation complète

Pour plus de détails :

| Document | Contenu |
|----------|---------|
| `INTEGRATION_COMPLETE.md` | Résumé complet de l'intégration |
| `FIGMA_UI_README.md` | Documentation détaillée de l'interface |
| `IMPLEMENTATION_PLAN.md` | Plan technique d'implémentation |
| `INSTALL_INTER_FONT.md` | Installation de la police Inter |

## ✅ Validation

Une fois testé, validez :

- [ ] Le design correspond à Figma
- [ ] Toutes les fonctionnalités marchent
- [ ] Les performances sont bonnes
- [ ] L'ergonomie est satisfaisante

Si tout est OK → Prêt pour la migration ! 🎉

Si des ajustements sont nécessaires → Notez-les et on les fait ensemble !

---

**Prêt à tester ? Lancez : `python launch_figma_ui.py`** 🚀
