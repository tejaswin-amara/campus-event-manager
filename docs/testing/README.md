# Testing and release evidence

## Current baseline

The repository contains 58 automated tests covering configuration, initialization, controllers, security, exception handling, rate limiting, services, and session behavior. The Maven `verify` lifecycle runs the suite against MySQL, generates JaCoCo output, and enforces minimum bundle coverage of 70% for lines and 40% for branches.

## Test layers

| Layer | Purpose | Current evidence |
| --- | --- | --- |
| Service unit tests | Business rules, filtering, analytics, registration-interest behavior, user/session logic | `src/test/java/com/tejaswin/campus/service` |
| Controller tests | View/redirect contracts, search/category behavior, validation, and external redirect behavior | `src/test/java/com/tejaswin/campus/controller` |
| Security tests | Admin boundaries, CSRF, login behavior, session fixation configuration, rate limiting | `AdminControllerSecurityTest`, `AdminControllerIntegrationTest`, `SessionFixationTest`, `RateLimitingFilterTest` |
| Context/integration tests | Flyway, JPA, MySQL-backed application startup, initialization, and audit logger behavior | `@SpringBootTest` classes |
| Smoke tests | Health, OpenAPI, and root-route availability | `scripts/smoke-test.sh` |
| Load checks | Concurrent health requests with recorded throughput and failures | `scripts/load-test.sh` |
| Accessibility | Manual checklist and future browser automation boundary | `docs/showcase.md`; future axe-core/Cypress integration |

## Commands

```bash
./mvnw -B verify
BASE_URL=http://localhost:9090 ./scripts/smoke-test.sh
REQUESTS=100 CONCURRENCY=10 BASE_URL=http://localhost:9090 ./scripts/load-test.sh
```

The supplied [Cypress Real World App](https://github.com/cypress-io/cypress-realworld-app) informs the future browser-E2E strategy: use seeded data, explicit authentication flows, deterministic cleanup, and CI artifacts. The current project does not vendor Cypress because it has no Node-based frontend test harness; the shell smoke path remains the minimal portable release gate.

The supplied [axe-core](https://github.com/dequelabs/axe-core) informs the accessibility backlog. Before adopting it, choose a browser runner and add checks for keyboard navigation, heading hierarchy, form labels, contrast, focus states, alt text, reduced motion, and error announcement behavior.

## Load-test method

The current load script sends concurrent requests to `/actuator/health` by default. It is a deployment sanity check, not a capacity certification. For a meaningful event-catalogue benchmark, run against `/student/dashboard` with a seeded database and record request count, concurrency, duration, throughput, latency percentiles, error rate, database CPU, connection-pool utilization, and JVM memory. Repeat the same scenario after indexing or caching changes.

A release record should include the exact environment, commit, Java/MariaDB/MySQL versions, request target, test parameters, and result. Do not present local sandbox throughput as a production SLA.

## Release gates

A release candidate must compile on Java 21, pass all tests, satisfy JaCoCo thresholds, pass the smoke script, build the container, contain no committed secrets, apply Flyway migrations cleanly, expose healthy status, and have reviewed documentation. Production deployment adds image scanning, TLS verification, backup/restore evidence, metrics scraping, and an approved rollback plan.

## References

[1]: https://github.com/cypress-io/cypress-realworld-app "Cypress Real World App testing reference"
[2]: https://github.com/dequelabs/axe-core "axe-core accessibility engine"
[3]: https://docs.github.com/en/actions "GitHub Actions documentation"
[4]: https://www.jacoco.org/jacoco/trunk/doc/check-mojo.html "JaCoCo check goal"
