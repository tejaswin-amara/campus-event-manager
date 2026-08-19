# CampusConnect security policy

> **Policy status:** Applies to the latest `main` branch
> **Security posture:** Production-oriented; deployment owners must provide environment-specific secrets, TLS, backups, monitoring, and incident ownership.

## Supported versions

| Version | Support status |
| --- | --- |
| Latest `main` branch | Supported |
| Older releases | Not supported unless explicitly agreed with the maintainer |

## Reporting a vulnerability

Do **not** open a public GitHub issue for a security vulnerability. Report it privately to the maintainer:

| Field | Value |
| --- | --- |
| Contact | Tejaswin Amara |
| Email | `TejaswinAmara1@duck.com` |
| Subject | `[SECURITY] CampusConnect — <brief description>` |

Please include a concise description, affected route or component, reproduction steps, impact assessment, relevant logs with secrets removed, and a suggested mitigation if available. Never include passwords, private keys, production database credentials, or unredacted personal data in a report.

The maintainer aims to acknowledge a report within 48 hours, provide an initial assessment within one week, and coordinate remediation and disclosure with the reporter. Timelines may vary for complex issues or third-party dependencies.

## Current security controls

| Area | Implemented control |
| --- | --- |
| Authentication | Session-based form login, BCrypt password hashing, dummy-hash timing mitigation, and production-required admin secret |
| Authorization | Explicit public allowlist and `ROLE_ADMIN` protection for administrative routes |
| Request integrity | CSRF protection for state-changing requests and session-fixation mitigation |
| Session cookies | HTTP-only and strict same-site behavior; `COOKIE_SECURE=true` in the production profile |
| Abuse control | Bucket4j login rate limiting backed by a bounded Caffeine cache |
| Input validation | Bean Validation, bounded request sizes, URL scheme checks, and controlled error responses |
| File uploads | MIME/type validation, size limits, safe generated names, and database-backed media handling |
| Database safety | Flyway-controlled schema, Hibernate validation, foreign keys, unique constraints, and pessimistic event-row locking |
| Browser hardening | Content Security Policy, frame denial, referrer policy, and content-type protection |
| Observability | Structured security audit logging with hashed identifiers and no raw secrets |
| Dependency hygiene | GitHub dependency review on pull requests and a verified MySQL-specific Flyway dependency for CI startup |

## Security review expectations

Changes affecting authentication, authorization, sessions, uploads, external links, migrations, logging, or dependencies require focused tests and a documentation update. Reviewers should confirm that error messages do not disclose internal state, redirects cannot be abused, metrics and actuator details are not publicly exposed, and production secrets are supplied through the deployment environment rather than source control.

The current threat model and control mapping are documented in [`docs/security/README.md`](docs/security/README.md). Implementation details are in [`TECHNICAL_GUIDE.md`](TECHNICAL_GUIDE.md#6-security-implementation), and DBSE&DBD evidence is indexed in [`docs/compliance-matrix.md`](docs/compliance-matrix.md).

## Secret and incident hygiene

Never commit `.env`, passwords, API keys, private keys, production database URLs, generated uploads, or temporary credentials. If a secret is exposed, revoke or rotate it immediately, preserve only sanitized evidence, and document the incident and affected commits. Git history should not be treated as a secret store.

## References

[1]: https://owasp.org/www-project-application-security-verification-standard/ "OWASP Application Security Verification Standard"
[2]: https://owasp.org/www-project-top-ten/ "OWASP Top Ten"
[3]: https://github.com/OWASP/CheatSheetSeries "OWASP Cheat Sheet Series"
