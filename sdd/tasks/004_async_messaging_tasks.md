# Tasks: Async Messaging Integration

## Phase 1: Infrastructure
- [x] 1.1 Install and configure RabbitMQ client library (e.g., `amqp` or equivalent based on stack)
- [x] 1.2 Create `internal/events/contracts.go` defining shared Event structures (OrderPlaced, PaymentProcessed)
- [x] 1.3 Implement `internal/events/publisher.go` with interface for publishing events
- [x] 1.4 Implement `internal/events/subscriber.go` with interface for consuming events
- [x] 1.5 Add configuration environment variables for RabbitMQ connection (URL, Queues)

## Phase 2: Orders Module
- [x] 2.1 Update `orders/services/order_service.py` to inject EventPublisher
- [x] 2.2 Modify `CreateOrder` logic to publish `OrderPlaced` event upon success
- [x] 2.3 Ensure event publishing is wrapped in transaction or handled with idempotency (e.g., Outbox pattern)

## Phase 3: Payments/Notifications
- [x] 3.1 Implement `payments/services/payment_consumer.py` to listen for `OrderPlaced` events
- [x] 3.2 Implement `notificaciones/services/notification_consumer.py` to listen for `OrderPlaced` events
- [x] 3.3 Ensure consumers acknowledge messages correctly and handle errors without losing messages (dead-letter queues)

## Phase 4: Verification
- [x] 4.1 Write integration test: Verify `OrderPlaced` event is published when order is created
- [x] 4.2 Write integration test: Verify `Payments` service receives `OrderPlaced` and triggers payment
- [x] 4.3 Write integration test: Verify `Notifications` service receives `OrderPlaced` and sends notification
- [x] 4.4 Test resilience: Verify system behavior when RabbitMQ is temporarily unavailable (retry logic)
