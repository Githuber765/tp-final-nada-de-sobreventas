import pika
import contextvars

correlation_id_ctx = contextvars.ContextVar("correlation_id", default=None)

def get_correlation_id():
    return correlation_id_ctx.get()

def inject_correlation_id(headers: dict):
    correlation_id = get_correlation_id()
    if correlation_id:
        headers["correlation_id"] = correlation_id
    return headers

def extract_correlation_id(headers: dict):
    return headers.get("correlation_id")
