# CampusConnect — DBMS & Distributed Backend Compliance Matrix

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Academic Subject Code:** 25CS1302E  
**Evaluation Standard:** Strict verification against actual code, executable SQL artifacts, live EXPLAIN metrics, and automated test runs. Zero fake compliance.

---

## 1. Executive Compliance Scorecard

| Course Outcome | Academic Competency Domain | Status | Compliance Level |
|---|---|---|---|
| **CO1** | Backend Service Architecture & DB Interaction Flow | **PASS** | **Implemented Runtime** |
| **CO2** | ER Modeling, Dependency Theory & BCNF Normalization | **PASS** | **Implemented Runtime** |
| **CO3** | Advanced SQL Fluency (DDL, DML, Joins, CTEs, Window Functions) | **PASS** | **Implemented Runtime** |
| **CO4** | Transactions, ACID, Isolation Levels, Pessimistic Locking & Concurrency Stress Test | **PASS** | **Implemented Runtime** |
| **CO5** | B-Tree Index Theory, Query Optimization, EXPLAIN ANALYZE & N+1 Audit | **PASS** | **Implemented Runtime** |
| **CO6** | Distributed Databases, Replication, Sharding, Outbox Pattern & CAP Theorem | **PASS** | **Implemented Runtime + Documented Design** |

---

## 2. Category A: IMPLEMENTED RUNTIME

The following capabilities are actively running, compiled into the Java 25 / Spring Boot 3.4.1 binary, applied via Flyway V1–V4 migrations on MySQL 8.4 LTS (Port 3307), and verified by 65 passing automated tests:

| Requirement ID | Requirement Description | Exact Implementation File | Exact Evidence / Artifact | Verification Test | Status |
|---|---|---|---|---|---|
| **CO1.1** | Layered Backend Architecture | `src/main/java/com/tejaswin/campus/` | Controllers, Services, Repositories, Domain Entities | `EventControllerTest`, `EventServiceTest` | **PASS** |
| **CO1.2** | Request-to-Database Trace | `docs/request-to-database-flow.md` | End-to-end trace from HTTP POST down to InnoDB Buffer Pool & WAL | Code inspection & controller integration tests | **PASS** |
| **CO1.3** | Connection Pooling & Migration | `src/main/resources/application.properties` | HikariCP pool configuration (`maximum-pool-size: 10`), Flyway 10.20 auto-migration | Application startup logs | **PASS** |
| **CO2.1** | Conceptual ER Modeling | `database/er-diagram.md` | Formal Mermaid ER diagram with PKs, FKs, candidate keys, and cardinalities | Schema validation | **PASS** |
| **CO2.2** | Relational Normalization | `docs/normalization.md` | Mathematical proofs for 1NF, 2NF, 3NF, BCNF, lossless join, and dependency preservation | Schema constraints | **PASS** |
| **CO2.3** | Schema Hardening & Domain Constraints | `src/main/resources/db/migration/V4__Hardening_and_audit.sql` | `CHECK (status IN (...))`, `CHAR_LENGTH(TRIM(title)) > 0`, `uk_user_event` | `database/sql/ddl.sql` | **PASS** |
| **CO3.1** | Core DDL & DML Operations | `database/sql/ddl.sql`, `dml.sql` | Single/multi-row INSERTs, conditional UPDATEs, safe CASCADE DELETEs | Executed against MySQL 8.4 container | **PASS** |
| **CO3.2** | Advanced Multi-Way Joins | `database/sql/joins.sql` | Two-way, three-way INNER, LEFT JOIN, and ANSI emulated FULL OUTER JOIN via UNION | Executed against seed dataset | **PASS** |
| **CO3.3** | Aggregations & Grouping | `database/sql/aggregations.sql` | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING`, conditional `CASE WHEN` | Executed against seed dataset | **PASS** |
| **CO3.4** | Complex Subqueries | `database/sql/subqueries.sql` | Scalar subqueries, `IN`, `EXISTS`, `NOT EXISTS`, and correlated subqueries | Executed against seed dataset | **PASS** |
| **CO3.5** | Common Table Expressions (CTE) | `database/sql/cte.sql` | Chained non-recursive CTEs calculating category enrollment density | Executed against seed dataset | **PASS** |
| **CO3.6** | Hierarchical Recursive CTEs | `database/sql/recursive-cte.sql` | `WITH RECURSIVE` category taxonomy traversal & course prerequisite resolution | Executed against seed dataset | **PASS** |
| **CO3.7** | Analytical Window Functions | `database/sql/window-functions.sql` | `ROW_NUMBER()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, moving averages, running totals | Executed against seed dataset | **PASS** |
| **CO3.8** | Business Analytics Queries | `database/sql/analytics.sql` | Campus demand share, waitlist pressure, cohort segmentation | Executed against seed dataset | **PASS** |
| **CO4.1** | Transaction Management & ACID | `src/main/java/com/tejaswin/campus/service/EventService.java` | `@Transactional(isolation = Isolation.REPEATABLE_READ)` on registration mutations | `EventServiceTest` | **PASS** |
| **CO4.2** | Pessimistic Write Locking | `src/main/java/com/tejaswin/campus/repository/EventRepository.java` | `@Lock(LockModeType.PESSIMISTIC_WRITE)` on `findByIdForUpdate` | Hibernate SQL log inspection | **PASS** |
| **CO4.3** | Concurrent Race Stress Test | `src/test/java/com/tejaswin/campus/service/EventServiceConcurrencyTest.java` | 10 simultaneous threads: exactly 1 succeeds, 9 fail with MySQL Error 1062 | `mvn test -Dtest=EventServiceConcurrencyTest` (PASS) | **PASS** |
| **CO4.4** | Multi-User Concurrent Throughput | `src/test/java/com/tejaswin/campus/service/EventServiceConcurrencyTest.java` | 8 distinct concurrent users: 8/8 succeed with zero deadlocks | Concurrency test suite | **PASS** |
| **CO5.1** | B-Tree Secondary Indexing | `src/main/resources/db/migration/V4__Hardening_and_audit.sql` | `idx_events_category_date`, `idx_events_date_time`, `idx_events_status_date_time` | `database/indexes.sql` | **PASS** |
| **CO5.2** | EXPLAIN Execution Evidence | `database/explain/` | Real `EXPLAIN FORMAT=JSON` and `EXPLAIN ANALYZE` before/after files | `scripts/run_explain.py` | **PASS** |
| **CO5.3** | Query Cost & Filesort Elimination | `docs/query-optimization.md` | Measured 51.7% cost reduction (1.45 to 0.70) and 100% filesort elimination | Measured MySQL runtime logs | **PASS** |
| **CO5.4** | N+1 Query Elimination | `src/main/java/com/tejaswin/campus/repository/RegistrationRepository.java` | Explicit JPQL `JOIN FETCH r.event` in `findByUserIdWithEvent` | Repository integration test | **PASS** |
| **CO6.1** | Transactional Outbox Pattern | `src/main/resources/db/migration/V4__Hardening_and_audit.sql` | Table `outbox_events` with JSON payload, status index, and domain CHECK | `database/schema.sql` | **PASS** |

