# ingestor/ingestor.py
# --------------------------------------------------
# Módulo Ingestor del SIEM
# Lee logs desde archivos y los normaliza en eventos
# --------------------------------------------------

import os
from datetime import datetime


class LogIngestor:
    """
    Clase encargada de la ingesta de logs desde una carpeta.
    """

    def __init__(self, log_folder="logs"):
        self.log_folder = log_folder
        os.makedirs(self.log_folder, exist_ok=True)

    def read_logs(self):
        """
        Lee todos los archivos .log de la carpeta y devuelve
        una lista de eventos normalizados (dict).
        """
        events = []

        for filename in os.listdir(self.log_folder):
            path = os.path.join(self.log_folder, filename)

            if not os.path.isfile(path) or not filename.endswith(".log"):
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    event = self.normalize_event(
                        line=line.strip(),
                        source=filename
                    )
                    if event:
                        events.append(event)
        return events

    def normalize_event(self, line, source):
        """
        Convierte una línea de log en un evento estructurado.
        """
        if not line:
            return None

        event_type = "generic"
        severity = "INFO"

        if "FAILED" in line or "ERROR" in line:
            event_type = "authentication"
            severity = "WARNING"

        if "LOGIN OK" in line:
            event_type = "authentication"
            severity = "INFO"

        if "SCAN" in line or "PORT" in line:
            event_type = "network"
            severity = "CRITICAL"

        return {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "event_type": event_type,
            "severity": severity,
            "message": line
        }


if __name__ == "__main__":
    ingestor = LogIngestor()
    events = ingestor.read_logs()
    print(f"[INFO] Eventos leídos: {len(events)}")
    for event in events:
        print(event)