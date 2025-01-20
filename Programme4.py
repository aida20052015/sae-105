import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Nom du fichier CSV généré précédemment
csv_file = "evenements.csv"

# Groupe de TP à rechercher
groupe_cible = "RT1-TP A1"

# Dictionnaire pour compter le nombre de séances par mois
seances_par_mois = {"Septembre": 0, "Octobre": 0, "Novembre": 0, "Décembre": 0}

# Vérification si le fichier existe
try:
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')  # Assurez-vous que le séparateur est correct
        for row in reader:
            # Vérification si la ligne contient les informations nécessaires
            if len(row) > 3:
                description = row[3]
                groupe = row[5]
                dtstart = row[1]  # Date de début (assumée en deuxième colonne)

                # Vérifier si c'est une séance de TP pour le groupe A1
                if "TP" in description and groupe_cible in groupe:
                    # Convertir la date de début en datetime
                    date_debut = datetime.strptime(dtstart, "%Y%m%dT%H%M%SZ")
                    
                    # Filtrer les événements entre septembre et décembre 2023
                    if 2023 <= date_debut.year <= 2023 and 9 <= date_debut.month <= 12:
                        # Incrémenter le compteur pour le mois approprié
                        if date_debut.month == 9:
                            seances_par_mois["Septembre"] += 1
                        elif date_debut.month == 10:
                            seances_par_mois["Octobre"] += 1
                        elif date_debut.month == 11:
                            seances_par_mois["Novembre"] += 1
                        elif date_debut.month == 12:
                            seances_par_mois["Décembre"] += 1

except FileNotFoundError:
    print(f"Erreur : Le fichier '{csv_file}' est introuvable. Assurez-vous qu'il est généré.")
    exit()

# Affichage des résultats (nombre de séances par mois)
print("Nombre de séances de TP pour le groupe A1 :")
for mois, nombre in seances_par_mois.items():
    print(f"{mois}: {nombre} séance(s)")

# Création du graphique
mois = list(seances_par_mois.keys())
nombre_seances = list(seances_par_mois.values())

# Diagramme en bâtons
plt.bar(mois, nombre_seances, color='skyblue')

# Titre et labels
plt.title("Nombre de séances de TP du groupe A1 (Septembre - Décembre 2023)", fontsize=14)
plt.xlabel("Mois", fontsize=12)
plt.ylabel("Nombre de séances", fontsize=12)

# Exporter le graphique au format PNG
plt.tight_layout()  # Pour s'assurer que les labels ne soient pas coupés
plt.savefig("seances_A1_TP_sept_dec_2023.png")

# Afficher le graphique
plt.show()

print("Le graphique a été exporté en format PNG sous le nom 'seances_A1_TP_sept_dec_2023.png'.")
