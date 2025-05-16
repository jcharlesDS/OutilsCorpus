""" Script de crawling

Script simple de crawling python.
"""

import requests
from bs4 import BeautifulSoup
import os

def crawl_urls(url, output_path='liens_extraits.txt'):
    """
    Extraits tous les liens d'une page web et les enregistre dans un fichier texte.

    Paramètres :
    - url (str) : L'URL de la page web à crawler.
    - output_file (str) : Le nom du fichier où sauvegarder les liens extraits.

    Retourne :
    - list[str] : Une liste des URLs extraites.
    """
    # Gestion des chemins
    if os.path.isdir(output_path) or output_path.endswith(os.sep):
        output_path = os.path.join(output_path, 'liens.txt')

    # Création du dossier de sortie s'il n'existe pas
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Requête GET à l'url cible
        response = requests.get(url)

        # Vérifie le code 200
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []

            # Parcours pour récupérer les attributs href
            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    links.append(href)

            # Ecriture dans le fichier texte
            with open(output_path, 'w', encoding='utf-8') as f:
                for l in links:
                    f.write(f"{l}\n")
            
            print(f"{len(links)} liens extraits et enregistrés dans '{output_path}'.")
            return links  
        else:
            print(f"Erreur HTTP : {response.status_code}")
            return []
        
    except requests.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return []

# Fonction principale
if __name__ == "__main__":
    url_cible = input("Entrez l'URL à crawler : ").strip()
    chemin_sortie = input("Entrez le chemin du fichier ou dossier de sortie : ").strip()
    crawl_urls(url_cible, chemin_sortie)