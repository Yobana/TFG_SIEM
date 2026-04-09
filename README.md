# TFG – SIEM Ligero en Raspberry Pi

Trabajo Fin de Grado – Ingeniería Informática - Yobana Nido Alvarez
Universidad de Burgos - 2026

## Descripción

Sistema de monitorización y detección de eventos de seguridad (SIEM) ligero,
diseñado para ejecutarse en una Raspberry Pi simulando un Polvorín Militar.

## Estructura del proyecto

- `ingestor/` – Módulo de lectura e ingestión de logs
- `correlation/` – Motor de correlación y reglas de detección
- `db/` – Base de datos SQLite para almacenamiento de eventos
- `api/` – API REST para consulta de datos
- `dashboard/` – Interfaz web de visualización
- `machine/` – Módulo de Machine Learning para detección de anomalías
- `logs/` – Logs de prueba para desarrollo y testing

## Estado

🚧 En desarrollo