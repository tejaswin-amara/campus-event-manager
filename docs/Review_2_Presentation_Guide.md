# CampusConnect — Review 2 Presentation Guide & Defense Manual

> **Project Title:** CampusConnect: A Trustworthy Campus Event Catalogue with a Secure Administrative Control Plane  
> **Review Stage:** Review 2 (Technical Architecture, Frontend Implementation, Database Design, ER Model, and Live Evidence)  
> **Presentation File:** [`docs/CampusConnect_Review_2_Presentation.pptx`](CampusConnect_Review_2_Presentation.pptx)  
> **Slide Count:** 15 Slides (Strictly adheres to the 10–15 slides requirement and addresses all 16 topics)  
> **Core Stack:** Java 25 LTS, Spring Boot 4.1.0, MySQL 8.4 LTS, Flyway 12.4.0, Spring Security, Thymeleaf & React  

---

## 1. Executive Summary of Review 2 Deliverables

In **Review 1**, the foundational milestones were approved: Project Title, Problem Statement, Existing System, Proposed System, Objectives, Scope, Technology Identification, Basic Architecture, and Abstract.

In **Review 2**, the objective is to demonstrate **actual technical implementation and progress**:
- **System Architecture:** Detailed C4 Layered Modular Monolith model.
- **Frontend Implementation:** Live screenshots of Student Discovery Feed, Admin Control Center, Create Event Form Modal, and Admin Authentication.
- **Database Engineering:** 3NF normalization, Flyway V1–V3 migration pipeline, query-aware indexing.
- **ER Model & Schema:** Entity-Relationship diagram, comprehensive schema table definitions, and real seed database records.
- **Engineering Quality:** 63 automated unit/integration tests passing in CI, pessimistic concurrency locks, and Zero-Trust credential security.

---

## 2. Slide-by-Slide Presentation Guide & Speaker Script

### Slide 1: Title Slide
- **Heading:** CampusConnect — A Trustworthy Campus Event Catalogue with a Secure Administrative Control Plane
- **Category Pill:** `ACADEMIC CAPSTONE PROJECT • REVIEW 2`
- **Presenters:** Project Team Members (Full-Stack Lead, Database Lead, Frontend/Security Specialist)
- **Supervision:** Project Guide / Faculty Mentor, Department of Computer Science & Engineering
- **Technical Baseline:** Java 25 | Spring Boot 4 | MySQL 8.4 LTS | React & Thymeleaf
- **Speaker Script:**
  > *"Good morning respected panel members and project evaluators. Welcome to the Review 2 presentation of our capstone project, **CampusConnect**.*  
  > *In Review 1, we established our problem statement and preliminary architecture. Today, for Review 2, we are excited to present our working technical implementation: our modular monolith architecture, our completed frontend interfaces and forms, our 3NF normalized database schema and ER design, live sample database records, and our engineering solutions to concurrency and migration challenges.*  
  > *Let us examine the problem statement and existing system gaps."*

---

### Slide 2: Problem Statement & Existing System Analysis
- **Heading:** Problem Statement & Existing System Analysis
- **Category Pill:** `PROBLEM & MOTIVATION`
- **Left Column (Existing System Gaps):**
  - **Information Fragmentation:** Event notices scattered across unverified WhatsApp groups, informal flyers, and personal social accounts.
  - **Broken Redirects & Phishing:** Students encounter expired links, broken redirects, or unverified third-party forms.
  - **No Verified Capacity Enforcement:** Organizers cannot broadcast seat exhaustion in real-time, resulting in venue overcrowding.
  - **Duplicate & Ghost Signups:** Absence of transactional constraints allows repeated signups, distorting headcount.
- **Right Column (CampusConnect Solution):**
  - **Single Source of Truth:** Centralized, searchable catalogue of verified campus events with instant category filtering.
  - **Validated Registration Links:** Server-side protocol whitelist ensures redirection only to authenticated campus portals.
  - **Transactional Interest Tracking:** Pessimistic write locking enforces unique registration states with zero duplicate record overhead.
  - **Secure Admin Control Plane:** Role-Based Access Control (RBAC) allows verified organizers to manage lifecycles and export telemetry.
