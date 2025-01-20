import numpy as np
import os
import csv
import matplotlib.pyplot as plt

try:
    with open("fichier SAE105.txt", encoding="utf8") as fh:
        res = fh.read()
except FileNotFoundError:
    print("Le fichier n'existe pas :", os.path.abspath('fichieratraiter.txt'))
    exit()

ress = res.split('\n')
tab_dest = np.array([])

with open("fichier.csv", "w", newline='') as fic:
    # test est le fichier d'arrivée des extractions
    writer = csv.writer(fic)
    evenement = ["DATE", "SOURCE", "PORT", "DESTINATION", "FLAG", "SEQ", "ACK", "WIN", "OPTIONS", "LENGTH"]
    writer.writerow(evenement)  # écriture de mes titres dans le tableau
    characters = ":"  # définir une variable avec le caractère ":" (qui nous sera utile pour la suite)

    for event in ress:
        if event.startswith('11:42'):
            # déclaration variables et remise à zéro
            seq = ""
            heure1 = ""
            nomip = ""
            port = ""
            flag = ""
            ack = ""
            win = ""
            options = ""
            length = ""

            # Pour la date de l'événement (première colonne)
            texte = event.split(" ")
            heure1 = texte[0]

            # Pour la source (2ème colonne)
            nomip1 = texte[2].split(".")
            nomip = ".".join(nomip1[:min(5, len(nomip1))])  # Utilisation de join pour construire l'IP

            flag2 = nomip not in tab_dest
            if flag2:
                tab_dest = np.append(tab_dest, nomip)

            # Port
            port1 = texte[2].split(".")
            port = port1[-1]

            # Pour la destination (3ème colonne)
            nomip2 = texte[4]

            # Flag
            texte = event.split("[")
            if len(texte) > 1:
                flag1 = texte[1].split("]")
                flag = flag1[0]

            # Seq
            texte = event.split(",")
            if len(texte) > 1 and texte[1].startswith(" seq"):
                seq1 = texte[1].split(" ")
                seq = seq1[2]

            # Ack
            if len(texte) > 2 and texte[2].startswith(" ack"):
                ack1 = texte[2].split(" ")
                ack = ack1[2]
            elif len(texte) > 1 and texte[1].startswith(" ack"):
                ack1 = texte[1].split(" ")
                ack = ack1[2]

            # Win
            if len(texte) > 3:
                if texte[3].startswith(" win"):
                    win1 = texte[3].split(" ")
                    win = win1[2]
                elif texte[2].startswith(" win"):
                    win1 = texte[2].split(" ")
                    win = win1[2]

            # Options
            texte = event.split("[")
            if len(texte) > 2:
                options1 = texte[2].split("]")
                options = options1[0]

            # Length (avec option)
            texte = event.split("]")
            if len(texte) > 2:
                length1 = texte[2].split(" ")
                length = length1[2].replace(characters, "")

            # Length (sans option)
            texte = event.split(",")
            if len(texte) > 3 and texte[3].startswith(" length"):
                length1 = texte[3].split(" ")
                length = length1[2]

            # Écrire dans le fichier CSV
            evenement = [heure1, nomip, port, nomip2, flag, seq, ack, win, options, length]
            writer.writerow(evenement)

print("Tableau final", tab_dest)

# Tracer le graphique
plt.plot(tab_dest, [1] * len(tab_dest))
plt.show()