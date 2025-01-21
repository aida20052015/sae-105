import pandas as pd

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('fichier_SAE105.csv')

# Convertir la colonne 'Length' en numérique (en remplaçant les valeurs non numériques par NaN)
df['Length'] = pd.to_numeric(df['Length'], errors='coerce')

# Définir un seuil pour identifier les anomalies de longueur (vous pouvez ajuster cette valeur selon votre besoin)
threshold_length = 1000  # Exemple de seuil

# Filtrer les anomalies de longueur
df_anomalies_length = df[df['Length'] > threshold_length]

# Afficher les anomalies
print(df_anomalies_length)

# Si vous souhaitez enregistrer ce résultat dans un nouveau fichier Excel
df_anomalies_length.to_excel('anomalies_length.xlsx', index=False)