- **Speaker Script:**
  > *"Today, universities suffer from extreme event fragmentation. When a technical club or cultural society hosts an event, notices are circulated informally across group chats. Links expire, venues change without notice, and students have no central portal to verify whether an event is authentic or fully booked.*  
  > *CampusConnect solves this by providing a unified, authoritative campus event catalogue. Crucially, we do not just build a UI—we enforce server-side validation on external links and apply transactional concurrency controls to eliminate duplicate signups."*

---

### Slide 3: Project Objectives & Scope Boundaries
- **Heading:** Project Objectives & Scope Boundaries
- **Category Pill:** `PROJECT SPECIFICATION`
- **Left Column (Core Technical Objectives):**
  - **Architect a Modular Monolith:** Build a unified Spring Boot 4 backend with clean domain boundaries ready for future microservice extraction.
  - **High-Performance Event Discovery:** Implement indexed search, category filtering, and explainable upcoming event recommendations.
  - **Zero-Trust Security Baseline:** Enforce BCrypt credential hashing, CSRF tokens, and Bucket4j IP-based login rate limiting.
  - **Automated Schema Governance:** Establish relational integrity via version-controlled Flyway V1–V3 migrations on MySQL 8.4 LTS.
- **Right Column (Defined Project Scope):**
  - **In-Scope (Current Working Implementation):** Public event catalogue, search/filtering, interest registration, admin CRUD operations, image uploads (BLOB), telemetry dashboard, CSV export, Actuator health, and Prometheus metrics.
  - **Authoritative Registration Boundary:** Internal interest is transactionally recorded, while the configured external registration link remains authoritative for seat ticket issuance.
  - **Honest Architectural Boundary:** Distributed message brokers (Kafka) and document stores (MongoDB) are documented as bounded evolution paths, not falsely claimed as deployed runtime components.
- **Speaker Script:**
  > *"On Slide 3, we define our measurable technical objectives and explicit scope boundaries. Our goal is to engineer an enterprise-grade modular monolith adhering to Course Outcomes CO1 through CO6.*  
  > *We also state our scope boundary clearly: in this sprint, CampusConnect tracks student interest and directs them to authoritative campus registration links. We intentionally avoid claiming to run an internal payment gateway or ticket-scanning system today; those are mapped into our future evolution roadmap."*

---

### Slide 4: Proposed System & Key Innovations
- **Heading:** Proposed System & Key Innovations
- **Category Pill:** `SYSTEM DESIGN`
- **4 Feature Grid Cards:**
  1. **Modular Monolith Architecture:** Single deployable Spring Boot container packaging controllers, business logic, security filters, and JPA entities with decoupled packages.
  2. **Zero-Trust Security Defense:** Multi-layer authentication with BCrypt 60-character salted password hashes, Bucket4j IP rate limiting, session-fixation protection, and CSRF token defense.
  3. **Relational Data Integrity:** 3NF normalized MySQL 8.4 database managed exclusively via Flyway migrations; pessimistic row-level locking prevents duplicate signups under high concurrency.
  4. **Intelligent Discovery & Telemetry:** Server-side heuristic scoring recommending top upcoming events based on category velocity, with Prometheus metrics and Actuator health probes.
- **Speaker Script:**
  > *"Slide 4 summarizes the four pillars of our proposed system. First, a modular monolith that provides simplicity and speed of deployment without microservice network latency. Second, zero-trust security featuring BCrypt, CSRF guards, and Bucket4j rate limiting. Third, relational integrity using Flyway migrations and row-level pessimistic locks. Fourth, intelligent event recommendations combined with Prometheus telemetry."*

---

### Slide 5: System Architecture (C4 Model)
- **Heading:** System Architecture (C4 Layered Model)
- **Category Pill:** `ARCHITECTURE`
- **Visual:** Embedded high-resolution C4 Architecture Diagram ([`presentation_assets/system_architecture.png`](../presentation_assets/system_architecture.png)).
- **Key Points:**
  - **Presentation Tier:** Dual web surfaces: server-rendered Thymeleaf templates and responsive React dashboard.
  - **Security Boundary:** Spring Security intercepts every HTTP request, enforcing CSRF tokens, BCrypt hashes, and RBAC roles (`STUDENT`, `ADMIN`).
  - **Service Layer:** Transactional domain services (`EventService`, `UserService`, `RecommendationService`) maintain business rules.
  - **Persistence Tier:** Spring Data JPA repositories interface with MySQL 8.4 LTS; Flyway migrations govern schema versions.
  - **Operational Plane:** Actuator exposes `/actuator/health` and Micrometer exposes Prometheus scrape endpoints.
