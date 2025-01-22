import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv('vehicle_sensor_data.csv')
df['speed'] = df['speed']/10

# 1. Traiter les valeurs manquantes
df['temp_engine'].fillna(df['temp_engine'].median(), inplace=True)

# 2. Remplacer les valeurs aberrantes
df.loc[df['speed'] > 300, 'speed'] = np.nan  # Supposons que 300 est la vitesse max réaliste
df['speed'].fillna(df['speed'].median(), inplace=True)

# 3. Nettoyer les erreurs textuelles
df['voltage_battery'] = pd.to_numeric(df['voltage_battery'], errors='coerce')
df['voltage_battery'].fillna(df['voltage_battery'].mean(), inplace=True)

print(df.head())
