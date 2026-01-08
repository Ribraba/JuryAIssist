# Guide des Branches Git - JuryAIssist

## Situation actuelle

Vous avez maintenant **2 branches** dans votre projet:

```
main                    ← Interface PyQt5 (ancienne)
  |
  └─ feature/flet-ui    ← Interface Flet (nouvelle)
```

## Qu'est-ce qu'une branche Git?

Une branche est comme une **copie parallèle** de votre projet. Elle permet de travailler sur de nouvelles fonctionnalités sans modifier le code principal.

### Avantages

- Tester de nouvelles idées sans risque
- Garder l'ancienne version fonctionnelle
- Faciliter le développement collaboratif
- Revenir en arrière facilement

## Commandes essentielles

### Voir toutes les branches

```bash
git branch
```

Résultat:
```
  main
* feature/flet-ui    ← Vous êtes ici (étoile)
```

### Basculer entre les branches

```bash
# Aller sur la branche principale (PyQt5)
git checkout main

# Aller sur la branche Flet (nouvelle interface)
git checkout feature/flet-ui
```

### Voir quelle branche est active

```bash
git branch
```

La branche avec `*` est celle où vous êtes actuellement.

### Voir l'historique des commits

```bash
# Historique de la branche actuelle
git log --oneline

# Historique graphique de toutes les branches
git log --oneline --graph --all
```

### Comparer les branches

```bash
# Voir les différences
git diff main feature/flet-ui

# Voir seulement les fichiers modifiés
git diff --name-only main feature/flet-ui

# Statistiques des changements
git diff --stat main feature/flet-ui
```

## Workflows pratiques

### Scénario 1: Tester la nouvelle interface Flet

```bash
# 1. Aller sur la branche Flet
git checkout feature/flet-ui

# 2. Vérifier que vous êtes sur la bonne branche
git branch
# → devrait montrer * feature/flet-ui

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python -m src.main
```

### Scénario 2: Revenir à l'ancienne interface PyQt5

```bash
# 1. Aller sur main
git checkout main

# 2. Réinstaller les dépendances PyQt5
pip install -r requirements.txt

# 3. Lancer l'application
python -m src.main
```

### Scénario 3: Développer une nouvelle fonctionnalité

```bash
# 1. Partir de la branche Flet
git checkout feature/flet-ui

# 2. Créer une nouvelle branche pour votre feature
git checkout -b feature/ma-nouvelle-fonctionnalite

# 3. Faire vos modifications
# ... coder ...

# 4. Commiter
git add .
git commit -m "feat: ajout de ma nouvelle fonctionnalité"

# 5. Revenir sur Flet et fusionner si tout fonctionne
git checkout feature/flet-ui
git merge feature/ma-nouvelle-fonctionnalite
```

### Scénario 4: Adopter définitivement Flet

Si après tests, vous voulez utiliser Flet comme interface principale:

```bash
# 1. Aller sur main
git checkout main

# 2. Fusionner Flet dans main
git merge feature/flet-ui

# 3. Optionnel: supprimer la branche Flet
git branch -d feature/flet-ui
```

### Scénario 5: Garder les deux interfaces

Vous pouvez garder les deux branches indéfiniment:

```bash
# Pour PyQt5
git checkout main
python -m src.main

# Pour Flet
git checkout feature/flet-ui
python -m src.main
```

## Résolution de problèmes

### Erreur: "Your local changes would be overwritten"

Cela signifie que vous avez des modifications non commitées.

**Solution 1**: Commiter vos changements
```bash
git add .
git commit -m "feat: mes changements"
git checkout autre-branche
```

**Solution 2**: Sauvegarder temporairement (stash)
```bash
git stash
git checkout autre-branche
# Plus tard, pour récupérer:
git stash pop
```

**Solution 3**: Abandonner les changements (ATTENTION: perte de données!)
```bash
git checkout -- .
git checkout autre-branche
```

### Erreur: "Branch already exists"

La branche existe déjà.