- **Speaker Script:**
  > *"Here on Slide 5 is our complete System Architecture following the C4 container model. On the left, student and admin browser requests enter our containerized Spring Boot runtime on Java 25. Every request traverses our Security Interceptor chain, checking session tokens and Bucket4j rate limits.*  
  > *Requests are handled by the appropriate Controller and transactional Service layer, which uses Spring Data JPA to talk to MySQL 8.4 LTS. Crucially, Flyway migrations run before Hibernate validation, ensuring the database schema is strictly version-controlled."*

---

### Slide 6: System Modules & Functional Breakdown
- **Heading:** System Modules & Functional Breakdown
- **Category Pill:** `MODULES`
- **4 Functional Modules:**
  1. **Module 1: Identity & Access Control:** Role-Based Access Control (`STUDENT`, `ADMIN`), BCrypt credential protection, Bucket4j token-bucket rate limiter, and secure session management.
  2. **Module 2: Event Discovery & Catalogue:** Paginated public listings, real-time multi-criteria search (title, venue, category), category filter pills, and event detail modal.
  3. **Module 3: Registration & Interest Engine:** Transactional interest registration, pessimistic write lock preventing race conditions, external link whitelist verification, and compound unique constraints.
  4. **Module 4: Admin Control Plane & Telemetry:** Full event CRUD lifecycle, image upload management (MEDIUMBLOB), real-time KPI metrics, and one-click CSV export.
- **Speaker Script:**
  > *"Slide 6 presents our four decoupled functional modules: Identity & Access Control manages authentication and brute-force protection. Event Discovery provides high-speed browsing and filtering. The Registration & Interest Engine guarantees race-condition-free signup tracking. Finally, the Admin Control Plane gives administrators complete CRUD lifecycle control and reporting."*

---

### Slide 7: Frontend Design: Discovery Feed & Authentication
- **Heading:** Frontend Design: Discovery Feed & Authentication
- **Category Pill:** `FRONTEND DESIGN`
- **Visuals:** Side-by-side high-resolution screenshots:
  - **Student Discovery Home Page** ([`presentation_assets/01_student_catalogue.png`](../presentation_assets/01_student_catalogue.png)): Hero banner, category pills (Technical, Cultural, Sports), event card grid, and upcoming recommendation badge.
  - **Admin Authentication Portal** ([`presentation_assets/04_admin_login.png`](../presentation_assets/04_admin_login.png)): Ambient glow backdrop, glassmorphic card, and Bucket4j security badge.
- **Speaker Script:**
  > *"Moving to our technical demonstration, Slide 7 illustrates our frontend user interface. On the left is the Student Discovery Catalogue. Notice our high-contrast dark theme with color-coded category pills and card grids designed for fast scanning.*  
  > *On the right is our Admin Login portal, featuring a glassmorphic card interface with visual feedback indicating BCrypt encryption and active rate limiting."*

---

### Slide 8: Frontend Implementation: Control Center & Forms
- **Heading:** Frontend Implementation: Control Center & Forms
- **Category Pill:** `LIVE DEMONSTRATION`
- **Visuals:** Side-by-side high-resolution screenshots:
  - **Admin Control Plane & Analytics** ([`presentation_assets/02_admin_dashboard.png`](../presentation_assets/02_admin_dashboard.png)): Real-time KPI cards (Total Events, Active Signups, Capacity), searchable registry table, and CSV export.
  - **Event Lifecycle Creation & Edit Form** ([`presentation_assets/03_create_event_form.png`](../presentation_assets/03_create_event_form.png)): Validated inputs for title, date/time, venue, capacity, category, registration link, and image upload.
- **Speaker Script:**
  > *"Slide 8 demonstrates our live administrative interface. On the left is the Admin Control Plane, displaying live KPI metrics for campus engagement, event capacity, and registrations. Administrators can search, delete, or export rosters to CSV with a single click.*  
  > *On the right is our Create Event form modal. It enforces Bean Validation: event end times must be after start times, venue and category cannot be blank, and capacities must be positive integers."*

---

