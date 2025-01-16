import folium
from folium import plugins
from branca.colormap import LinearColormap
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import streamlit as st
from streamlit.components.v1 import html
from bokeh.plotting import figure
from bokeh.io import output_notebook, show

class AgriculturalMap:
    def __init__(self, data_manager):
        """
        Initialise la carte avec le gestionnaire de données
        """
        self.data_manager = data_manager
        self.map = None
        self.yield_colormap = LinearColormap(
            colors=['red', 'yellow', 'green'],
            vmin=0,
            vmax=12  # Rendement maximum en tonnes/ha
        )

    def create_base_map(self):
        """
        Crée la carte de base avec les couches appropriées
        """
        first_row = self.data_manager.monitoring_cultures.iloc[0]  # Récupérer la première ligne pour centrer la carte
        lat, lon = first_row['latitude'], first_row['longitude']
        
        # Initialiser la carte avec Folium
        self.map = folium.Map(location=[lat, lon], zoom_start=10)
    
    def add_yield_history_layer(self):
        """
        Ajoute une couche visualisant l’historique des rendements
        """
        for _, row in self.data_manager.historique_rendements.iterrows():
            lat, lon = row['latitude'], row['longitude']
            yield_value = row['rendement']  # Colonne contenant le rendement
            
            # Ajouter le marqueur sur la carte avec une couleur en fonction du rendement
            color = self.yield_colormap(yield_value)
            folium.CircleMarker([lat, lon], radius=6, color=color, fill=True, fill_color=color, fill_opacity=0.7).add_to(self.map)

    def add_current_ndvi_layer(self):
        """
        Ajoute une couche de la situation NDVI actuelle
        """
        for _, row in self.data_manager.meteo_detaillee.iterrows():
            lat, lon = row['latitude'], row['longitude']
            ndvi_value = row['NDVI']  # Colonne contenant le NDVI actuel
            
            # Ajouter le marqueur sur la carte avec une couleur en fonction du NDVI
            color = self.ndvi_colormap(ndvi_value)
            folium.CircleMarker([lat, lon], radius=6, color=color, fill=True, fill_color=color, fill_opacity=0.7).add_to(self.map)

    def add_risk_heatmap(self):
        """
        Ajoute une carte de chaleur des zones à risque
        """
        risk_data = self.data_manager.sols[['latitude', 'longitude', 'risque']].dropna()  # Assure-toi d'avoir une colonne 'risque'
        heat_data = [[row['latitude'], row['longitude'], row['risque']] for _, row in risk_data.iterrows()]
        
        folium.plugins.HeatMap(heat_data).add_to(self.map)

    def _calculate_yield_trend(self, history):
        """
        Calcule la tendance des rendements pour une parcelle
        """
        X = np.array(range(len(history))).reshape(-1, 1)  # Indices de l'historique
        y = np.array(history['rendement'])  # Rendement
        model = LinearRegression()
        model.fit(X, y)
        return model.coef_[0]  # Retourner la pente de la régression

    def _create_yield_popup(self, history, mean_yield, trend):
        """
        Crée le contenu HTML du popup pour l’historique des rendements
        """
        crops = self._format_recent_crops(history)
        popup_content = f"""
        <b>Rendement moyen:</b> {mean_yield} t/ha<br>
        <b>Tendance:</b> {'Croissant' if trend > 0 else 'Décroissant'}<br>
        <b>Cultures récentes:</b> {crops}
        """
        return popup_content

    def _format_recent_crops(self, history):
        """
        Formate la liste des cultures récentes pour le popup
        """
        crops = history['crop_name'].unique()
        return ', '.join(crops)

    def _create_ndvi_popup(self, row):
        """
        Crée le contenu HTML du popup pour les données NDVI actuelles
        """
        popup_content = f"""
        <b>NDVI:</b> {row['NDVI']}<br>
        <b>Zone:</b> {row['zone']}
        """
        return popup_content


class IntegratedDashboard:
    def __init__(self, data_manager):
        """
        Crée un tableau de bord intégré combinant
        graphiques Bokeh et carte Folium
        """
        self.data_manager = data_manager
        self.bokeh_dashboard = AgriculturalDashboard(data_manager)
        self.map_view = AgriculturalMap(data_manager)

    def initialize_visualizations(self):
        """
        Initialise toutes les composantes visuelles
        """
        self.map_view.create_base_map()
        self.map_view.add_yield_history_layer()
        self.map_view.add_current_ndvi_layer()
        self.map_view.add_risk_heatmap()

    def create_streamlit_dashboard(self):
        """
        Crée une interface Streamlit intégrant toutes les visualisations
        """
        st.title("Tableau de Bord Agricole Intégré")
        
        # Ajouter les visualisations ici
        st.subheader("Carte Agricole")
        folium_map = self.map_view.map
        
        # Afficher la carte Folium dans Streamlit via HTML
        folium_map_html = folium_map._repr_html_()  # Convertir la carte en HTML
        html(folium_map_html, height=600)  # Intégrer la carte dans Streamlit
        
        st.subheader("Graphiques Bokeh")
        self.bokeh_dashboard.show()  # Afficher les graphiques Bokeh ici

    def update_visualizations(self, parcelle_id):
        """
        Met à jour toutes les visualisations pour une parcelle donnée
        """
        # Logique pour mettre à jour la carte et les graphiques en fonction de la parcelle sélectionnée
        pass

    def setup_interactions(self):
        """Configure les interactions entre les composantes"""
        self.map_view.map.on_click(self.handle_map_hover)  # Lorsque la carte est survolée
        self.bokeh_dashboard.on_selection(self.handle_parcelle_selection)  # Lorsqu'une parcelle est sélectionnée

    def handle_parcelle_selection(self, attr, old, new):
        """Gère la sélection d’une nouvelle parcelle"""
        # Mettre à jour les visualisations en fonction de la parcelle sélectionnée
        pass

    def handle_map_hover(self, feature):
        """Gère le survol d’une parcelle sur la carte"""
        # Mettre en évidence la parcelle sur les graphiques
        pass
