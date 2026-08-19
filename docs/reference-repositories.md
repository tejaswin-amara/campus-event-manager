# Reference repository integration register

This register records how the supplied repositories are used in the CampusConnect upgrade. “Use” does not mean that code is copied into this repository. The safest and most maintainable interpretation is to reuse **patterns, checklists, contracts, and documented practices**, while retaining CampusConnect’s Java/Spring/MySQL architecture unless a direct dependency provides a clear production benefit.

The repository metadata was checked with GitHub CLI on 19 August 2026. The source list supplied by the user is preserved in the table below so every reference has a deliberate disposition.

| Repository | CampusConnect use | Integration decision |
| --- | --- | --- |
| [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | Resource-discovery model for this register and future technology selection | Used as a curation reference; no runtime code |
| [progit/progit2](https://github.com/progit/progit2) | Git workflow, branching, history, recovery, and release guidance | Used in contribution and release guidance; no runtime code |
| [github/choosealicense.com](https://github.com/github/choosealicense.com) | License-selection awareness and license documentation workflow | Used as a licensing reference; existing repository license retained |
| [conventional-commits/conventionalcommits.org](https://github.com/conventional-commits/conventionalcommits.org) | Standardized commit subjects for readable history and automated changelog readiness | Adopted in `CONTRIBUTING.md` and PR guidance |
| [cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter) | Template/scaffolding concept for future service extraction or companion repositories | Documented as a future template strategy; not added as a build dependency |
| [makeplane/plane](https://github.com/makeplane/plane) | Issue, sprint, roadmap, and triage workflow inspiration | Used for project-management guidance; not embedded in the runtime |
| [github/opensource.guide](https://github.com/github/opensource.guide) | Contribution, issue-template, review, and maintainer practice | Used to strengthen contribution and review documentation |
| [google/eng-practices](https://github.com/google/eng-practices) | Author/reviewer checklist and risk-focused code review | Used in PR template and release review gates; repository is archived, so it is treated as guidance rather than a dependency |
| [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) | Whiteboarding and stakeholder-sketch workflow before implementation | Used as a diagramming reference; final repository diagrams are reproducible Mermaid sources |
| [t3-oss/create-t3-app](https://github.com/t3-oss/create-t3-app) | Comparison point for typed full-stack scaffolding and API-first development | Used only for future frontend/API evolution; incompatible with current server-rendered Java stack |
| [t3-oss/create-t3-turbo](https://github.com/t3-oss/create-t3-turbo) | Monorepo/mobile sharing pattern for a possible future CampusConnect mobile client | Documented as a future option; not introduced into the current release |
| [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) | Reference for a FastAPI gateway or extracted search/aggregation service, Compose, and CI layout | Used in the CO3/CO5 evolution notes; no duplicate Python service added to the stable release |
| [alan2207/bulletproof-react](https://github.com/alan2207/bulletproof-react) | Frontend feature-folder, state, test, and linting patterns | Used as a future frontend modernization reference; current UI is Thymeleaf/vanilla JS |
| [gothinkster/realworld](https://github.com/gothinkster/realworld) | Contract-first auth, CRUD, pagination, and interoperability benchmark | Used to shape API documentation and acceptance criteria |
| [gothinkster/spring-boot-realworld-example-app](https://github.com/gothinkster/spring-boot-realworld-example-app) | Spring layering, DTO/contract discipline, and REST example reference | Used for API/documentation comparison; no code copied because CampusConnect is a different domain and uses Thymeleaf controllers |
| [spring-petclinic/spring-petclinic-reactjs](https://github.com/spring-petclinic/spring-petclinic-reactjs) | Spring domain layering and React/Spring split comparison | Used as a future frontend-separation reference; not integrated into the current UI |
| [shadcn-ui/ui](https://github.com/shadcn-ui/ui) | Accessible component ownership and design-system principles | Used as a future UI modernization reference; not added because the current frontend is not React |
| [dequelabs/axe-core](https://github.com/dequelabs/axe-core) | Accessibility test strategy and WCAG-oriented review checklist | Used in `docs/testing/README.md` and the showcase checklist; dependency addition is deferred until a browser E2E runner is selected |
| [prisma/prisma](https://github.com/prisma/prisma) | Schema-first ORM and migration comparison for future Node services | Used in polyglot persistence trade-off documentation; current source of truth remains JPA/Flyway |
| [better-auth/better-auth](https://github.com/better-auth/better-auth) | Modern auth capability comparison: passkeys, 2FA, SSO, and tenancy | Used in the authentication evolution backlog; not added to a Spring Boot application |
| [OWASP/CheatSheetSeries](https://github.com/OWASP/CheatSheetSeries) | Authentication, session, validation, file-upload, secrets, and API security checklists | Directly used to structure `docs/security/README.md` and release gates |
| [cypress-io/cypress-realworld-app](https://github.com/cypress-io/cypress-realworld-app) | End-to-end test organization, seeded data, auth flows, and CI evidence | Used to shape smoke-test and future browser-E2E strategy; current executable smoke path uses shell/curl because no Cypress frontend harness exists |
| [actions/starter-workflows](https://github.com/actions/starter-workflows) | GitHub Actions structure for Java verification, artifacts, and dependency review | Used in `.github/workflows/ci.yml` |
| [docker/awesome-compose](https://github.com/docker/awesome-compose) | Compose service health, dependency gating, local networking, and persistent volumes | Used in the rewritten `docker-compose.yml` |
| [ripienaar/free-for-dev](https://github.com/ripienaar/free-for-dev) | Deployment/hosting comparison framework and cost-awareness checklist | Used in `docs/operations/README.md`; no provider is selected automatically |
| [umami-software/umami](https://github.com/umami-software/umami) | Privacy-first analytics alternative to invasive third-party tracking | Used in the analytics/privacy decision record; current admin metrics remain first-party |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | Educational practice model for understanding infrastructure fundamentals | Used in the learning appendix; not production code |
| [calcom/cal.diy](https://github.com/calcom/cal.diy) | Scheduling-domain comparison for time zones, availability, recurrence, and booking workflows | Used to identify future event scheduling gaps; CampusConnect currently uses fixed event start/end values |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | Scaling, caching, reliability, bottleneck analysis, and architecture trade-off vocabulary | Used in architecture evolution and load-test interpretation |
| [kamranahmedse/developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) | Learning sequence for full-stack, DevOps, and production skills | Used in `docs/showcase.md` and follow-up backlog |
| [practical-tutorials/project-based-learning](https://github.com/practical-tutorials/project-based-learning) | Evidence-driven practice and end-to-end project learning structure | Used to shape the handout evidence trail and showcase flow |
| [anthropics/skills](https://github.com/anthropics/skills) | Modular skill/documentation approach for repeatable agent-assisted work | Used as a process reference only; no external skill code is vendored |
| [tejaswin-amara/Campus-Connect-Firebase-Addition](https://github.com/tejaswin-amara/Campus-Connect-Firebase-Addition) | React/Firebase feature prototype: recommendation scoring, QR pass/calendar UX, waitlist/attendance/notification concepts, and feature-level comparison | Adopted the recommendation concept as a server-side Spring/MySQL service; retained existing calendar/QR behavior; rejected direct Firebase/client-auth/mock-payment duplication; details in `docs/hybrid-integration-decision.md` |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Modular skill and checklist organization for repeatable engineering, product, compliance, and research work | Used as a process reference; no agent code or plugin runtime is vendored |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Production-oriented agent workflows for planning, implementation, testing, and review | Used to shape the cleanup plan and evidence gates; no JavaScript agent runtime is added |
| [microsoft/agent-governance-toolkit](https://github.com/microsoft/agent-governance-toolkit) | Zero-trust identity, policy enforcement, sandboxing, reliability, and OWASP-oriented agent governance concepts | Used in `docs/cleanup-audit.md` and automation guidance; not claimed as a deployed CampusConnect component |
| [vudovn/ag-kit](https://github.com/vudovn/ag-kit) | Lightweight agent workflow and kit organization | Used only as a process comparison; no unrelated TypeScript dependency is introduced |
| [ocornut/imgui](https://github.com/ocornut/imgui) | Minimal-dependency UI design and an explicit comparison point for native UI scope | Retained as a negative boundary; CampusConnect remains a server-rendered Java website with no C++ UI layer |
| [rust-lang/rust](https://github.com/rust-lang/rust) | Toolchain discipline, reproducible builds, and explicit language-boundary comparison | Used as a technology-selection boundary; no Rust service or toolchain is added |
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | Local-first design workflow and presentation-quality review ideas | Used for visual/documentation review; no desktop application or TypeScript design runtime is copied |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Responsive layout, accessibility, visual hierarchy, and UI review checklist concepts | Used to review the existing Thymeleaf/Bootstrap presentation; no generated frontend replacement is added |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Whole-repository over-engineering audit, ranked deletion candidates, and complexity discipline | Applied in `docs/cleanup-audit.md`; Ponytail findings remain advisory and do not override security or handout evidence |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | Public-source discovery and research workflow | Used only for optional documentation research; no scraper, credential, or network agent is added to the website |
| [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | Reference-aware code intelligence and framework reachability analysis | Used as a review model for symbol/reference checks; no source-indexing service is shipped with CampusConnect |
| [kunchenguid/no-mistakes](https://github.com/kunchenguid/no-mistakes) | Git safety habits: verify status, inspect diff, test before push, and avoid destructive history operations | Adopted in the cleanup execution and release checklist; no Go helper is vendored |

## Directly integrated patterns

The current release directly incorporates the highest-value patterns that fit the existing codebase: the Firebase-Addition recommendation concept rewritten as a tested server-side Spring service; conventional commit and review guidance; a source-linked documentation register; health-gated Compose startup; explicit environment configuration; Flyway-first schema control with the required `flyway-mysql` 12.4.0 module; JaCoCo verification; GitHub Actions artifact/dependency gates; OWASP-oriented security review; reproducible smoke/load scripts; and an architecture evolution record that distinguishes implemented behavior from future service extraction. The successful repair run [32272882649](https://github.com/tejaswin-amara/campus-connect/actions/runs/32272882649) confirms the MySQL 8.4 path.

## Deliberately not vendored

Large frameworks, UI libraries, alternate ORMs, complete demo applications, project-management platforms, analytics platforms, and educational repositories are not copied into CampusConnect. Vendoring them would increase attack surface, licensing complexity, build time, and operational cost without making the current event-management release more reliable. Their contribution is retained as documented design evidence and a prioritized future backlog.

## References

[1]: https://docs.github.com/en/rest/repos/ "GitHub repository metadata API"
[2]: https://owasp.org/API-Security/editions/2023/en/0x00-header/ "OWASP API Security Top 10"
[3]: https://www.conventionalcommits.org/en/v1.0.0/ "Conventional Commits specification"
