# main.py
# **********************************************
# Orquestador principal del SIEM
# **********************************************

import time
import threading

from ingestor.ingestor import LogIngestor
from correlation.engine import CorrelationEngine
# from api.server import run_server
from db.db import DatabaseManager
from sensors.status_manager import (
    update_sensor_status,
    check_inactive_sensors,
    print_sensor_status
)

"""def run_api():
    run_server()"""


def run_siem():
    ingestor = LogIngestor()
    correlator = CorrelationEngine()
    db = DatabaseManager()

    print("[+] SIEM iniciado")

    while True:
        events = ingestor.read_logs()
        alerts = correlator.correlate(events)

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
        
        for alert in alerts:
            print("[ALERTA]", alert)
            db.save_alert(alert)

        time.sleep(3)


if __name__ == "__main__":

    """api_thread = threading.Thread(
        target=run_api,
        daemon=True
    )
    api_thread.start()"""

    run_siem()