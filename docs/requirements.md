# CampusConnect requirements

## Problem statement

University event information is often scattered across clubs, departments, social channels, and external registration forms. Students need a trustworthy place to discover events and follow a consistent path to details and registration. Administrators need controlled event lifecycle management, engagement visibility, and exportable records without exposing privileged operations to public users.

CampusConnect addresses this problem with a public discovery experience, an administrator-only management surface, relational event and interest data, validated media handling, and operational controls suitable for a controlled production deployment.

## Actors and responsibilities

| Actor | Responsibilities | Access boundary |
| --- | --- | --- |
| Student/guest | Browse, search, filter, view event details, and follow an external registration path | Public student routes; no administrative mutation |
| Administrator | Create, edit, delete, analyze, filter, and export event data | Spring Security `ADMIN` role and CSRF-protected state changes |
| Database operator | Provision MySQL, manage credentials, apply migrations, back up data, and verify restore procedures | Infrastructure responsibility; no application UI access implied |
| Release operator | Review CI results, publish an approved image, configure secrets/TLS, and monitor health/metrics | Repository and deployment responsibility |

## Functional requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| FR-01 | The system shall display upcoming and historical campus events with title, description, time, venue, category, and optional media. | Student dashboard and event detail views; controller tests |
| FR-02 | The system shall support search and category filtering with pagination. | `EventController`, `EventRepository`, service tests, and smoke flow |
| FR-03 | Only an authenticated administrator with the `ADMIN` role shall mutate event data or access administrative dashboards. | `SecurityConfig`, security integration tests, RBAC matrix |
| FR-04 | Event create/edit operations shall validate required fields, dates, URLs, capacities, and media inputs. | Bean Validation, controller validation, and test cases |
| FR-05 | The system shall record at most one interest row per user-event pair. | Unique database constraint and transaction-safe registration-interest workflow |
| FR-06 | The system shall redirect a user only to a configured HTTP/HTTPS registration URL. | URL scheme validation and controller test |
| FR-07 | The system shall provide event analytics and CSV export to authorized administrators. | Admin dashboard and export test |
| FR-08 | The system shall apply versioned database migrations before JPA validation. | Flyway V1–V3 and `DDL_AUTO=validate` production contract |
| FR-09 | The system shall expose an unauthenticated health check and generated OpenAPI document for operational and review purposes. | `/actuator/health`, `/v3/api-docs`, and smoke script |
| FR-10 | The system shall provide structured logs, audit events, and Prometheus-compatible metrics for operational analysis. | Logback configuration, audit logger, Micrometer registry, and operations guide |

## Non-functional requirements

The application shall start reproducibly from documented environment variables and shall fail fast when required production secrets are absent. Schema changes shall be migration-controlled, application containers shall run as a non-root user, and state-changing requests shall preserve CSRF and RBAC protections. The system shall keep error responses free of stack traces and shall default to informational application logging rather than debug verbosity.

The delivery pipeline shall compile on Java 21, run the existing integration-backed test suite against MySQL, enforce line and branch coverage thresholds, upload a JaCoCo artifact, build the container image, and review dependency changes on pull requests. Runtime validation shall include health, OpenAPI, smoke, and lightweight load checks.

## Scope boundaries

The current release intentionally does not represent a complete ticketing, payment, calendar-recurrence, or internal registration platform. The `registrations` table records interest before an external registration redirect; it is not an authoritative seat-allocation ledger. MongoDB, vector search, Kafka, FastAPI, Node.js, Kubernetes, and a React mobile client are documented as carefully bounded evolution options in the architecture package. They should be introduced only when a real product requirement and an operational owner exist.

## Future requirements

The next evolution slice should add explicit event status and moderation workflows, time-zone-aware scheduling, internal capacity reservations, notifications, audit retention, and privacy controls. If semantic discovery becomes a priority, the vector adapter should be implemented behind a feature flag with lexical fallback and authorization-aware filtering. If independent deployment becomes necessary, the event catalogue, identity, registration, and activity contexts are the first extraction candidates.

## References

[1]: https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html "Spring Security authorization"
[2]: https://documentation.red-gate.com/flyway/reference "Flyway reference"
[3]: https://owasp.org/API-Security/editions/2023/en/0x00-header/ "OWASP API Security Top 10"