### Slide 9: Database Design & Relational Foundation
- **Heading:** Database Design & Relational Foundation
- **Category Pill:** `DATA ENGINEERING`
- **3 Architectural Columns:**
  1. **Third Normal Form (3NF):** Elimination of transitive dependencies; user credentials decoupled from event metadata; associative table `registrations` resolves M:N mapping.
  2. **Flyway Migration Authority:** Version-controlled migrations: `V1__Initial_Schema.sql` (baseline tables), `V2__Add_Image_Blob.sql` (BLOB storage), `V3__Indexes_Integrity.sql` (query indexes & checks).
  3. **Performance & Concurrency Locking:** Composite indexes on `(date_time)` and `(category, date_time)`; JPA `PESSIMISTIC_WRITE` locks during interest registration; Hibernate `DDL_AUTO=validate`.
- **Speaker Script:**
  > *"On Slide 9, we highlight our database engineering principles. Our relational schema is strictly in Third Normal Form (3NF). We avoid manual schema edits or letting Hibernate alter tables dynamically. Instead, all changes are version-controlled using Flyway migrations running against MySQL 8.4 LTS, with Hibernate strictly in validate mode."*

---

### Slide 10: Entity-Relationship (ER) Diagram
- **Heading:** Entity-Relationship (ER) Diagram
- **Category Pill:** `DATABASE MODEL`
- **Visual:** Embedded high-resolution ER Diagram ([`presentation_assets/er_diagram.png`](../presentation_assets/er_diagram.png)).
- **Key Relational Semantics:**
  - **USERS (1) to REGISTRATIONS (N):** One student account creates multiple registration-interest entries.
  - **EVENTS (1) to REGISTRATIONS (N):** Each campus event receives registrations from multiple students.
  - **Compound Unique Constraint:** `UNIQUE (user_id, event_id)` prevents duplicate signups at the database layer.
  - **Cascading Deletion:** Foreign keys with `ON DELETE CASCADE` ensure referential integrity if an event is removed.
- **Speaker Script:**
  > *"Slide 10 presents our Entity-Relationship (ER) model. We have three core entities: USERS, EVENTS, and the associative entity REGISTRATIONS. Examining the cardinalities: one user can have many registrations (1 to N), and one event can have many registrations (1 to N).*  
  > *Notice the compound unique constraint `UNIQUE (user_id, event_id)`. Even if concurrent network requests bypass the application layer, the database engine guarantees that duplicate registrations are physically impossible."*

---

### Slide 11: Database Tables & Schema Definition
- **Heading:** Database Tables & Schema Definition
- **Category Pill:** `SCHEMA SPECIFICATION`
- **3 Formatted PPT Native Tables:**
  - **`users` Table:** `id` (BIGINT PK), `username` (VARCHAR(50) UK), `password` (VARCHAR(255)), `role` (VARCHAR(20)), `email` (VARCHAR(254) UK).
  - **`events` Table:** `id` (BIGINT PK), `title` (VARCHAR(255)), `date_time` (DATETIME INDEX), `end_date_time` (DATETIME), `venue` (VARCHAR(255)), `category` (VARCHAR(50) INDEX), `max_capacity` (INT CHECK > 0), `image_data` (MEDIUMBLOB).
  - **`registrations` Table:** `id` (BIGINT PK), `user_id` (BIGINT FK), `event_id` (BIGINT FK), `registration_date` (DATETIME), `status` (VARCHAR(20)), `UNIQUE (user_id, event_id)`.
- **Speaker Script:**
  > *"Slide 11 shows the exact DDL specifications. Notice our field constraints: passwords are sized at VARCHAR(255) to accommodate salted BCrypt hashes. In the events table, we enforce check constraints on capacity and date ordering. In the registrations table, we restrict status vocabulary to INTERESTED, CONFIRMED, CANCELLED, and WAITLISTED."*

---

### Slide 12: Sample Database Records & Live State
- **Heading:** Sample Database Records & Live State
- **Category Pill:** `DATABASE VERIFICATION`
- **Live Seed Data Tables:**
  - **`users` Records:** Admin (`admin`, role `ADMIN`, BCrypt hash `$2a$10$...`) and Student (`guest`, role `STUDENT`, BCrypt hash).
  - **`events` Records:** "AI & Autonomous Agents Hackathon" (Technical, 120 capacity) and "Spring Symphony & Cultural Gala" (Cultural, 500 capacity).
  - **`registrations` Records:** Associative rows linking user 2 to events 1 and 2 with status `INTERESTED`.
