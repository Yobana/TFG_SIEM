# Módulo de correlación de eventos
# Analiza eventos normalizados y genera alertas según las reglas implementadas
# *************************************************
# correlation/engine.py
# *************************************************

import re

from config.settings import (
    TEMPERATURE_MAX,
    HUMIDITY_MAX
)

class CorrelationEngine:
    """
    Motor de correlación de eventos

    Recibe una lista de eventos normalizados por el ingestor y devuelve
    una lista de alertas cuando detecta las situaciones según las reglas
    implementadas que consideramos peligrosas.
    """
    def extract_numeric_value(self, message):
        """
        Extrae el primer valor numérico encontrado en el mensaje del evento.
        """
        match = re.search(r"(\d+(?:\.\d+)?)", message)

        if match:
            return float(match.group(1))

        return None
    
    def correlate(self, events):
        """
        Aplicamos reglas de correlación sobre los eventos que recibimos
        """
        alerts = []

        for event in events:
            event_type = event.get("event_type")
            result = event.get("result")
            severity = event.get("severity")
            deposit_id = event.get("deposit_id")
            device_id = event.get("device_id")
            access_point = event.get("access_point")
            message = event.get("message", "")

            # Regla 1: Apertura de depósito
            if event_type == "intrusion" and result == "opened":
                alerts.append({
                    "alert_type": "door_opened",
                    "severity": "CRITICAL",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Apertura detectada en el depósito {deposit_id}"
                })

            # Regla 2: Temperatura elevada
            if event_type == "environment" and "temp" in device_id:
                value = self.extract_numeric_value(message)

                if value is not None and value > TEMPERATURE_MAX:
                    alerts.append({
                        "alert_type": "temperature_alert",
                        "severity": "WARNING",
                        "deposit_id": deposit_id,
                        "device_id": device_id,
                        "message": f"Temperatura elevada en el depósito {deposit_id}: {value}ºC"
                    })
            
            # Regla 3: Humedad elevada
            if event_type == "environment" and "hum" in device_id:
                value = self.extract_numeric_value(message)

                if value is not None and value > HUMIDITY_MAX:
                    alerts.append({
                        "alert_type": "humidity_alert",
                        "severity": "WARNING",
                        "deposit_id": deposit_id,
                        "device_id": device_id,
                        "message": f"Humedad elevada en el depósito {deposit_id}: {value}%"
                    })

            # Regla 4: Detección de movimiento en un depósito
            if event_type == "intrusion" and result == "detected":
                alerts.append({
                    "alert_type": "movement_detected",
                    "severity": "CRITICAL",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Movimiento detectado en {access_point}"
                })
                
            # Regla 5: Fallo en la comunicación del módulo
            if event_type == "system" and result == "failed":
                alerts.append({
                    "alert_type": "system_failure",
                    "severity": "ERROR",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Fallo del sistema en el dispositivo {device_id}"
                })

            # Regla 6: Fallo crítico del sistema eléctrico
            if event_type == "power" and severity == "CRITICAL":
                alerts.append({
                    "alert_type": "power_failure",
                    "severity": "CRITICAL",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": "Fallo crítico en el sistema eléctrico"
                })

        return alerts     