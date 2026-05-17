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

@app.get("/sensors/status")
def get_sensor_status():

    conn = sqlite3.connect("db/siem.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sensor_status")

    sensors = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {"sensors": sensors}