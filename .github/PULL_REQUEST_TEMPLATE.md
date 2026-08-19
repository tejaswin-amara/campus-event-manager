## Description
<!-- Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context. -->

Fixes # (issue)

## Type of change
<!-- Please delete options that are not relevant. -->
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## How Has This Been Tested?
<!-- Please describe the tests that you ran to verify your changes. -->
- [ ] Maven Test Suite (`./mvnw clean test`)
- [ ] Local Manual Verification 

## Checklist:
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes


## Production and architecture review
- [ ] The commit subject follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format.
- [ ] Database migrations are backward-compatible, reviewed, and tested against MySQL.
- [ ] Authorization, CSRF, validation, upload, redirect, and secret-handling implications were reviewed.
- [ ] No credentials, `.env` files, private keys, generated uploads, or local machine paths are committed.
- [ ] I ran `./mvnw -B verify` and the JaCoCo gate passes.
- [ ] I ran `scripts/smoke-test.sh` against the changed runtime where applicable.
- [ ] I updated the relevant requirement, architecture, API, security, operations, testing, or compliance documentation.
- [ ] If this changes a service boundary or distributed workflow, I documented ownership, contracts, retries, idempotency, and rollback/compensation behavior.
