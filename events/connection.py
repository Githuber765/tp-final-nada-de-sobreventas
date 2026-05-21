import pika
import os

def get_rabbitmq_connection():
    rabbitmq_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    params = pika.URLParameters(rabbitmq_url)
    return pika.BlockingConnection(params)
