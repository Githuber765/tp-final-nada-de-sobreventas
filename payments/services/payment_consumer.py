import pika
import json
import logging
from events.connection import get_rabbitmq_connection
from common.observability.logging import setup_logging
from common.observability.tracing import correlation_id_ctx

setup_logging()
logger = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    correlation_id = properties.headers.get('X-Correlation-Id') if properties.headers else None
    token = correlation_id_ctx.set(correlation_id) if correlation_id else None
    
    try:
        data = json.loads(body)
        logger.info(f"Received {data}", extra={"correlation_id": correlation_id})
        ch.basic_ack(delivery_tag=method.delivery_tag)
    finally:
        if token:
            correlation_id_ctx.reset(token)

def start_consumer():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange='order_events', exchange_type='fanout')
    
    result = channel.queue_declare(queue='payments_queue', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='order_events', queue=queue_name)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()
