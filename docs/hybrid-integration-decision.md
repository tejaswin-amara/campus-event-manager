# Hybrid integration decision record

## Decision summary

The production Campus Connect repository remains the integration base. The Firebase-Addition repository contributes **portable product concepts and presentation patterns**, not a second runtime stack or a second authoritative database. This choice keeps the existing Spring Boot/MySQL/Flyway/security/CI foundation intact while adding a low-risk recommendation experience inspired by the Firebase repository.

The Firebase repository is a strong React/Vite/Firebase feature prototype, but its principal domain screen places Firestore reads, registration transactions, waitlist state, payment simulation, certificates, social graph loading, geofence decisions, feedback, and modal orchestration in a single client page. Those features are valuable as a product reference but must not be copied directly into the compliant backend because doing so would move authorization and transactional integrity into a client-heavy, duplicated architecture.

## Feature comparison

| Capability | Firebase-Addition | Current Campus Connect | Final decision | Handout impact |
| --- | --- | --- | --- | --- |
| Event discovery and filtering | React dashboard with search/category filtering and event cards | Thymeleaf dashboard with server-side pagination, search, category/status filters, calendar, and registration QR | Retain Spring implementation; borrow card/presentation ideas only | Preserves CO3 API/backend evidence and CO6 simplicity |
| Event CRUD and media | Firestore writes plus Firebase Storage upload | Spring MVC, Bean Validation, MySQL/Flyway, validated database-backed image storage | Retain Spring/MySQL authority | Strengthens CO1 constraints, transactions, and deployment evidence |
| Recommendations | Pure matchmaker based on category affinity, peers, and capacity fill rate | `RecommendationService` and `RecommendedEvent` provide server-side derived recommendations from existing event and interest data | **Implemented as a server-side Java service** with deterministic unit tests | Adds a testable derived-data feature without CO1 compromise |
| QR pass/ticket | QR payload contains user/event/registration IDs; attendance scanner marks `ATTENDED` | QR currently represents external registration link; registration record is `INTERESTED` | Document as future capacity/attendance slice; do not misrepresent external interest as a ticket | Prevents false CO1/CO5 claims and keeps current semantics honest |
| Waitlist | Firestore transaction and Cloud Function auto-promotion | No authoritative internal seat allocation; max capacity is metadata | Document future design; do not implement partial waitlist | Preserves transaction and distributed-systems credibility |
| Paid events | Mock Stripe checkout/session and mock payment webhook | No payment flow | Reject mock payment code; document real payment boundary as future work | Avoids insecure/demonstration-only payment claims |
| Certificates | Client-side PDF generation and bulk export | CSV event export exists | Retain as future attendance evidence; no client-issued certificate now | Avoids unverifiable attendance and client-trust risks |
| Social graph/squad alerts | Firestore connections, peer registration queries, FCM | No social graph | Keep as future activity/notification bounded context | Provides CO2/CO5 evolution evidence without duplicate store |
| Feedback prompts | Firestore feedback and FCM prompt after `ATTENDED` | No attendance state | Document future event activity context | Preserves bounded-context roadmap |
| Firebase Auth | Client provider with admin-email fallback and Firestore role document | Spring Security, BCrypt, CSRF, session fixation protection, admin RBAC | Reject direct client role/bootstrap behavior; retain Spring auth | Stronger CO3 security evidence |
| Firebase hosting/emulators | Hosting, Firestore, Storage, Functions emulators | Docker/Compose, MySQL, GitHub Actions | Retain Firebase repo as optional prototype/reference; production baseline remains Docker/Spring | Keeps CO6 deployment reproducible |
| Frontend framework | React 19, Vite 8, Tailwind 4, TypeScript, Framer Motion | Thymeleaf, Bootstrap, vanilla JS | Do not add a second frontend in this slice | Avoids competing application shells and build complexity |

## Selected implementation

The first hybrid feature is an implemented **server-side “Recommended for you” section** on the student dashboard. It follows the Firebase matchmaker’s useful logic: exclude already-interesting events, prioritize categories represented in prior student activity, add a popularity/capacity signal, and return at most three upcoming events with human-readable reasons. The algorithm runs in Java inside the existing service/controller boundary, uses MySQL-backed queries, and is covered by `RecommendationServiceTest` and `RecommendedEventTest`.

The UI will remain Thymeleaf/Bootstrap/vanilla JavaScript. The existing calendar action and registration-link QR flow are retained because they already cover part of the Firebase pass experience without claiming that an external registration link is an attendance ticket. Firebase’s ticket scanner, waitlist, payments, certificates, and FCM workflows remain documented as future bounded contexts until the relational model and product semantics support them.

## Data ownership

MySQL remains authoritative for events, users, and interest records. Recommendations are derived per request and are not persisted as a second event store. No Firebase SDK, Firestore collection, Firebase private key, or service-account credential is added to the production website in this slice. If Firebase is adopted later for notifications or identity, it must be behind a tested adapter with explicit ownership, retention, security rules, emulator/mocked tests, and rollback.

## Compliance mapping

| Outcome | Hybrid evidence |
| --- | --- |
| CO1 | Existing V1–V3 Flyway schema, normalized entities, unique user-event constraint, indexed registration queries, transaction-safe interest write, and recommendation reads over relational data |
| CO2 | Decision record distinguishes authoritative SQL data from future Firestore/activity/vector derived data; recommendations use lexical/relational signals and preserve a future semantic-search boundary |
| CO3 | Spring MVC/OpenAPI/security boundary remains authoritative; the new recommendation model is server-generated rather than trusting client-supplied scores or roles |
| CO4 | Spring service/module retained; React/Firebase and Functions are evaluated as alternative frontend/serverless references rather than duplicated runtime services |
| CO5 | Firebase Functions’ waitlist/notification ideas are retained as future asynchronous bounded contexts with outbox/idempotency requirements, not copied as unowned dual writes |
| CO6 | Docker, MySQL 8.4, CI, tests, smoke/load scripts, C4 diagrams, showcase, and compliance docs remain the release evidence; the successful Flyway repair run [32272882649](https://github.com/tejaswin-amara/campus-connect/actions/runs/32272882649) confirms the production baseline |

## Provenance and licensing

The Firebase-Addition repository is MIT-licensed and is used as a feature and architecture reference. The final implementation will not copy large React pages, Firebase rules, mock payment handlers, or client-side authorization logic into the Spring repository. Any future direct asset reuse must preserve attribution and be reviewed in the repository’s provenance register.

## References

[1]: https://github.com/tejaswin-amara/Campus-Connect-Firebase-Addition "Firebase-Addition source repository"
[2]: https://github.com/tejaswin-amara/campus-connect "CampusConnect production baseline"
[3]: https://firebase.google.com/docs/firestore/security/rules-conditions "Firestore security rules"
[4]: https://firebase.google.com/docs/functions "Cloud Functions documentation"
[5]: https://github.com/OWASP/CheatSheetSeries "OWASP Cheat Sheet Series"
