import streamlit as st
import requests
import pandas as pd
import json

from datetime import time
from pathlib import Path

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

CONFIG_PATH = Path("config/system_config.json")

default_config = {
    "temperature_max": 25,
    "temperature_min": 5,
    "humidity_max": 75,
    "humidity_min": 20,
    "access_start": "06:00",
    "access_end": "21:00",
    "sensor_timeout_minutes": 5,
    "critical_alert_threshold": 8,
    "sms_enabled": False,
    "sms_recipient": "Capitan"
}

if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)
else:
    config = default_config

def str_to_time(value):
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


temp_max = st.number_input(
    "Temperatura máxima (°C)",
    value=config["temperature_max"]
)

temp_min = st.number_input(
    "Temperatura mínima (°C)",
    value=config["temperature_min"]
)

hum_max = st.number_input(
    "Humedad máxima (%)",
    value=config["humidity_max"]
)

hum_min = st.number_input(
    "Humedad mínima (%)",
    value=config["humidity_min"]
)

hora_inicio = st.time_input(
    "Hora de inicio acceso",
    value=str_to_time(config["access_start"])
)

hora_fin = st.time_input(
    "Hora de fin acceso",
    value=str_to_time(config["access_end"])
)

sensor_timeout = st.number_input(
    "Tiempo máximo sin comunicación del sensor (minutos)",
    value=config["sensor_timeout_minutes"]
)

critical_alert_threshold = st.number_input(
    "Nivel mínimo para alerta crítica",
    min_value=1,
    max_value=10,
    value=config["critical_alert_threshold"]
)

sms_enabled = st.checkbox(
    "Activar simulación de SMS",
    value=config["sms_enabled"]
)

sms_recipient = st.text_input(
    "Destinatario de SMS",
    value=config["sms_recipient"]
)

if st.button("Guardar configuración"):

    new_config = {
        "temperature_max": temp_max,
        "temperature_min": temp_min,
        "humidity_max": hum_max,
        "humidity_min": hum_min,
        "access_start": hora_inicio.strftime("%H:%M"),
        "access_end": hora_fin.strftime("%H:%M"),
        "sensor_timeout_minutes": sensor_timeout,
        "critical_alert_threshold": critical_alert_threshold,
        "sms_enabled": sms_enabled,
        "sms_recipient": sms_recipient
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as file:
        json.dump(new_config, file, indent=4)

    st.success("Configuración guardada correctamente")