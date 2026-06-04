# ===========================================================
# dashboard/app.py
# Dashboard de monitorización del sistema SIEM
# - Visualización de estadísticas, anomalías y estado general.
# - Actualización automática cada 10 segundos.
# ============================================================

import streamlit as st
import requests
import pandas as pd

from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from pathlib import Path

# Configuración página
st.set_page_config(
    page_title="TFG SIEM Dashboard",
    layout="wide"
)

logo_path = Path(__file__).parent / "images" / "logo.png"

col1, col2 = st.columns([1, 8])

with col1:
    st.image(str(logo_path), width=120)
with col2:
    st.title("Sistema SIEM - Polvorín militar simulado")
    st.markdown(
    "Monitorización de eventos de seguridad, sensores y alertas del entorno simulado."
    )

    DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
    st.caption(
        f"Última actualización: {datetime.now().strftime(DATETIME_FORMAT)}"
    )

# Autorefresco cda 10 segundos
st_autorefresh(interval=10000, key="dashboard_refresh")

# URLs API
STATS_URL = "http://127.0.0.1:8000/stats"
EVENTS_URL = "http://127.0.0.1:8000/events?limit=200"
SENSORS_URL = "http://127.0.0.1:8000/sensors/status"
ANOMALIES_URL = "http://127.0.0.1:8000/anomalies"
RECENT_EVENTS_URL = "http://127.0.0.1:8000/events/recent"

# Obtener anomalías
total_anomalies = 0
max_risk_score = 0
anomalies = []

anomalies_response = requests.get(ANOMALIES_URL, timeout=5)

if anomalies_response.status_code == 200:
    anomalies_data = anomalies_response.json()
    total_anomalies = anomalies_data["total_anomalies"]
    anomalies= anomalies_data["anomalies"]

    if anomalies:
        max_risk_score = max(
            anomaly["risk_score"] 
            for anomaly in anomalies
        )
    
# Obtener sensores
inactive_sensors = 0

sensors_response = requests.get(SENSORS_URL, timeout=5)

if sensors_response.status_code == 200:
    sensors_data = sensors_response.json()
    inactive_sensors = sensors_data["summary"]["inactive"]

# =========================
# ESTADO GENERAL
# =========================

st.header("Estado general del sistema")

if total_anomalies > 0:
    st.error("🔴 ESTADO CRÍTICO: anomalías detectadas en el sistema")
elif inactive_sensors > 0:
    st.warning("🟡 SISTEMA DEGRADADO: existen dispositivos sin comunicación")
else:
    st.success("🟢 SISTEMA OPERATIVO: sin incidencias detectadas")
    
col1, col2, col3, col4 = st.columns(4)

col1.success("🟢 SIEM OPERATIVO")
col2.success("🌐 API ONLINE")

if inactive_sensors > 0:
    col3.warning("📡 SENSORES CON INCIDENCIAS")
else:
    col3.success("📡 SENSORES ACTIVOS")

if total_anomalies > 0:
    col4.warning(
        f"⚠️ ANOMALÍAS DETECTADAS\n\nNivel máximo: {max_risk_score}/10"
        )
else:
    col4.success("✅ SIN ANOMALÍAS")


# =========================
# ESTADÍSTICAS
# =========================

st.header("Estadísticas generales")

stats_response = requests.get(STATS_URL, timeout=5)

if stats_response.status_code == 200:
    stats = stats_response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Eventos", stats["total_events"])
    col2.metric("Alertas", stats["total_alerts"])
    col3.metric("Alertas críticas", stats["critical_alerts"])


# =========================
# RESUMEN DE ANOMALÍAS
# =========================

st.header("Resumen de anomalías")

st.metric(
    "Anomalías detectadas",
    total_anomalies
)

if anomalies:

    anomalies_df = pd.DataFrame(anomalies)

    anomalies_df = anomalies_df.sort_values(
        by="risk_score",
        ascending=False
    )

    def anomaly_color(val):
        if val >= 8:
            return "background-color: red; color: white;"
        elif val >= 5:
            return "background-color: orange;"
        elif val >= 3:
            return "background-color: yellow;"
        return "background-color: lightgreen;"

    styled_anomalies = anomalies_df.style.map(
        anomaly_color,
        subset=["risk_score"]
    )

    st.dataframe(
        styled_anomalies,
        use_container_width=True
    )

else:
    st.success("No se detectaron anomalías")

# =========================
# ACTIVIDAD RECIENTE
# =========================

st.header("Actividad reciente del sistema")

recent_response = requests.get(RECENT_EVENTS_URL, timeout=5)

if recent_response.status_code == 200:
    recent_events = recent_response.json()["recent_events"]

    for event in recent_events:
        st.markdown(
            f"""
            **{event['timestamp']}**  
            {event['event_type'].upper()} - {event['message']}
            """
        )

        st.divider()

# =========================
# EVOLUCIÓN MENSUAL DE EVENTOS
# =========================

st.subheader("Evolución mensual de eventos")

events_response = requests.get(EVENTS_URL, timeout=5)

if events_response.status_code == 200:
    events = events_response.json()["events"]

    events_df = pd.DataFrame(events)

    MONTH_FORMAT = "%Y-%m" 
    
    if not events_df.empty:
        events_df["timestamp"] = pd.to_datetime(events_df["timestamp"])
        events_df["mes"] = events_df["timestamp"].dt.strftime(MONTH_FORMAT)

        monthly_stats = events_df.groupby("mes").size()

        st.bar_chart(monthly_stats)
