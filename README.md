
**Las tres comillas invertidas DEBEN estar al inicio y al final del bloque, y la palabra `bash` debe estar pegada a las primeras tres comillas (sin espacio).**

---

## 📝 **CÓDIGO COMPLETO CORREGIDO PARA EL README**

**Copia y pega EXACTAMENTE este contenido en tu `README.md`** (reemplaza todo el contenido anterior):

````markdown
# 🚀 Sistema de Predicción ML con Docker

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aplicación completa de **Machine Learning** con frontend (Streamlit) y backend (FastAPI) contenerizada con Docker.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación Rápida](#instalación-rápida)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Desarrollo Local](#desarrollo-local)
- [Despliegue en la Nube](#despliegue-en-la-nube)
- [API Documentation](#api-documentation)
- [Pruebas](#pruebas)

---

## ✨ Características

- **Backend**: FastAPI con endpoints REST para predicciones
- **Frontend**: Dashboard interactivo con Streamlit
- **Containerización**: Docker y Docker Compose
- **Escalable**: Soporte para predicciones individuales y batch
- **Documentación**: Swagger UI y ReDoc automáticos

---

## 🔧 Requisitos

| Herramienta | Versión Mínima |
|-------------|----------------|
| Docker | 20.10+ |
| Docker Compose | 2.0+ |
| Git | 2.30+ |
| Python | 3.10+ (solo desarrollo) |

---

## 🚀 Instalación Rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/PonchitoSalcedo/FASE_2.git
cd FASE_2
```

### 2. Ejecutar con Docker Compose

```bash
docker-compose up --build
```

### 3. Acceder a la aplicación

| Servicio | URL |
|----------|-----|
| **Frontend** | http://localhost:8501 |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## 📁 Estructura del Proyecto

```
FASE_2/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── models/
│   └── model.pkl
├── tests/
│   ├── test_model.py
│   └── test_api.py
├── docs/
│   ├── manual_despliegue.md
│   └── validacion_pruebas.md
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 💻 Desarrollo Local

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Streamlit)

```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
```

---

## ☁️ Despliegue en la Nube

### Google Cloud Run

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ml-app
gcloud run deploy ml-app --image gcr.io/PROJECT_ID/ml-app --platform managed
```

---

## 📊 API Documentation

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `GET` | `/health` | Health check del servicio |
| `POST` | `/predict` | Predicción individual |
| `POST` | `/batch_predict` | Predicción en lote |

### Ejemplo de Uso

```python
import requests

data = {
    "feature1": 25.5,
    "feature2": 30.2,
    "feature3": 45.8,
    "feature4": 12.3
}
response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

---

## 🧪 Pruebas

```bash
cd tests
python test_model.py
python test_api.py
```

---

## 📄 Licencia

MIT License

## 📧 Contacto

- **GitHub**: [@PonchitoSalcedo](https://github.com/PonchitoSalcedo)

---

⭐ **¡No olvides darle una estrella al repositorio si te fue útil!**