- **Speaker Script:**
  > *"Slide 12 provides concrete evidence of our database state. Passwords are never in plaintext—they are verified BCrypt hashes. Events have structured metadata, dates, and capacities. The registrations table shows active interest entries linked by foreign keys."*

---

### Slide 13: Current Progress & Verification Status
- **Heading:** Current Progress & Verification Status
- **Category Pill:** `PROGRESS ASSESSMENT`
- **Left Column (Implementation Checklist):**
  - ✅ Modular Monolith Architecture (Spring Boot 4 + Java 25)
  - ✅ Database Schema & Migrations (Flyway V1–V3 on MySQL 8.4)
  - ✅ Security & Rate Limiting (BCrypt, CSRF, Bucket4j)
  - ✅ Frontend Surfaces (Catalogue, Admin Console, Modals)
  - ✅ Automated Test Suite (63 unit & integration tests)
  - ✅ Automated CI Pipeline (GitHub Actions passing)
- **Right Column (Quality Metrics):**
  - **63 Passing Automated Tests:** Full coverage over services, controllers, locking, and security.
  - **JaCoCo Coverage Gates:** Strict line and branch coverage gates in CI.
  - **Operational Endpoints:** `/actuator/health` reporting UP; OpenAPI specs active at `/v3/api-docs`.
- **Speaker Script:**
  > *"Slide 13 details our progress for Review 2: 85% of our core platform is operational and tested. All 63 automated tests are passing in our build pipeline, validated against a real MySQL 8.4 instance in GitHub Actions CI. Our health check and OpenAPI documentation endpoints are fully operational."*

---

### Slide 14: Challenges Faced & Technical Solutions
- **Heading:** Challenges Faced & Technical Solutions
- **Category Pill:** `ENGINEERING RESOLUTIONS`
- **4 Real Technical Challenges & Remediations:**
  1. **Concurrent Interest Race Conditions:** Rapid clicks could bypass application-layer checks $\to$ Resolved using JPA `PESSIMISTIC_WRITE` locking on the event row + compound DB unique constraint.
  2. **Flyway 12 & MySQL 8.4 Dialect Mismatch:** Default Flyway starter failed to recognize MySQL 8.4 LTS $\to$ Resolved by explicitly integrating `org.flywaydb:flyway-mysql:12.4.0`.
  3. **Admin Secret Ingestion & Zero-Trust:** Hardcoded admin passwords create security vulnerabilities $\to$ Resolved by environment injection (`ADMIN_PASSWORD`) with undisclosed 32-byte CSPRNG token fallback.
  4. **Image Storage & Deployment Portability:** Ephemeral container file storage causes image loss upon restart $\to$ Resolved with database-backed `MEDIUMBLOB` persistence with MIME validation.
- **Speaker Script:**
  > *"Engineering always encounters obstacles. On Slide 14, we present four real challenges we overcame: race conditions during registration, solved via pessimistic locking; Flyway 12 compatibility with MySQL 8.4, solved by adding the dedicated MySQL dialect module; zero-trust admin secret injection; and durable image persistence via database BLOBs."*

---

### Slide 15: Future Work & Project Conclusion
- **Heading:** Future Work & Project Conclusion
- **Category Pill:** `CONCLUSION & ROADMAP`
- **Left Column (Sprint 3 Roadmap):**
  - **Internal Seat Ticketing:** Implement an internal seat reservation state machine with real-time capacity decrementing.
  - **Asynchronous Notifications:** Outbox pattern with RabbitMQ/Kafka for email and push notifications.
  - **Semantic Vector Search:** pgvector adapter for semantic event discovery based on student interest embeddings.
  - **Progressive Web App (PWA):** Mobile offline caching and installable client.
- **Right Column (Review 2 Concluding Summary):**
  - **Production-Ready Foundation:** Working modular monolith with high-performance discovery and secure control plane.
  - **Verified Relational Engineering:** 3NF schema, Flyway migrations, and concurrency locks provide rock-solid reliability.
  - **Proven Quality Assurance:** 63 passing tests and active CI pipeline guarantee zero-regression stability.
