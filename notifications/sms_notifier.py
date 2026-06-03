# ===========================================================
# notifications/sms_notifier.py
# Módulo de notificaciones críticas (simulación de SMS)
#  - Simula el envío de SMS a los responsables de seguridad.
# ===========================================================

import json
from pathlib import Path
from datetime import datetime

class SMSNotifier:

    def __init__(self):
        base_path = Path(__file__).resolve().parent.parent

        self.config_path = base_path / "config" / "system_config.json"
        self.log_path = base_path / "logs" / "sms_notifications.log"

    # Simulamos el envio de SMS, carga la configuración y envia la notificación
    def send_sms(self, message):

        if not self.config_path.exists():
            print("[SMS] No se encuentra system_config.json")
            return False
        
        with open(self.config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
        
        if not config.get("sms_enabled", False):
            print("[SMS] Simulación SMS desactivada")
            return False

        recipient = config.get("sms_recipient", "Responsable")

        sms_text = (f"[SMS] Enviado a {recipient}: {message}\n")

        print(sms_text)

        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.log_path, "a", encoding="utf-8") as log:
            log.write(f"{datetime.now().isoformat()} - {sms_text}")    

        return True