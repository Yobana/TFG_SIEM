"""
Módulo básico de detección de anomalías.

Analiza eventos almacenados en SQLite y detecta
situaciones potencialmente anómalas.
"""

import sqlite3


class AnomalyDetector:

    def __init__(self):
        self.db_path = "db/siem.db"

    def detect_anomalies(self):

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        anomalies = []

        # =====================================
        # Temperaturas elevadas
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

            if "30" in message or "35" in message:

                anomalies.append({
                    "type": "high_temperature",
                    "severity": "WARNING",
                    "message": message
                })

        # =====================================
        # Accesos denegados
        # =====================================

        cursor.execute("""
            SELECT *
            FROM events
            WHERE result = 'denied'
        """)

        denied_events = cursor.fetchall()

        if len(denied_events) >= 3:

            anomalies.append({
                "type": "multiple_denied_access",
                "severity": "CRITICAL",
                "message": f"Se detectaron {len(denied_events)} accesos denegados"
            })

        conn.close()

        return anomalies