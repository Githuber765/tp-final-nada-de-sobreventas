# Informe TP2: Arquitectura de Microservicios para Market-Place-Inc

## 1. Introducción

El presente informe documenta el desarrollo del Trabajo Práctico N.º 2 de Sistemas Distribuidos, cuyo objetivo fue evolucionar el sistema de Market-Place-Inc desde una arquitectura monolítica hacia una arquitectura distribuida basada en microservicios.

En el TP anterior se trabajó sobre un monolito desarrollado con FastAPI y MySQL, donde distintos módulos del sistema compartían el mismo proceso, la misma base de datos y el mismo ciclo de ejecución. Esta arquitectura permitió observar problemas típicos de sistemas no distribuidos bajo carga: acoplamiento fuerte, saturación de recursos compartidos, dificultad para aislar fallos y propagación de errores entre módulos.

En este TP se plantea una evolución hacia microservicios, separando responsabilidades en servicios independientes y utilizando herramientas propias de sistemas distribuidos, como Docker, Docker Compose, RabbitMQ, MySQL, contratos gRPC/Protobuf y manifiestos básicos de Kubernetes.

El objetivo principal no fue construir una plataforma productiva completa, sino demostrar los principios fundamentales de una arquitectura distribuida: separación de servicios, comunicación por red, desacoplamiento mediante mensajería, despliegue en contenedores, identificación de puntos únicos de falla y análisis de resiliencia.

---

## 2. Objetivos del trabajo

Los objetivos principales del trabajo fueron:

- Separar el sistema en servicios independientes.
- Implementar una arquitectura basada en microservicios.
- Contenerizar los servicios mediante Docker.
- Orquestar localmente el sistema con Docker Compose.
- Implementar comunicación síncrona entre servicios.
- Implementar comunicación asíncrona mediante RabbitMQ.
- Incorporar persistencia con MySQL.
- Documentar un contrato `.proto` para comunicación gRPC.
- Incluir manifiestos básicos de Kubernetes.
- Identificar SPOFs y analizar limitaciones de resiliencia.
- Validar el flujo end-to-end de creación de pedidos.

---

## 3. Arquitectura general del sistema

La arquitectura desarrollada se compone de varios servicios independientes que se ejecutan dentro de una red de Docker Compose.

Los principales componentes son:

| Componente | Responsabilidad |
|---|---|
| Orders Service | Recibe pedidos, valida productos y publica eventos |
| Catalog Service | Administra y expone productos |
| Notification Service | Consume eventos publicados en RabbitMQ |
| RabbitMQ | Broker de mensajería para comunicación asíncrona |
| MySQL | Base de datos relacional para persistencia |
| Payments Service | Servicio preparado para lógica de pagos |

La arquitectura busca reducir el acoplamiento del monolito separando funcionalidades en unidades independientes. Cada servicio puede ejecutarse en su propio contenedor, tener su propio proceso y evolucionar de forma más aislada.

El flujo principal inicia cuando el usuario crea un pedido mediante el endpoint `POST /orders`. El servicio de órdenes valida el producto consultando el catálogo y luego publica un evento en RabbitMQ. Este evento puede ser consumido por el servicio de notificaciones, permitiendo que el procesamiento posterior ocurra de forma desacoplada.

---

## 4. Comunicación entre servicios

### 4.1 Comunicación síncrona

La comunicación síncrona se utiliza cuando un servicio necesita una respuesta inmediata para continuar.

En este sistema, el flujo síncrono principal es:

```text
Usuario → Orders Service → Catalog Service
```

Cuando el usuario crea un pedido, `Orders Service` necesita consultar el catálogo para validar la existencia del producto. Esta operación es síncrona porque el pedido no debería confirmarse si el producto no existe o si no puede validarse correctamente.

Este tipo de comunicación tiene ventajas:

- es simple de entender,
- permite obtener una respuesta inmediata,
- facilita validaciones directas,
- resulta adecuada para flujos donde una operación depende estrictamente de otra.

Pero también introduce desventajas:

- genera acoplamiento temporal,
- si el servicio destino está caído, el servicio origen puede fallar,
- puede propagar latencia,
- puede generar fallas en cascada.

Por ese motivo, no todos los flujos deben resolverse de forma síncrona.

### 4.2 Comunicación asíncrona

La comunicación asíncrona se implementó mediante RabbitMQ.

