# ==========================================================================
# main.py
# Autor: Yobana Nido Álvarez
# TFG, Universidad de Burgos, 2025-2026
#
# Orquestador principal del SIEM
#  - Inicializa los módulos del sistema.
#  - Ejecuta el ciclo continuo de monitorización, correlación y notificación.
#  - Mantiene y actualiza el estado de los sensores.
# ==========================================================================

import time

from ingestor.ingestor import LogIngestor
from correlation.engine import CorrelationEngine
from db.db import DatabaseManager
from sensors.status_manager import (
    update_sensor_status,
    check_inactive_sensors,
    print_sensor_status
)
from notifications.sms_notifier import SMSNotifier


def run_siem():
    """
    Función principal del SIEM
    
    Inicializa los módulos del sistema y ejecuta el
    ciclo continuo de monitorización, correlación y notificación.
    """

    ingestor = LogIngestor()
    correlator = CorrelationEngine()
    db = DatabaseManager()
    sms_notifier = SMSNotifier()

    print("[+] SIEM iniciado")

    # Bucle principal de monitorización
    while True:
        events = ingestor.read_logs()
        alerts = correlator.correlate(events)

        # Procesamos los eventos y los almacenamos en la BD
        for event in events:
            print("[EVENTO]", event)

            # Actualizar estado de sensores
            if event["event_type"] in ["intrusion", "environment"]:
                update_sensor_status(event["device_id"])
            db.save_event(event)
        
        inactive_sensors = check_inactive_sensors()
        
        if events:
            print_sensor_status()

        for sensor in inactive_sensors:
            print("[WARNING] Sensor inactivo:", sensor)
        
        # Procesamos las alertas generadas por el motor de correlación
        for alert in alerts:
            print("[ALERTA]", alert)
            db.save_alert(alert)

            if alert.get("risk_score", 0) >= 8:
                sms_notifier.send_sms(
                    alert["message"]
                )

        time.sleep(3)


if __name__ == "__main__":
    run_siem()