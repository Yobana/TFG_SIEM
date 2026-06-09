# ===========================================================
# notifications/sms_notifier.py
# Módulo de notificaciones críticas
#  - Servicio de envío de SMS a los responsables de seguridad.
# ===========================================================

import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client

class SMSNotifier:

    '''def __init__(self):
        """
        Inicializa el notificador de SMS, definiendo las rutas de configuración y log.
         - system_config.json: archivo de configuración del sistema, donde se indica si la simulación de SMS está activada y el destinatario.
         - sms_notifications.log: archivo donde se registran las simulaciones de envío de SMS.
        """
        
        base_path = Path(__file__).resolve().parent.parent

        self.config_path = base_path / "config" / "system_config.json"
        self.log_path = base_path / "logs" / "sms_notifications.log"'''


    load_dotenv()

    def send_sms(message: str) -> None:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")
        to_phone = os.getenv("ALERT_PHONE_NUMBER")

        if not all([account_sid, auth_token, from_phone, to_phone]):
            raise ValueError("Faltan variables de entorno para el envío de SMS")

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
    

    # Simulamos el envio de SMS, carga la configuración y envia la notificación
    '''def send_sms(self, message):

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

        return True'''