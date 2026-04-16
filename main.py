# main.py
# **********************************************
# Orquestador principal del SIEM
# **********************************************

import time
import threading

from api.server import run_server
from ingestor.ingestor import LogIngestor
from correlation.engine import CorrelationEngine
from db.db import DatabaseManager

def run_api():
    run_server()


def run_siem():
    ingestor = LogIngestor()
    correlator = CorrelationEngine()
    db = DatabaseManager()

    print("[+] SIEM iniciado")

    while True:
        events = ingestor.read_logs()
        alerts = correlator.correlate(events)

        for event in events:
            db.save_event(event)

        for alert in alerts:
            db.save_alert(alert)

        time.sleep(10)


if __name__ == "__main__":

    api_thread = threading.Thread(
        target=run_api,
        daemon=True
    )
    api_thread.start()

    run_siem()