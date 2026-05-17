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
def get_sensor_status():

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sensor_status")

    sensors = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {"sensors": sensors}

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