# Spec-Driven Development Initialization

## Project Overview
This project implements a monolithic marketplace system using FastAPI and MySQL, designed to demonstrate scalability limitations under load testing conditions.

## Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: MySQL (via SQLAlchemy async with aiomysql)
- **Testing**: Locust for load testing
- **Persistence**: SQLAlchemy ORM with async session management

## Current Architecture
The system is a single monolithic application with:
- Shared database connection pool (pool_size=5, max_overflow=10)
- Shared business logic across all modules
- Centralized data access layer
- Synchronous processing with simulated latency on payment endpoint

## Persistence Setup
The persistence layer uses:
- SQLAlchemy async engine with aiomysql driver
- Connection pooling configuration (pool_size=5, max_overflow=10)
- Async session management with dependency injection
- ORM models for Producto and PedidoORM

## Key Limitations Identified
1. **Resource contention**: Shared database connection pool leads to QueuePool limit exceeded errors
2. **Blocking operations**: Simulated payment delay blocks entire request processing
3. **Coupling**: All modules share the same database and session lifecycle
4. **Fault propagation**: Single point of failure for both database and application

## SDD Implementation Plan
This SDD setup will enable:
- Spec-driven development of modular components
- Clear separation of concerns for each module
- Improved testability and maintainability
- Better scalability planning for future microservices migration