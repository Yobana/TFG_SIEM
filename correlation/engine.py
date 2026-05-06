# Módulo de correlación de eventos
# Analiza eventos normalizados y genera alertas según las reglas implementadas
# *************************************************
# correlation/engine.py
# *************************************************

class CorrelationEngine:
    """
    Motor de correlación de eventos

    Recibe una lista de eventos normalizados por el ingestor y devuelve
    una lista de alertas cuando detecta las situaciones según las reglas
    implementadas que consideramos peligrosas.
    """

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

            # Regla 1: Apertura de depósito
            if event_type == "intrusion" and result == "opened":
                alerts.append({
                    "alert_type": "door_opened",
                    "severity": "CRITICAL",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Apertura detectada en el depósito {deposit_id}"
                })

            # Regla 2: Fallo en sensores, temperatura o humedad
            if event_type == "environment" and result == "high":
                alerts.append({
                    "alert_type": "environment_alert",
                    "severity": "WARNING",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Condición ambiental elevada en el depósito {deposit_id}"
                })

            # Regla 3: Detección de movimiento en un depósito
            if event_type == "intrusion" and result == "detected":
                alerts.append({
                    "alert_type": "movement_detected",
                    "severity": "CRITICAL",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Movimiento detectado en {access_point}"
                })
                
            # Regla 4: Fallo en la comunicación del módulo
            if event_type == "system" and result == "failed":
                alerts.append({
                    "alert_type": "system_failure",
                    "severity": "ERROR",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": f"Fallo del sistema en el dispositivo {device_id}"
                })

            # Regla 5: Fallo crítico del sistema eléctrico
            if event_type == "power" and severity == "CRITICAL":
                alerts.append({
                    "alert_type": "power_failure",
                    "severity": "CRITICAL",
                    "deposit_id": deposit_id,
                    "device_id": device_id,
                    "message": "Fallo crítico en el sistema eléctrico"
                })

        return alerts     