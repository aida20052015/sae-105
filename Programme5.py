import csv
from datetime import datetime
import matplotlib.pyplot as plt
import markdown

# Nom du fichier CSV généré précédemment
csv_file = "evenements.csv"

# Ressource et groupe de TP à rechercher
ressource_cible = "R1.07 TP"
groupe_cible = "RT1-TP B2"

# Tableau pour stocker les résultats
resultats = []

# Vérification si le fichier existe
try:
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')  # Assurez-vous que le séparateur est correct
        for row in reader:
            if len(row) > 3:
                description = row[3]
                groupe = row[5]
                dtstart = row[1]  # Date de début (assumée en deuxième colonne)
                dtend = row[2]  # Date de fin (assumée en troisième colonne)

                # Vérifier si c'est une séance de TP pour le groupe RT1-TP B2
                if ressource_cible in description and groupe_cible in groupe:
                    # Convertir les dates en objets datetime pour calculer la durée
                    date_debut = datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ")
                    date_fin = datetime.strptime(dtend, "%Y%m%dT%H%M%SZ")
                    duree = (date_fin - date_debut).total_seconds() / 3600  # Durée en heures

                    # Ajouter l'entrée au tableau des résultats
                    resultats.append({
                        "Date": date_debut.strftime("%Y-%m-%d %H:%M"),
                        "Durée (h)": round(duree, 2),
                        "Type de séance": "TP",
                    })
except FileNotFoundError:
    print(f"Erreur : Le fichier '{csv_file}' est introuvable. Assurez-vous qu'il est généré.")
    exit()

# Créer un tableau en Markdown pour afficher les séances de TP
markdown_table = "| Date | Durée (h) | Type de séance |\n"
markdown_table += "|------|-----------|----------------|\n"
for res in resultats:
    markdown_table += f"| {res['Date']} | {res['Durée (h)']} | {res['Type de séance']} |\n"

# Créer un dictionnaire pour les séances par mois
seances_par_mois = {"Septembre": 0, "Octobre": 0, "Novembre": 0, "Décembre": 0}
for res in resultats:
    # Extraire le mois à partir de la date
    mois = datetime.strptime(res["Date"], "%Y-%m-%d %H:%M").strftime("%B")
    if mois in seances_par_mois:
        seances_par_mois[mois] += 1

# Vérification que toutes les valeurs de seances_par_mois sont des entiers et non des NaN
for mois, count in seances_par_mois.items():
    if not isinstance(count, int):
        print(f"Attention : '{mois}' a une valeur non entière ({count}). Elle est remplacée par 0.")
        seances_par_mois[mois] = 0

# Préparer les données pour le graphique
sizes = [seances_par_mois[mois] for mois in ["Septembre", "Octobre", "Novembre", "Décembre"]]
labels = ["Septembre", "Octobre", "Novembre", "Décembre"]

# S'il y a des NaN dans sizes, les remplacer par 0 explicitement
sizes = [0 if isinstance(size, float) and size != size else size for size in sizes]

# Vérification avant de passer au graphique
print("Données pour le graphique :")
print(f"Labels : {labels}")
print(f"Sizes : {sizes}")

# Créer un diagramme circulaire
plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title("Répartition des séances de TP par mois")
plt.axis('equal')  # Pour faire un cercle parfait

# Sauvegarder le graphique au format PNG
graph_image_path = "graph_seances_par_mois.png"
plt.savefig(graph_image_path)

# Générer un fichier HTML avec le tableau et le graphique
html_content = f"""
# Tableau des séances de TP pour la ressource {ressource_cible} et le groupe {groupe_cible}

{markdown_table}

# Diagramme circulaire : Répartition des séances de TP par mois

![Répartition des séances de TP](graph_seances_par_mois.png)
"""

# Convertir le Markdown en HTML
html_output = markdown.markdown(html_content)

# Sauvegarder le contenu HTML dans un fichier
output_html_file = "seances_TP_R1.07_et_graphique.html"
with open(output_html_file, "w", encoding="utf-8") as f:
    f.write(html_output)

# Informer l'utilisateur
print(f"Le fichier HTML a été généré sous le nom '{output_html_file}'.")
