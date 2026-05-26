"""
Módulo básico de detección de anomalías.

Analiza eventos almacenados en SQLite y detecta
situaciones potencialmente anómalas.
"""

import sqlite3
from datetime import datetime


class AnomalyDetector:

    def __init__(self):
        self.db_path = "db/siem.db"

    def detect_anomalies(self):

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        anomalies = []

        # =====================================
        # Temperaturas fuera de rango
        # =====================================

        cursor.execute("""
            SELECT *
            FROM events
            WHERE event_type = 'environment'
            AND message LIKE '%Temperatura%'
        """)

        temperature_events = cursor.fetchall()

        for event in temperature_events:
            message = event["message"]

            if "elevada" in message.lower() or "baja" in message.lower():
                anomalies.append({
                    "type": "temperature_anomaly",
                    "severity": "WARNING",
                    "message": message
                })

        # =====================================
        # Humedad fuera de rango
        # =====================================

        cursor.execute("""
            SELECT *
            FROM events
            WHERE event_type = 'environment'
            AND message LIKE '%Humedad%'
        """)

        humidity_events = cursor.fetchall()

        for event in humidity_events:
            message = event["message"]

            if "elevada" in message.lower() or "baja" in message.lower():
                anomalies.append({
                    "type": "humidity_anomaly",
                    "severity": "WARNING",
                    "message": message
                })

        # =====================================
        # Accesos denegados múltiples
        # =====================================

        cursor.execute("""
            SELECT *
            FROM events
            WHERE result = 'denied'
        """)

        denied_events = cursor.fetchall()

        if len(denied_events) >= 3:anomalies.append({
                "type": "multiple_denied_access",
                "severity": "CRITICAL",
                "message": f"Se detectaron {len(denied_events)} accesos denegados"
            })

        # =====================================
        # Accesos fuera de horario
        # =====================================

        cursor.execute("""
            SELECT *
            FROM events
            WHERE event_type = 'access'
        """)

        access_events = cursor.fetchall()

        for event in access_events:
            
            timestamp = event["timestamp"]
            message = event["message"].lower()

            try:
                event_time = datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M:%S"
                )

                hour = event_time.hour

                if hour < 6 or hour >= 21 or "fuera de horario" in message:
                    anomalies.append({
                        "type": "out_of_schedule_access",
                        "severity": "CRITICAL",
                        "message": f"Acceso fuera de horario detectado en {event['access_point']} - {timestamp}"
                    })

            except ValueError:
                pass

        conn.close()

        return anomalies