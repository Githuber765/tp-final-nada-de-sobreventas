# Proposal: async-messaging-integration

## Intent

Decouple modules (Orders, Payments, Notifications) to prevent cascading failures by introducing asynchronous messaging using RabbitMQ.

## Scope

### In Scope
- Add RabbitMQ to infrastructure.
- Implement Event-Driven communication (Publisher-Consumer).
- Events to support: `order.created`, `payment.completed`, `payment.failed`.

### Out of Scope
- Migrating existing synchronous HTTP endpoints (will be kept as a fallback or for direct user queries).
- Implementing complex message ordering guarantees (at-least-once delivery is sufficient).

## Approach

- Use RabbitMQ as the message broker.
- Define events as shared contracts/schemas using Pydantic models.
- Implement Publisher/Consumer patterns in affected modules (Orders, Payments, Notifications).
- Guarantee at-least-once delivery with publisher confirms and manual ACKs.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `infrastructure/` | New | Add RabbitMQ container |
| `orders/` | Modified | Publish `order.created` event |
| `payments/` | Modified | Consume `order.created`, Publish `payment.completed`/`payment.failed` |
| `notifications/`| New | Consume `payment.completed`/`payment.failed` |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Message loss | Low | Use publisher confirms and manual ACKs |
| Increased system complexity | Medium | Use well-defined schemas and shared contracts |
| RabbitMQ downtime | Low | Use container orchestration/resilience strategies |

## Rollback Plan

Revert changes to publisher/consumer logic in modules and remove/disable RabbitMQ infrastructure components.

## Dependencies

- RabbitMQ (Infrastructure)
- `pika` or `aio-pika` library

## Success Criteria

- [ ] Orders are created without blocking on payment processing.
- [ ] Payments are processed asynchronously via webhooks/consumers.
- [ ] Eventual consistency is maintained between services.
- [ ] No cascading failures when one module is down.
