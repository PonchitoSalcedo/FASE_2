
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="ML Prediction Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS
st.markdown('''
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
''', unsafe_allow_html=True)

# Configuración de API
API_URL = os.getenv("API_URL", "http://backend:8000")

def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def make_prediction(features):
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=features,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la predicción: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        return None

def batch_prediction(data):
    try:
        response = requests.post(
            f"{API_URL}/batch_predict",
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en predicción batch: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión: {e}")
        return None

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuración")
    api_status = check_api_health()
    if api_status:
        st.success("✅ API conectada")
    else:
        st.error("❌ API no disponible")
    
    prediction_mode = st.radio("Modo de predicción", ["Individual", "Batch"])
    confidence_threshold = st.slider("Umbral de confianza", 0.5, 0.95, 0.7, 0.05)

# Header
st.markdown('<p class="main-header">🤖 Sistema de Predicción ML</p>', unsafe_allow_html=True)

if prediction_mode == "Individual":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Datos de Entrada")
        feature1 = st.number_input("Característica 1", 0.0, 100.0, 25.5)
        feature2 = st.number_input("Característica 2", 0.0, 100.0, 30.2)
        feature3 = st.number_input("Característica 3", 0.0, 100.0, 45.8)
        feature4 = st.number_input("Característica 4", 0.0, 100.0, 12.3)
    
    with col2:
        st.subheader("🔧 Características Opcionales")
        use_extra = st.checkbox("Usar características adicionales")
        if use_extra:
            feature5 = st.number_input("Característica 5", 0.0, 100.0, 15.7)
            feature6 = st.number_input("Característica 6", 0.0, 100.0, 22.1)
        else:
            feature5 = None
            feature6 = None
    
    if st.button("🔮 Realizar Predicción", type="primary"):
        with st.spinner("Procesando predicción..."):
            features = {
                "feature1": feature1,
                "feature2": feature2,
                "feature3": feature3,
                "feature4": feature4
            }
            if use_extra:
                features["feature5"] = feature5
                features["feature6"] = feature6
            
            result = make_prediction(features)
            
            if result:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Predicción", f"{result['prediction']:.2f}")
                with col2:
                    st.metric("Confianza", f"{result['confidence']:.1%}")
                with col3:
                    st.metric("Timestamp", result['timestamp'][:19])

else:
    st.subheader("📋 Predicción en Lote")
    uploaded_file = st.file_uploader("Subir archivo CSV", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            
            if st.button("🚀 Realizar Predicciones"):
                with st.spinner("Procesando..."):
                    data = df.to_dict('records')
                    results = batch_prediction(data)
                    
                    if results:
                        results_df = pd.DataFrame(results)
                        combined = pd.concat([df, results_df], axis=1)
                        st.dataframe(combined)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Predicción Promedio", f"{results_df['prediction'].mean():.2f}")
                        with col2:
                            st.metric("Confianza Promedio", f"{results_df['confidence'].mean():.1%}")
                        with col3:
                            st.metric("Total Predicciones", len(results_df))
        except Exception as e:
            st.error(f"Error: {e}")

# Información adicional
with st.expander("ℹ️ Información del Sistema"):
    st.write("**Versión del Modelo:** 1.0.0")
    st.write("**API Endpoint:**", API_URL)
    st.write("**Timestamp:**", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
