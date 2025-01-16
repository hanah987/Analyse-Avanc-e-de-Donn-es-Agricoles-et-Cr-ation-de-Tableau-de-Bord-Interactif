
# Importation des bibliothèques nécessaires
import pandas as pd  # Utilisation de pandas pour la manipulation des données
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar  # Importation des outils Bokeh pour la visualisation
from bokeh.plotting import figure, output_notebook, show  # Fonctionnalités de Bokeh pour créer des graphiques et afficher les résultats
from bokeh.layouts import column  # Permet de disposer les graphiques en colonne
from bokeh.palettes import RdYlBu11 as palette  # Palette de couleurs RdYlBu pour la matrice de stress

# Chargement des données à partir de fichiers CSV
monitoring_data = pd.read_csv("monitoring_cultures.csv")  # Données de surveillance des cultures
sols_data = pd.read_csv("sols.csv")  # Données sur les sols
historique_rendements = pd.read_csv("historique_rendements.csv")  # Historique des rendements

# Vérification de la présence de la colonne 'date' dans les DataFrames et transformation si nécessaire
if 'date' not in monitoring_data.columns:
    print("Colonne 'date' non trouvée dans monitoring_data")
else:
    monitoring_data['date'] = pd.to_datetime(monitoring_data['date'], errors='coerce')  # Conversion de la colonne 'date' en format datetime

if 'date' not in historique_rendements.columns:
    print("Colonne 'date' non trouvée dans historique_rendements, création à partir de l'année")
    historique_rendements['date'] = pd.to_datetime(historique_rendements['annee'], format='%Y')  # Création de la colonne 'date' à partir de 'annee'

# Fusion des données avec 'sols_data' sur la colonne 'parcelle_id'
combined_data = monitoring_data.merge(sols_data, on="parcelle_id", how="inner") if 'parcelle_id' in sols_data.columns else pd.DataFrame()

# Préparation des sources de données pour Bokeh (les sources sont les objets contenant les données pour les graphiques)
hist_source = ColumnDataSource(historique_rendements)  # Source pour les rendements historiques
source = ColumnDataSource(monitoring_data)  # Source pour les données de surveillance
stress_source = ColumnDataSource(combined_data)  # Source pour les données combinées

# Graphique : Historique des rendements
yield_history_plot = figure(
    title="Historique des Rendements par Parcelle",  # Titre du graphique
    x_axis_type="datetime",  # Type de l'axe des x : date
    height=400,  # Hauteur du graphique
    width=800,  # Largeur du graphique
    tools="pan,wheel_zoom,box_zoom,reset",  # Outils pour interagir avec le graphique (zoom, déplacement)
)
# Tracer la courbe des rendements historiques
yield_history_plot.line(source=hist_source, x="date", y="rendement", line_width=2, color="blue", legend_label="Rendement")
# Ajouter un outil de survol avec des informations sur la date et le rendement
yield_history_plot.add_tools(HoverTool(tooltips=[("Date", "@date{%F}"), ("Rendement", "@rendement")], formatters={"@date": "datetime"}))
yield_history_plot.legend.location = "top_left"  # Position de la légende

# Graphique : Évolution du NDVI avec les seuils
ndvi_plot = figure(
    title="Évolution du NDVI et Seuils Historiques",
    x_axis_type="datetime",
    height=400,
    width=800,
    tools="pan,wheel_zoom,box_zoom,reset",
)
# Tracer la courbe du NDVI
ndvi_plot.line(source=source, x="date", y="ndvi", line_width=2, color="green", legend_label="NDVI")
# Tracer les seuils bas et hauts
ndvi_plot.line(x="date", y="lower_threshold", source=source, color="red", line_dash="dashed", legend_label="Seuil Bas")
ndvi_plot.line(x="date", y="upper_threshold", source=source, color="orange", line_dash="dashed", legend_label="Seuil Haut")
# Ajouter un outil de survol pour afficher le NDVI et la date
ndvi_plot.add_tools(HoverTool(tooltips=[("Date", "@date{%F}"), ("NDVI", "@ndvi")], formatters={"@date": "datetime"}))
ndvi_plot.legend.location = "top_left"

# Matrice de stress hydrique et conditions météorologiques
mapper = LinearColorMapper(palette=palette, low=0, high=1)  # Mappage des couleurs en fonction de la valeur
stress_matrix_plot = figure(
    title="Matrice de Stress",
    x_axis_label="Stress Hydrique",
    y_axis_label="Conditions Météo",
    tools="hover",
    tooltips=[("Stress", "@value")],  # Affichage des informations de stress survolées
    height=400,
    width=400,
)
# Tracer la matrice de stress avec un rectangle pour chaque combinaison de stress et condition météorologique
stress_matrix_plot.rect(
    x="stress_hydrique",
    y="meteo_condition",
    width=0.1,
    height=0.1,
    source=stress_source,
    fill_color={"field": "value", "transform": mapper},  # Remplissage en fonction de la valeur
    line_color=None,
)
# Ajouter une barre de couleurs pour la matrice
color_bar = ColorBar(color_mapper=mapper, location=(0, 0))
stress_matrix_plot.add_layout(color_bar, "right")

# Graphique : Prédiction des rendements
yield_prediction_plot = figure(
    title="Prédiction des Rendements",
    x_axis_type="datetime",
    height=400,
    width=800,
    tools="pan,wheel_zoom,box_zoom,reset",
)
# Tracer les rendements prédits
yield_prediction_plot.line(source=source, x="date", y="predicted_yield", line_width=2, color="purple", legend_label="Prédiction")
# Ajouter un outil de survol pour les prédictions
yield_prediction_plot.add_tools(HoverTool(tooltips=[("Date", "@date{%F}"), ("Prédiction", "@predicted_yield")], formatters={"@date": "datetime"}))
yield_prediction_plot.legend.location = "top_left"

# Mise en page du tableau de bord : Les graphiques sont affichés dans une colonne
layout = column(
    yield_history_plot,
    ndvi_plot,
    stress_matrix_plot,
    yield_prediction_plot
)

# Affichage
output_notebook()
show(layout)  # Affiche le tableau de bord avec tous les graphiques