from fastapi import FastAPI
import sqlite3
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

    # Inventario de sensores esperado
    expected_sensors = []

    for i in range(1, 21):
        deposit = f"d{i:02d}"

        expected_sensors.extend([
            f"temp_{deposit}",
            f"hum_{deposit}",
            f"magnetico_{deposit}",
            f"volumetrico_{deposit}"
        ])

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

    last_events = {}

    for row in cursor.fetchall():
        last_events[row["device_id"]] = {
            "last_event_id": row["last_event_id"],
            "last_result": row["last_result"]
        }

    sensors = []

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

@app.get("/anomalies")
def get_anomalies():

    anomalies = anomaly_detector.detect_anomalies()

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    }