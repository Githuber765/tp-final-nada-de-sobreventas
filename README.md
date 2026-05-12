# TP2 — Arquitectura de Microservicios para Market-Place-Inc

## Sistemas Distribuidos — TP2

## Integrantes

* Ezequiel Castro Burgos

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

# IA Log

## Uso de IA durante el desarrollo

La IA fue utilizada como herramienta de apoyo para:

* diagnóstico de errores Docker,
* configuración de RabbitMQ,
* debugging de networking entre contenedores,
* generación de documentación,
* comprensión conceptual de microservicios.

---

## Correcciones realizadas manualmente

Las principales correcciones manuales fueron:

* estructura de Dockerfiles,
* networking interno,
* configuración MySQL,
* resolución de dependencias Python,
* organización del docker-compose.

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
