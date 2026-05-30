# TP Final — Nada de Sobreventas

## Sistemas Distribuidos

## Integrantes

* Ezequiel Castro Burgos
* Emmanuel Orozco

---

# Introducción

Este proyecto implementa una solución distribuida para evitar el problema de **sobreventa de productos** (*overselling*) en un sistema de comercio electrónico.

El sistema parte de una arquitectura basada en microservicios y agrega un mecanismo de reserva de stock mediante **Redis Lock**, con pruebas concurrentes, monitoreo con **Prometheus y Grafana**, pruebas de carga con **Locust** y automatización de tests con **GitHub Actions**.

El objetivo principal es asegurar que, aunque muchos usuarios intenten reservar un mismo producto al mismo tiempo, el stock nunca quede negativo y no se vendan más unidades de las disponibles.

---

# Problema: Overselling

El **overselling** ocurre cuando el sistema vende más unidades de un producto que las realmente disponibles en stock.

Ejemplo:

```text
Stock disponible: 1 unidad
Usuario A intenta comprar 1 unidad
Usuario B intenta comprar 1 unidad al mismo tiempo
```

Si ambos procesos leen el stock antes de que se actualice, los dos podrían confirmar la compra y el stock terminaría en negativo.

Este problema es grave porque puede generar:

* ventas imposibles de cumplir;
* inconsistencias en inventario;
* reclamos de clientes;
* pérdida de confianza;
* errores en la operación del negocio.

---

# Solución Implementada

Se agregó un endpoint de reserva:

```http
POST /reserve
```

Este endpoint utiliza un **candado distribuido con Redis** para evitar que dos usuarios modifiquen el stock del mismo producto al mismo tiempo.

Flujo general:

```text
Cliente / Locust / Swagger
        ↓
Catalog Service - POST /reserve
        ↓
Redis Lock
        ↓
MySQL - Tabla productos
        ↓
Respuesta HTTP
```

---

# Funcionamiento de `/reserve`

El endpoint realiza los siguientes pasos:

1. Recibe `product_id` y `quantity`.
2. Intenta tomar un lock en Redis.
3. Si el lock está ocupado, espera brevemente y reintenta.
4. Si obtiene el lock, consulta el producto en MySQL.
5. Verifica si hay stock suficiente.
6. Si hay stock, descuenta la cantidad solicitada.
7. Si no hay stock, rechaza la operación.
8. Libera el lock.
9. Devuelve la respuesta correspondiente.

Ejemplo de body:

```json
{
  "product_id": 1,
  "quantity": 1
}
```

Respuesta exitosa:

```json
{
  "status": "reserved",
  "product_id": 1,
  "quantity": 1,
  "stock_remaining": 4
}
```

Respuesta sin stock:

```json
{
  "detail": "Sin stock suficiente"
}
```

---

# Redis Lock

La reserva usa Redis con la operación:

```python
redis.set(lock_key, lock_value, nx=True, ex=5)
```

Significado:

| Parámetro    | Significado                                  |
| ------------ | -------------------------------------------- |
| `lock_key`   | Clave del candado, asociada al producto      |
| `lock_value` | Valor guardado en Redis                      |
| `nx=True`    | Solo crea la clave si todavía no existe      |
| `ex=5`       | El lock expira automáticamente en 5 segundos |

Esto permite que solo una operación de reserva modifique el stock de un producto a la vez.

---

# Arquitectura del Proyecto

La arquitectura se compone de los siguientes servicios:

| Servicio             | Responsabilidad                                  |
| -------------------- | ------------------------------------------------ |
| Catalog Service      | Gestión de productos, stock, reservas y métricas |
| Orders Service       | Servicio de pedidos del sistema base             |
| Notification Service | Servicio preparado para consumir eventos         |
| RabbitMQ             | Broker de mensajería del sistema base            |
| MySQL                | Persistencia de productos y stock                |
| Redis                | Candado distribuido para evitar sobreventas      |
| Prometheus           | Recolección de métricas                          |
| Grafana              | Visualización de métricas                        |
| Locust               | Pruebas de carga                                 |
| GitHub Actions       | Ejecución automática de tests                    |