El flujo principal es:

```text
Orders Service → RabbitMQ → Notification Service
```

Cuando se crea un pedido, `Orders Service` publica un evento en la cola `orders`. Luego, el consumidor puede procesar ese evento sin bloquear la respuesta HTTP original.

Este enfoque permite desacoplar servicios. `Orders Service` no necesita esperar a que `Notification Service` termine de procesar el mensaje. Incluso si el consumidor no está disponible temporalmente, RabbitMQ puede conservar el mensaje en la cola.

Ventajas principales:

- desacoplamiento entre productor y consumidor,
- mejor tolerancia a fallos,
- procesamiento en segundo plano,
- reducción de latencia percibida por el usuario,
- posibilidad de reintentos,
- mejor escalabilidad del procesamiento de eventos.

---

## 5. Docker y Docker Compose

Para ejecutar el sistema se utilizó Docker. Cada servicio cuenta con su propio `Dockerfile`, lo que permite empaquetar la aplicación junto con sus dependencias.

Docker Compose se utilizó para levantar el entorno completo de forma local. El archivo `docker-compose.yml` define los servicios necesarios:

- MySQL,
- RabbitMQ,
- Catalog Service,
- Orders Service,
- Notification Service.

Una ventaja importante de Docker Compose es que crea una red interna donde los servicios pueden comunicarse por nombre. Por ejemplo, dentro de los contenedores no se debe usar `localhost` para conectarse a MySQL, sino el nombre del servicio:

```text
mysql
```

Del mismo modo, para RabbitMQ se utiliza:

```text
rabbitmq
```

Durante el desarrollo se detectó este problema al intentar conectar servicios usando `localhost`. En Docker, `localhost` representa el propio contenedor, no otro servicio. Por eso fue necesario corregir las cadenas de conexión.

---

## 6. RabbitMQ y mensajería

RabbitMQ cumple el rol de broker de mensajería.

Su función es recibir eventos publicados por un servicio productor y almacenarlos en una cola hasta que un consumidor los procese.

En este trabajo, cuando se ejecuta `POST /orders`, el servicio de órdenes publica un evento en RabbitMQ. Luego, ese mensaje queda disponible en la cola `orders`.

Esto se validó desde el panel web de RabbitMQ, accesible en:

```text
http://localhost:15672
```

La existencia de mensajes en la cola demostró que el flujo asíncrono estaba funcionando correctamente.

RabbitMQ mejora la arquitectura porque evita que todos los servicios dependan directamente entre sí. En lugar de llamar a cada consumidor, el productor publica un evento y continúa su ejecución.

---

## 7. Persistencia con MySQL

MySQL se utilizó como base de datos relacional para persistencia.

El servicio de catálogo inicializa la tabla de productos y permite consultar productos mediante endpoints expuestos con FastAPI.

Durante la ejecución del sistema, SQLAlchemy se encarga de crear la tabla `productos` si no existe e insertar datos iniciales.

Uno de los problemas encontrados fue que MySQL 8 utiliza métodos modernos de autenticación, por lo que fue necesario agregar la dependencia `cryptography` para que `aiomysql` pudiera conectarse correctamente.

También fue necesario corregir las credenciales de conexión, incorporando usuario y contraseña en la URL:

```text
root:root
```

---

## 8. Kubernetes

El repositorio incluye manifiestos básicos de Kubernetes en la carpeta `k8s/`.

Estos manifiestos representan una primera aproximación al despliegue del sistema en un entorno orquestado.

Kubernetes aporta conceptos fundamentales en sistemas distribuidos:

- Deployments,
- Services,
- service discovery,
- self-healing,
- reinicio de pods,
- separación entre definición declarativa y ejecución.

Aunque Docker Compose permite ejecutar el sistema localmente, Kubernetes representa un paso más cercano a entornos productivos, donde los servicios pueden reiniciarse, escalarse y descubrirse mediante nombres internos.

