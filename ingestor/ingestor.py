# Módulo ingestor
# Crea un lector básico de logs, prepara el SIEM para que ingiera archivos de cualquier servicio
# da un módulo que se podrá integrar en la base de datos y el motor de reglas

# ingestor/ingestor.py
# *************************************************
# Módulo Ingestor del SIEM
# Lee logs desde archivos y los normaliza en eventos
# *************************************************

import os
import time

class LogIngestor:

    def __init__(self, log_folder: str ="logs"):
        self.log_folder = log_folder
        self._offsets: dict[str, int] = {} # No reele líneas ya leídas
        os.makedirs(self.log_folder, exist_ok=True)

    def read_logs(self):
        """
        Lee las líneas nuevas de cada .log.
        """
        events = []

        for filename in os.listdir(self.log_folder):

            if filename == "sms_notifications.log":
                continue

            path = os.path.join(self.log_folder, filename)
            
            # Sólo archivos .log
            if not os.path.isfile(path) or not filename.endswith(".log"):
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                # Vamos a la última posición leída
                last_offset = self._offsets.get(path, 0)
                f.seek(last_offset)
                
                for line in f:
                    event = self.normalize_event(
                        line=line.strip(),
                        source=filename
                     )
                    if event:
                        events.append(event)
                # Guardamos la posición
                self._offsets[path] = f.tell()

        return events
    
    def normalize_event(self, line, source):
        """
        Convierte una línea de log en un evento estructurado.
        El formato esperado; timestamp | source | event_type | severity | user_id | access_point |
         deposit_id | device_id | result | message
        """
        if not line:
            return None
        
        parts = [p.strip() for p in line.split("|")]

        # Formato nuevo 10 campos
        if len(parts) != 10:
            print(f"[WARN] Línea ignorada: {line}")
            return None
        
        timestamp, event_source, event_type, severity, user_id, access_point, deposit_id, device_id, result, message = parts
        
        return {
            "timestamp": timestamp,
            "source": event_source,
            "event_type": event_type,
            "severity": severity,
            "user_id": user_id,
            "access_point": access_point,
            "deposit_id": deposit_id,
            "device_id": device_id,
            "result": result,
            "message": message
        }


    def watch(self, interval=5, iterations=2):
        """
        Modo pruebas: ejecuta la ingesta un número limitado de veces.
        """
        print("[INFO] Ingestor iniciado")

        for i in range(iterations):
            events = self.read_logs()
            print(f"[INFO] Iteración {i+1}: {len(events)} eventos")

            for event in events:
                print(event)

            time.sleep(interval)

if __name__ == "__main__":
    ingestor = LogIngestor()
    #ingestor.watch()
    ingestor.watch(interval=10, iterations=5)