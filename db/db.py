"""
Módulo encargado de gestionar el almacenamiento en base de datos SQLite.

Permite:
- Crear las tablas necesarias del sistema.
- Guardar eventos procesados por el SIEM.
- Guardar alertas generadas por el motor de correlación.
"""

import sqlite3

from config.settings import DB_PATH


class DatabaseManager:
    """
    Gestor de base de datos SQLite del SIEM.
    """

    def __init__(self):
        self.db_path = DB_PATH
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    source TEXT,
                    event_type TEXT,
                    severity TEXT,
                    user_id TEXT,
                    access_point TEXT,
                    deposit_id TEXT,
                    device_id TEXT,
                    result TEXT,
                    message TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_type TEXT,
                    severity TEXT,
                    risk_score INTEGER, 
                    status TEXT,
                    deposit_id TEXT,
                    device_id TEXT,
                    message TEXT
                )
            """)

            conn.commit()

    def save_event(self, event):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO events (
                    timestamp, source, event_type, severity, user_id,
                    access_point, deposit_id, device_id, result, message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.get("timestamp"),
                event.get("source"),
                event.get("event_type"),
                event.get("severity"),
                event.get("user_id"),
                event.get("access_point"),
                event.get("deposit_id"),
                event.get("device_id"),
                event.get("result"),
                event.get("message")
            ))

            conn.commit()

    def save_alert(self, alert):
        with self.connect() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO alerts (
                    alert_type, 
                    severity, 
                    risk_score, 
                    status, 
                    deposit_id, 
                    device_id, 
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.get("alert_type"),
                alert.get("severity"),
                alert.get("risk_score"),
                alert.get("status"),
                alert.get("deposit_id"),
                alert.get("device_id"),
                alert.get("message")
            ))

            conn.commit()