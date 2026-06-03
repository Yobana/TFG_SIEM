# TFG – SIEM Ligero en Raspberry Pi

Trabajo Fin de Grado – Ingeniería Informática 
Universidad de Burgos - 2026
Autor: Yobana Nido Álvarez

## Descripción

Este proyecto consiste en el desarrollo de un sistema SIEM (Security Information and Event Management) ligero, diseñado para ejecutarse en una Raspberry Pi.

El sistema simula un entorno de seguridad en un Polvorín Militar, permitiendo la monitorización de eventos,el análisis de actividad y la detección de situaciones potencialmente peligrosas mediante reglas de correlación y supervisión de sensores.

La solución ha sido desarrollada siguiendo una arquitectura modular, permitiendo su ampliación futura mediante dashboards web, APIs REST y módulos de detección de anomalías mediante Machine Learning.

## Funcionalidades actuales
- Ingesta de logs desde archivos
- Lectura incremental de logs (sin duplicados)
- Normalización de eventos en formato estructurado
- Estructura de eventos extendida (10 campos)
- Simulación de entorno realista del polvorín
- Motor básico de correlación de eventos
- Detección de intrusiones y movimientos
- Monitorización ambiental (temperatura y humedad)
- Supervisión del estado de sensores y detección de inactivos
- Almacenamiento persistente mediante SQLite
- API REST desarrollada con FastAPI
- Documentación de la Api mediante Swagger
- Dashboard web desarrollado con Streamlit.
- Visualización de eventos, alertas, anomalías, sensores y estadísticas.
- Pantalla de configuración con parámetros persistentes.
- Simulación de notificaciones SMS para alertas críticas.

## Tecnologías utilizadas
- Python 3.14
- SQLite
- FastAPI
- Uvicorn
- Streamlit
- Pandas
- Plotly
- JSON
- Git y GitHub
- Visual Studio Code

## Estructura del proyecto

- `api/` → API REST para consultar eventos, alertas, anomalías y sensores
- `config/` → Archivos de configuración del sistema
- `correlation/` → Motor de correlación y reglas
- `dashboard/` → Dashboard web para la monitorización y configuración
- `db/` → Gestión y almacenamiento en SQLite
- `docs/` → Memoria y documentación del TFG
- `ingestor/` → Lectura e ingestión de logs
- `logs/` → Archivos de eventos yregistros generados
- `machine/` → Detección de anomalías mediante reglas
- `notifications/` → Gestión de notificaciones y envío de SMS (simulados)
- `sensors/` → Gestión y monitorización de sensores

## Instalación
Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución
### 1. Ejecutar el SIEM
Inicia el proceso principal de monitorización, correlación de eventos y generación de alertas.

```bash
python main.py
```

### 2. Ejecutar la API REST
Permite consultar eventos, alertas, anomalías y sensores desde el dashboard.
```bash
python -m uvicorn api.server:app --reload
```

### 3. Ejecutar el dashboard
Inicia la interfaz web de monitorización y configuración.

```bash
streamlit run dashboard/app.py
```

### Acceso a la documentación de la API
Una vez iniciada la API, la documentación interactiva estará disponible en:

```text
http://127.0.0.1:8000/docs
```


## Endpoints disponibles
### Eventos
- '/events'
- ' /events?limit=10'
- ' /events/recent'
### Alertas
- '/alerts'
- ' /alerts?limit=10'
- ' /alerts/severity/'CRITICAL'
### Anomalías
- '/anomalies'
### Sensores
- '/sensors/status'
### Estadísticas
- '/stats'
### Esquema de base de datos
- '/database/schema'
### Documentación de la API
- '/docs'

## Formato de los logs

El sistema trabaja con eventos estructurados en el siguiente formato:

```text
timestamp | source | event_type | severity | user_id | access_point | deposit_id | device_id | result | message
```

### Ejemplo

```text
2026-05-01 08:00:12 | torno_principal | access | INFO | U001 | acceso_polvorin | - | torno_01 | allowed | Acceso autorizado con tarjeta
```

## Estado

✅ Proyecto funcional finalizado.

Actualmente el sistema es capaz de ingerir eventos desde archivos de log, normalizarlos, almacenarlos en una base de datos SQLite y procesarlos mediante un motor de correlación basado en reglas.

La solución incorpora una API REST desarrollada con FastAPI, un dashboard web implementado con Streamlit, monitorización de sensores, detección de anomalías, clasificación de alertas por nivel de riesgo y simulación de notificaciones SMS para eventos críticos.

El proyecto ha sido desarrollado como Trabajo Fin de Grado de Ingeniería Informática en la Universidad de Burgos, utilizando un entorno simulado de polvorín militar para la validación de los requisitos de seguridad y monitorización.

## Objetivo
Construir un sistema SIEM funcional capaz de:

- Detectar intentos de intrusión y accesos no autorizados.
- Identificar comportamientos anómalos mediante reglas de detección.
- Generar alertas de seguridad clasificadas por nivel de criticidad.
- Supervisar el estado de sensores y dispositivos monitorizados.
- Proporcionar capacidades de visualización, análisis y configuración mediante un dashboard web.
- Simular un entorno realista de seguridad aplicado a infraestructuras críticas.
- Servir como base para futuras ampliaciones y nuevas capacidades de monitorización.