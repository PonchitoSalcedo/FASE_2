# Manual de Despliegue en la Nube

## 1. Prerrequisitos
- Cuenta de Google Cloud Platform
- Google Cloud SDK instalado
- Docker instalado localmente

## 2. Preparación del Entorno
```bash
# Autenticación
gcloud auth login
gcloud config set project PROJECT_ID

# Crear Artifact Registry
gcloud artifacts repositories create ml-app \
    --repository-format=docker \
    --location=us-central1
```

## 3. Construcción de Imágenes
```bash
# Backend
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/ml-app/backend:latest ./backend

# Frontend
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/ml-app/frontend:latest ./frontend

# Subir imágenes
docker push us-central1-docker.pkg.dev/PROJECT_ID/ml-app/backend:latest
docker push us-central1-docker.pkg.dev/PROJECT_ID/ml-app/frontend:latest
```

## 4. Despliegue en Cloud Run
```bash
# Backend
gcloud run deploy ml-backend \
    --image=us-central1-docker.pkg.dev/PROJECT_ID/ml-app/backend:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated

# Frontend
gcloud run deploy ml-frontend \
    --image=us-central1-docker.pkg.dev/PROJECT_ID/ml-app/frontend:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --set-env-vars="API_URL=https://ml-backend-xxxxx-uc.a.run.app"
```

## 5. Verificación
```bash
# Health check
curl https://ml-backend-xxxxx-uc.a.run.app/health

# Probar API
curl -X POST https://ml-backend-xxxxx-uc.a.run.app/predict \
    -H "Content-Type: application/json" \
    -d '{"feature1": 25.5, "feature2": 30.2, "feature3": 45.8, "feature4": 12.3}'
```

## 6. CI/CD con GitHub Actions
El workflow automático está configurado en .github/workflows/ci-cd.yml
