"""
Módulo de notificaciones críticas.

Actualmente simula el envío de SMS
a responsables de seguridad.
"""


class SMSNotifier:

    def send_sms(self, recipient, message):

        print(
            f"[SMS] Enviado a {recipient}: {message}"
        )

        return True