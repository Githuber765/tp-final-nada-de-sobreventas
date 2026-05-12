# Tasks: Payments Module

## Phase 1: Foundation (Structure, DB, Models)

- [x] 1.1 Create `payments/` directory structure.
- [x] 1.2 Define `payment_methods`, `payments`, and `transactions` database schemas in `payments/models/`.
- [x] 1.3 Implement models and repository interfaces in `payments/models/` and `payments/database/`.
- [x] 1.4 Define configuration structure for payment providers in `payments/config/`.

## Phase 2: Core Functionality (Processing, Status)

- [x] 2.1 Implement `CreatePaymentIntent` service in `internal/payments/service/`.
- [x] 2.2 Build webhook handler for payment providers in `internal/payments/api/webhook_handler.go`.
- [x] 2.3 Implement status querying service in `internal/payments/service/`.
- [x] 2.4 Add robust error handling and logging for payment failures in `internal/payments/errors/`.

## Phase 3: Testing and Validation

- [x] 3.1 Write unit tests for payment intent logic and status mapping in `tests/payments/test_services.py`.
- [x] 3.2 Create integration tests for repository layer in `tests/payments/test_repository.py`.
- [x] 3.3 Implement E2E test suite with mock payment provider in `tests/payments/test_e2e.py`.

## Phase 4: Migration and Refactoring (Integration into main app)

- [x] 4.1 Expose public API endpoints for payment operations in `payments/api/` and mount them in `main.py`.
- [x] 4.2 Refactor checkout flow in the main application to integrate the `payments` module service.
- [x] 4.3 Update API documentation and finalize module code structure.