- **Speaker Script:**
  > *"To conclude Review 2, CampusConnect has evolved into a robust, secure, and tested modular monolith. Our frontend interfaces, database schema, and security configurations are fully verified. In Sprint 3, we look forward to implementing internal seat ticketing and asynchronous notifications. Thank you for your time. We are now ready for your questions."*

---

## 3. Team Member Presentation Split

To fulfill the rule: *"Every team member must participate in the presentation; each member should explain a specific part of the project."*

| Presenter | Assigned Slides | Topics Covered | Key Talking Focus |
|---|---|---|---|
| **Member 1 (Team Lead)** | **Slides 1 – 4** | Title, Problem Statement, Objectives, Proposed System | Project vision, existing campus gaps, scope boundaries, core architecture pillars |
| **Member 2 (Architecture & Frontend Lead)** | **Slides 5 – 8** | System Architecture, Modules, Frontend Design & Live Screenshots | C4 container model, web layers, live UI demonstration (Home, Login, Dashboard, Forms) |
| **Member 3 (Database & Data Engineering Lead)** | **Slides 9 – 12** | Database Design, ER Diagram, Schema DDL, Sample Records | 3NF normalization, Flyway V1–V3 migrations, cardinalities, compound unique keys, seed data |
| **Member 4 (QA, Security & DevOps Lead)** | **Slides 13 – 15** | Current Progress, Challenges & Solutions, Future Work & Conclusion | 63 automated tests, CI/CD pipeline, concurrency locking, MySQL 8.4 Flyway fix, roadmap |

*(Note: If the team has 3 members, Member 1 can cover Slides 1–4, Member 2 can cover Slides 5–8 and 14–15, and Member 3 can cover Slides 9–13).*

---

## 4. Panel Q&A Defense Guide

### Question 1: "Why did you build a Modular Monolith instead of Microservices from Day 1?"
**Answer:**
> *"Starting as a distributed microservice system introduces distributed network latency, distributed transaction coordination (2PC or Sagas), and operational infrastructure complexity that is premature for our current transaction volume. Instead, we architected a **Modular Monolith**. We strictly segregated the application into explicit domain packages (Identity, Event Catalogue, Registrations, Recommendations) with clear repository boundaries. When throughput requires it, these modules can be extracted into standalone microservices with minimal refactoring."*

### Question 2: "How do you prevent race conditions when multiple students click register simultaneously?"
**Answer:**
> *"We implement a dual-layer defense. At the application layer, `EventService.registerStudent` executes within a transaction and obtains a JPA `PESSIMISTIC_WRITE` lock on the event row in MySQL (`SELECT ... FOR UPDATE`). This serializes concurrent registration requests for that specific event. At the persistence layer, the `registrations` table enforces a compound unique constraint `UNIQUE (user_id, event_id)`. If any thread attempts to insert a duplicate record, MySQL raises a duplicate key violation, preventing dirty writes."*

### Question 3: "Why did you use Flyway instead of letting Hibernate create the schema (`ddl-auto=update`)?"
**Answer:**
> *"Using `ddl-auto=update` in production is an anti-pattern. Hibernate cannot reliably handle column drops, index modifications, complex check constraints, or database-specific optimizations. We use **Flyway versioned migrations (`V1`, `V2`, `V3`)** as the sole schema authority. Hibernate runs in `validate` mode (`DDL_AUTO=validate`), failing fast upon startup if the entity mappings do not exactly match the database schema. This guarantees identical database states across local developer machines, GitHub Actions CI, and production."*

### Question 4: "How do you secure passwords and prevent brute-force attacks?"
**Answer:**
> *"Passwords are never stored in plaintext. They are encoded using **BCrypt** with an adaptive salt factor producing 60-character hashes. Furthermore, our login endpoint is protected by a **Bucket4j token-bucket rate limiter** in `RateLimitingFilter`, which limits login attempts by client IP address, effectively stopping automated credential stuffing. We also enforce CSRF token validation and HTTP-only session cookies with session-fixation protection."*

### Question 5: "What is your testing strategy and current test coverage?"
**Answer:**
> *"We maintain a comprehensive automated test suite of **63 automated tests** using JUnit 5, Mockito, and Spring Boot Test. Our suite covers unit tests for domain logic and recommendations, slice tests for controllers, and full integration tests validating pessimistic locking and database constraints against a containerized MySQL instance. Our GitHub Actions CI pipeline enforces JaCoCo line and branch coverage gates on every commit."*
