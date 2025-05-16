""" Prétraitement multi-label

Script permettant de lire les fichiers textes d'un dossier,
extrait les thèmes des paroles (inscrites sur la seconde ligne des fichiers),
récupère le texte également, crée un encodage multi-hot des thèmes et
enregistre le résultat en JSON.
"""

import os
import json
import re
import tkinter as tk
from tkinter import filedialog

def extraire_themes(ligne):
    """Extrait les thèmes entre crochets [ ] sous forme de liste
    """
    match = re.search(r'\[(.*?)\]', ligne)
    if match:
        return [t.strip().lower() for t in match.group(1).split(',')]
    return []

def preprocess_folder(folder_path, output_json_path):
    """ Processus de prétraitement des fichiers pour une classification multi-label
    """
    all_labels = set()
    data = []

    print("Analyse des fichiers...")
    # Récupérer tous les labels (les thèmes des paroles)
    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:
                continue

            themes = extraire_themes(lines[1])
            all_labels.update(themes)

    all_labels = sorted(all_labels)
    print(f"{len(all_labels)} thèmes trouvés : {all_labels}")

    # Construire les lignes du dataset
    for filename in os.listdir(folder_path):
        if not filename.endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, filename)
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 3:
                continue

            themes = extraire_themes(lines[1])
            texte = ''.join(lines[2:]).strip()

            if not texte:
                continue

            # Création du dictionnaire contenant les paroles et les labels (thèmes)
            song_data = {
                "titre": lines[0].strip(),
                "themes": themes,
                "paroles": texte
            }

            data.append(song_data)

    # Création du fichier JSON
    with open(output_json_path,'w', encoding='utf-8') as out_json:
        json.dump(data, out_json, ensure_ascii=False, indent=4)

    print(f"Fichier JSON écrit à : {output_json_path}")
    print(f"Total exemples : {len(data)}")

# Fonction principale
if __name__ == "__main__":
    
    root = tk.Tk()
    root.withdraw()

    dossier_entree = filedialog.askdirectory(title="Choisissez le dossier contenant les fichiers .txt")
    if not dossier_entree:
        print("Aucun dossier sélectionné.")
        exit()

    chemin_sortie = filedialog.asksaveasfilename(
        title="Choisissez le nom du fichier de sortie JSON",
        defaultextension=".json",
        filetypes=[("Fichier JSON", "*.json")]
    )

    if not chemin_sortie:
        print("Aucun fichier de sortie sélectionné.")
        exit()

    preprocess_folder(dossier_entree, chemin_sortie)
