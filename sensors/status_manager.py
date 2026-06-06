# =========================================================
# sensors/status_manager.py
# Módulo de gestión de estado de sensores del Sistema SIEM.
# - Registro de última comunicación de cada sensor.
# - Detección de sensores inactivos mediante timeout.
# - Consulta del estado actual de los dispositivos monitorizados.
# =========================================================

from datetime import datetime, timedelta

SENSOR_TIMEOUT_MINUTES = 5

sensor_status = {}


def update_sensor_status(device_id):
    sensor_status[device_id] = {
        "status": "active",
        "last_seen": datetime.now()
    }


def check_inactive_sensors():
    inactive_sensors = []
    now = datetime.now()

    for device_id, data in sensor_status.items():
        last_seen = data["last_seen"]

        if now - last_seen > timedelta(minutes=SENSOR_TIMEOUT_MINUTES):
            data["status"] = "inactive"
            inactive_sensors.append(device_id)

    return inactive_sensors


def get_sensor_status():
    return sensor_status

def print_sensor_status():
    """Muestra por consola el estado actual de los sensores monitorizados."""

    print("\n[ESTADO SENSORES]")

    if not sensor_status:
        print("No hay sensores registrados.")
        return

    for device_id, data in sensor_status.items():
        print(
            f"{device_id} | "
            f"Estado: {data['status']} | "
            f"Última comunicación: {data['last_seen']}"
        )