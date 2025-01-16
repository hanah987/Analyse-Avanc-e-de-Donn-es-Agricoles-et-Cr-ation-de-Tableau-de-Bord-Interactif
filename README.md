# Projet Agricole : Surveillance des Cultures et Prédiction des Rendements

Ce projet vise à analyser, surveiller et prédire les rendements agricoles à partir de différentes sources de données, telles que les données météorologiques, les conditions des sols et les rendements passés. Il utilise des techniques de visualisation interactives pour permettre aux utilisateurs de suivre l'évolution des cultures, d'évaluer les conditions des sols et d'analyser les facteurs influençant la production agricole.

## Fonctionnalités
- **Analyse des rendements agricoles** : Visualisation de l'historique des rendements par parcelle.
- **Suivi des conditions climatiques** : Suivi de l'évolution du NDVI (indice de végétation par différence normalisée) et des seuils météorologiques critiques.
- **Évaluation des conditions des sols** : Matrice de stress hydrique en fonction des conditions météorologiques.
- **Prédiction des rendements** : Estimation des rendements agricoles futurs en fonction des données passées et des conditions actuelles.
- **Visualisations interactives** : Tableau de bord interactif pour afficher les résultats sous forme de graphiques et de cartes.

## Installation

1. **Clonez ce dépôt GitHub** :
   ```bash
   git clone https://github.com/votre-nom-utilisateur/projet_agricole.git
   cd projet_agricole


python -m venv env
source env/bin/activate  # Sur Windows : env\Scripts\activate


pip install -r requirements.txt


pandas
bokeh
folium
streamlit
jupyter


python src/dashboard.py


http://localhost:8501


projet_agricole/
│
├── data/                           # Dossier contenant les fichiers de données sources
│   ├── monitoring_cultures.csv     # Données de surveillance des cultures
│   ├── meteo_detaillee.csv         # Données météorologiques détaillées
│   ├── sols.csv                    # Données sur les sols
│   └── historique_rendements.csv   # Historique des rendements agricoles
│
├── src/                            # Dossier contenant les scripts Python
│   ├── data_manager.py             # Script pour la gestion des données
│   ├── dashboard.py                # Code pour créer le tableau de bord interactif
│   ├── map_visualization.py        # Visualisation géographique des données
│   └── report_generator.py         # Génération de rapports automatisés
│
├── notebooks/                      # Dossier contenant les notebooks Jupyter pour les analyses exploratoires
│   └── analyses_exploratoires.ipynb # Notebook pour l'analyse exploratoire des données
│
├── reports/                        # Dossier contenant les rapports générés
│   └── <rapports générés>          # Rapports finaux générés sous format PDF/Word
│
└── templates/                      # Dossier contenant les templates pour la génération de rapports
    └── <templates>                 # Templates et configurations pour les rapports



### Instructions supplémentaires

1. **Assurez-vous de créer un fichier `requirements.txt`** qui inclut toutes les bibliothèques nécessaires pour votre projet, comme mentionné dans le README.
   
   Exemple de contenu de `requirements.txt` :



2. **Téléversez tous les fichiers dans votre dépôt GitHub**, y compris les scripts Python, les fichiers de données (ou un lien vers des fichiers de données externes si nécessaire), et le fichier `README.md`.

3. **Mettre à jour les liens GitHub** : Remplacez `https://github.com/votre-nom-utilisateur/projet_agricole.git` par l'URL réelle de votre dépôt GitHub.

Cela permettra aux autres utilisateurs de comprendre facilement le projet, de l'installer et de le faire fonctionner sur leur propre machine.
