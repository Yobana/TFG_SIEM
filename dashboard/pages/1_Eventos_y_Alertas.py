# ==========================================================
# Dashboard de eventos y alertas
# - Muestra las alertas y eventos registrados en el sistema.
# - Permite filtrar por severidad y depósito
# - Colorea las filas según la severidad
# ==========================================================

import streamlit as st
import requests
import pandas as pd

# URLs
EVENTS_URL = "http://127.0.0.1:8000/events?limit=500"
ALERTS_URL = "http://127.0.0.1:8000/alerts?limit=500"

st.title("Eventos y alertas")

# =========================
# ALERTAS
# =========================

st.header("Alertas")

alerts_response = requests.get(ALERTS_URL)

if alerts_response.status_code == 200:
    alerts = alerts_response.json()["alerts"]

    alerts_df = pd.DataFrame(alerts)

    if not alerts_df.empty:
        alerts_df = alerts_df.sort_values(
            by="id",
            ascending=False
        )

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
    else:
        st.info("No hay alertas registradas.")
else:
    st.error("No se pudo conectar con la API de alertas.")
    
# =========================
# EVENTOS
# =========================

st.header("Eventos")

events_response = requests.get(EVENTS_URL)

if events_response.status_code == 200:
    events = events_response.json()["events"]

    events_df = pd.DataFrame(events)

    deposit_filter = st.selectbox(
        "Filtrar por depósito",
        ["Todos"] + sorted(events_df["deposit_id"].dropna().unique().tolist())
    )

    if deposit_filter != "Todos":
        events_df = events_df[
            events_df["deposit_id"] == deposit_filter
        ]
    
    events_df["timestamp"] = pd.to_datetime(events_df["timestamp"])

    events_by_hour = events_df.groupby(
        events_df["timestamp"].dt.hour
    ).size()

    events_df = events_df.sort_values(
        by="id",
        ascending=False
    )

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
    
    st.subheader("Eventos por hora")
    st.line_chart(events_by_hour)

