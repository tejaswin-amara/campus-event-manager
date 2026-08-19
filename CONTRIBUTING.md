# Contributing to CampusConnect

> **Audience:** Students, maintainers, reviewers, and operators contributing to the CampusConnect website.
> **Repository principle:** Prefer the smallest change that solves the stated problem while preserving security, database integrity, and handout evidence.

Thank you for contributing to CampusConnect. The project is a Java 25 / Spring Boot 4.1.0 modular monolith backed by MySQL 8.4. Read the [README](README.md), [technical guide](TECHNICAL_GUIDE.md), and [project structure](PROJECT_STRUCTURE.md) before changing runtime behavior.

## Before starting

Search the [issue tracker](https://github.com/tejaswin-amara/campus-connect/issues) for an existing report, read the relevant requirement in [`docs/requirements.md`](docs/requirements.md), and identify whether the change affects data, authentication, authorization, migrations, operations, or the CO1–CO6 evidence package. For cleanup work, read [`docs/cleanup-audit.md`](docs/cleanup-audit.md) first.

## Development workflow

Clone the repository and create a focused topic branch.

```bash
git clone https://github.com/tejaswin-amara/campus-connect.git
cd campus-connect
git switch -c feat/short-description
# or: git switch -c fix/short-description
```

Use Docker Compose for the most reproducible local stack.

```bash
cp .env.example .env
# Fill .env with local-only values; do not commit it.
docker compose up --build -d
```

For code-only work, the Maven Wrapper is the canonical build entry point. Runtime-backed checks require MySQL configuration; CI and Compose use MySQL 8.4.

```bash
./mvnw -B verify
```

## Change standards

Write the smallest clear implementation that fits the existing layers. Do not introduce a new framework, service, ORM, frontend stack, agent runtime, or native-language component unless the requirement demonstrates a concrete benefit and the architecture documentation is updated.

| Area | Standard |
| --- | --- |
| Java | Follow existing package boundaries, constructor injection, validation, and readable naming |
| Web | Preserve CSRF, session protection, safe redirects, accessibility labels, responsive states, and user-safe errors |
| Database | Add a Flyway migration for schema changes; never edit an applied migration or use production `ddl-auto=update` |
| Security | Preserve explicit authorization, rate limits, secure cookies, upload validation, secret requirements, and structured audit behavior |
| Tests | Add focused tests for changed behavior and run the full verification command before review |
| Documentation | Update the relevant guide, requirement, API contract, compliance evidence, and version claim in the same change |
| Dependencies | Prefer platform/framework capabilities already present; remove dependencies only after reference-aware validation and a full build |

## Cleanup and deletion policy

Ponytail is used as an **advisory over-engineering audit**, not as an automatic deletion command. A deletion must be supported by reference searches, framework reachability checks, test coverage, and a clear explanation of why the file is not runtime, security, operations, rollback, or handout evidence. Ambiguous candidates are deferred rather than removed. See [`docs/cleanup-audit.md`](docs/cleanup-audit.md).

## Commit and pull-request conventions

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), for example:

```text
feat: add event capacity validation
fix: prevent duplicate interests
security: tighten upload validation
docs: map CO1 database evidence
ci: publish coverage artifact
```

Keep commits focused so reviewers can distinguish behavior, database, security, documentation, and infrastructure changes. A pull request should explain the problem, affected routes or tables, security impact, rollback considerations, and verification evidence. Link the relevant issue with `Closes #123` or `Fixes #456` where appropriate.

Before opening a pull request, use the following Git safety sequence.

```bash
git status --short
git diff --check
./mvnw -B verify
BASE_URL=http://localhost:9090 ./scripts/smoke-test.sh
REQUESTS=100 CONCURRENCY=10 BASE_URL=http://localhost:9090 ./scripts/load-test.sh
git diff --stat
git status --short
```

Do not force-push shared branches, rewrite remote history, or push a change whose expected file list has not been inspected. Confirm that workflow changes have the required GitHub permission before pushing them.

## Secrets and generated files

Never commit `.env`, passwords, private keys, production database URLs, generated uploads, `target/`, logs, or temporary credentials. Use `.env.example` for placeholders and repository/environment secret stores for deployment values.

## Review checklist

Reviewers should confirm that the change has a clear requirement, preserves the authentication and authorization matrix, validates user input, handles failure safely, avoids N+1 database behavior, preserves migration ordering, adds or updates tests, and keeps documentation internally consistent. For visual changes, verify keyboard navigation, focus states, labels, contrast, alt text, reduced-motion behavior, and mobile layout.

## Code of conduct

Contributors are expected to communicate respectfully, review ideas rather than people, and follow the project’s applicable community standards.

## References

[1]: https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail-audit/SKILL.md "Ponytail audit skill"
[2]: https://github.com/kunchenguid/no-mistakes "No Mistakes Git safety reference"
[3]: https://github.com/google/eng-practices "Google Engineering Practices"
[4]: https://github.com/github/opensource.guide "GitHub Open Source Guide"
[5]: https://owasp.org/www-project-application-security-verification-standard/ "OWASP Application Security Verification Standard"