```bash
# Pour basculer sur une branche existante:
git checkout nom-branche

# Pour créer une nouvelle branche avec un autre nom:
git checkout -b nouveau-nom-branche
```

### Voir les différences avant de basculer

```bash
# Voir ce qui changerait
git diff nom-autre-branche
```

## Commandes avancées

### Sauvegarder temporairement son travail

```bash
# Sauvegarder
git stash

# Voir la liste des stash
git stash list

# Récupérer le dernier stash
git stash pop

# Récupérer un stash spécifique
git stash pop stash@{0}
```

### Créer une branche depuis un commit spécifique

```bash
# Voir l'historique
git log --oneline

# Créer une branche depuis un commit
git checkout -b nouvelle-branche abc1234
```

### Supprimer une branche

```bash
# Supprimer une branche locale (seulement si fusionnée)
git branch -d nom-branche

# Forcer la suppression (même si non fusionnée)
git branch -D nom-branche
```

## Bonnes pratiques

### Nommage des branches

- `main`: Branche principale stable
- `feature/nom`: Nouvelle fonctionnalité
- `fix/nom`: Correction de bug
- `refactor/nom`: Refactoring de code
- `experiment/nom`: Expérimentation

### Commits réguliers

Faire des petits commits fréquents plutôt qu'un gros commit:

```bash
# Mauvais (trop gros)
git add .
git commit -m "Ajout de plein de trucs"

# Bon (commits atomiques)
git add src/gui_flet/components/sidebar.py
git commit -m "feat: add sidebar component"

git add src/gui_flet/components/audio_player.py
git commit -m "feat: add audio player component"
```

### Messages de commit clairs

Format recommandé:
```
type: description courte

Description détaillée (optionnelle)
```

Types:
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `refactor`: Refactoring
- `docs`: Documentation
- `test`: Tests
- `chore`: Maintenance

Exemples:
```bash
git commit -m "feat: add dark mode support"
git commit -m "fix: audio player not updating position"
git commit -m "refactor: simplify sidebar component"
git commit -m "docs: update README with Flet instructions"
```

## Visualisation

### État actuel de vos branches

```
main (PyQt5)
├── src/gui/                  ← Ancienne interface PyQt5
├── requirements.txt          ← PyQt5>=5.15.0
└── src/main.py              ← Lance PyQt5

feature/flet-ui (Flet)
├── src/gui_flet/            ← Nouvelle interface Flet
├── requirements.txt          ← flet>=0.80.0
└── src/main.py              ← Lance Flet
```

### Historique des commits

```
main:      A──B──C──D
                     \
feature/flet-ui:      E──F  ← Vous êtes ici

A: Initial commit
B: Ajout audio
C: Ajout transcription
D: Ajout PyQt5 GUI
E: Remove PyQt5, add Flet
F: Complete Flet UI
```

## Aide-mémoire rapide

| Commande | Description |
|----------|-------------|
| `git branch` | Voir les branches |
| `git checkout nom` | Changer de branche |
| `git checkout -b nom` | Créer et changer de branche |
| `git status` | Voir l'état des fichiers |
| `git diff` | Voir les modifications |
| `git log --oneline` | Voir l'historique |
| `git merge nom` | Fusionner une branche |
| `git stash` | Sauvegarder temporairement |

## Questions?

### Quelle branche utiliser pour développer?

- **Nouvelles fonctionnalités Flet**: Partir de `feature/flet-ui`
- **Corrections PyQt5**: Partir de `main`
- **Expérimentations**: Créer une nouvelle branche

### Comment synchroniser avec GitHub?

```bash
# Envoyer vos branches sur GitHub
git push origin main
git push origin feature/flet-ui

# Récupérer les modifications depuis GitHub
git pull origin main
git pull origin feature/flet-ui
```

### Comment partager une branche?

```bash
# Envoyer la branche
git push origin feature/flet-ui

# Quelqu'un d'autre peut la récupérer avec:
git fetch origin
git checkout feature/flet-ui
```

---

**Conseil**: Ne vous inquiétez pas, Git garde tout. Vous pouvez toujours revenir en arrière!
