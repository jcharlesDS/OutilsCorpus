""" Script d'analyses statistiques

Script permettant d'analyser les fichiers textes,
créer un rapport contenant les analyses textuels (nombres de mots,
mots uniques, richesse lexicale, les catégories grammaticales les plus représentés)
et des visualisations des fréquences de mots et des catégories grammaticales.
"""

import os
import string
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from tkinter import filedialog, Tk

# Chargement du modèle spaCy (français)
nlp = spacy.load("fr_core_news_sm")

def charger_fichiers():
    """
    Fonction ouvrant une boîte de dialogue pour sélectionner des fichiers texte.
    """
    Tk().withdraw()
    fichiers = filedialog.askopenfilenames(title="Choisissez les fichiers .txt", filetypes=[("Fichiers texte", "*.txt")])
    return fichiers

def choisir_dossier_sortie():
    """
    Ouvre une boite de dialogue pour choisir le dossier où enregistrer les résultats de l'analyse.
    """
    Tk().withdraw()
    dossier = filedialog.askdirectory(title="Choisir le dossier de sortie")
    return dossier

def nettoyer_texte(texte):
    """
    Fonction de nettoyage du texte.
    """
    return texte.lower().translate(str.maketrans("", "", string.punctuation))

def analyser_texte(texte):
    """
    Fonction d'analyse de texte (nombre de mots, mots uniques, catégories grammaticales)
    """
    doc = nlp(texte)
    mots = [token.text for token in doc if token.is_alpha]
    uniques = set(mots)
    pos_tags = [token.pos_ for token in doc if token.is_alpha]
    return mots, uniques, len(mots), pos_tags

def afficher_visualisations(fichier, freqs, pos_counter, dossier_sortie):
    """
    Génère les visualisations des mots fréquents et des catégories grammaticales.
    """
    base = os.path.splitext(os.path.basename(fichier))[0]

    # Graphique des mots fréquents
    plt.figure(figsize=(10, 6))
    mots_communs = freqs.most_common(15)
    mots, comptes = zip(*mots_communs)
    sns.barplot(x=list(comptes), hue=list(mots), palette="viridis", legend=False)
    plt.title(f"15 mots les plus fréquents : {base}")
    plt.xlabel("Fréquence")
    plt.tight_layout()
    plt.savefig(os.path.join(dossier_sortie, f"{base}_frequence_mots.png"))
    plt.close()

    # Graphique des catégories grammaticales
    plt.figure(figsize=(6, 6))
    labels, valeurs = zip(*pos_counter.most_common(6))
    plt.pie(valeurs, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title(f"Catégories grammaticales principales : {base}")
    plt.tight_layout()
    plt.savefig(os.path.join(dossier_sortie, f"{base}_repartition_pos.png"))
    plt.close()

def générer_rapport(fichier, total, uniques, freqs, pos_counter, dossier_sortie):
    """
    Fonction créant un rapport texte résumant l'analyse.
    """
    base = os.path.splitext(os.path.basename(fichier))[0]
    ratio_lexical = len(uniques) / total if total else 0

    rapport = [
        f"Rapport statistique pour : {base}",
        "-" * 40,
        f"Nombre total de mots       : {total}",
        f"Nombre de mots uniques     : {len(uniques)}",
        f"Richesse lexicale : {ratio_lexical:.2f}",
        "",
        "Mots les plus fréquents :"
    ]
    for mot, count in freqs.most_common(10):
        rapport.append(f"  {mot} : {count}")

    rapport.append("\nParties du discours (POS) les plus fréquentes :")
    for pos, count in pos_counter.most_common(10):
        rapport.append(f"  {pos} : {count}")

    rapport_path = os.path.join(dossier_sortie, f"{base}_rapport.txt")
    with open(rapport_path, "w", encoding="utf-8") as f:
        f.write("\n".join(rapport))
    print(f"Rapport sauvegardé : {base}_rapport.txt")

def main():
    """
    Fonction principale du script
    """
    fichiers = charger_fichiers()
    if not fichiers:
        print("Aucun fichier sélectionné.")
        return
    
    dossier_sortie = choisir_dossier_sortie()
    if not dossier_sortie:
        print("Aucun dossier de sortie séléctionné.")
        return

    for fichier in fichiers:
        print(f"\nAnalyse de : {fichier}")
        with open(fichier, "r", encoding="utf-8") as f:
            texte = nettoyer_texte(f.read())

        mots, uniques, total, pos_tags = analyser_texte(texte)
        freqs = Counter(mots)
        pos_counter = Counter(pos_tags)

        générer_rapport(fichier, total, uniques, freqs, pos_counter, dossier_sortie)
        afficher_visualisations(fichier, freqs, pos_counter, dossier_sortie)

if __name__ == "__main__":
    main()
