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

## Nuevos problemas encontrados durante integración distribuida

| Fecha | Área | Problema detectado | Corrección aplicada |
| :--- | :--- | :--- | :--- |
| 12/05 | Docker Compose | Los servicios no iniciaban porque algunos Dockerfiles estaban vacíos o ausentes. | Se crearon Dockerfiles individuales para cada microservicio y se corrigieron rutas de build en `docker-compose.yml`. |
| 12/05 | Networking Docker | Los contenedores intentaban conectarse utilizando `localhost`, provocando errores de conexión entre servicios. | Se reemplazó `localhost` por el hostname interno `mysql` dentro de las cadenas de conexión. |
| 12/05 | RabbitMQ | El contenedor de órdenes fallaba por ausencia del módulo `pika`. | Se agregó `pika` a `requirements.txt` y se reconstruyeron las imágenes Docker. |
| 12/05 | Persistencia MySQL | SQLAlchemy no podía autenticarse contra MySQL (`Access denied for user root`). | Se corrigió la URL de conexión agregando usuario y contraseña (`root:root`). |
| 12/05 | Dependencias Python | `aiomysql` requería el paquete `cryptography` para autenticación moderna de MySQL 8. | Se agregó `cryptography` a `requirements.txt`. |
| 12/05 | Startup distribuido | Los servicios intentaban conectarse a MySQL antes de que el contenedor terminara de iniciar. | Se implementó `healthcheck`, `depends_on` y `restart: always` en Docker Compose. |
| 12/05 | RabbitMQ | Se necesitaba validar persistencia y desacoplamiento de mensajes. | Se probó el flujo end-to-end mediante `POST /orders` verificando la cola `orders` en RabbitMQ Dashboard. | 

## Aprendizajes

1. **Idempotencia:** La IA suele omitirla por defecto en consumers. Es obligatorio verificar cada vez.
2. **Timeouts:** Es fundamental configurar timeouts explícitos en llamadas síncronas entre servicios para evitar *cascading failures*.
3. **Tipado:** En sistemas distribuidos, la inconsistencia entre UUIDs e Integers puede romper la persistencia y el tracing.
4. **Networking distribuido:** Dentro de Docker Compose los servicios se comunican mediante DNS interno y no mediante `localhost`.
5. **Startup order:** El orden de inicio de servicios es crítico en arquitecturas distribuidas; un servicio puede fallar aunque la configuración sea correcta si la dependencia aún no terminó de iniciar.
6. **Mensajería asíncrona:** RabbitMQ permite desacoplar productores y consumidores, aumentando resiliencia y tolerancia a fallos.
7. **Debugging distribuido:** Diagnosticar problemas en microservicios es considerablemente más complejo que en un monolito debido a networking, contenedores y sincronización.