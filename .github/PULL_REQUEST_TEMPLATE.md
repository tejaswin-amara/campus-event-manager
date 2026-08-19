## Description

<!-- Explain the problem, the user or operational impact, and the smallest solution. Link the relevant issue or requirement. -->

Fixes #

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Database or migration change
- [ ] Security change
- [ ] Documentation-only change
- [ ] CI/CD or operations change
- [ ] Cleanup or deletion
- [ ] Breaking change

## Scope and impact

- Affected routes, templates, services, or jobs:
- Affected tables or migrations:
- Authentication, authorization, CSRF, upload, redirect, or secret impact:
- Rollback or recovery consideration:

## Verification evidence

<!-- Describe the exact commands and environment. CI and Compose use Java 25 and MySQL 8.4. -->

- [ ] `./mvnw -B verify`
- [ ] Focused tests for changed behavior
- [ ] `BASE_URL=http://localhost:9090 ./scripts/smoke-test.sh`
- [ ] `REQUESTS=100 CONCURRENCY=10 BASE_URL=http://localhost:9090 ./scripts/load-test.sh`
- [ ] Manual browser verification where applicable
- [ ] Documentation links and commands reviewed

If the full verification path was blocked by the local environment, explain the limitation and identify the CI/Compose evidence that covers it.

## Checklist

- [ ] The commit subject follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- [ ] The implementation follows the existing modular boundaries and avoids an unnecessary framework or dependency.
- [ ] New behavior has focused tests; the suite remains consistent with the documented 63-test baseline or the count is updated.
- [ ] Database migrations are additive, reviewed, and tested against MySQL 8.4.
- [ ] Flyway migration ownership and Hibernate `validate` behavior are preserved.
- [ ] Authorization, CSRF, validation, upload, redirect, session, and secret-handling implications were reviewed.
- [ ] No credentials, `.env` files, private keys, generated uploads, target output, or local machine paths are committed.
- [ ] `git diff --check` passes.
- [ ] The relevant README, architecture, API, security, operations, testing, requirements, or compliance documentation is updated.

## Cleanup-specific review

- [ ] Any deletion was checked against source, template, configuration, migration, test, CI, and documentation references.
- [ ] Deleted material was not required for runtime, security, rollback, operations, contributor workflows, or DBSE&DBD evidence.
- [ ] The disposition is recorded in [`docs/cleanup-audit.md`](../docs/cleanup-audit.md) when applicable.

## References

[1]: https://www.conventionalcommits.org/en/v1.0.0/ "Conventional Commits"
[2]: https://documentation.red-gate.com/flyway/reference "Flyway reference"
[3]: https://owasp.org/www-project-application-security-verification-standard/ "OWASP Application Security Verification Standard"
