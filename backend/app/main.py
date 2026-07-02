from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # <--- IMPORTANTE: ESTABA FALTANDO
from typing import Optional, List
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import joblib
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Predicción ML",
    description="API para predicciones usando modelo de Machine Learning",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic - CORREGIDO
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: Optional[float] = None  # <--- CORREGIDO
    feature6: Optional[float] = None  # <--- CORREGIDO

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    timestamp: str
    model_version: str

# Variables globales
model = None
model_version = "1.0.0"

def load_model():
    """Carga el modelo de ML desde el archivo o crea uno dummy para demo"""
    global model
    try:
        model_path = os.getenv("MODEL_PATH", "models/model.pkl")
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            logger.info(f"Modelo cargado desde {model_path}")
        else:
            logger.warning("Modelo no encontrado, usando modelo dummy")
            model = None
    except Exception as e:
        logger.error(f"Error cargando modelo: {e}")
        model = None

def dummy_prediction(input_data):
    """Función dummy para demostración"""
    features = np.array([input_data.feature1, input_data.feature2, 
                         input_data.feature3, input_data.feature4])
    # <--- CORREGIDO: Usar feature5 y feature6 correctamente
    if input_data.feature5 is not None and input_data.feature6 is not None:
        features = np.append(features, [input_data.feature5, input_data.feature6])
    
    prediction = np.mean(features) * 1.5 + np.random.normal(0, 0.1)
    confidence = 0.85 + np.random.normal(0, 0.05)
    confidence = min(0.99, max(0.7, confidence))
    
    return float(prediction), float(confidence)

@app.on_event("startup")
async def startup_event():
    load_model()
    logger.info("API iniciada correctamente")

@app.get("/")
async def root():
    return {
        "message": "API de Predicción ML",
        "docs": "/docs",
        "status": "running",
        "version": model_version
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": model_version,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(input_data: PredictionInput):
    try:
        if input_data.feature1 < 0 or input_data.feature2 < 0:
            raise HTTPException(status_code=400, detail="Los valores no pueden ser negativos")
        
        prediction, confidence = dummy_prediction(input_data)
        
        return PredictionResponse(
            prediction=prediction,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            model_version=model_version
        )
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch_predict")
async def batch_predict(data: List[PredictionInput]):
    try:
        results = []
        for item in data:
            prediction, confidence = dummy_prediction(item)
            results.append({
                "prediction": prediction,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat(),
                "model_version": model_version
            })
        return results
    except Exception as e:
        logger.error(f"Error en batch prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
