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
- Supervisión del estado de sensores
- Detección de dispositivos inactivos
- Configuración centralizada mediante settings.py
- Almacenamiento persistente mediante SQLite
- API REST desarrollada con FastAPI
- Filtrado y consulta avanzada de eventos y alertas
- Estadísticas básicas del sistema
- Documentación automática mediante Swagger

## Tecnologías utilizadas
- Python 3.14
- SQLite
- FastAPI
- Uvicorn
- Git y GitHub
- Visual Studio Code

## Estructura del proyecto

- `ingestor/` → Lectura e ingestión de logs
- `correlation/` → Motor de correlación y reglas
- `db/` → Base de datos SQLite
- `api/` → API REST
- `dashboard/` → Futuro panel web de visualización
- `machine/` → Módulo de Machine Learning
- `logs/` → Archivos de logs simulados
- `docs/` → Memoria y documentación del TFG
- `sensors/` → Gestión y monitorización de sensores

## Instalación
Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución
Ejecutar el sistema principal:
```bash
python main.py
```

Ejecutar únicamente la API REST:
```bash
python -m uvicorn api.server:app --reload
```

Ejecutar únicamente el módulo de ingesta:
```bash
python ingestor/ingestor.py
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
### Estadísticas
- '/stats'
### Swagger
- '/docs'

## Formato logs
El sistema trabaja con logs estructurados en el siguiente formato:

timestamp | source | event_type | severity | user_id | access_point | deposit_id | device_id | result | message

Ejemplo:
2026-05-01 08:00:12 | torno_principal | access | INFO | U001 | acceso_polvorin | - | torno_01 | allowed | Acceso autorizado con tarjeta

## Estado

🚧 En desarrollo (Fase 3)
Actualmente el sistema dispone de un entorno funcional capaz de ingerir eventos, normalizarlos, procesarlos mediante reglas de correlación y supervisar el estado de distintos sensores simulados.

Actualmente el proyecto se encuentra en desarrollo de la Fase 3, centrada en la API REST, visualización y futuras capacidades de análisis avanzado.

## Objetivo
Construir un sistema SIEM funcional capaz de:

- Detectar intentos de intrusión
- Identificar comportamientos anómalos
- Generar alertas de seguridad
- Servir como base para futuras ampliaciones (ML, dashboard, etc.)
- Simular un entorno realista de seguridad en infraestructuras críticas.