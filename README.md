# CampusConnect — Campus Event Aggregator & Manager

> **Academic Subject:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
> **Repository Branch:** `feat/complete-dbms-pbl-hardening`  
> **Runtime Environment:** Java 25 LTS, Spring Boot 4.1.0, MySQL 8.4 LTS (InnoDB Engine), Flyway 10.20, Docker

[![Build & Test Status](https://img.shields.io/badge/tests-65%2F65%20passing-brightgreen)](src/test/java/com/tejaswin/campus/service/EventServiceConcurrencyTest.java)
[![Database](https://img.shields.io/badge/database-MySQL%208.4%20LTS-blue?logo=mysql&logoColor=white)](database/schema.sql)
[![Migrations](https://img.shields.io/badge/flyway-V1--V4-red?logo=flyway&logoColor=white)](src/main/resources/db/migration/)
[![Java](https://img.shields.io/badge/Java-25%20LTS-orange?logo=openjdk&logoColor=white)](https://openjdk.org/projects/jdk/25/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-4.1.0-green?logo=springboot&logoColor=white)](https://spring.io/projects/spring-boot)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 1. System Overview

**CampusConnect** is an enterprise-grade campus event aggregator and student registration management platform engineered for strict ACID transactional consistency, high-throughput concurrency safety, and sub-millisecond query performance.

### Key Capabilities
* **ACID Registration & Race Condition Protection:** Pessimistic row-level locking (`SELECT ... FOR UPDATE`) paired with database-level composite unique constraints (`uk_user_event`), verified under 10-thread simultaneous contention.
* **Boyce-Codd Normal Form (BCNF) Schema:** Fully normalized 4-table relational architecture with mathematical lossless join and dependency preservation proofs.
* **Exhaustive SQL Portfolio:** 12 executable SQL modules covering multi-way joins, aggregations, correlated subqueries, chained CTEs, recursive taxonomy trees, and analytical window functions.
* **Empirical Query Optimization:** Secondary composite B-Tree indexes yielding measured **51.7% query cost reductions** and **100% filesort elimination**, backed by real `EXPLAIN ANALYZE` evidence.
* **Distributed Scalability & Outbox Pattern:** Decoupled asynchronous event publishing via table `outbox_events` (Flyway V4), alongside documented high-availability replication, read-write routing, and tenant sharding designs.

---

## 2. Architecture & Data Flow

```mermaid
flowchart TD
    Client[Web Browser / Postman] -->|HTTP / Form POST| SpringSec[Spring Security 6.4\nCSRF + BCrypt + Session]
    SpringSec --> Ctrl[StudentController / AdminController]
    Ctrl --> Svc[EventService\n@Transactional REPEATABLE_READ]
    
    subgraph Data Access Layer
        Svc -->|Pessimistic Lock| RepoE[EventRepository\nfindByIdForUpdate]
        Svc -->|Unique Constraint uk_user_event| RepoR[RegistrationRepository\nsave & findByUserIdWithEvent]
        Svc -->|Decoupled Async Events| Outbox[OutboxRepository\nsave OutboxEvent]
    end

    RepoE & RepoR & Outbox --> Hikari[HikariCP Connection Pool\nMax: 10]
    Hikari --> MySQL[(MySQL 8.4 LTS InnoDB\nPort 3307 / 3306)]
    
    subgraph Storage Engine
        MySQL --> Clustered[Clustered B+ Tree Primary Keys]
        MySQL --> BTreeIdx[Composite B-Tree Indexes\nidx_events_category_date]
        MySQL --> WAL[Write-Ahead Logging\nib_logfile0 Redo/Undo]
    end
```

---

## 3. Quickstart & Local Execution

### 3.1 Start MySQL 8.4 Database Container
The project includes a ready-to-run MySQL 8.4 container pre-configured on host port **3307** (to avoid conflicts with local port 3306):

```bash
docker run -d \
  --name campus_events_db \
  -e MYSQL_ROOT_PASSWORD=campus_root_password \
  -e MYSQL_DATABASE=campus_events \
  -e MYSQL_USER=campus_app \
  -e MYSQL_PASSWORD=campus_app_password \
  -p 3307:3306 \
  mysql:8.4
```

### 3.2 Initialize Seed Dataset
Load the authoritative 11-user, 12-event master demonstration dataset:

```bash
mysql -h 127.0.0.1 -P 3307 -u campus_app -pcampus_app_password campus_events < database/seed.sql
```

### 3.3 Run Automated Test Suite (65/65 Passing)
```bash
# Set environment coordinates
export MYSQLHOST=127.0.0.1
export MYSQLPORT=3307
export MYSQLDATABASE=campus_events
export MYSQLUSER=campus_app
export MYSQLPASSWORD=campus_app_password

./mvnw test
```

### 3.4 Launch Application
```bash
./mvnw spring-boot:run
```
Access the application at `http://localhost:9090` (default port 9090 prevents host proxy collisions).
* **Student Login:** `aarav.sharma@campus.edu` / `password123`
* **Admin Login:** `admin@campus.edu` / `admin123`
* **OpenAPI Docs:** `http://localhost:9090/v3/api-docs`

---

## 4. Course Outcome (CO1–CO6) Evidence Index

| Course Outcome | Academic Domain | Artifact / Evidence Link | Status |
|---|---|---|---|
| **CO1** | Backend Service Architecture & DB Flow | [`docs/request-to-database-flow.md`](docs/request-to-database-flow.md)<br>End-to-end trace from HTTP POST down to InnoDB page buffer pool. | **PASS (Runtime)** |
| **CO2** | ER Modeling & Normalization | [`database/er-diagram.md`](database/er-diagram.md), [`docs/normalization.md`](docs/normalization.md)<br>Formal proofs for 1NF, 2NF, 3NF, BCNF, lossless join, and dependency preservation. | **PASS (Runtime)** |
| **CO3** | Advanced SQL Fluency | [`database/sql/`](database/sql/)<br>12 SQL modules: Joins, Aggregations, Subqueries, Chained CTEs, Recursive CTEs, Window Functions, Analytics. | **PASS (Runtime)** |
| **CO4** | Transactions, ACID & Concurrency Stress Test | [`database/transactions.sql`](database/transactions.sql), [`docs/concurrency-test.md`](docs/concurrency-test.md)<br>10-thread race test: exactly 1 succeeds, 9 fail with MySQL Error 1062. | **PASS (Runtime)** |
| **CO5** | Indexing Theory & EXPLAIN Optimization | [`database/indexes.sql`](database/indexes.sql), [`database/explain/README.md`](database/explain/README.md), [`docs/query-optimization.md`](docs/query-optimization.md)<br>51.7% cost reduction, filesort elimination, JPQL `JOIN FETCH` N+1 fix. | **PASS (Runtime)** |
| **CO6** | Distributed Databases & Outbox Pattern | [`src/main/resources/db/migration/V4__Hardening_and_audit.sql`](src/main/resources/db/migration/V4__Hardening_and_audit.sql), [`docs/distributed-database.md`](docs/distributed-database.md)<br>Flyway V4 `outbox_events` table, Primary-Replica GTID, read scaling, tenant sharding. | **PASS (Runtime + Design)** |

---

## 5. Concurrency Stress Test Results

CampusConnect implements a real multi-threaded integration stress test in [`EventServiceConcurrencyTest.java`](src/test/java/com/tejaswin/campus/service/EventServiceConcurrencyTest.java) utilizing a dual `CountDownLatch` barrier:

```text
[pool-2-thread-1] INFO EventService - Registration committed successfully. ID: 29
[pool-2-thread-2] ERROR o.h.e.jdbc.spi.SqlExceptionHelper - Duplicate entry '1-1' for key 'registrations.uk_user_event'
[pool-2-thread-3] ERROR o.h.e.jdbc.spi.SqlExceptionHelper - Duplicate entry '1-1' for key 'registrations.uk_user_event'
...
[pool-2-thread-10] ERROR o.h.e.jdbc.spi.SqlExceptionHelper - Duplicate entry '1-1' for key 'registrations.uk_user_event'
```

* **Simultaneous Threads:** 10
* **Expected Result:** Exactly 1 Success, 9 Duplicate Rejections
* **Actual Result:** **1 Success, 9 Rejected (MySQL Error 1062, SQLState 23000)**
* **Multi-User Throughput Test:** 8 distinct users simultaneously registering for the same event $\rightarrow$ **8/8 Success, 0 Deadlocks**.

---

## 6. Query Optimization & EXPLAIN ANALYZE Evidence

Query performance was benchmarked directly on MySQL 8.4 using `scripts/run_explain.py`:

```sql
SELECT id, title, category, date_time, venue, status
FROM events
WHERE category = 'Technical'
ORDER BY date_time ASC;
```

* **Before Indexing:** Full Table Scan (`type: ALL`), `Using filesort`, Cost = `1.45`, Execution = `0.0768 ms`.
* **After Indexing (`idx_events_category_date`):** Index Lookup (`type: ref`), **filesort eliminated**, Cost = `0.70`, Execution = `0.0384 ms`.
* **Improvement:** **51.7% query cost reduction, 50% latency drop, 100% external filesort elimination**.

---

## 7. Documentation Directory Guide

* **Comprehensive Design Report (20 Sections):** [`docs/design-report.md`](docs/design-report.md)
* **DBMS Compliance Matrix:** [`docs/dbms-compliance.md`](docs/dbms-compliance.md)
* **Data Dictionary:** [`docs/data-dictionary.md`](docs/data-dictionary.md)
* **Normalization Theory:** [`docs/normalization.md`](docs/normalization.md)
* **Request-to-Database Flow (CO1):** [`docs/request-to-database-flow.md`](docs/request-to-database-flow.md)
* **Transaction & ACID Analysis (CO4):** [`docs/transaction-analysis.md`](docs/transaction-analysis.md)
* **Concurrency Stress Test Report (CO4):** [`docs/concurrency-test.md`](docs/concurrency-test.md)
* **Query Optimization Report (CO5):** [`docs/query-optimization.md`](docs/query-optimization.md)
* **Distributed Database Architecture (CO6):** [`docs/distributed-database.md`](docs/distributed-database.md)
* **Data Architecture Decision (ADR):** [`docs/data-architecture-decision.md`](docs/data-architecture-decision.md)
* **Disaster Recovery & PITR Runbook:** [`docs/backup-recovery.md`](docs/backup-recovery.md)
* **Event Lifecycle State Machine:** [`docs/event-lifecycle.md`](docs/event-lifecycle.md)
* **Live Faculty Demo Script:** [`docs/demo-script.md`](docs/demo-script.md)
* **Postman Collection:** [`postman/CampusConnect.postman_collection.json`](postman/CampusConnect.postman_collection.json)

---

## 8. License

Released under the [MIT License](LICENSE).