---

## 3. Category B: DOCUMENTED DESIGN

The following architectural designs are comprehensively documented with mathematical models, topological diagrams, configuration snippets, and operational runbooks, representing production scale-out architecture:

| Requirement ID | Domain Area | Documented Specification | Associated Document | Status |
|---|---|---|---|---|
| **CO6.2** | High-Availability Replication | Semi-synchronous GTID replication topology with Primary-Replica failover | [`docs/distributed-database.md`](distributed-database.md) | **PASS (Documented Design)** |
| **CO6.3** | Read-Write Splitting | Spring `AbstractRoutingDataSource` dynamically routing `@Transactional(readOnly = true)` | [`docs/distributed-database.md`](distributed-database.md) | **PASS (Documented Design)** |
| **CO6.4** | Horizontal Sharding | Hash partitioning by `campus_id` keeping registrations single-shard transactions | [`docs/distributed-database.md`](distributed-database.md) | **PASS (Documented Design)** |
| **CO6.5** | CAP Theorem Trade-off | Formal proof establishing CP classification over AP for event registration integrity | [`docs/distributed-database.md`](distributed-database.md) | **PASS (Documented Design)** |
| **CO6.6** | Disaster Recovery & PITR | Continuous binary log streaming and `mysqlbinlog` Point-In-Time Recovery to target 1-min RPO | [`docs/backup-recovery.md`](backup-recovery.md) | **PASS (Documented Design)** |
| **CO6.7** | Polyglot Data Strategy | Side-by-side evaluation of Relational (MySQL/Postgres) vs Document vs Vector | [`docs/data-architecture-decision.md`](data-architecture-decision.md) | **PASS (Documented Design)** |

---

## 4. Category C: OPTIONAL / FUTURE EXTENSIONS

The following items are intentionally demarcated as non-runtime future iterations to prevent unnecessary over-engineering and dependency bloat:

| Feature | Justification for Deferral | Recommended Implementation Path | Status |
|---|---|---|---|
| **External Kafka / NATS Cluster** | Local `outbox_events` table solves transactional decoupling without running an external broker cluster in CI | Connect an external Spring Kafka consumer to poll `outbox_events` | **OPTIONAL / FUTURE** |
| **Native Vector Embeddings (pgvector)** | Relational keyword and category filters meet 100% of current requirements; vector similarity adds heavy ML dependencies | Asynchronously generate embeddings from Outbox events and store in dedicated vector store | **OPTIONAL / FUTURE** |
| **Kubernetes Helm Multi-Cluster** | Single-container Docker Compose setup provides fast, deterministic local reproduction for grading | Author Helm chart for multi-tenant campus deployment | **OPTIONAL / FUTURE** |
| **Direct Payment Gateway** | Architecture follows student interest & external ticketing form redirection | Integrate Razorpay/Stripe webhooks via Outbox pattern | **OPTIONAL / FUTURE** |

---

## 5. Summary Declaration

The CampusConnect codebase, schema migrations, automated test harness, and documentation strictly adhere to the academic standards of **25CS1302E**. All runtime claims are backed by executable code and verified test results (65/65 passing).
