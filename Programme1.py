import os

# Fichier ICS
ics_file = "evenementSAE_15(1).ics"

if not os.path.exists(ics_file):
    print(f"Erreur : Le fichier '{ics_file}' est introuvable. Vérifiez son emplacement.")
else:
    # Lire le contenu du fichier ICS
    with open(ics_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Variables pour stocker les informations extraites
    event_data = []
    current_event = {}
    inside_event = False

    # Parcourir les lignes
    for line in lines:
        line = line.strip()
        if line == "BEGIN:VEVENT":
            inside_event = True
            current_event = {}
        elif line == "END:VEVENT":
            inside_event = False
            event_data.append(current_event)
        elif inside_event:
            # Extraire clé:valeur (par exemple, DTSTAMP:20240110T053220Z)
            if ":" in line:
                key, value = line.split(":", 1)
                current_event[key] = value

    # Générer le pseudo-code CSV
    csv_header = "DTSTAMP,DTSTART,DTEND,SUMMARY,LOCATION,DESCRIPTION,UID,CREATED,LAST-MODIFIED,SEQUENCE"
    csv_data = [csv_header]

    for event in event_data:
        row = [
            event.get("DTSTAMP", ""),
            event.get("DTSTART", ""),
            event.get("DTEND", ""),
            event.get("SUMMARY", ""),
            event.get("LOCATION", ""),
            event.get("DESCRIPTION", "").replace("\n", " "),  # Nettoyer les retours à la ligne
            event.get("UID", ""),
            event.get("CREATED", ""),
            event.get("LAST-MODIFIED", ""),
            event.get("SEQUENCE", ""),
        ]
        csv_data.append(";".join(row))

    # Afficher le pseudo-code CSV
    print("\n".join(csv_data))

    #  Sauvegarder le pseudo-code CSV dans un fichier
    csv_file = "evenement.csv"
    with open(csv_file, "w", encoding="utf-8") as file:
        file.write("\n".join(csv_data))
    print(f"Les données ont été exportées dans le fichier '{csv_file}'.")
