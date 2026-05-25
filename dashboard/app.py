import streamlit as st
import requests
import pandas as pd

# Configuración página
st.set_page_config(
    page_title="TFG SIEM Dashboard",
    layout="wide"
)

st.title("TFG SIEM - Dashboard de Monitorización")

# URLs API
EVENTS_URL = "http://127.0.0.1:8000/events"
ALERTS_URL = "http://127.0.0.1:8000/alerts"
STATS_URL = "http://127.0.0.1:8000/stats"

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

    st.dataframe(alerts_df, use_container_width=True)

# =========================
# EVENTOS
# =========================

st.header("Eventos")

events_response = requests.get(EVENTS_URL)

if events_response.status_code == 200:
    events = events_response.json()["events"]

    events_df = pd.DataFrame(events)

    st.dataframe(events_df, use_container_width=True)