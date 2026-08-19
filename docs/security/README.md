# Security architecture and review

## Security posture

The current verified baseline is Java 25, Spring Boot 4.1.0, Spring Security 7.1.0, MySQL 8.4, and Flyway 12.4.0 with the `flyway-mysql` database module. The latest repair run [32272882649](https://github.com/tejaswin-amara/campus-connect/actions/runs/32272882649) passed the CI build, tests, coverage, and container-build path.

CampusConnect uses a defense-in-depth web security model: BCrypt password hashing, Spring Security role checks, CSRF protection, session-fixation mitigation, secure headers, login rate limiting, validated uploads, safe external redirect schemes, audit logging, database constraints, and resilience fallback. These controls reduce common risks but do not replace deployment-level TLS, secret management, patching, backups, or monitoring.

The security checklist is organized using the supplied [OWASP Cheat Sheet Series](https://github.com/OWASP/CheatSheetSeries) and the OWASP API Security reference [6].

## Authentication and authorization

| Control | Implementation | Verification |
| --- | --- | --- |
| Password storage | BCrypt with configurable strength and constant-time dummy path in authentication logic | `UserServiceTest`, security review |
| Admin role boundary | `/admin/**` requires `ROLE_ADMIN` | `AdminControllerSecurityTest`, `SecurityConfig` |
| CSRF | Cookie-backed CSRF tokens for state-changing form requests | `AdminControllerIntegrationTest`, `SessionFixationTest` |
| Session fixation | Session migration/invalidation on custom admin login | `SecurityConfig`, `SessionFixationTest` |
| Login throttling | Bucket4j-based rate limiting filter | `RateLimitingFilterTest` |
| Session cookie | HttpOnly and SameSite settings, Secure enabled through production profile | `application.properties`, `application-prod.properties` |
| Audit logging | Hashed user identifiers and login/security-link/upload events | `SecurityAuditLoggerTest` |

## Threat model summary

| Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- |
| Admin account | Credential stuffing or brute force | BCrypt, login rate limit, audit events | MFA/SSO is not yet implemented |
| Event mutation | Unauthorized create/edit/delete | Spring Security role check and CSRF | Deployment misconfiguration could bypass TLS or expose sessions |
| Registration URL | Open redirect or unsafe scheme | HTTP/HTTPS scheme allow-list | External destination may still be malicious; administrators must review links |
| Uploaded media | Path traversal, spoofed file types, oversized input | MIME/extension/size validation, UUID paths, upload limits | Malware scanning and object-storage isolation are future work |
| Database | Credential theft or destructive writes | Environment secrets, least-privilege target, Flyway plus `flyway-mysql`, constraints, and MySQL 8.4 CI verification | Managed database network/TLS/backup configuration is environment-specific |
| Metrics/operations | Information disclosure | Health details hidden by default; metrics should be private | Ingress/network policy must be enforced in deployment |
| Student data | Excess retention or unintended exposure | Role boundaries, audit logging, documented retention responsibility | Institutional privacy policy and deletion workflow are future work |

## OWASP API Security review

The current application is primarily server-rendered, so the checklist is applied to both page routes and API-like endpoints. Object-level authorization is enforced by route boundaries today; future JSON APIs must add resource-owner checks wherever user-specific objects are introduced. Authentication failures must not leak whether a username exists. Unrestricted resource consumption is addressed through pagination, upload limits, and rate limiting, but future search and bulk-export endpoints need explicit quotas. Security misconfiguration is controlled through environment-driven secrets, hidden health details, non-root containers, and production profile settings. Unsafe consumption of external registration links is reduced by scheme validation, but destination trust remains a human/admin responsibility.

## Secret and credential policy

No production credential should appear in source, README examples, Docker image layers, CI logs, or committed `.env` files. `.env.example` contains placeholders only. CI uses a clearly labeled test fixture for the existing authentication tests; deployment workflows must use repository/environment secrets and never reuse the test fixture.

## Incident response

On suspected credential compromise, revoke or rotate the affected secret, invalidate active sessions where possible, preserve relevant audit logs, inspect recent administrative changes, verify database and upload integrity, and redeploy from a reviewed commit. Vulnerabilities should follow the reporting process in [`SECURITY.md`](../../SECURITY.md), not a public issue.

## References

[1]: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html "OWASP Authentication Cheat Sheet"
[2]: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html "OWASP Session Management Cheat Sheet"
[3]: https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html "OWASP File Upload Cheat Sheet"
[4]: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html "OWASP Secrets Management Cheat Sheet"
[5]: https://github.com/OWASP/CheatSheetSeries "OWASP Cheat Sheet Series repository"
[6]: https://owasp.org/API-Security/editions/2023/en/0x00-header/ "OWASP API Security Top 10"