---

# Tecnologías Utilizadas

| Tecnología     | Uso                          |
| -------------- | ---------------------------- |
| Python         | Lenguaje principal           |
| FastAPI        | Implementación de APIs       |
| MySQL          | Base de datos                |
| SQLAlchemy     | ORM                          |
| Redis          | Lock distribuido             |
| Docker         | Contenedores                 |
| Docker Compose | Ejecución local de servicios |
| Prometheus     | Recolección de métricas      |
| Grafana        | Dashboard de monitoreo       |
| Locust         | Pruebas de carga             |
| Pytest         | Tests automatizados          |
| GitHub Actions | Integración continua         |

---

# Estructura del Proyecto

```text
tp-final-nada-de-sobreventas/
│
├── catalog/
│   ├── api/
│   │   ├── products.py
│   │   └── reserve.py
│   ├── database/
│   │   ├── connection.py
│   │   └── init.py
│   ├── models/
│   │   └── product.py
│   ├── app.py
│   ├── metrics.py
│   └── Dockerfile
│
├── orders/
│   └── ...
│
├── notificaciones/
│   └── ...
│
├── events/
│   └── ...
│
├── prometheus/
│   └── prometheus.yml
│
├── tests/
│   └── test_reserve.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── docker-compose.yml
├── locustfile_reserve.py
├── requirements.txt
└── README.md
```

---

# Ejecución del Proyecto

## Requisitos

* Docker Desktop instalado y en ejecución.
* Python 3.11 o superior.
* Docker Compose.
* Navegador web.

---

## Levantar el sistema

Desde la raíz del proyecto:

```bash
docker compose up --build
```

Este comando construye las imágenes y levanta los contenedores definidos en `docker-compose.yml`.

---

## Detener el sistema

```bash
docker compose down
```

---

# Servicios Disponibles

| Servicio           | URL                        |
| ------------------ | -------------------------- |
| Catalog Swagger    | http://localhost:8001/docs |
| Orders Swagger     | http://localhost:8000/docs |
| Prometheus         | http://localhost:9090      |
| Grafana            | http://localhost:3000      |
| Locust             | http://localhost:8089      |
| RabbitMQ Dashboard | http://localhost:15672     |

Credenciales por defecto de RabbitMQ:

```text
usuario: guest
password: guest
```

Credenciales por defecto de Grafana:

```text
usuario: admin
password: admin
```

---

# Prueba Manual de Reserva

Ingresar a:

```text
http://localhost:8001/docs
```

Ejecutar:

```http
POST /reserve
```

Body:

```json
{
  "product_id": 1,
  "quantity": 1
}
```

También se puede probar un caso sin stock:

```json
{
  "product_id": 1,
  "quantity": 999
}
```

El sistema debe rechazar la operación con:

```json
{
  "detail": "Sin stock suficiente"
}
```

---

# Tests Automatizados

Los tests se encuentran en:

```text
tests/test_reserve.py
```

Ejecutar:

```bash
pytest -v tests/test_reserve.py
```

Los tests validan:

1. Dos usuarios intentan reservar el mismo producto con stock 1.
2. Cincuenta usuarios intentan reservar productos con stock limitado.
3. El endpoint responde rápidamente.

Resultado esperado:

```text
3 passed
```

---

# GitHub Actions

El proyecto incluye un workflow de CI en:

```text
.github/workflows/ci-cd.yml
```

Este workflow se ejecuta automáticamente al hacer `push` sobre la rama `main`.

El pipeline realiza:

1. Checkout del repositorio.
2. Instalación de Python.
3. Instalación de dependencias.
4. Levantamiento del sistema con Docker Compose.
5. Ejecución de tests con Pytest.
6. Apagado de contenedores.

El resultado esperado es que GitHub Actions muestre el estado en verde.

---

# Métricas con Prometheus

El servicio Catalog expone métricas en:

```text
http://localhost:8001/metrics
```

Prometheus las recolecta desde:

```text
catalog:8000/metrics
```

Archivo de configuración:

```text
prometheus/prometheus.yml
```

Métricas principales:

