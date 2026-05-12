# Distributed Tracing and Structured Logging Specification

## Purpose

This specification defines the requirements for implementing distributed tracing via `correlation_id` injection and extraction, as well as structured JSON logging across all microservices (Catalog, Orders, Payments, Notifications) to improve observability and reduce debugging time.

## Requirements

### Requirement: Correlation ID Middleware

The system MUST generate a unique `correlation_id` (UUID) for every incoming HTTP request if one is not present in the `X-Correlation-Id` header.
The system MUST include the `correlation_id` in every log entry produced within the scope of the request.
The system MUST propagate the `correlation_id` to downstream services via HTTP headers.

#### Scenario: Correlation ID generation and logging
- GIVEN a request arrives without an `X-Correlation-Id` header
- WHEN the request is processed
- THEN a new `correlation_id` is generated
- AND all log entries for this request contain the generated `correlation_id`

### Requirement: RabbitMQ Header Propagation

The system MUST propagate the `correlation_id` in the message headers when publishing to RabbitMQ.
The system MUST extract the `correlation_id` from message headers when consuming from RabbitMQ and use it for subsequent logging.

#### Scenario: Message header propagation
- GIVEN a request generates a `correlation_id`
- WHEN a message is published to RabbitMQ
- THEN the `correlation_id` is included in the message headers
- AND when the consumer processes the message, it logs using that `correlation_id`

### Requirement: Structured JSON Logging

The system MUST produce logs in a standardized JSON format.
Each log entry MUST include the `correlation_id`, `timestamp`, `level`, `service_name`, and `message`.

#### Scenario: Log format validation
- GIVEN an application event occurs
- WHEN a log is generated
- THEN the output is in JSON format
- AND contains `correlation_id`, `timestamp`, `level`, `service_name`, and `message`
