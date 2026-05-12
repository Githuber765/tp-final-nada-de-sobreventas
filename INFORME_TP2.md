# Informe TP2: Marketplace Distribuido

## 1. Introducción
Resumen de la transformación del monolito (FastAPI + MySQL) a una arquitectura modular y distribuida.

## 2. Arquitectura de Módulos
Justificación de la división en `Catalog`, `Orders`, `Payments`.
- Patrón: *Module-based decomposition*.
- Estrategia de DB: *Database-per-module*.

## 3. Comunicación Inter-servicio
- **Síncrona (gRPC):** Uso para `Orders` -> `Catalog` (reserva de stock, contrato fuerte, baja latencia).
- **Asíncrona (RabbitMQ):** Uso para flujos no bloqueantes (`Orders` -> `Notificaciones` / `Payments`). Justificación: resiliencia ante caídas de servicios.

## 4. Observabilidad
- Implementación de `Correlation ID` (Middleware + Headers de RabbitMQ).
- Logs estructurados en formato JSON para facilitar auditoría.

## 5. Resiliencia
- Análisis de SPOFs (RabbitMQ, K8s control plane).
- Patrones aplicados: Circuit Breaker (diseñado), Retry con backoff, Idempotencia en consumers.

## 6. Conclusiones y Aprendizajes
- Desafíos encontrados (Dual-write problem, consistencia de tipos).
- Importancia de los tests E2E y de resiliencia.
