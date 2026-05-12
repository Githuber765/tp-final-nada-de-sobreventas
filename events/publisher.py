import pika
import json
import os
from events.connection import get_rabbitmq_connection
from common.observability.tracing import correlation_id_ctx

class EventPublisher:
    def __init__(self):
        self.connection = get_rabbitmq_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='order_events', exchange_type='fanout')

    def publish(self, event_type: str, message: dict):
        correlation_id = correlation_id_ctx.get()
        headers = {}
        if correlation_id:
            headers['X-Correlation-Id'] = correlation_id

        self.channel.basic_publish(
            exchange='order_events',
            routing_key='',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=2, # make message persistent
                headers=headers
            )
        )
