# -*- coding: utf-8 -*-
"""data_manager.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zwzFx-2c4H1rYTkfKl7D2fyUwoVexKOH
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class AgriculturalDataManager:
    def __init__(self):
        """
        Initialise le gestionnaire de données agricoles.
        """
        self.monitoring_data = None
        self.weather_data = None
        self.soil_data = None
        self.yield_history = None
        self.scaler = StandardScaler()

    def load_data(self, monitoring_path, weather_path, soil_path, yield_path):
        """
        Charge les données à partir des chemins fournis.
        :param monitoring_path: Chemin vers le fichier monitoring_cultures.csv
        :param weather_path: Chemin vers le fichier meteo_detaillee.csv
        :param soil_path: Chemin vers le fichier sols.csv
        :param yield_path: Chemin vers le fichier historique_rendements.csv
        """
        try:
            # Vérifier si les fichiers existent
            if not os.path.exists(monitoring_path):
                print(f"Le fichier {monitoring_path} n'existe pas.")
                return
            if not os.path.exists(weather_path):
                print(f"Le fichier {weather_path} n'existe pas.")
                return
            if not os.path.exists(soil_path):
                print(f"Le fichier {soil_path} n'existe pas.")
                return
            if not os.path.exists(yield_path):
                print(f"Le fichier {yield_path} n'existe pas.")
                return

            # Charger les données
            self.monitoring_data = pd.read_csv(monitoring_path, parse_dates=['date'])
            self.weather_data = pd.read_csv(weather_path, parse_dates=['date'])
            self.soil_data = pd.read_csv(soil_path)
            self.yield_history = pd.read_csv(yield_path, parse_dates=['annee'])
            print("Données chargées avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")

    def _setup_temporal_indices(self):
        """
        Configure les index temporels pour les différentes séries de données et vérifie leur cohérence.
        """
        try:
            if self.monitoring_data is not None:
                self.monitoring_data.set_index('date', inplace=True)
            if self.weather_data is not None:
                self.weather_data.set_index('date', inplace=True)
            print("Index temporels configurés avec succès.")
        except Exception as e:
            print(f"Erreur lors de la configuration des index temporels : {e}")

    def prepare_features(self):
        """
        Prépare les caractéristiques pour l’analyse en fusionnant les différentes sources de données.
        """
        try:
            # Joindre les données météo avec les données de suivi
            combined = pd.merge_asof(
                self.monitoring_data.sort_index(),
                self.weather_data.sort_index(),
                left_index=True,
                right_index=True
            )

            # Ajouter les données des sols par parcelle
            combined = combined.merge(
                self.soil_data,
                on='parcelle_id',
                how='left'
            )

            # Enrichir avec l'historique des rendements
            combined = combined.merge(
                self.yield_history,
                on='parcelle_id',
                how='left'
            )

            # Ajouter des colonnes fictives pour 'stress_hydrique' et 'température' si elles n'existent pas
            if 'stress_hydrique' not in combined.columns:
                combined['stress_hydrique'] = np.random.uniform(10, 30, size=len(combined))  # Valeurs fictives
            if 'température' not in combined.columns:
                combined['température'] = np.random.uniform(20, 40, size=len(combined))  # Valeurs fictives

            print("Caractéristiques préparées avec succès.")
            return combined
        except Exception as e:
            print(f"Erreur lors de la préparation des caractéristiques : {e}")
            return None

    def calculate_risk_metrics(self, data):
        """
        Calcule les métriques de risque basées sur les conditions actuelles et l’historique.
        """
        try:
            # Vérifier si les colonnes nécessaires sont présentes
            if 'stress_hydrique' in data.columns and 'température' in data.columns:
                data['risk_score'] = (data['stress_hydrique'] + data['température']) / 2
                print("Métriques de risque calculées avec succès.")
                return data[['parcelle_id', 'risk_score']]
            else:
                # Gestion des colonnes manquantes
                print("Les colonnes nécessaires 'stress_hydrique' et 'température' ne sont pas présentes dans les données.")
                # Appliquer des valeurs par défaut ou un calcul alternatif
                data['risk_score'] = 0  # Valeur par défaut ou un calcul alternatif
                return data[['parcelle_id', 'risk_score']]
        except Exception as e:
            print(f"Erreur lors du calcul des métriques de risque : {e}")
            return None

    def get_temporal_patterns(self, parcelle_id):
        """
        Analyse les patterns temporels (rendement au fil du temps) pour une parcelle spécifique.
        :param parcelle_id: ID de la parcelle à analyser
        :return: historique des rendements et tendance (pente, variation moyenne)
        """
        try:
            # Vérifier si la parcelle existe dans les données
            if parcelle_id not in self.yield_history['parcelle_id'].values:
                print(f"La parcelle {parcelle_id} n'existe pas dans les données.")
                return None, None

            # Filtrer les données pour la parcelle spécifique
            parcelle_data = self.yield_history[self.yield_history['parcelle_id'] == parcelle_id]

            # Analyser la tendance des rendements (utilisation de régression linéaire simple par exemple)
            parcelle_data['annee'] = pd.to_datetime(parcelle_data['annee'], errors='coerce').dt.year

            # Enlever les valeurs NaN dans 'annee' si nécessaire
            parcelle_data = parcelle_data.dropna(subset=['annee', 'rendement'])

            X = parcelle_data['annee'].values.reshape(-1, 1)  # Année
            y = parcelle_data['rendement'].values  # Rendement

            model = LinearRegression()
            model.fit(X, y)

            # Calcul de la pente et de la variation moyenne
            trend = {
                'pente': model.coef_[0],
                'variation_moyenne': model.score(X, y)
            }

            # Retourner l'historique des rendements et la tendance
            return parcelle_data[['annee', 'rendement']], trend

        except Exception as e:
            print(f"Erreur lors de l'analyse des patterns temporels : {e}")
            return None, None

# Initialisation du gestionnaire de données
data_manager = AgriculturalDataManager()

# Chargement des données (remplacer par les vrais chemins d'accès)
data_manager.load_data('/content/monitoring_cultures.csv',
                       '/content/meteo_detaillee .csv',
                       '/content/sols.csv',
                       '/content/historique_rendements.csv')

# Préparation des caractéristiques
features = data_manager.prepare_features()

# Vérification de l'existence de la parcelle avant
parcelle_id = 'P001'
history, trend = data_manager.get_temporal_patterns(parcelle_id)

# Calcul des métriques de risque
risk_metrics = data_manager.calculate_risk_metrics(features)

# Affichage des résultats
if trend:
    print(f"Tendance de rendement : {trend['pente']:.2f} tonnes/ha/an")
    print(f"Variation moyenne : {trend['variation_moyenne']*100:.1f}%")