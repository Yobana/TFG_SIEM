# TFG – SIEM Ligero en Raspberry Pi

Trabajo Fin de Grado – Ingeniería Informática - Yobana Nido Alvarez
Universidad de Burgos - 2026

## Descripción

Este proyecto consiste en el desarrollo de un sistema SIEM (Security Information and Event Management) ligero, diseñado para ejecutarse en una Raspberry Pi.

El sistema simula un entorno de seguridad en un Polvorín Militar, permitiendo la monitorización de eventos, su análisis y la detección de situaciones potencialmente peligrosas.

El sistema está diseñado con una arquitectura modular que permite su ampliación y adaptación a entornos más complejos.

## Funcionalidades actuales
- Ingesta de logs desde archivos
- Normalización de eventos en formato estructurado
- Lectura incremental de logs (sin duplicados)
- Estructura de eventos extendida (10 campos)
- Simulación de entorno realista (polvorín)
- Motor básico de correlación de eventos
- Detección de intrusiones y movimientos
- Monitorización ambiental (temperatura y humedad)
- Configuración centralizada mediante settings.py
- Supervisión de sensores y detección de dispositivos inactivos
- Gestión homogénea de eventos con campos opcionales
- Almacenamiento persistente de eventos y alertas mediante SQLite

## Estructura del proyecto

- `ingestor/` – Módulo de lectura e ingestión de logs
- `correlation/` – Motor de correlación y reglas de detección
- `db/` – Base de datos SQLite para almacenamiento de eventos
- `api/` – API REST para consulta de datos
- `dashboard/` – Interfaz web de visualización
- `machine/` – Módulo de Machine Learning para detección de anomalías
- `logs/` – Logs para desarrollo
- `docs/` – Memoria del TFG y documentación asociada
- `sensors/` – Gestión y monitorización del estado de sensores

## Ejecución
Desde la raíz del proyecto:
python main.py
Para probar solo el ingestor:
python ingestor/ingestor.py

## Formato logs
El sistema trabaja con logs estructurados en el siguiente formato:

timestamp | source | event_type | severity | user_id | access_point | deposit_id | device_id | result | message

Ejemplo:
2026-05-01 08:00:12 | torno_principal | access | INFO | U001 | acceso_polvorin | - | torno_01 | allowed | Acceso autorizado con tarjeta

## Estado

🚧 En desarrollo (Fase 2 ampliada)
Actualmente el sistema dispone de un entorno funcional capaz de ingerir eventos, normalizarlos, procesarlos mediante reglas de correlación y supervisar el estado de distintos sensores simulados.

La Fase 2 continúa abierta para completar la integración con almacenamiento en base de datos, mejorar la API REST y consolidar las pruebas internas del sistema.

## Objetivo
Construir un sistema SIEM funcional capaz de:

Detectar intentos de intrusión
Identificar comportamientos anómalos
Generar alertas de seguridad
Servir como base para futuras ampliaciones (ML, dashboard, etc.)
Simular un entorno realista de seguridad en infraestructuras críticas.