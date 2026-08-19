# CampusConnect documentation

> **Documentation status:** Maintained for the current `main` branch
> **Audience:** Developers, reviewers, release operators, security reviewers, and DBSE&DBD evaluators
> **System posture:** Production-oriented Spring Boot modular monolith with documented evolution boundaries

This directory is the evidence package for CampusConnect. It explains **what is implemented**, **how to run and verify it**, and **which distributed or polyglot capabilities are intentionally documented as future evolution rather than misrepresented as live services**.

## Start here

| Need | Read |
| --- | --- |
| Understand the product and run it locally | [`README.md`](../README.md) |
| Navigate the system and C4 views | [`architecture/README.md`](architecture/README.md) |
| Understand the relational model and migrations | [`data/README.md`](data/README.md) |
| Review routes, authentication, and validation | [`api/README.md`](api/README.md) |
| Operate, deploy, back up, and troubleshoot | [`operations/README.md`](operations/README.md) |
| Review threats and security controls | [`security/README.md`](security/README.md) |
| Run tests and collect release evidence | [`testing/README.md`](testing/README.md) |
| Prepare the five-to-ten-minute demonstration | [`showcase.md`](showcase.md) |

## Documentation map

### Product and requirements

| Document | Purpose |
| --- | --- |
| [`requirements.md`](requirements.md) | Problem statement, actors, scope, functional requirements, and non-functional acceptance criteria |
| [`compliance-matrix.md`](compliance-matrix.md) | CO1–CO6 traceability from handout outcome to source, test, and operational evidence |
| [`showcase.md`](showcase.md) | Demonstration script, reviewer talking points, and evidence sequence |

### Engineering and architecture

| Document | Purpose |
| --- | --- |
| [`architecture/README.md`](architecture/README.md) | C4 context, container, component, deployment, bounded contexts, and evolution decisions |
| [`data/README.md`](data/README.md) | Normalization, constraints, indexes, transactions, migration ownership, and SQL/NoSQL/vector trade-offs |
| [`api/README.md`](api/README.md) | Current HTML-plus-targeted-endpoint contract, route inventory, validation, errors, and future JSON boundaries |
| [`services/README.md`](services/README.md) | Current logical modules and safe extraction boundaries for future services |
| [`hybrid-integration-decision.md`](hybrid-integration-decision.md) | Comparison with Firebase-Addition and provenance of the implemented recommendation feature |
| [`reference-repositories.md`](reference-repositories.md) | Complete register of supplied repositories and how each informed the solution |
| [`cleanup-audit.md`](cleanup-audit.md) | Ponytail findings, deletion dispositions, reachability safeguards, and cleanup evidence |
| [`stable-versions.md`](stable-versions.md) | Stable version policy, compatibility decisions, and upgrade evidence |

### Delivery and governance

| Document | Purpose |
| --- | --- |
| [`operations/README.md`](operations/README.md) | Configuration, migrations, health, metrics, deployment, backups, and incident handling |
| [`security/README.md`](security/README.md) | Threat model, authentication, authorization, OWASP-oriented controls, and residual risk |
| [`testing/README.md`](testing/README.md) | Test pyramid, coverage, smoke/load checks, CI gates, and release evidence |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | Branching, commits, review, test evidence, and secret hygiene |
| [`../SECURITY.md`](../SECURITY.md) | Vulnerability reporting policy |
| [`../PROJECT_STRUCTURE.md`](../PROJECT_STRUCTURE.md) | Source tree and responsibility map |
| [`../TECHNICAL_GUIDE.md`](../TECHNICAL_GUIDE.md) | Implementation-oriented guide for maintainers |

## Reading conventions

The documentation uses the following language consistently.

| Term | Meaning |
| --- | --- |
| **Implemented** | Present in source, exercised by tests or runtime checks, and safe to claim as current behavior |
| **Documented evolution** | A designed future boundary or technology option that is not deployed in the current release |
| **External registration** | The configured registration URL remains authoritative; the local `registrations` table records student interest and analytics |
| **Production-oriented** | Suitable for controlled deployment after environment-specific secrets, TLS, storage, backups, and operational ownership are configured |

## Verification commands

```bash
# Complete build, test, package, migration validation, and coverage gate
./mvnw -B verify

# Runtime checks after starting the application
BASE_URL=http://localhost:9090 ./scripts/smoke-test.sh
REQUESTS=100 CONCURRENCY=10 BASE_URL=http://localhost:9090 ./scripts/load-test.sh
```

The committed CI and Compose paths target **MySQL 8.4**. If a local sandbox only provides MySQL 8.0, Flyway 12 may reject it; use the documented migration procedure in [`operations/README.md`](operations/README.md) rather than weakening the production configuration.

## Source references

[1]: https://docs.spring.io/spring-boot/docs/current/reference/html/ "Spring Boot reference documentation"
[2]: https://documentation.red-gate.com/flyway/reference "Flyway reference documentation"
[3]: https://docs.github.com/en/actions "GitHub Actions documentation"
[4]: https://owasp.org/API-Security/editions/2023/en/0x00-header/ "OWASP API Security Top 10"
