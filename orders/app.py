from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json
import os
import uuid
import requests

app = FastAPI(title="Orders Service")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog:8000")


class OrderRequest(BaseModel):
    product_id: int
    quantity: int


@app.get("/health")
def health():
    return {"status": "ok", "service": "orders"}


@app.post("/orders")
def create_order(order: OrderRequest):
    # Comunicación síncrona con catálogo
    response = requests.get(f"{CATALOG_URL}/products/{order.product_id}", timeout=3)

    if response.status_code != 200:
        return {"error": "Producto no encontrado"}

    product = response.json()

    if product["stock"] < order.quantity:
        return {"error": "Stock insuficiente"}

    order_id = str(uuid.uuid4())

    event = {
        "order_id": order_id,
        "product_id": order.product_id,
        "quantity": order.quantity
    }

    # Comunicación asíncrona con RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()
    channel.queue_declare(queue="orders", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="orders",
        body=json.dumps(event),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

    return {
        "message": "Pedido creado",
        "order_id": order_id,
        "event_sent": True
    }