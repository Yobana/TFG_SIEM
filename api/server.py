from fastapi import FastAPI
import sqlite3

app = FastAPI(title="TFG SIEM API")


@app.get("/")
def home():
    return {"message": "API del SIEM funcionando correctamente"}

@app.get("/events")
def get_events():

    conn = sqlite3.connect("db/siem.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")

    events = cursor.fetchall()

    conn.close()

    return {"events": events}