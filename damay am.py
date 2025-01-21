import csv
import webbrowser
import matplotlib.pyplot as plt
from scapy.all import rdpcap
import os

def traiter_fichier_txt(fichier):
    # Variables pour stocker les informations extraites
    ipsr = []
    ipde = []
    longueur = []
    flag = []
    seq = []
    heure = []

    # Compteurs pour diverses statistiques
    flagcounterP = 0
    flagcounterS = 0
    flagcounter = 0
    framecounter = 0
    requestcounter = 0
    replycounter = 0
    seqcounter = 0
    ackcounter = 0
    wincounter = 0

    for ligne in fichier:
        split = ligne.split(" ")

        if "IP" in ligne:
            framecounter += 1

            if "[P.]" in ligne:
                flag.append("[P.]")
                flagcounterP += 1
            elif "[.]" in ligne:
                flag.append("[.]")
                flagcounter += 1
            elif "[S]" in ligne:
                flag.append("[S]")
                flagcounterS += 1

            if "seq" in ligne:
                seqcounter += 1
                seq.append(split[8])

            if "win" in ligne:
                wincounter += 1

            if "ack" in ligne:
                ackcounter += 1

            ipsr.append(split[2])
            ipde.append(split[4])
            heure.append(split[0])

            if "length" in ligne:
                split = ligne.split(" ")
                longueur.append(split[-2] if "HTTP" in ligne else split[-1])

            if "ICMP" in ligne:
                if "request" in ligne:
                    requestcounter += 1
                elif "reply" in ligne:
                    replycounter += 1

    # Retourner les statistiques et les données extraites
    return (ipsr, ipde, longueur, flag, seq, heure, framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter)

def traiter_fichier_pcap(fichier):
    # Listes pour stocker les informations extraites
    ipsr = []
    ipde = []
    longueur = []
    flag = []
    seq = []
    heure = []

    # Compteurs pour diverses statistiques
    flagcounterP = 0
    flagcounterS = 0
    flagcounter = 0
    framecounter = 0
    requestcounter = 0
    replycounter = 0
    seqcounter = 0
    ackcounter = 0
    wincounter = 0

    # Charger le fichier pcap avec Scapy
    packets = rdpcap(fichier)

    for packet in packets:
        if packet.haslayer('IP'):
            framecounter += 1
            ip_src = packet['IP'].src
            ip_dst = packet['IP'].dst
            flags = packet.sprintf("%TCP.flags%")  # Extraire les flags TCP
            seq_number = packet['TCP'].seq if packet.haslayer('TCP') else None
            ack_number = packet['TCP'].ack if packet.haslayer('TCP') else None
            win_size = packet['TCP'].window if packet.haslayer('TCP') else None

            # Enregistrer les informations dans les listes correspondantes
            ipsr.append(ip_src)
            ipde.append(ip_dst)
            seq.append(seq_number)
            flag.append(flags)
            heure.append(packet.time)  # Le temps de capture du paquet
            longueur.append(len(packet))

            # Mise à jour des compteurs de flags
            if "[P.]" in flags:
                flagcounterP += 1
            elif "[S]" in flags:
                flagcounterS += 1
            elif "[.]" in flags:
                flagcounter += 1

            # Mise à jour des compteurs de requêtes et réponses ICMP
            if packet.haslayer('ICMP'):
                if "request" in packet.summary():
                    requestcounter += 1
                elif "reply" in packet.summary():
                    replycounter += 1

            # Mise à jour des compteurs pour les numéros de séquence, ack, et taille de fenêtre
            if seq_number:
                seqcounter += 1
            if ack_number:
                ackcounter += 1
            if win_size:
                wincounter += 1

    # Retourner les statistiques et les données extraites
    return (ipsr, ipde, longueur, flag, seq, heure, framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter)

