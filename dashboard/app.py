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

col1, col2 = st.columns([4, 1])

with col1:
    st.title("Sistema SIEM - Polvorín militar simulado")
    st.markdown(
        "Monitorización de eventos de seguridad, sensores y alertas del entorno simulado."
    )
    st.caption(
        f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )

with col2:
    st.image(
        "dashboard/images/polvorin.png",
        width=300
    )

# Auto-refresco cada 10 segundos
st_autorefresh(interval=10000, key="dashboard_refresh")

# URLs API
EVENTS_URL = "http://127.0.0.1:8000/events?limit=20"
ALERTS_URL = "http://127.0.0.1:8000/alerts?limit=20"
STATS_URL = "http://127.0.0.1:8000/stats"
SENSORS_URL = "http://127.0.0.1:8000/sensors/status"
ANOMALIES_URL = "http://127.0.0.1:8000/anomalies"

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
# ALERTAS
# =========================

st.header("Alertas")

alerts_response = requests.get(ALERTS_URL)

if alerts_response.status_code == 200:
    alerts = alerts_response.json()["alerts"]

    alerts_df = pd.DataFrame(alerts)

    # Filtro severidad
    severity_filter = st.selectbox(
        "Filtrar severidad",
        ["Todas", "CRITICAL", "ERROR", "WARNING", "INFO"]
    )

    if severity_filter != "Todas":
        alerts_df = alerts_df[
            alerts_df["severity"] == severity_filter
        ]

    # Coloreamos
    def color_severity(val):
        if val == "CRITICAL":
            return "background-color: red; color: white;"
        elif val == "ERROR":
            return "background-color: orange;"
        elif val == "WARNING":
            return "background-color: yellow;"
        return ""

    styled_df = alerts_df.style.map(
        color_severity,
        subset=["severity"]
    )

    st.dataframe(styled_df, use_container_width=True)

# Gráfico 
st.subheader("Distribución de alertas por severidad")
severity_counts = alerts_df["severity"].value_counts()
st.plotly_chart(
    {
        "data": [
            {
                "values": severity_counts.values,
                "labels": severity_counts.index,
                "type": "pie",
                "hole": 0.4
            }
        ],
        "layout": {
            "title": "Alertas por severidad"
        }
    },
    use_container_width=True
)


# =========================
# EVENTOS
# =========================

st.header("Eventos")

events_response = requests.get(EVENTS_URL)

if events_response.status_code == 200:
    events = events_response.json()["events"]

    events_df = pd.DataFrame(events)

    # Coloreamos
    def color_event_severity(val):
        if val == "CRITICAL":
            return "background-color: red; color: white;"
        elif val == "ERROR":
            return "background-color: orange;"
        elif val == "WARNING":
            return "background-color: yellow;"
        elif val == "INFO":
            return "background-color: lightblue;"
        return ""

    styled_events_df = events_df.style.map(   
        color_event_severity,
        subset=["severity"]
    )

    st.dataframe(styled_events_df, use_container_width=True)

    # Gráfico
    st.subheader("Distribución de eventos por tipo")

    event_type_counts = events_df["event_type"].value_counts()

    st.plotly_chart(
        {
            "data": [
                {
                    "values": event_type_counts.values,
                    "labels": event_type_counts.index,
                    "type": "pie",
                    "hole": 0.4
                }
            ],
            "layout": {
                "title": "Eventos por tipo"
            }
        },
        use_container_width=True
    )

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
col3.metric("Inactivos", summary["inactive"])

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

        def anomaly_color(val):
            if val == "CRITICAL":
                return "background-color: red; color: white;"
            elif val == "WARNING":
                return "background-color: yellow;"
            return ""

        styled_anomalies = anomalies_df.style.map(
            anomaly_color,
            subset=["severity"]
        )

        st.dataframe(
            styled_anomalies,
            use_container_width=True
        )

    else:
        st.success("No se detectaron anomalías")
