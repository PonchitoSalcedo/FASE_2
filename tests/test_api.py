import requests
import json
import time
from datetime import datetime

print("🧪 Probando API...")

# Configuración
BASE_URL = "http://localhost:8000"

def test_health():
    """Prueba el endpoint de health"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check: OK")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except:
        print("❌ No se pudo conectar a la API")
        return False

def test_prediction():
    """Prueba el endpoint de predicción"""
    data = {
        "feature1": 25.5,
        "feature2": 30.2,
        "feature3": 45.8,
        "feature4": 12.3
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Predicción exitosa!")
            print(f"   Predicción: {result['prediction']:.2f}")
            print(f"   Confianza: {result['confidence']:.1%}")
            return True
        else:
            print(f"❌ Predicción falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch():
    """Prueba el endpoint de batch prediction"""
    data = [
        {"feature1": 10, "feature2": 20, "feature3": 30, "feature4": 40},
        {"feature1": 50, "feature2": 60, "feature3": 70, "feature4": 80},
        {"feature1": 15, "feature2": 25, "feature3": 35, "feature4": 45}
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/batch_predict", json=data)
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Batch prediction exitosa! ({len(results)} predicciones)")
            return True
        else:
            print(f"❌ Batch prediction falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extreme_cases():
    """Prueba casos extremos"""
    test_cases = [
        {"feature1": 0, "feature2": 0, "feature3": 0, "feature4": 0},
        {"feature1": 100, "feature2": 100, "feature3": 100, "feature4": 100},
        {"feature1": -1, "feature2": 30, "feature3": 45, "feature4": 12}  # Valor negativo
    ]
    
    print("🧪 Probando casos extremos...")
    for i, case in enumerate(test_cases, 1):
        try:
            response = requests.post(f"{BASE_URL}/predict", json=case)
            if response.status_code == 200:
                print(f"   Caso {i}: ✅")
            else:
                print(f"   Caso {i}: ❌ (Status: {response.status_code})")
        except:
            print(f"   Caso {i}: ❌ (Error)")

print("📋 Ejecutando suite de pruebas...")
print("=" * 50)

# Ejecutar pruebas
tests_passed = 0
tests_total = 3

if test_health():
    tests_passed += 1
print()

if test_prediction():
    tests_passed += 1
print()

if test_batch():
    tests_passed += 1
print()

test_extreme_cases()
print()
print("=" * 50)
print(f"📊 Resultados: {tests_passed}/{tests_total} pruebas pasaron")
print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
