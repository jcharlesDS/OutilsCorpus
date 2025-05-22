""" Script d'augmentation des données

Script utilisant GPT2-French Small, permettant de créer des données
de manière synthétique (ici, une tentative
de génération de paroles de musiques fictives) en
fonction des thèmes (prompts) donnés par l'utilisateur.
"""

import os
from transformers import pipeline, set_seed
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

# Paramètres principaux du script

MODEL_NAME = "dbddv01/gpt2-french-small"  # Simple modèle francophone 
TEMPERATURE = 0.9
MAX_LENGTH = 150
SEED = 42

# Initialisation du modèle de génération
set_seed(SEED)
generator = pipeline("text-generation", model=MODEL_NAME)


def generer_paroles(theme, prompt=None, num_variants=3):
    """
    Génère une ou plusieurs variantes de paroles de chanson à partir d'un thème donné et les nettoye.
    """
    if not prompt:
        prompt = f"Paroles de chanson sur le thème : {theme}\n"

    resultats = generator(
        prompt,
        max_length=MAX_LENGTH,
        num_return_sequences=num_variants,
        temperature=TEMPERATURE,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        pad_token_id=generator.tokenizer.eos_token_id
    )

     # Nettoyage des résultats
    paroles_nettoyees = []
    for r in resultats:
        texte = r["generated_text"].strip()
        # Supprime les éléments superflus
        if prompt.strip() in texte:
            texte = texte.replace(prompt.strip(), "").strip()
        paroles_nettoyees.append(texte)

    return paroles_nettoyees

    


def sauvegarder_paroles(dossier_sortie, titre, theme, texte):
    """
    Sauvegarde les paroles générées dans un fichier texte, formaté pour une analyse future.
    """
    safe_title = titre.replace(" ", "_").replace("/", "_")
    chemin = os.path.join(dossier_sortie, f"{safe_title}.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(f"{titre}\n[{theme}]\n{texte}\n")


def augmenter_par_theme(themes, dossier_sortie, chansons_par_theme=5, variantes_par_chanson=3):
    """
    Pour chaque thème fourni, génère plusieurs chansons de manière synthétique et les sauvegarde.
    """
    os.makedirs(dossier_sortie, exist_ok=True)
    for theme in tqdm(themes, desc="Génération par thème"):
        for i in range(chansons_par_theme):
            titre = f"{theme.title()} Synth {i+1}"
            textes = generer_paroles(theme, num_variants=variantes_par_chanson)
            for j, texte in enumerate(textes):
                titre_unique = f"{titre} Variant{j+1}"
                sauvegarder_paroles(dossier_sortie, titre_unique, theme, texte)


if __name__ == "__main__":
    # Choix du dossier de sortie
    root = tk.Tk()
    root.withdraw()
    dossier_sortie = filedialog.askdirectory(title="Choisis le dossier de sortie")
    if not dossier_sortie:
        print("Aucun dossier choisi.")
        exit()

    # Saisie des thèmes/prompts
    themes_utilisateur = input("Entrez les thèmes séparés par des virgules : ")
    themes = [t.strip().lower() for t in themes_utilisateur.split(",") if t.strip()]
    if not themes:
        print("Aucun thème fourni.")
        exit()

    # Nombre de chansons générés par thèmes/prompts
    try:
        nb_chansons = int(input("Combien de chansons par thème voulez-vous générer ? "))
    except ValueError:
        print("Entrée invalide. Valeur par défaut : 3 .")
        nb_chansons = 3

    # Nombre de variantes par chanson
    nb_variantes = input("Combien de variantes voulez-vous générer par chanson ? ")
    variantes_par_chanson = int(nb_variantes)

    # Génération de chansons
    augmenter_par_theme(themes, dossier_sortie, chansons_par_theme=nb_chansons)

    print("Génération terminée.")
