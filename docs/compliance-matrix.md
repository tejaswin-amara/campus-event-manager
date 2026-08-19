# DBSE&DBD compliance matrix

The attached handout emphasizes relational engineering, SQL/NoSQL/vector concepts, backend APIs, polyglot framework awareness, microservices, deployment, observability, CI/CD, security, load testing, C4 diagrams, README quality, and a final showcase. This matrix records what is implemented, what is documented as an evolution design, and where the evidence lives.

| CO | Outcome focus | Implemented evidence | Design/documentation evidence | Status |
| --- | --- | --- | --- | --- |
| CO1 | Normalized relational schema, optimized SQL, transactions, and backend integration | `V1__Initial_Schema.sql`, V2/V3 migrations, JPA models/repositories, Flyway startup, `EventService` transaction, pessimistic event-row lock, indexes/checks, analytics queries, 58 passing tests | [`docs/data/README.md`](data/README.md) and ER diagram | **Implemented** |
| CO2 | SQL/NoSQL comparison, polyglot persistence, vector/semantic search | MySQL relational core and indexed lexical search are implemented | SQL/NoSQL/vector decision table, document-store/activity boundary, pgvector/vector adapter with lexical fallback, authorization-aware derived data | **Partially implemented; design evidence complete** |
| CO3 | Production-quality APIs, validation, authentication, JWT/OAuth2 concepts, OpenAPI, testing | Spring MVC routes, Bean Validation, Spring Security, CSRF, RBAC, rate limiting, session handling, Springdoc `/v3/api-docs`, controller/security tests | [`docs/api/README.md`](api/README.md) describes current HTML/API mix and future JSON contract | **Implemented for current Spring MVC architecture** |
| CO4 | Node.js/Express and Spring Boot services, SOA and architectural thinking | Spring Boot modular service layer, controller/service/repository separation, Resilience4j | Bounded-context and future Node.js/Express/FastAPI extraction options in [`docs/services/README.md`](services/README.md) and architecture C4 views | **Spring implemented; polyglot evolution documented** |
| CO5 | Microservice decomposition, REST and asynchronous messaging, distributed concepts | Current single deployment has explicit logical modules, transaction boundaries, resilience fallback, and external integration boundary | Service ownership, future gateway, outbox/Kafka, idempotency, Saga/compensating-action strategy in architecture/services docs | **Architecture evidence complete; distributed runtime deferred** |
| CO6 | Containerized delivery, C4 documentation, CI/CD, observability, security, load test, showcase | Dockerfile, secret-required Compose, health check, Prometheus registry, Actuator, GitHub Actions, JaCoCo gate, dependency review, smoke/load scripts, README | C4 context/container/component/deployment diagrams, operations/runbook, security guide, showcase script, repository-reference register | **Implemented for a production-oriented modular monolith** |

## Evidence index

| Evidence type | Path |
| --- | --- |
| Product and quick start | [`README.md`](../README.md) |
| Requirements | [`docs/requirements.md`](requirements.md) |
| Architecture/C4 | [`docs/architecture/README.md`](architecture/README.md) |
| Data engineering | [`docs/data/README.md`](data/README.md) |
| API contract | [`docs/api/README.md`](api/README.md) |
| Service evolution | [`docs/services/README.md`](services/README.md) |
| Operations | [`docs/operations/README.md`](operations/README.md) |
| Security | [`docs/security/README.md`](security/README.md) |
| Testing and release evidence | [`docs/testing/README.md`](testing/README.md) |
| Showcase | [`docs/showcase.md`](showcase.md) |
| Supplied repository integration | [`docs/reference-repositories.md`](reference-repositories.md) |
| Runtime smoke test | [`scripts/smoke-test.sh`](../scripts/smoke-test.sh) |
| Runtime load check | [`scripts/load-test.sh`](../scripts/load-test.sh) |
| CI/CD | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| Schema migrations | [`src/main/resources/db/migration/`](../src/main/resources/db/migration/) |

## Honest limitations

The matrix intentionally distinguishes implementation from design. The current codebase does not contain a MongoDB service, vector index, Kafka broker, FastAPI gateway, Node.js service, Kubernetes deployment, or React frontend. Those technologies are represented through bounded-context decisions, contract guidance, and a prioritized evolution path. Adding them without a product requirement would increase deployment risk and slow the production path.
