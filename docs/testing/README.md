# Testing and release evidence

> **Current baseline:** 63 automated tests
> **Coverage gates:** JaCoCo line coverage at least 70%; branch coverage at least 40%
> **Release runtime:** Java 25 with MySQL 8.4 in CI and Compose

## Test layers

| Layer | Purpose | Current evidence |
| --- | --- | --- |
| Service unit tests | Business rules, filtering, analytics, registration-interest behavior, recommendation scoring, and user/session logic | `src/test/java/com/tejaswin/campus/service` |
| Model tests | Domain invariants and derived DTO behavior | `EventTest`, `RecommendedEventTest` |
| Controller tests | View/redirect contracts, search/category behavior, validation, and external redirect behavior | `src/test/java/com/tejaswin/campus/controller` |
| Security tests | Admin boundaries, CSRF, login behavior, session fixation, rate limiting, and audit logging | `AdminControllerSecurityTest`, `AdminControllerIntegrationTest`, `SessionFixationTest`, `RateLimitingFilterTest`, `SecurityAuditLoggerTest` |
| Context/integration tests | Flyway, JPA, MySQL-backed application startup, initialization, and secured request behavior | `@SpringBootTest` classes |
| Smoke tests | Health, OpenAPI, and root-route availability | `scripts/smoke-test.sh` |
| Load checks | Concurrent health requests with recorded throughput and failures | `scripts/load-test.sh` |
| Accessibility | Manual checklist and future browser automation boundary | [`docs/showcase.md`](../showcase.md); future axe-core/Cypress integration |

The suite contains **63 tests**. Test count is evidence for the current commit and should be updated whenever a test is added or removed.

## Verification commands

```bash
# Full build, tests, migrations, package, and coverage gate
./mvnw -B verify

# Runtime checks after starting the application
BASE_URL=http://localhost:9090 ./scripts/smoke-test.sh
REQUESTS=100 CONCURRENCY=10 BASE_URL=http://localhost:9090 ./scripts/load-test.sh
```

The committed CI workflow and Docker Compose path use **MySQL 8.4**. The sandbox used for code-only work may expose MySQL 8.0 or no usable credentials; Flyway 12 can reject an unsupported server, so that limitation must be reported rather than hidden by weakening production configuration. Runtime-backed tests should be run through MySQL 8.4 in CI/Compose or an equivalently configured environment.

The supplied [Cypress Real World App](https://github.com/cypress-io/cypress-realworld-app) informs a future browser-E2E strategy: use seeded data, explicit authentication flows, deterministic cleanup, and CI artifacts. The current project does not vendor Cypress because it has no Node-based frontend test harness; the shell smoke path remains the minimal portable release gate.

The supplied [axe-core](https://github.com/dequelabs/axe-core) informs the accessibility backlog. Before adoption, choose a browser runner and add checks for keyboard navigation, heading hierarchy, form labels, contrast, focus states, alt text, reduced motion, and error announcement behavior.

## Load-test method

The current load script sends concurrent requests to `/actuator/health` by default. It is a deployment sanity check, not a capacity certification. For a meaningful event-catalogue benchmark, run against `/student/dashboard` with a seeded database and record request count, concurrency, duration, throughput, latency percentiles, error rate, database CPU, connection-pool utilization, and JVM memory. Repeat the same scenario after indexing or caching changes.

A release record should include the exact environment, commit, Java/MySQL versions, request target, test parameters, and result. Do not present local sandbox throughput as a production SLA.

## Release gates

A release candidate must compile on Java 25, pass all 63 tests, satisfy the JaCoCo thresholds, pass the smoke script, build the container, contain no committed secrets, apply Flyway migrations cleanly on MySQL 8.4, expose healthy status, and have reviewed documentation. Production deployment adds image scanning, TLS verification, backup/restore evidence, metrics scraping, and an approved rollback plan.

## References

[1]: https://github.com/cypress-io/cypress-realworld-app "Cypress Real World App testing reference"
[2]: https://github.com/dequelabs/axe-core "axe-core accessibility engine"
[3]: https://docs.github.com/en/actions "GitHub Actions documentation"
[4]: https://www.jacoco.org/jacoco/trunk/doc/check-mojo.html "JaCoCo check goal"
[5]: https://documentation.red-gate.com/flyway/reference "Flyway reference"
