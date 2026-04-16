# Módulo ingestor
# Crea un lector básico de logs, prepara el SIEM para que ingiera archivos de cualquier servicio
# da un módulo que se podrá integrar en la base de datos y el motor de reglas

# ingestor/ingestor.py
# *************************************************
# Módulo Ingestor del SIEM
# Lee logs desde arvhicos y los normaliza en eventos
# *************************************************

from pathlib import Path
from datetime import datetime

class LogIngestor:

    def __init__(self, log_file="logs/test.log"):
        self.log_file = log_file

    def parse_line(self, line, source):
        """
        Convierte una línea de log en un evento básico.
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "event_type": "log",
            "severity": "info",
            "message": line.strip()
        }


    def read_logs(self):
        """
        Lee un archivo de log y devuelve una lista de eventos.
        """
        events = []

        path = Path(self.log_file)
        if not path.exists():
            print(f"Archivo no encontrado: {self.log_file}")
            return events

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    events.append(self.parse_line(line, path.name))

        return events