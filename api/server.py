from fastapi import FastAPI
import sqlite3

app = FastAPI(title="TFG SIEM API")


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

    cursor.execute("""
        SELECT device_id, MAX(id) as last_event_id
        FROM events
        WHERE device_id IS NOT NULL
        AND device_id != '-'
        AND (
            device_id LIKE 'temp_%'
            OR device_id LIKE 'hum_%'
            OR device_id LIKE 'magnetico_%'
            OR device_id LIKE 'volumetrico_%'
            OR device_id LIKE 'camara_%'
        )
        GROUP BY device_id
        ORDER BY device_id
    """)

    sensors = []

    for row in cursor.fetchall():
        sensors.append({
            "device_id": row["device_id"],
            "status": "active",
            "last_event_id": row["last_event_id"]
        })

    conn.close()

    summary = {
    "total_sensors": len(sensors),
    "active": len([s for s in sensors if s["status"] == "active"]),
    "inactive": len([s for s in sensors if s["status"] == "inactive"])
    }
    
    return {"sensors": sensors, "summary": summary}

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