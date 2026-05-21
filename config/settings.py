# config/settings.py
# --------------------------------------------------
# Configuración general del SIEM
# --------------------------------------------------

# Ruta de la carpeta de logs
LOG_FOLDER = "logs"

# Ruta de la base de datos
DB_PATH = "db/siem.db"

# API Key para autenticación
API_KEY = "siem-tfg-2026"

# Puerto de la API
API_PORT = 8000

# Configuración ambiental
TEMPERATURE_MAX = 25
TEMPERATURE_MIN = 5

HUMIDITY_MAX = 75
HUMIDITY_MIN = 20