# Proposal: Distributed Tracing and Structured Logging

## Intent
To improve observability in our microservices architecture by enabling end-to-end request tracing and standardized, structured logging, significantly reducing debugging time.

## Scope

### In Scope
- Implement `correlation_id` FastAPI middleware for Catalog, Orders, Payments, and Notifications services.
- RabbitMQ message header propagation for `correlation_id`.
- Standardize JSON-formatted logging across all services.

### Out of Scope
- Integration with external APM tools (e.g., Jaeger, Datadog).
- Log aggregation/analysis backend infrastructure.

## Approach
1. Create a shared utility/middleware package to be used by all FastAPI services for generating/extracting the `X-Correlation-Id` header.
2. Update RabbitMQ publisher/consumer wrappers to inject and extract the `correlation_id` from message headers.
3. Configure the Python `logging` library to use a JSON formatter in all service entry points.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| All Microservices (`/services/*`) | Modified | Integration of new middleware and logging configuration |
| RabbitMQ Infrastructure code | Modified | Update message handling to propagate headers |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Performance overhead of extra header handling | Low | Minimal overhead, will test under load |
| Inconsistent implementation across services | Medium | Use a shared library/package for core observability code |

## Rollback Plan
Remove middleware injection and revert logging configuration changes in the affected microservices.

## Dependencies
- FastAPI
- pika (or equivalent RabbitMQ library)

## Success Criteria
- [ ] All logs within a single request flow share the same `correlation_id`.
- [ ] Log searching by `correlation_id` in a central logging system is trivial.
