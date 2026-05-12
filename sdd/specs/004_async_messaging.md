# Asynchronous Messaging Specification

## Purpose
Define asynchronous communication patterns for microservices using RabbitMQ, ensuring reliability, consistency, and idempotency.

## Requirements

### Requirement: Publisher Reliability
The publisher MUST implement publisher confirms to ensure events are successfully received by the RabbitMQ broker.

### Requirement: Consumer Reliability
The consumer MUST implement manual acknowledgment (ACK) to ensure event processing completion before the message is removed from the queue.

### Requirement: Idempotent Consumers
All consumers MUST be designed as idempotent to handle duplicate events safely.

## Scenarios

### Scenario: Order Created Triggers Notification
- GIVEN the Order Service has successfully persisted an order
- WHEN the Order Service publishes an `order.created` event to RabbitMQ
- THEN the Notification Service MUST consume the `order.created` event
- AND the Notification Service MUST send an email confirmation to the customer

### Scenario: Payment Failure Cancels Order
- GIVEN a payment attempt has failed
- WHEN the Payment Service publishes a `payment.failed` event to RabbitMQ
- THEN the Order Service MUST consume the `payment.failed` event
- AND the Order Service MUST update the order status to "CANCELLED"
