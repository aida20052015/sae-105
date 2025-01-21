import csv
import webbrowser
import matplotlib.pyplot as plt

# Ouvrir le fichier "fichier SAE105.txt"
with open("fichier SAE105.txt", "r") as fichier:
    ipsr = []
    ipde = []
    longueur = []
    flag = []
    seq = []
    heure = []

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

# Ajouter une vérification pour éviter la division par zéro
globalreqrepcounter = replycounter + requestcounter
if globalreqrepcounter != 0:
    req = requestcounter / globalreqrepcounter
    rep = replycounter / globalreqrepcounter
else:
    req = rep = 0

globalflagcounter = flagcounter + flagcounterP + flagcounterS
P = flagcounterP / globalflagcounter
S = flagcounterS / globalflagcounter
A = flagcounter / globalflagcounter

flagcounter = [flagcounter]
flagcounterP = [flagcounterP]
flagcounterS = [flagcounterS]
framecounter = [framecounter]
requestcounter = [requestcounter]
replycounter = [replycounter]
seqcounter = [seqcounter]
ackcounter = [ackcounter]
wincounter = [wincounter]

# Créer le graphique circulaire pour les drapeaux
name = ['Flag [.]', 'Flag [P]', 'Flag [S]']
data = [A, P, S]

explode = (0, 0, 0)
plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
plt.axis('equal')
plt.savefig("graphe1 SAE105.png")
plt.show()

# Créer le graphique circulaire pour les requêtes et réponses
name2 = ['Request', 'Reply']
data2 = [req, rep]
explode = (0, 0)
plt.pie(data2, explode=explode, labels=name2, autopct='%1.1f%%', startangle=90, shadow=True)
plt.savefig("graphe2 SAE105.png")
plt.show()

# Contenu de la page web
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
       <center><p>Sur cette page web, nous vous présentons les informations et données pertinentes trouvées dans le fichier à traiter (fichier SAE105.txt).</p></center>
       <center><h3> Nombre total de trames échangées</h3> %s</center>
       <br>
       <center><h3> Drapeaux (Flags)<h3></center>
       <center>Nombre de flags [P] (PUSH) = %s
       <br>Nombre de flags [S] (SYN) = %s  
       <br>Nombre de flag [.] (ACK) = %s
       <br>
       <br>
       <img src="graphe1.png">
       <h3> Nombre de requêtes et réponses </h3>
       Request = %s
       <br>
       Reply = %s
       <br>
       <br>
       <img src="graphe2 SAE105.png">
       <h3>Statistiques entre seq, win et ack </h3>
       Nombre de seq = %s
       <br>
       Nombre de win = %s
       <br>
       Nombre de ack = %s
       <footer>
       <center><p>PROJET SAE 105</p></center>
       </footer>
   </body>
</html>
''' % (framecounter[0], flagcounterP[0], flagcounterS[0], flagcounter[0], requestcounter[0], replycounter[0], seqcounter[0], wincounter[0], ackcounter[0])

# Ouvrir un fichier CSV pour les données extraites du fichier texte non traité
with open('fichier SAE105.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['Heure', 'IP source', 'IP destination', 'Flag', 'Seq', 'Length'])
    writer.writerows(zip(heure, ipsr, ipde, flag, seq, longueur))

# Ouvrir un fichier CSV pour les statistiques générales
with open('Stats SAE105.csv', 'w', newline='') as fichier2:
    writer = csv.writer(fichier2)
    writer.writerow(['Flag[P] (PUSH)', 'Flag[S] (SYN)', 'Flag[.] (ACK)', 'Nombre total de trames',
                     'Nombre de request', 'Nombre de reply', 'Nombre de sequence', 'Nombre de acknowledg', 'Nombre de window'])
    writer.writerows(zip(flagcounterP, flagcounterS, flagcounter, framecounter, requestcounter, replycounter, seqcounter, ackcounter, wincounter))

# Ouvrir une page web avec des informations importantes et des statistiques
with open("data.html", "w") as html:
    html.write(htmlcontenu)
    print("Page web créée avec succès.")