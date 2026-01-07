# Commandes essentielles - Interface Figma

## 🚀 Lancement

```bash
# Activer l'environnement
source venv/bin/activate

# Lancer la NOUVELLE interface (Figma)
python launch_figma_ui.py

# Lancer l'ANCIENNE interface (pour comparaison)
python -m src.main
```

## 🧪 Tests

```bash
# Tester les imports (sans GUI)
python test_figma_ui.py

# Lancer les tests unitaires
pytest tests/

# Vérifier le style de code
flake8 src/gui/
```

## 📁 Navigation

```bash
# Voir les widgets Figma
ls -la src/gui/widgets/ | grep figma

# Voir les icônes
ls -la src/gui/icons_figma/

# Voir la documentation
ls -la *.md
```

## 🔍 Inspection

```bash
# Voir les design tokens
cat src/gui/design_tokens.py

# Voir les styles
cat src/gui/figma_styles.py

# Voir le rapport d'analyse Figma
cat figma_analysis_report.md
```

## 📝 Édition

```bash
# Éditer la fenêtre principale
code src/gui/main_window_figma.py

# Éditer un widget spécifique
code src/gui/widgets/sidebar.py
code src/gui/widgets/scrolling_transcript_timeline.py

# Éditer les styles
code src/gui/figma_styles.py
```

## 🔧 Développement

```bash
# Ajouter une dépendance
pip install <package>
pip freeze > requirements.txt

# Mettre à jour les design tokens depuis Figma
python fetch_figma_design.py
python analyze_figma_design.py

# Créer un nouveau widget
touch src/gui/widgets/nouveau_widget.py
```

## 📊 Analyse

```bash
# Compter les lignes de code
find src/gui -name "*.py" -exec wc -l {} + | tail -1

# Lister tous les widgets
find src/gui/widgets -name "*.py" -type f

# Chercher un pattern
grep -r "ScrollingTranscript" src/gui/
```

## 🎨 Design

```bash
# Ouvrir le design Figma
open "https://www.figma.com/design/0ieFrBWSvz46jv5zOYcW4e/JuryAIssist"

# Voir les couleurs utilisées
grep "COLORS" src/gui/design_tokens.py

# Voir les polices utilisées
grep "TYPOGRAPHY" src/gui/design_tokens.py
```

## 📚 Documentation

```bash
# Lire le guide de démarrage
cat QUICK_START.md

# Lire le résumé complet
cat INTEGRATION_COMPLETE.md

# Lire la doc de l'interface
cat FIGMA_UI_README.md
```

## 🐛 Dépannage

```bash
# Vérifier l'environnement Python
which python
python --version

# Vérifier les dépendances installées
pip list | grep -i pyqt

# Voir les logs (si l'app tourne)
tail -f /tmp/juryaissist.log

# Tuer le processus si bloqué
pkill -f launch_figma_ui.py
```

## 📦 Export

```bash
# Créer une archive du projet
tar -czf juryaissist-figma.tar.gz \
  src/gui/figma*.py \
  src/gui/widgets/sidebar.py \
  src/gui/widgets/figma*.py \
  src/gui/widgets/scrolling*.py \
  src/gui/widgets/pedal*.py \
  src/gui/icons_figma/ \
  launch_figma_ui.py \
  *.md

# Extraire
tar -xzf juryaissist-figma.tar.gz
```

## 🔄 Git (si utilisé)

```bash
# Voir les fichiers créés
git status

# Ajouter les nouveaux fichiers
git add src/gui/figma*.py
git add src/gui/widgets/
git add *.md

# Commit
git commit -m "feat: Intégration complète du design Figma"

# Créer une branche
git checkout -b feature/figma-ui
```

## 💾 Backup

```bash
# Sauvegarder le code Figma
mkdir -p ~/backups/juryaissist-figma-$(date +%Y%m%d)
cp -r src/gui/ ~/backups/juryaissist-figma-$(date +%Y%m%d)/
cp *.md ~/backups/juryaissist-figma-$(date +%Y%m%d)/
```

## 🎯 Raccourcis utiles

```bash
# Alias à ajouter dans ~/.bashrc ou ~/.zshrc
alias jury-figma="cd ~/Documents/Projets/JuryAIssist && source venv/bin/activate && python launch_figma_ui.py"
alias jury-old="cd ~/Documents/Projets/JuryAIssist && source venv/bin/activate && python -m src.main"
alias jury-test="cd ~/Documents/Projets/JuryAIssist && source venv/bin/activate && python test_figma_ui.py"

# Puis recharger le shell
source ~/.bashrc  # ou ~/.zshrc

# Utiliser
jury-figma  # Lance l'interface Figma
jury-old    # Lance l'ancienne interface
jury-test   # Lance les tests
```

---

**Aide** : `cat QUICK_START.md` pour le guide complet
