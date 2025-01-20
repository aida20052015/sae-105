import csv
from datetime import datetime

# Nom du fichier CSV généré précédemment
csv_file = "evenements.csv"

# Ressource et groupe de TP à rechercher
ressource_cible = "R1.07 TP"
groupe_cible = "RT1-TP B2"  # Par exemple, le groupe de TP

# Tableau pour stocker les résultats
resultats = []

# Vérification si le fichier existe
try:
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')  # Modifier le délimiteur pour s'adapter au format CSV

        for row in reader:
            # Affichage de chaque ligne pour voir son contenu
            print(row)  # Vous permet de vérifier que les données sont lues correctement

            # Vérifier si les colonnes existent et correspondent aux critères
            if len(row) > 3:  # S'assurer qu'il y a suffisamment de colonnes
                description = row[3]  # La ressource est souvent dans la 4ème colonne
                groupe = row[5]  # Le groupe est souvent dans la 6ème colonne
                
                if ressource_cible in description and groupe_cible in groupe:
                    # Extraire la date de la séance
                    dtstart = row[1]  # Assumer que la date de début est dans la 2ème colonne
                    dtend = row[2]    # Assumer que la date de fin est dans la 3ème colonne

                    # Convertir les dates en objets datetime pour calculer la durée
                    date_debut = datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ")
                    date_fin = datetime.strptime(dtend, "%Y%m%dT%H%M%SZ")
                    duree = (date_fin - date_debut).total_seconds() / 3600  # Durée en heures

                    # Déterminer le type de séance (CM, TD, TP)
                    type_seance = "vide"
                    if "CM" in description:
                        type_seance = "CM"
                    elif "TD" in description:
                        type_seance = "TD"
                    elif "TP" in description:
                        type_seance = "TP"

                    # Ajouter l'entrée au tableau des résultats
                    resultats.append({
                        "Date": date_debut.strftime("%Y-%m-%d %H:%M"),
                        "Durée (h)": round(duree, 2),
                        "Type de séance": type_seance,
                    })

except FileNotFoundError:
    print(f"Erreur : Le fichier '{csv_file}' est introuvable. Assurez-vous qu'il est généré.")
    exit()

# Afficher les résultats
if resultats:
    print(f"Séances pour la ressource '{ressource_cible}' et le groupe '{groupe_cible}' :")
    print(f"{'Date':<20} {'Durée (h)':<10} {'Type de séance':<10}")
    print("-" * 40)
    for res in resultats:
        print(f"{res['Date']:<20} {res['Durée (h)']:<10} {res['Type de séance']:<10}")
else:
    print(f"Aucune séance trouvée pour la ressource '{ressource_cible}' et le groupe '{groupe_cible}'.")

# Facultatif : Sauvegarder dans un fichier CSV
output_file = "seances_R1.07_TP.csv"
with open(output_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Date", "Durée (h)", "Type de séance"])
    writer.writeheader()
    writer.writerows(resultats)
print(f"Les résultats ont été exportés dans le fichier '{output_file}'.")
