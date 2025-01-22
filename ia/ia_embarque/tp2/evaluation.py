from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

# Charger les données nettoyées (si nécessaire)
df = pd.read_csv('vehicle_sensor_data.csv')

# Remettre le modèle Isolation Forest
model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = model.fit_predict(df[['temp_engine', 'speed', 'voltage_battery']])

# Étiquettes réelles : 1 pour anomalies, 0 pour normales
true_labels = np.concatenate([np.zeros(5000), np.ones(50)])

# Recalculer les étiquettes prédites : -1 -> 1 (anomalie) et 1 -> 0 (normal)
predicted_labels = (df['anomaly'] == -1).astype(int)

# 1. Matrice de confusion
conf_matrix = confusion_matrix(true_labels, predicted_labels)
print("Matrice de confusion :\n", conf_matrix)

# 2. Rapport de classification
report = classification_report(true_labels, predicted_labels)
print("\nRapport de classification :\n", report)

# 3. Précision globale
accuracy = accuracy_score(true_labels, predicted_labels)
print(f"Précision globale : {accuracy:.2f}")
