# =============================================================================
# api/server.py
# API del Sistema SIEM
#  - Proporciona endpoints para consultar eventos, alertas, estado de sensores,
#    estadísticas y anomalías detectadas para visualizar en el dashboard.
# =============================================================================

import sqlite3

from fastapi import FastAPI
from machine.anomaly_detector import AnomalyDetector

app = FastAPI(title="TFG SIEM API")
anomaly_detector = AnomalyDetector()

@app.get("/")
def home():
    return {"message": "API del SIEM funcionando correctamente"}

@app.get("/events")
def get_events(limit: int = 20):

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))

    events = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {"events": events}

@app.get("/alerts")
def get_alerts(limit: int = 20):

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,))

    alerts = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {"alerts": alerts}

@app.get("/alerts/severity/{severity}")
def get_alerts_by_severity(severity: str):

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM alerts WHERE severity = ?",
        (severity.upper(),)
    )

    alerts = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {"alerts": alerts}

@app.get("/sensors/status")
def get_sensors_status():

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Inventario de sensores esperados
    expected_sensors = []

    # Generamos los sensores de cada depósito
    for i in range(1, 21):
        deposit = f"d{i:02d}"

        expected_sensors.extend([
            f"temp_{deposit}",
            f"hum_{deposit}",
            f"magnetico_{deposit}",
            f"volumetrico_{deposit}"
        ])
    # Generamos el inventario de las cámaras de seguridad
    for i in range(1, 15):
        expected_sensors.append(f"camara_{i:02d}")
    
    cursor.execute("""
        SELECT 
            e.device_id,
            e.id as last_event_id,
            e.result as last_result

        FROM events e

        INNER JOIN (
            SELECT 
                device_id,
                MAX(id) as max_id

            FROM events

            WHERE device_id IS NOT NULL
            AND device_id != '-'

            GROUP BY device_id

        ) latest

        ON e.device_id = latest.device_id
        AND e.id = latest.max_id
    """)

    # Guardamos el último estado de cada sensor
    last_events = {}

    for row in cursor.fetchall():
        last_events[row["device_id"]] = {
            "last_event_id": row["last_event_id"],
            "last_result": row["last_result"]
        }

    sensors = []

    # Estado actual de cada sensor comparando el inventario esperado con los últimos eventos.
    for device_id in expected_sensors:

        if device_id in last_events:

            status = "inactive" if last_events[device_id]["last_result"] == "failed" else "active"

            last_event_id = last_events[device_id]["last_event_id"]

        else:

            status = "inactive"
            last_event_id = None

        sensors.append({
            "device_id": device_id,
            "status": status,
            "last_event_id": last_event_id
        })

    conn.close()

    # Resumen general del estado para mostrar en el dashboard.
    summary = {
        "total_sensors": len(sensors),
        "active": len([s for s in sensors if s["status"] == "active"]),
        "inactive": len([s for s in sensors if s["status"] == "inactive"])
    }

    return {
        "sensors": sensors,
        "summary": summary
    }

@app.get("/stats")
def get_stats():

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    total_events = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE severity = 'CRITICAL'"
    )
    critical_alerts = cursor.fetchone()[0]

    conn.close()

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts
    }

@app.get("/events/recent")
def get_recent_events():

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM events ORDER BY id DESC LIMIT 5"
    )

    events = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {"recent_events": events}

# Endpoint para obtener las últimas anomalías detectadas por el modelo de ML
# almacenadas en la base de datos, para visualizarlas en el dashboard y alertar al usuario.
@app.get("/anomalies")
def get_anomalies():

    # Ejecutamos el detector de anomalías
    anomalies = anomaly_detector.detect_anomalies()

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    }

@app.get("/database/schema")
def get_database_schema():

    conn = sqlite3.connect("db/siem.db")
    cursor = conn.cursor()

    schema = {}

    for table in ["events", "alerts"]:

        cursor.execute(f"PRAGMA table_info({table})")

        columns = []

        for column in cursor.fetchall():
            columns.append({
                "name": column[1],
                "type": column[2]
            })

        schema[table] = columns

    conn.close()

    return {"schema": schema}