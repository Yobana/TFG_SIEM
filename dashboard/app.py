import streamlit as st
import requests
import pandas as pd

from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# Configuración página
st.set_page_config(
    page_title="TFG SIEM Dashboard",
    layout="wide"
)

st.title("Sistema SIEM - Polvorín militar simulado")
st.markdown(
    "Monitorización de eventos de seguridad, sensores y alertas del entorno simulado."
)

st.caption(
    f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
)

# URLs API
STATS_URL = "http://127.0.0.1:8000/stats"
SENSORS_URL = "http://127.0.0.1:8000/sensors/status"
ANOMALIES_URL = "http://127.0.0.1:8000/anomalies"

# Obtener anomalías
anomalies_response = requests.get(ANOMALIES_URL)

total_anomalies = 0
max_risk_score = 0

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
sensors_response = requests.get(SENSORS_URL)

inactive_sensors = 0

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

# Auto-refresco cada 10 segundos
st_autorefresh(interval=10000, key="dashboard_refresh")

# =========================
# ESTADÍSTICAS
# =========================

st.header("Estadísticas generales")

stats_response = requests.get(STATS_URL)

if stats_response.status_code == 200:
    stats = stats_response.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Eventos", stats["total_events"])
    col2.metric("Alertas", stats["total_alerts"])
    col3.metric("Alertas críticas", stats["critical_alerts"])


# =========================
# SENSORES
# =========================

st.header("Estado de sensores")

sensors_response = requests.get(SENSORS_URL)

if sensors_response.status_code == 200:

    data = sensors_response.json()
    summary = data["summary"]
    sensors = data["sensors"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total dispositivos", summary["total_sensors"])
    col2.metric("Activos", summary["active"])
    col3.metric("Inactivos / Sin comunicación", summary["inactive"])

    sensors_df = pd.DataFrame(sensors)

    def sensor_status_color(val):
        if val == "active":
            return "background-color: lightgreen;"
        elif val == "inactive":
            return "background-color: red; color: white;"
        return ""

    styled_sensors = sensors_df.style.map(
        sensor_status_color,
        subset=["status"]
    )

    st.dataframe(
        styled_sensors,
        use_container_width=True
    )

# =========================
# ANOMALÍAS
# =========================

st.header("Detección de anomalías")

anomalies_response = requests.get(ANOMALIES_URL)

if anomalies_response.status_code == 200:

    anomalies_data = anomalies_response.json()

    total_anomalies = anomalies_data["total_anomalies"]

    anomalies = anomalies_data["anomalies"]

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

recent_response = requests.get(
    "http://127.0.0.1:8000/events/recent"
)

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
