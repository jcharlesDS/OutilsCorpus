## *Projet - Outil de traitement de corpus*

1 - Quel sujet allez-vous traiter ?
- L'Analyse des paroles de musiques étant dans le Top 10 France (via Spotify)

2 - Quel type de tâche allez-vous réaliser ?
- Une analyse statistique et textuelle.

3 - Quel type de données allez-vous exploiter ?
- Des données textuelles (fichiers textes bruts)

4 - Où allez-vous récupérer vos données ?
- Pour récupérer les paroles de musiques, j'ai utilisé un site spécialisé sur les paroles de musiques populaires (Genius)

5 - Sont-elles libres d'accés ?
- D'après le robots.txt du site, il semblerait que ce soit le cas.

-------------------------------------

## Résumé :

- 10 musiques
- 10 textes (paroles) au format texte brut
- 7 scripts : **requirements.py** (script vérifiant si l'environnement virtuel conitent tout les modules nécessaires au projet), **crawler.py** (simple crawler), **scrap.py** (scrapper dédié au site), **analyse_stat_textuel.py** (analyse statistique et textuelle des données), **pretraitement_texte.py** (prétraitement des textes pour le fine-tuning), **generation_paroles.py** (augmentation des données synthétique), **fine_tuning_et_eval.py** (finetuning et evaluation du modèle)
- Visualisations de l'analyse statistique et textuelle.

--------------------------------------

Processus :

- Crawling
- Scraping
- Analyse statistique et textuelle
- Augmentation des données (génération synthétique)
- Pre-traitement des textes avant fine-tuning
- Fine-tuning & Evaluation (perplexité)

--------------------------------------

**Objectif initial** : Voir s'il était possible de traiter les paroles de musiques, en français. Obtenir les thèmes les plus récurrents des musiques les plus populaires récentes, dans le pays. Enfin, de générer des paroles de musique par l'intérmédiaire d'un modèle Transformer.

**Élément perturbateur** : La grande majorité des musiques du corpus initial (les 10 musiques les plus écoutés en france via Spotify durant ce mois : Mai 2025) sont majoritairement en registre de langue familier (très familier), utilisation du verlan, beaucoup d'emprunts à d'autres langues, des onomatopés, etc...
Cela ne facilitant pas mon analyse.

Deuxième point, les modèles, en tout cas, en français, comme **camembert** ou encore **gpt2-french-small** ne sont pas conçus ni entrainés pour générer des paroles de musiques. Les résultats sont...particuliers. (avant fine-tuning précis)

**Décision** : Abandon de l'analyse de sentiment des paroles. Etant donné que le corpus synthétique et le corpus d'origine sont très particuliers, les données me semblent difficilement exploitable pour des résultats pertinents.


**Mot de la fin** :
Projet intéressant, que j'aimerai approfondir par la suite.