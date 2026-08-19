---
name: Bug report
about: Report a reproducible CampusConnect problem
title: ""
labels: bug
assignees: ""
---

## Summary

Describe the observed behavior and the user or operational impact. Do not include passwords, private keys, production credentials, or unredacted personal data.

## Reproduction

1. Start the documented Java 25 / MySQL 8.4 environment, or describe the deviation.
2. Navigate to the affected route or administrative workflow.
3. Provide the smallest sequence of actions that reproduces the issue.
4. State whether the behavior is deterministic.

## Expected behavior

Describe what should have happened, including the expected page, redirect, status, validation response, or database effect.

## Actual behavior

Describe what happened. Include a sanitized error message, status code, relevant log excerpt, or screenshot when useful.

## Environment

| Field | Value |
| --- | --- |
| Commit or branch | |
| Operating system | |
| Browser and version | |
| Java version | |
| MySQL version or CI/Compose | |
| Docker/Maven command | |
| Affected route or component | |

## Additional context

Explain whether the issue affects authentication, authorization, CSRF, uploads, external redirects, migrations, data integrity, health/metrics, or only presentation. For suspected vulnerabilities, do not use this template; follow [`SECURITY.md`](../../SECURITY.md).
