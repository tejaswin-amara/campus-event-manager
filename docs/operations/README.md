# Operations and delivery

## Runtime topology

The supported local topology is Docker Compose with one MySQL service and one non-root Java application container. The database has a health check; the application waits for the database to become healthy before starting. The application writes event images to a named uploads volume and exposes a health endpoint for deployment probes.

```bash
cp .env.example .env
# Replace every placeholder in .env.
docker compose up --build -d
curl --fail http://localhost:9090/actuator/health
```

The Compose file binds the database and application to localhost by default. A production deployment should place the application behind HTTPS and a private database network rather than exposing MySQL publicly.

## Configuration and secret handling

Required credentials are passed through environment variables and are not embedded as usable defaults. `ADMIN_PASSWORD` is mandatory for Compose and for the `prod` profile. The application profile defaults to `DDL_AUTO=validate`, and Flyway applies migrations before JPA validates the schema. The production profile enables TLS-oriented settings and secure session cookies, but provider-specific certificate verification and secret-manager wiring remain deployment responsibilities.

The supplied [Docker Awesome Compose](https://github.com/docker/awesome-compose) repository informs the health-gated dependency and volume approach. The supplied [free-for-dev](https://github.com/ripienaar/free-for-dev) repository is a comparison source for hosting options, not a deployment decision. A provider should be selected only after evaluating database durability, TLS, secret storage, logs, metrics, egress, and backup limits.

## Database operations

Production startup follows this order: provision the database and least-privilege application user; configure the JDBC URL and credentials; run the application with `SPRING_PROFILES_ACTIVE=prod`; let Flyway validate and apply pending migrations; allow Hibernate to validate the resulting schema; then verify `/actuator/health` and the smoke script. Do not use schema auto-update in production.

Back up both MySQL and the uploads volume. Restore testing must include migration replay, representative event images, users, event interest records, and application startup against the restored database. Define retention and deletion rules for personally identifiable data and audit records before operating at institutional scale.

## Observability

| Signal | Current implementation | Operating use |
| --- | --- | --- |
| Health | `/actuator/health` | Liveness/readiness and dependency probe |
| Metrics | Micrometer Prometheus registry and `/actuator/prometheus` | Request, JVM, and application trend monitoring |
| Logs | SLF4J/Logback with structured/audit logging | Incident investigation and security review |
| Resilience | Registration circuit-breaker configuration | Detect downstream degradation and fallback behavior |
| Coverage | JaCoCo report artifact in CI | Regression guard for tested behavior |

Protect metrics and detailed actuator endpoints at the network or authentication layer. Do not expose health details, environment values, or thread dumps to the public internet.

## CI/CD pipeline

The GitHub Actions workflow performs checkout, Java 21 setup, Maven verification against a MySQL service, JaCoCo artifact upload, container image build, and dependency review for pull requests. The workflow is intentionally build-and-verify only; publishing requires a separately approved release workflow with registry credentials, signed artifacts, deployment credentials, and rollback policy.

The workflow structure is informed by [GitHub starter workflows](https://github.com/actions/starter-workflows) and [GitHub Actions documentation](https://docs.github.com/en/actions). A production extension should add immutable image tags, SBOM generation, vulnerability thresholds, environment approvals, database migration policy, deployment smoke checks, and automatic rollback criteria.

## Kubernetes awareness

The application container is compatible with a future Kubernetes deployment, but this repository does not claim a production Kubernetes cluster. A future deployment should define a Deployment with at least two replicas where the database and uploads strategy support it, a Service, readiness/liveness probes, resource requests/limits, a Secret reference, a ConfigMap for non-secret settings, an Ingress with TLS, and a PodDisruptionBudget. Stateful data should use a managed database and durable object/file storage rather than local pod disks.

## Release checklist

Before release, verify that the target commit is reviewed, CI is green, migrations are backward-compatible, secrets are configured, the container is non-root, health and smoke checks pass, the image is scanned, backups exist, restore ownership is assigned, metrics are scraped, and rollback steps are documented. The final release must record the exact commit, image digest, migration version, and environment.

## References

[1]: https://docs.docker.com/compose/ "Docker Compose documentation"
[2]: https://docs.github.com/en/actions "GitHub Actions documentation"
[3]: https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html "Spring Boot Actuator reference"
[4]: https://micrometer.io/docs/registry/prometheus "Micrometer Prometheus registry"
[5]: https://github.com/ripienaar/free-for-dev "Free-for-dev comparison list"
