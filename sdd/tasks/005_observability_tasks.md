# Tasks: Distributed Tracing and Structured Logging

## Phase 1: Middleware and Logging Foundation

- [x] 1.1 Create `common/observability/logging.py` with JSON log formatter.
- [x] 1.2 Create `common/observability/middleware.py` with FastAPI `CorrelationIdMiddleware`.
- [x] 1.3 Create `common/observability/tracing.py` for Correlation ID handling.
- [x] 1.4 Update `catalog/app.py`, `orders/api/orders.py`, `payments/api/payments.py` to use `CorrelationIdMiddleware`.
- [x] 1.5 Configure logging in all services (`catalog`, `orders`, `payments`, `notificaciones`) to use the JSON formatter from `common/observability/logging.py`.

## Phase 2: Orders/Payments/Notificaciones Integration

- [x] 2.1 Update `events/publisher.py` to inject `correlation_id` into RabbitMQ message headers.
- [x] 2.2 Update `orders/services/order_service.py` to extract `correlation_id` from context and use it during publishing.
- [x] 2.3 Update `notificaciones/services/notification_consumer.py` to extract `correlation_id` from RabbitMQ headers.
- [x] 2.4 Update `payments/services/payment_consumer.py` to extract `correlation_id` from RabbitMQ headers.

## Phase 3: Verification

- [x] 3.1 Verify HTTP requests have `X-Correlation-Id` header.
- [x] 3.2 Verify logs in all services contain the `correlation_id`.
- [x] 3.3 Verify RabbitMQ messages contain the `correlation_id` header and that consumers use it for logging.
