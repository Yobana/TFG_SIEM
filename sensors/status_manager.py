"""
Módulo encargado de gestionar el estado de los sensores del sistema SIEM.

Permite:
- Registrar la última comunicación de cada sensor.
- Detectar sensores inactivos mediante timeout.
- Consultar el estado actual de los dispositivos monitorizados.
"""

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