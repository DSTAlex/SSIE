import pandas as pd
import numpy as np

np.random.seed(42)
n_samples = 5000

# Données normales
normal_data = np.random.randn(n_samples, 3) * [10, 50, 2] + [50, 3000, 12]  # temp, speed, voltage

# Données anormales
anomaly_data = np.random.randn(50, 3) * [20, 200, 4] + [100, 5000, 8]

# Concatenate normal and anomaly data
data = np.concatenate([normal_data, anomaly_data], axis=0)
df = pd.DataFrame(data, columns=['temp_engine', 'speed', 'voltage_battery'])

# Simuler du "garbage" dans les données
# 1. Ajouter des valeurs NaN
df.loc[np.random.choice(df.index, size=50, replace=False), 'temp_engine'] = np.nan

# 2. Valeurs aberrantes
df.loc[np.random.choice(df.index, size=20, replace=False), 'speed'] = 9999

# 3. Colonnes inversées ou bruitées
df.loc[np.random.choice(df.index, size=30, replace=False), 'voltage_battery'] = np.random.choice(['ERROR', 'N/A'], 30)

# Sauvegarder les données
df.to_csv('vehicle_sensor_data.csv', index=False)
print("Données simulées avec du 'garbage' générées.")
