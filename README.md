# TP2 — Arquitectura de Microservicios para Market-Place-Inc

## Sistemas Distribuidos — TP2

## Integrantes

* Ezequiel Castro Burgos 
* Emmanuel Orozco

---

# Introducción

Este trabajo práctico tiene como objetivo transformar una arquitectura monolítica en una arquitectura basada en microservicios utilizando tecnologías modernas de sistemas distribuidos.

El caso de estudio corresponde a **Market-Place-Inc**, una plataforma de e-commerce que originalmente presentaba problemas de escalabilidad, acoplamiento y fallas en cascada durante eventos de alta concurrencia, como el Hot Sale.

A partir de esta problemática se desarrolló una solución basada en:

* separación de servicios,
* contenedorización,
* mensajería asíncrona,
* comunicación distribuida,
* orquestación básica,
* y desacoplamiento entre módulos.

---

# Objetivos del TP

* Separar funcionalidades del monolito en microservicios independientes.
* Implementar comunicación síncrona y asíncrona.
* Utilizar Docker y Docker Compose para la ejecución distribuida.
* Incorporar RabbitMQ como broker de mensajería.
* Simular un entorno distribuido con múltiples servicios.
* Implementar manifiestos básicos de Kubernetes.
* Comprender problemas reales de sistemas distribuidos.

---

# Arquitectura del Sistema

La arquitectura implementada se compone de los siguientes servicios:

| Servicio              | Responsabilidad                 |
| --------------------- | ------------------------------- |
| Catalog Service       | Gestión y consulta de productos |
| Orders Service        | Creación de pedidos             |
| RabbitMQ              | Broker de mensajería            |
| MySQL                 | Persistencia de datos           |
| Notification Consumer | Consumo de eventos asincrónicos |

---

# Comunicación entre Servicios

## Comunicación síncrona

La comunicación síncrona ocurre cuando el servicio de órdenes necesita consultar información del catálogo.

Características:

* request-response,
* dependencia inmediata,
* bloqueo hasta obtener respuesta,
* menor complejidad,
* mayor acoplamiento temporal.

---

## Comunicación asíncrona

La comunicación asíncrona se implementó mediante RabbitMQ.

Flujo:

1. Orders Service crea el pedido.
2. Orders publica un evento en RabbitMQ.
3. Notification Consumer consume el mensaje.
4. El procesamiento ocurre desacoplado del request HTTP original.

Ventajas:

* desacoplamiento,
* resiliencia,
* tolerancia a fallos,
* procesamiento en background,
* menor impacto de latencia.

---

# Tecnologías Utilizadas

| Tecnología      | Uso                      |
| --------------- | ------------------------ |
| Python          | Lenguaje principal       |
| FastAPI         | Framework backend        |
| Docker          | Contenedores             |
| Docker Compose  | Orquestación local       |
| RabbitMQ        | Cola de mensajes         |
| MySQL           | Base de datos            |
| SQLAlchemy      | ORM                      |
| Pika            | Cliente RabbitMQ         |
| Kubernetes      | Orquestación             |
| gRPC / Protobuf | Comunicación distribuida |
| Swagger/OpenAPI | Documentación de APIs    |
| Locust          | Pruebas de carga         |

---

# Estructura del Proyecto

```text
tp2-market-place-main/
│
├── catalog/
├── orders/
├── payments/
├── notificaciones/
├── events/
├── grpc/
├── k8s/
├── tests/
├── docker-compose.yml
└── README.md
```

---

# Ejecución del Proyecto

## Requisitos

* Docker Desktop
* Docker Compose
* Python 3.11+

---

## Levantar el entorno

```bash
docker compose up --build
```

---

# Servicios Disponibles