def main():
    # Demander le fichier à traiter (txt, pcap, etc.)
    fichier_path = input("Enter the path of the file (txt, pcap): ")

    # Vérification du type de fichier
    if not os.path.exists(fichier_path):
        print("File not found!")
        return

    extension = fichier_path.split('.')[-1]

    if extension == 'txt':
        with open(fichier_path, 'r') as fichier:
            (ipsr, ipde, longueur, flag, seq, heure, framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter) = traiter_fichier_txt(fichier)
    elif extension == 'pcap':
        (ipsr, ipde, longueur, flag, seq, heure, framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter) = traiter_fichier_pcap(fichier_path)
    else:
        print("Unsupported file format!")
        return

    # Calcul des statistiques globales
    globalreqrepcounter = replycounter + requestcounter
    req = requestcounter / globalreqrepcounter if globalreqrepcounter != 0 else 0
    rep = replycounter / globalreqrepcounter if globalreqrepcounter != 0 else 0

    globalflagcounter = flagcounter + flagcounterP + flagcounterS
    P = flagcounterP / globalflagcounter
    S = flagcounterS / globalflagcounter
    A = flagcounter / globalflagcounter

    # Créer les graphiques circulaires
    name = ['Flag [.]', 'Flag [P]', 'Flag [S]']
    data = [A, P, S]
    plt.pie(data, explode=(0, 0, 0), labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    plt.savefig("graphe1_SAE105.png")
    plt.show()

    name2 = ['Request', 'Reply']
    data2 = [req, rep]
    plt.pie(data2, explode=(0, 0), labels=name2, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.savefig("graphe2_SAE105.png")
    plt.show()

    # Sauvegarder les résultats dans un fichier CSV
    with open('fichier_SAE105.csv', 'w', newline='') as fichiercsv:
        writer = csv.writer(fichiercsv)
        writer.writerow(['Heure', 'IP source', 'IP destination', 'Flag', 'Seq', 'Length'])
        writer.writerows(zip(heure, ipsr, ipde, flag, seq, longueur))

    with open('Stats_SAE105.csv', 'w', newline='') as fichier2:
        writer = csv.writer(fichier2)
        writer.writerow(['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)', 'Nombre total de trames',
                     'Nombre de request', 'Nombre de reply', 'Nombre de sequence', 'Nombre de acknowledg', 'Nombre de window'])
    
    # Enregistrer les données dans le fichier CSV
        writer.writerows(zip([flagcounterP], [flagcounterS], [flagcounter], [framecounter], 
                         [requestcounter], [replycounter], [seqcounter], [ackcounter], [wincounter]))


    # Créer une page web avec les statistiques
    htmlcontenu = '''
    <html lang="fr">
       <head>
          <meta charset="utf-8">
          <title> Traitement de données </title>
          <style>
          body{
              background-image: url('https://cdn.pixabay.com/photo/2018/03/15/16/11/background-3228704_1280.jpg');
              background-repeat: no-repeat;
              background-size: cover;
              color:#e5f2f7;
              background-attachment: fixed;
              }
          </style>
       </head>
       <body>
           <center><h1>ADJA AIDA NDIAYE FALL</h1></center>
           <center><h2>Projet SAE105</h2></center>
           <center><p>Sur cette page web, nous vous présentons les informations et données pertinentes trouvées dans le fichier à traiter.</p></center>
           <center><h3> Nombre total de trames échangées</h3> %s</center>
           <center><h3> Drapeaux (Flags)<h3></center>
           <center>Nombre de flags [P] (PUSH) = %s
           <br>Nombre de flags [S] (SYN) = %s  
           <br>Nombre de flag [.] (ACK) = %s
           <br><br><img src="graphe1_SAE105.png">
           <h3> Nombre de requêtes et réponses </h3>
           Request = %s
           <br>Reply = %s
           <br><br><img src="graphe2_SAE105.png">
           <h3>Statistiques entre seq, win et ack </h3>
           Nombre de seq = %s
           <br>Nombre de win = %s
           <br>Nombre de ack = %s
           <footer><center><p>PROJET SAE 105</p></center></footer>
       </body>
    </html>
    ''' % (framecounter, flagcounterP, flagcounterS, flagcounter, requestcounter, replycounter, seqcounter, wincounter, ackcounter)

    with open("data.html", "w") as html:
        html.write(htmlcontenu)
        print("Page web créée avec succès.")

if __name__ == "__main__":
    main()
