import os

# Nom du fichier ICS
ics_file = "ADE.ics"

if not os.path.exists(ics_file):
    print(f"Erreur : Le fichier '{ics_file}' est introuvable. Vérifiez son emplacement.")
else:
    # Lire le contenu du fichier ICS
    with open(ics_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Variables pour stocker les informations extraites
    events = []  # Liste des événements
    current_event = {}
    inside_event = False

    # Parcourir les lignes du fichier
    for line in lines:
        line = line.strip()
        if line == "BEGIN:VEVENT":
            inside_event = True
            current_event = {}
        elif line == "END:VEVENT":
            inside_event = False
            # Ajouter l'événement extrait à la liste des événements
            events.append(current_event)
        elif inside_event:
            # Extraire clé:valeur (par exemple, DTSTAMP:20240110T053220Z)
            if ":" in line:
                key, value = line.split(":", 1)
                if key in current_event:
                    # Gérer les cas où il y a plusieurs salles ou professeurs
                    current_event[key] += f" | {value}"
                else:
                    current_event[key] = value

    # Générer un tableau de pseudo-code CSV
    csv_header = ["DTSTAMP", "DTSTART", "DTEND", "SUMMARY", "LOCATION", "DESCRIPTION", "UID", "CREATED", "LAST-MODIFIED", "SEQUENCE"]
    csv_table = [",".join(csv_header)]

    for event in events:
        row = [
            event.get("DTSTAMP", "vide"),
            event.get("DTSTART", "vide"),
            event.get("DTEND", "vide"),
            event.get("SUMMARY", "vide"),
            event.get("LOCATION", "vide"),
            event.get("DESCRIPTION", "vide").replace("\n", " "),  # Nettoyer les retours à la ligne
            event.get("UID", "vide"),
            event.get("CREATED", "vide"),
            event.get("LAST-MODIFIED", "vide"),
            event.get("SEQUENCE", "vide"),
        ]
        csv_table.append(";".join(row))

    # Afficher le tableau pseudo-code CSV
    for row in csv_table:
        print(row)

    # Facultatif : Sauvegarder dans un fichier CSV
    csv_file = "evenements.csv"
    with open(csv_file, "w", encoding="utf-8") as file:
        file.write("\n".join(csv_table))
    print(f"Les données ont été exportées dans le fichier '{csv_file}'.")
