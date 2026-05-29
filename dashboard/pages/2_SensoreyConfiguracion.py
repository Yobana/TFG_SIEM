import streamlit as st
import requests
import pandas as pd

from datetime import time

# URLs
SENSORS_URL = "http://127.0.0.1:8000/sensors/status"

st.title("Sensores y configuración")

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

    if not sensors_df.empty:

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
    else:
        st.info("No hay sensores registrados.")
else:
    st.error("No se pudo conectar con la API de sensores")


# =========================
# CONFIGURACIÓN
# =========================

st.header("Configuración")

temp_max = st.number_input(
    "Temperatura máxima (°C)",
    value=25
)

temp_min = st.number_input(
    "Temperatura mínima (°C)",
    value=5
)

hum_max = st.number_input(
    "Humedad máxima (%)",
    value=70
)

hum_min = st.number_input(
    "Humedad mínima (%)",
    value=20
)

hora_inicio = st.time_input(
    "Hora de inicio acceso",
    value=time(6,0)
)

hora_fin = st.time_input(
    "Hora de fin acceso",
    value=time(21,0)
)

sensor_timeout = st.number_input(
    "Tiempo máximo sin comunicación del sensor (minutos)",
    value=5
)

if st.button("Guardar configuración"):
    st.success("Configuración guardada correctamente")