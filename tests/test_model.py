import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

print("🚀 Entrenando modelo de prueba...")

# Generar datos sintéticos
np.random.seed(42)
n_samples = 1000
X = np.random.rand(n_samples, 4) * 100
y = (X[:, 0] * 0.3 + X[:, 1] * 0.2 + X[:, 2] * 0.4 + X[:, 3] * 0.1 + 
     np.random.randn(n_samples) * 5)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar modelo
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Modelo entrenado!")
print(f"📊 MSE: {mse:.4f}")
print(f"📊 R²: {r2:.4f}")

# Guardar modelo
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/model.pkl')
print("✅ Modelo guardado en: models/model.pkl")

# Probar predicción
test_data = np.array([[25.5, 30.2, 45.8, 12.3]])
prediction = model.predict(test_data)
print(f"🔮 Predicción de prueba: {prediction[0]:.2f}")
