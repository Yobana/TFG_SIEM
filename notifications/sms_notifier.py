# ===========================================================
# notifications/sms_notifier.py
# Módulo de notificaciones críticas
#  - Servicio de envío de SMS al Jefe del Polvorín
# ===========================================================

import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client

class SMSNotifier:

    def __init__(self):

        load_dotenv()

        base_path = Path(__file__).resolve().parent.parent

        self.config_path = base_path / "config" / "system_config.json"
        self.log_path = base_path / "logs" / "sms_notifications.log"

    def send_sms(self, message: str) -> bool:

        # Comprobamoms la configuración si esta activado el envío de SMS
        if not self.config_path.exists():
            print("[SMS] No se encuentra system_config.json")
            return False

        with open(self.config_path, "r", encoding="utf-8") as file:
            config = json.load(file)

        if not config.get("sms_enabled", False):
            print("[SMS] Envío de SMS desactivado")
            return False
        
        # Cogemos los credenciales de Twilio
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")
        to_phone = os.getenv("ALERT_PHONE_NUMBER")


        if not all([account_sid, auth_token, from_phone, to_phone]):
            raise ValueError("Faltan variables de entorno para el envío de SMS")

        # Envío de SMS con Twilio
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )

        # Guardamos los SMS enviados en un fichero log
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.log_path, "a", encoding="utf-8") as log:
            log.write(
                f"{datetime.now().isoformat()} - SMS enviado a {to_phone}: {message}\n"
            )

        print("[SMS] SMS enviado correctamente")
        return True
    