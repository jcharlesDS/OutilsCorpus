""" Scrapper de paroles (lyrics)

Ce script permet à l'utilisateur, d'ajouter des URLs de paroles provenant du site Genius.com,
de les récupérer, les nettoyer, les enregistrer dans des fichiers .txt portant le nom des musiques.
Il vous demandera un dossier de sortie pour les fichiers textes récupérés.

Ce script utilise deux modules qui doit être installer par vous-mêmes dans votre environnement Python :

- Requests (pip install requests)
- BeautifulSoup (pip install beautifulsoup4)
"""


import requests
from bs4 import BeautifulSoup
import time
import random
import os
import re
from tkinter import filedialog, Tk

def choisir_dossier_sortie():
    """
    Fonction créant une boite de dialogue permettant à l'utilisateur
    de choisir le dossier dans lequel les paroles seront sauvegardées.
    """
    root = Tk()
    root.withdraw()  # Affiche uniquement la boite de dialogue (et pas la fenêtre d'application)
    dossier = filedialog.askdirectory(title="Choisir le dossier de sortie")
    return dossier if dossier else "paroles"  # Dossier par défaut si aucune réponse

def nettoyer_texte(texte):
    """
    Nettoie le texte en supprimant les crochets [ ... ] et les lignes vides.

    Paramètres :
    - texte (str) : Texte brut extrait de la page.

    Retourne :
    - texte nettoyé (str)
    """
    # Supprimer les caractères invisibles
    texte = texte.replace('\u200b', '')

    # Supprimer tout ce qui est entre crochets (ex: [Refrain], [Couplet 1], etc.)
    texte = re.sub(r"\[.*?\]", "", texte)

    # Supprimer les lignes vides ou contenant uniquement des espaces
    lignes = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]
    return "\n".join(lignes)

def scrap_genius_lyrics(url, output_dir):
    """
    Scrape les paroles d'une chanson depuis une URL du site Genius.

    Paramètres :
    - url (str) : Lien vers la page Genius contenant les paroles.
    - output_dir (str) : Dossier dans lequel enregistrer le fichier texte.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ParoleScraper/1.0)"
    }

    try:
        # Requête HTTP pour récupérer le contenu de la page
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Erreur pour {url} : {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Supprimer les éléments superflus capturés par le scrap
        for excluded in soup.find_all(attrs={"data-exclude-from-selection": "true"}):
            excluded.decompose()

        # Extraire le titre de la chanson
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Titre inconnu"
        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)

        # Extraire les paroles
        lyrics_divs = soup.find_all("div", {"data-lyrics-container": "true"})
        lyrics_raw = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)

        # Nettoyer les paroles
        lyrics = nettoyer_texte(lyrics_raw)

        if not lyrics.strip():
            print(f"[!] Aucune parole trouvée pour {url}")
            return

        # Créer le dossier de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)

        # Enregistrer les paroles dans un fichier texte
        filepath = os.path.join(output_dir, f"{safe_title}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{title}\n\n{lyrics}")

        print(f"[✓] Paroles de « {title} » enregistrées dans {filepath}")

    except Exception as e:
        print(f"[!] Erreur lors du traitement de {url} : {e}")

def main():
    """
    Fonction principale : demande le dossier de sortie,
    puis scrape les paroles pour une liste d'URLs.
    """
    print("Sélection du dossier de sortie...")
    dossier = choisir_dossier_sortie()

    # Liste d'URLs à scraper
    urls = [
        "https://genius.com/Hamza-kyky2bondy-lyrics",
        "https://genius.com/Jul-mimi-lyrics",
        "https://genius.com/Gims-ninao-lyrics",
        "https://genius.com/Keblack-melrose-place-lyrics",
        "https://genius.com/Gims-ciel-lyrics",
        "https://genius.com/Keblack-mood-lyrics",
        "https://genius.com/Jul-phenomenal-lyrics",
        "https://genius.com/Werenoi-and-gims-piano-lyrics",
        "https://genius.com/L2b-pelican-lyrics",
        "https://genius.com/Attaching-boy-chambre-04-lyrics"
    ]

    for i, url in enumerate(urls, start=1):
        print(f"\n--- ({i}/{len(urls)}) Scraping : {url}")
        scrap_genius_lyrics(url, dossier)

        # Gestion des pauses pour les requêtes
        if i % 10 == 0:
            print("Pause longue après 10 morceaux...")
            time.sleep(20) # Pour changer le temps d'attente à chaque fois que l'on atteint 10 éléments scrappés
        else:
            delay = random.uniform(3.0, 6.0) # Pour changer la tranche aléatoire de temps entre les requests
            print(f"Pause de {delay:.2f} secondes...\n")
            time.sleep(delay)

if __name__ == "__main__":
    main()
