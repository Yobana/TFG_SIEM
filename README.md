# TFG – SIEM Ligero en Raspberry Pi

Trabajo Fin de Grado – Ingeniería Informática - Yobana Nido Alvarez
Universidad de Burgos - 2026

## Descripción

Este proyecto consiste en el desarrollo de un sistema SIEM (Security Information and Event Management) ligero, diseñado para ejecutarse en una Raspberry Pi.

El sistema simula un entorno de seguridad en un Polvorín Militar, permitiendo la monitorización de eventos, su análisis y la detección de situaciones potencialmente peligrosas.

## Funcionalidades actuales
Ingesta de logs desde archivos
Normalización de eventos en formato estructurado
Lectura incremental de logs (sin duplicados)
Base para correlación de eventos

## Estructura del proyecto

- `ingestor/` – Módulo de lectura e ingestión de logs
- `correlation/` – Motor de correlación y reglas de detección
- `db/` – Base de datos SQLite para almacenamiento de eventos
- `api/` – API REST para consulta de datos
- `dashboard/` – Interfaz web de visualización
- `machine/` – Módulo de Machine Learning para detección de anomalías
- `logs/` – Logs de prueba para desarrollo y testing

## Ejecución
Desde la raíz del proyecto:
python main.py
Para probar solo el ingestor:
python ingestor/ingestor.py

## Formato logs
El sistema trabaja con logs estructurados en el siguiente formato:

timestamp | source | severity | message

Ejemplo:
2026-04-16 08:00:12 | access | INFO | Usuario sargento1 accede al polvorín

## Estado

🚧 En desarrollo (Fase 2)
Actualmente se está implementando el motor de correlación de eventos para la detección de alertas.

## Objetivo
Construir un sistema SIEM funcional capaz de:

Detectar intentos de intrusión
Identificar comportamientos anómalos
Generar alertas de seguridad
Servir como base para futuras ampliaciones (ML, dashboard, etc.)