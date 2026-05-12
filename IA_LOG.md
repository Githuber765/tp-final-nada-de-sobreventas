# IA Log: Registro de Interacciones y Correcciones

## Introducción
Este documento registra las interacciones clave con el asistente de IA durante el desarrollo del TP2, destacando los errores detectados y las decisiones arquitectónicas tomadas para garantizar la calidad y resiliencia del sistema.

## Registro de Interacciones Críticas

| Fecha | Tarea | Error detectado por la IA / Humano | Corrección aplicada |
| :--- | :--- | :--- | :--- |
| 02/05 | Fase 3 Pagos | Inconsistencia: Modelo `Payment` (Integer ID) vs `PaymentService` (UUID string). | Se modificó el modelo `Payment` para aceptar String (UUID) para mantener consistencia en sistemas distribuidos. |
| 02/05 | Fase 3 Pagos | Inconsistencia: Consultas SQL crudas fallaban (MissingGreenlet) y uso incorrecto de `select(Payment)`. | Se refactorizó la capa de persistencia para utilizar `select(Payment)` de SQLAlchemy correctamente en un contexto asíncrono. |
| 02/05 | Fase 3 Pagos | Inconsistencia: El `webhook_handler` no inyectaba la sesión de DB (`Depends(get_db)` faltaba). | Se inyectó la dependencia `db: AsyncSession` correctamente en el handler. |
| 02/05 | Integración | Conflicto de rutas: `main.py` y `orders/api/orders.py` registraban la misma ruta `/orders`. | Se limpió `main.py` eliminando la lógica antigua y delegando exclusivamente al router de `orders`. |

## Aprendizajes
1. **Idempotencia:** La IA suele omitirla por defecto en consumers. Es obligatorio verificar cada vez.
2. **Timeouts:** Es fundamental configurar timeouts explícitos en llamadas síncronas entre servicios para evitar *cascading failures*.
3. **Tipado:** En sistemas distribuidos, la inconsistencia entre UUIDs y Integers en IDs puede romper la persistencia. Se debe validar estrictamente.
