""" Requirements

Script python permettant de vérifier si votre environnement virtuel
contient les modules nécessaires à l'execution du projet.
"""

import importlib
import subprocess
import sys

# Modules à vérifier/installer
required_modules = [
    "requests",
    "bs4", 
    "spacy",
    "matplotlib",
    "seaborn",
    "torch",
    "datasets",
    "transformers",
    "sklearn", 
    "tqdm",
    "pandas",
    "numpy"
]

pip_names = {
    "bs4": "beautifulsoup4",
    "sklearn": "scikit-learn"
}

def install_package(package):
    """
    Fonction d'installation des modules manquants
    """
    print(f"Installation de {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_modules():
    """
    Fonction de vérification des modules nécessaires au projet
    """
    print("Vérification des dépendances...\n")
    for module in required_modules:
        pip_name = pip_names.get(module, module)
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} est manquant.")
            install = input(f"Souhaites-tu installer '{pip_name}' ? (o/n) : ").strip().lower()
            if install == "o":
                install_package(pip_name)

if __name__ == "__main__":
    check_modules()