| Servicio           | URL                                                      |
| ------------------ | -------------------------------------------------------- |
| Orders Service     | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Catalog Service    | [http://localhost:8001/docs](http://localhost:8001/docs) |
| RabbitMQ Dashboard | [http://localhost:15672](http://localhost:15672)         |

---

# Credenciales RabbitMQ

```text
usuario: guest
password: guest
```

---

# Ejemplo de Flujo End-to-End

## 1. Crear pedido

Endpoint:

```http
POST /orders
```

Body:

```json
{
  "product_id": 1,
  "quantity": 1
}
```

---

## 2. Respuesta esperada

```json
{
  "message": "Pedido creado",
  "order_id": "..."
}
```

---

## 3. Verificar RabbitMQ

Ingresar a:

```text
http://localhost:15672
```

Luego:

* Queues and Streams
* verificar cola `orders`

---

# Docker y Contenedores

Cada microservicio posee su propio:

* Dockerfile,
* proceso independiente,
* entorno aislado,
* dependencias específicas.

Docker Compose permite:

* levantar todos los servicios,
* configurar networking,
* administrar dependencias,
* simplificar el entorno distribuido.

---

# Kubernetes

El proyecto incluye manifiestos básicos de Kubernetes dentro de la carpeta:

```text
/k8s
```

Se incluyen:

* Deployments,
* Services,
* RabbitMQ deployment.

Conceptos aplicados:

* service discovery,
* self-healing,
* separación de pods,
* comunicación interna.

---

# Problemas Encontrados y Soluciones

## 1. Dockerfiles vacíos

Problema:

* Docker Compose no podía construir imágenes.

Solución:

* creación de Dockerfiles individuales por servicio.

---

## 2. Error con dependencias RabbitMQ

Problema:

* módulo `pika` no encontrado.

Solución:

* agregar dependencia en `requirements.txt`.

---

## 3. Conexión MySQL entre contenedores

Problema:

* uso de `localhost` dentro de Docker.

Solución:

* reemplazar por hostname del servicio:

```python
mysql
```

---

## 4. Orden de inicio de servicios

Problema:

* los servicios intentaban conectarse antes de que MySQL estuviera listo.

Solución:

* uso de `depends_on`
* reinicio automático de contenedores.

---

# Conceptos de Sistemas Distribuidos Aplicados

Durante el desarrollo se trabajó con:

* desacoplamiento,
* colas de mensajes,
* comunicación síncrona,
* comunicación asíncrona,
* contenedorización,
* fallas distribuidas,
* service discovery,
* aislamiento de servicios,
* resiliencia,
* arquitectura basada en eventos.

---

# IA Log: Registro de Interacciones y Correcciones

## Introducción

Este apartado registra las interacciones clave con el asistente de IA durante el desarrollo del TP2, destacando los errores detectados y las decisiones arquitectónicas tomadas para garantizar la calidad, resiliencia y funcionamiento del sistema distribuido.

## Uso de IA durante el desarrollo

La IA fue utilizada como herramienta de apoyo para:

- diagnóstico de errores Docker,
- configuración de RabbitMQ,
- debugging de networking entre contenedores,
- generación de documentación,
- comprensión conceptual de microservicios.

## Registro de Interacciones Críticas

| Fecha | Tarea | Error detectado por la IA / Humano | Corrección aplicada |
| :--- | :--- | :--- | :--- |
| 02/05 | Fase 3 Pagos | Inconsistencia: Modelo `Payment` (Integer ID) vs `PaymentService` (UUID string). | Se modificó el modelo `Payment` para aceptar String (UUID) para mantener consistencia en sistemas distribuidos. |
| 02/05 | Fase 3 Pagos | Inconsistencia: Consultas SQL crudas fallaban (`MissingGreenlet`) y uso incorrecto de `select(Payment)`. | Se refactorizó la capa de persistencia para utilizar `select(Payment)` de SQLAlchemy correctamente en un contexto asíncrono. |
| 02/05 | Fase 3 Pagos | Inconsistencia: El `webhook_handler` no inyectaba la sesión de DB (`Depends(get_db)` faltaba). | Se inyectó la dependencia `db: AsyncSession` correctamente en el handler. |
| 02/05 | Integración | Conflicto de rutas: `main.py` y `orders/api/orders.py` registraban la misma ruta `/orders`. | Se limpió `main.py`, eliminando la lógica antigua y delegando exclusivamente al router de `orders`. |
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

 ---
# Conclusión

El trabajo permitió comprender las diferencias entre una arquitectura monolítica y una arquitectura basada en microservicios.

La implementación mostró ventajas importantes:

* desacoplamiento,
* escalabilidad,
* resiliencia,
* separación de responsabilidades.

También se observaron nuevas complejidades:

* networking distribuido,
* sincronización,
* dependencias entre servicios,
* manejo de colas,
* debugging distribuido.

Finalmente, el TP permitió aplicar herramientas modernas utilizadas actualmente en entornos reales de desarrollo distribuido y DevOps.
