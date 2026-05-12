
## 1. Introducción

El presente trabajo práctico tiene como objetivo analizar el comportamiento de un sistema monolítico bajo condiciones de carga, utilizando como caso de estudio la empresa ficticia **Market-Place-Inc**.

Se desarrolló una API mínima en FastAPI que centraliza los módulos de catálogo, pedidos, pagos y salud del sistema en un único archivo, compartiendo la misma base de datos. El propósito no es optimizar el sistema, sino evidenciar sus limitaciones y problemas estructurales.

---

## 2. Arquitectura del sistema

El sistema implementado corresponde a un **monolito**, donde todos los módulos se ejecutan dentro de la misma aplicación y comparten recursos.

### Diagrama lógico

```
[ Usuario ]
      ↓
[ API Monolito (FastAPI) ]
   ├── Catálogo (/products)
   ├── Pedidos (/orders)
   ├── Pagos (simulado)
   └── Health (/health)
      ↓
[ Base de Datos MySQL ]
      ↓
[ Proveedor de pagos externo ]
```

### SPOFs (Single Points of Failure)

* **Base de datos**: única instancia → si falla, el sistema completo queda inutilizable
* **Backend monolítico**: única aplicación → si cae, no hay servicio
* **Proveedor de pagos**: dependencia externa → impacta directamente en `/orders`

---

## 3. Implementación

Se desarrolló una API en FastAPI con los siguientes endpoints:

* `GET /products` → listado de productos
* `GET /products/{id}` → detalle de producto
* `POST /orders` → creación de pedido (incluye pago simulado)
* `GET /health` → estado del sistema

El endpoint `/orders` incluye una simulación de latencia mediante:

```python
await asyncio.sleep(3)
```

Esto representa la llamada a un servicio externo de pagos y permite evidenciar problemas de concurrencia.

Todos los endpoints utilizan la misma conexión a base de datos, generando acoplamiento entre módulos.

---

## 4. Test de carga

Se utilizó **Locust** para simular múltiples usuarios concurrentes.

### Configuración

* Usuarios: 20
* Distribución de tareas:

  * Compras (`/orders`)
  * Consulta de catálogo (`/products`)
  * Health (`/health`)

---

## 5. Resultados

Durante las pruebas se observaron los siguientes comportamientos:

* `/orders` presenta alta latencia (~3000 ms), debido a la simulación del pago
* `/products` responde rápidamente en baja carga
* `/health` mantiene tiempos mínimos (~2 ms) y no se ve afectado

### Interpretación

* El endpoint `/orders` es el principal **cuello de botella**
* La latencia del pago impacta en la disponibilidad del sistema
* El uso compartido de la base de datos introduce contención de recursos
* `/health` demuestra que el problema no está en el servidor, sino en la lógica de negocio y el acceso a DB

---

## 6. Análisis CAP

### Inventario → CP (Consistency + Partition Tolerance)

Se prioriza la consistencia para evitar overselling.
Ante fallas, el sistema puede rechazar operaciones en lugar de aceptar datos incorrectos.

### Notificaciones → AP (Availability + Partition Tolerance)

Se prioriza la disponibilidad.
Se tolera inconsistencia temporal debido a bajo impacto en el negocio.

---

## 7. Falencias del monolito

Se identificaron los siguientes problemas:

* Fuerte acoplamiento entre módulos
* Uso compartido de recursos críticos (base de datos)
* Bloqueo de operaciones durante llamadas externas
* Falta de aislamiento entre funcionalidades
* Propensión a fallos en cascada

---

## 8. Evidencia del problema

El error observado:

```
QueuePool limit exceeded
```

demuestra que:

* las conexiones a la base de datos se agotan
* las requests quedan en espera
* el sistema deja de responder

Esto evidencia un caso de **resource starvation** y fallo en cascada.

---

## 9. IA Log

### Interacción 1

**Prompt:** construcción de monolito en FastAPI
**Resultado:** generación de `main.py` completo
**Adaptación:** ajuste de conexión a MySQL
**Aprendizaje:** impacto del acoplamiento y uso compartido de DB

### Interacción 2

**Prompt:** teorema CAP
**Resultado:** explicación de C, A y P
**Adaptación:** aplicado a inventario y notificaciones
**Aprendizaje:** imposibilidad de cumplir las tres propiedades simultáneamente

### Interacción 3

**Prompt:** error QueuePool
**Resultado:** explicación de saturación del pool
**Adaptación:** aplicado al test de carga
**Aprendizaje:** comprensión de fallos en cascada y cuellos de botella

---

## 10. Conclusión

El sistema monolítico presenta limitaciones importantes en términos de escalabilidad y resiliencia. La dependencia de una base de datos única, la centralización de la lógica de negocio y la falta de aislamiento entre módulos generan un entorno propenso a fallos bajo carga.

El test de carga permitió evidenciar cómo una operación lenta puede impactar en todo el sistema, confirmando los problemas típicos de arquitecturas monolíticas en sistemas distribuidos.

---

## 11. Tecnologías utilizadas

* FastAPI
* MySQL
* SQLAlchemy / aiomysql
* Locust
* Python

