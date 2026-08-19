# CampusConnect showcase script

## Demonstration objective

This demonstration shows a reviewer that CampusConnect is a working event-management product with a controlled relational backend, secure administration, reproducible delivery, and an honest architecture-evolution story aligned to CO1–CO6.

## Five-to-ten-minute flow

| Time | Demonstration | Evidence mapped |
| --- | --- | --- |
| 0:00–1:00 | Show the README, requirements, architecture context/container diagrams, and the current modular-monolith decision | CO4, CO6 |
| 1:00–2:00 | Start with `docker compose up --build -d`, show health-gated startup, then run `scripts/smoke-test.sh` | CO6 |
| 2:00–3:30 | Browse the student dashboard, search by event title/venue, filter by category, open an event, and follow the validated external registration flow | CO1, CO3 |
| 3:30–5:00 | Log in as an administrator, create or edit an event, upload an image, inspect validation behavior, view analytics, and export CSV | CO1, CO3 |
| 5:00–6:00 | Show Flyway migration V3, relational ER diagram, constraints, query indexes, and the event-row lock used by interest tracking | CO1 |
| 6:00–7:00 | Open `/v3/api-docs`, `/actuator/health`, and `/actuator/prometheus` through the appropriate review/monitoring path | CO3, CO6 |
| 7:00–8:00 | Show GitHub Actions CI, JaCoCo artifact, dependency review, container build, and test summary | CO6 |
| 8:00–9:00 | Run the load script and explain that the local result is a repeatable sanity check, not a production SLA | CO5, CO6 |
| 9:00–10:00 | Explain SQL/NoSQL/vector trade-offs, bounded contexts, and the future FastAPI/Node/Kafka evolution path without claiming unimplemented services | CO2, CO4, CO5 |

## Reviewer talking points

The strongest implemented evidence is the migration-controlled relational core, secure admin boundary, transaction-safe interest tracking, Docker/Compose startup, CI verification, health/metrics, and test/coverage artifacts. The strongest design evidence is the bounded-context map, polyglot persistence decision, semantic-search fallback strategy, and outbox/Saga evolution path.

The project should explicitly state that student “registration” currently means interest tracking plus external redirect. This avoids overclaiming internal seat allocation. If the reviewer asks for CO2 or CO5 implementation depth, show the data and services documents, then identify the next bounded slice rather than presenting a diagram as if it were deployed infrastructure.

## Final proof points

A clean checkout is the proof of reproducibility. The reviewer should be able to follow the README, configure placeholders, start the stack, see health become available, run the smoke test, inspect the OpenAPI document, execute the Maven verification lifecycle, and read a source-linked compliance matrix. Every production claim should point to an implementation artifact, a test, or a measured result.


## Hybrid feature proof point

After the student dashboard loads, show the **Recommended for you** section. Explain that the idea came from the Firebase-Addition matchmaker, but the final implementation is a server-side `RecommendationService` over MySQL events and registrations. The score is derived, explainable, limited to three upcoming events, covered by unit tests, and does not create a second data store or trust client-supplied roles or scores. The existing calendar and registration-link QR behavior remains available, while Firebase’s attendance pass, waitlist, mock payment, and notification features remain explicitly documented as future bounded contexts.