Comandos documentados:

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get services
kubectl delete pod <nombre-del-pod>
```

---

## 9. SPOFs identificados

Un SPOF, o Single Point of Failure, es un componente que puede afectar al sistema completo o a una parte crítica si falla.

En esta implementación se identificaron los siguientes SPOFs:

### MySQL

MySQL es un SPOF porque se ejecuta como una única instancia. Si la base de datos cae, los servicios que dependen de persistencia no pueden consultar ni guardar datos.

Impacto:

- el catálogo puede dejar de responder correctamente,
- las operaciones que requieran persistencia pueden fallar,
- el sistema pierde disponibilidad parcial o total.

### RabbitMQ

RabbitMQ también es un SPOF porque se ejecuta como una única instancia. Si el broker cae, los eventos asincrónicos no pueden publicarse ni consumirse.

Impacto:

- las notificaciones no se procesan,
- los eventos quedan interrumpidos,
- se afecta la comunicación asíncrona.

### Control Plane de Kubernetes

En un entorno Kubernetes local o mínimo, el control plane también puede considerarse un punto crítico. Si falla, se dificulta administrar el cluster, crear pods o aplicar cambios.

---

## 10. Problemas encontrados durante el desarrollo

Durante el desarrollo se encontraron varios problemas técnicos propios de sistemas distribuidos.

### Dockerfiles vacíos o incompletos

Al ejecutar `docker compose up --build`, algunos servicios no podían construirse porque sus Dockerfiles estaban vacíos o no existían. Se resolvió creando Dockerfiles individuales para cada servicio.

### Dependencia `pika`

El servicio de órdenes fallaba porque no encontraba el módulo `pika`, necesario para comunicarse con RabbitMQ. Se corrigió agregando la dependencia al archivo `requirements.txt`.

### Uso incorrecto de `localhost`

Los servicios intentaban conectarse usando `localhost`, lo cual falla dentro de Docker porque cada contenedor tiene su propio entorno de red. Se reemplazó por nombres de servicio como `mysql` y `rabbitmq`.

### Error de autenticación MySQL

SQLAlchemy no podía autenticarse contra MySQL porque la cadena de conexión no tenía la contraseña correcta. Se corrigió incorporando `root:root`.

### Dependencia `cryptography`

`aiomysql` requería el paquete `cryptography` para conectarse a MySQL 8. Se agregó la dependencia al proyecto.

### Orden de inicio de servicios

El servicio de catálogo intentaba conectarse a MySQL antes de que la base terminara de iniciar. Se corrigió usando `depends_on`, `restart: always` y healthchecks.

---

## 11. Validación end-to-end

Se validó el flujo completo del sistema mediante Swagger y RabbitMQ.

El endpoint utilizado fue:

```http
POST /orders
```

Con el siguiente body:

```json
{
  "product_id": 1,
  "quantity": 1
}
```

La respuesta obtenida fue exitosa:

```json
{
  "message": "Pedido creado",
  "order_id": "...",
  "event_sent": true
}
```

Luego se verificó en RabbitMQ que existía un mensaje en la cola `orders`.

Esto demuestra que:

- Orders recibe pedidos,
- Catalog responde consultas,
- RabbitMQ almacena eventos,
- la comunicación síncrona y asíncrona funciona,
- el entorno Docker Compose levanta correctamente.

---

## 12. Limitaciones

La implementación corresponde a un entorno académico y local. Por lo tanto, tiene algunas limitaciones:

- MySQL no tiene replicación.
- RabbitMQ no está en cluster.
- No hay alta disponibilidad real.
- No se implementó autenticación entre servicios.
- Kubernetes está representado mediante manifiestos básicos.
- No se implementó observabilidad completa con Prometheus, Grafana o Jaeger.
- El sistema prioriza demostrar conceptos distribuidos antes que cubrir todos los casos productivos.

---

## 13. Conclusión

El desarrollo del TP permitió comprender de forma práctica la diferencia entre un monolito y una arquitectura basada en microservicios.

La separación del sistema en servicios independientes permitió observar ventajas como desacoplamiento, aislamiento de responsabilidades, posibilidad de comunicación asíncrona y mayor claridad arquitectónica.

Sin embargo, también aparecieron nuevas complejidades: configuración de red, dependencias entre contenedores, orden de inicio, debugging distribuido, manejo de colas y necesidad de observabilidad.

El uso de Docker, Docker Compose, RabbitMQ, MySQL, FastAPI, gRPC y Kubernetes permitió simular un entorno distribuido realista y aplicar conceptos centrales de la materia.

En conclusión, la arquitectura implementada resuelve parte de los problemas del monolito original, pero también evidencia que los microservicios no eliminan la complejidad: la desplazan hacia la comunicación, la infraestructura y la operación del sistema.