| Métrica                      | Descripción                                     |
| ---------------------------- | ----------------------------------------------- |
| `reserve_attempts_total`     | Cantidad de intentos de reserva según resultado |
| `reserve_duration_seconds`   | Duración de las operaciones de reserva          |
| `inventory_stock_level`      | Stock actual por producto                       |
| `overselling_attempts_total` | Cantidad de sobreventas detectadas              |

La métrica más importante del TP es:

```text
overselling_attempts_total
```

Debe mantenerse en:

```text
0
```

---

# Dashboard en Grafana

Grafana se utiliza para visualizar las métricas recolectadas por Prometheus.

URL:

```text
http://localhost:3000
```

Datasource configurado:

```text
http://prometheus:9090
```

Paneles creados:

| Panel                          | Métrica                          |
| ------------------------------ | -------------------------------- |
| Reservas exitosas y rechazadas | `reserve_attempts_total`         |
| Stock actual por producto      | `inventory_stock_level`          |
| Cantidad de reservas medidas   | `reserve_duration_seconds_count` |
| Intentos de sobreventa         | `overselling_attempts_total`     |

El dashboard permite verificar visualmente que, incluso bajo carga, los intentos de sobreventa se mantienen en 0.

---

# Prueba de Carga con Locust

El archivo de prueba de carga es:

```text
locustfile_reserve.py
```

Ejecutar:

```bash
locust -f locustfile_reserve.py --host=http://localhost:8001
```

Luego ingresar a:

```text
http://localhost:8089
```

Configuración utilizada:

```text
Number of users: 50
Spawn rate: 5
Host: http://localhost:8001
```

La prueba realiza múltiples solicitudes concurrentes al endpoint:

```http
POST /reserve
```

Durante la prueba se espera observar:

* muchos intentos de reserva;
* reservas exitosas hasta agotar stock;
* rechazos por falta de stock;
* 0% de failures técnicos en Locust;
* `overselling_attempts_total = 0` en Grafana.

---

# Teorema CAP aplicado al inventario

En un sistema distribuido, ante una falla de comunicación o partición de red, no siempre se pueden garantizar simultáneamente consistencia, disponibilidad y tolerancia a particiones.

Aplicado al inventario:

* Priorizar **consistencia** significa no aceptar reservas si no se puede verificar correctamente el stock.
* Priorizar **disponibilidad** significa aceptar operaciones aunque no se pueda confirmar completamente el estado del stock.

En este proyecto se prioriza la **consistencia**, ya que el sistema rechaza operaciones cuando no puede asegurar que el stock sea válido. Esto evita confirmar ventas que podrían producir sobreventa.

---

# Resultados Obtenidos

Se validó que:

* el endpoint `/reserve` descuenta stock correctamente;
* las reservas sin stock son rechazadas;
* los tests concurrentes pasan correctamente;
* GitHub Actions ejecuta los tests de forma automática;
* Prometheus recolecta métricas del servicio Catalog;
* Grafana muestra el comportamiento del sistema;
* Locust permite simular usuarios concurrentes;
* la métrica `overselling_attempts_total` se mantiene en 0.

---

# Comandos Útiles

Levantar servicios:

```bash
docker compose up --build
```

Detener servicios:

```bash
docker compose down
```

Ver contenedores:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Ejecutar tests:

```bash
pytest -v tests/test_reserve.py
```

Ejecutar Locust:

```bash
locust -f locustfile_reserve.py --host=http://localhost:8001
```

---

# Conclusión

El trabajo permitió implementar una solución concreta para evitar sobreventas en un entorno distribuido.

La incorporación de Redis como candado distribuido permitió controlar el acceso concurrente al stock de productos. Los tests automatizados demostraron que, aun con múltiples usuarios intentando reservar al mismo tiempo, el stock no queda negativo.

Además, se incorporó observabilidad mediante Prometheus y Grafana, lo que permitió monitorear reservas, stock e intentos de sobreventa. Finalmente, la prueba de carga con Locust permitió validar el comportamiento del sistema bajo concurrencia.

El resultado final es una solución académica funcional que integra microservicios, contenedores, locks distribuidos, pruebas automatizadas, CI/CD y monitoreo.
