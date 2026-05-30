from prometheus_client import Counter, Gauge, Histogram


reserve_attempts_total = Counter(
    "reserve_attempts_total",
    "Cantidad total de intentos de reserva",
    ["result"]
)

reserve_duration_seconds = Histogram(
    "reserve_duration_seconds",
    "Duracion de las reservas en segundos"
)

inventory_stock_level = Gauge(
    "inventory_stock_level",
    "Stock actual por producto",
    ["product_id"]
)

overselling_attempts_total = Counter(
    "overselling_attempts_total",
    "Cantidad de intentos de overselling detectados"
)