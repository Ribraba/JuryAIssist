#!/bin/bash

# ============================================================================
# Script de Setup - Environnement de Développement
# Projet: Logiciel de Transcription Audio Juridique
# ============================================================================

set -e  # Arrêt si erreur

echo "🚀 Configuration de l'environnement de développement..."

# Couleurs pour output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ============================================================================
# 1. Vérification de Python
# ============================================================================

echo -e "\n${BLUE}[1/6] Vérification de Python...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    echo "Installez Python 3.9+ depuis https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} détecté${NC}"

# Vérification version minimale (3.9+)
REQUIRED_VERSION="3.9"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null; then
    echo -e "${RED}❌ Python 3.9+ requis (version actuelle: ${PYTHON_VERSION})${NC}"
    exit 1
fi

# ============================================================================
# 2. Installation des dépendances système (macOS)
# ============================================================================

echo -e "\n${BLUE}[2/6] Installation des dépendances système...${NC}"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Détection de macOS"
    
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}❌ Homebrew n'est pas installé${NC}"
        echo "Installez Homebrew : /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    echo "Installation de hidapi..."
    brew install hidapi || echo "hidapi déjà installé"
    
    echo "Installation de VLC (si nécessaire)..."
    brew install --cask vlc || echo "VLC déjà installé"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Détection de Linux"
    
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y libhidapi-dev vlc libvlc-dev python3-venv
    elif command -v dnf &> /dev/null; then
        # Fedora
        sudo dnf install -y hidapi-devel vlc vlc-devel python3-virtualenv
    else
        echo -e "${RED}⚠️  Distribution Linux non reconnue${NC}"
        echo "Installez manuellement: hidapi, vlc, python3-venv"
    fi
else
    echo -e "${RED}⚠️  OS non supporté: ${OSTYPE}${NC}"
fi

echo -e "${GREEN}✓ Dépendances système installées${NC}"

# ============================================================================
# 3. Création de l'environnement virtuel
# ============================================================================

echo -e "\n${BLUE}[3/6] Création de l'environnement virtuel...${NC}"

if [ -d "venv" ]; then
    echo -e "${RED}⚠️  Le dossier 'venv' existe déjà${NC}"
    read -p "Voulez-vous le recréer? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
    else
        echo "Conservation de l'environnement existant"
    fi
fi

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Environnement virtuel créé${NC}"
else
    echo -e "${GREEN}✓ Environnement virtuel existant${NC}"
fi

# ============================================================================
# 4. Activation et mise à jour de pip
# ============================================================================

echo -e "\n${BLUE}[4/6] Activation de l'environnement...${NC}"

source venv/bin/activate

echo -e "${GREEN}✓ Environnement activé${NC}"

echo "Mise à jour de pip..."
pip install --upgrade pip setuptools wheel

# ============================================================================
# 5. Installation des dépendances Python
# ============================================================================

echo -e "\n${BLUE}[5/6] Installation des dépendances Python...${NC}"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Dépendances installées depuis requirements.txt${NC}"
else
    echo -e "${RED}⚠️  requirements.txt non trouvé${NC}"
    echo "Installation des dépendances de base..."
    
    # Dépendances essentielles
    pip install \
        PyQt5 \
        python-vlc \
        hidapi \
        pytest \
        pytest-qt \
        pytest-cov \
        black \
        pylint \
        mypy
    
    echo -e "${GREEN}✓ Dépendances de base installées${NC}"
fi

# ============================================================================
# 6. Vérification de l'installation
# ============================================================================

echo -e "\n${BLUE}[6/6] Vérification de l'installation...${NC}"

# Test imports critiques
python3 << EOF
import sys
errors = []

try:
    import PyQt5
    print("✓ PyQt5")
except ImportError as e:
    errors.append(f"✗ PyQt5: {e}")

try:
    import vlc
    print("✓ python-vlc")
except ImportError as e:
    errors.append(f"✗ python-vlc: {e}")

try:
    import hid
    print("✓ hidapi")
except ImportError as e:
    errors.append(f"✗ hidapi: {e}")

try:
    import pytest
    print("✓ pytest")
except ImportError as e:
    errors.append(f"✗ pytest: {e}")

if errors:
    print("\n⚠️  Erreurs détectées:")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
else:
    print("\n✅ Tous les modules importés avec succès!")
EOF

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Configuration terminée avec succès!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "\nPour activer l'environnement:"
    echo -e "  ${BLUE}source venv/bin/activate${NC}"
    echo -e "\nPour désactiver:"
    echo -e "  ${BLUE}deactivate${NC}"
else
    echo -e "\n${RED}❌ Des erreurs se sont produites${NC}"
    exit 1
fi
