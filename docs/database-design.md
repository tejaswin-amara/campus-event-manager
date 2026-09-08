# CampusConnect — Database Systems Engineering Architecture & Design

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Authoritative Runtime Engine:** MySQL 8.4 LTS (InnoDB Storage Engine)  
**Schema Version:** Flyway V1 through V4 (`V4__Hardening_and_audit.sql`)

---

## 1. Executive Summary

CampusConnect's persistence layer is engineered to deliver strict ACID guarantees, eliminate race conditions under concurrent registration rushes, and achieve sub-millisecond query latencies.

The architecture comprises three primary representations:
1. **Conceptual Model:** Entity-Relationship (ER) model defining cardinalities and participation invariants ([`database/er-diagram.md`](../database/er-diagram.md)).
2. **Logical Model:** Boyce-Codd Normal Form (BCNF) relational schema with formal mathematical decomposition proofs ([`docs/normalization.md`](normalization.md)).
3. **Physical Model:** InnoDB clustered B+ Trees, composite secondary indexes, domain CHECK constraints, and WAL durability configuration ([`database/schema.sql`](../database/schema.sql)).

---

## 2. Relational Architecture & Entity Definitions

```
                     ┌────────────────────────────────────┐
                     │               users                │
                     ├────────────────────────────────────┤
                     │ PK  id           BIGINT            │
                     │ UK  email        VARCHAR(150)      │
                     │     name         VARCHAR(100)      │
                     │     password     VARCHAR(255)      │
                     │ IDX role         VARCHAR(20)       │
                     │     department   VARCHAR(100)      │
                     │     created_at   TIMESTAMP         │
                     └─────────────────┬──────────────────┘
                                       │ 1
                                       │
                                       │ 0..*
                     ┌─────────────────▼──────────────────┐
                     │           registrations            │
                     ├────────────────────────────────────┤
                     │ PK  id                BIGINT       │
                     │ FK  user_id           BIGINT       │
                     │ FK  event_id          BIGINT       │
                     │     registration_date TIMESTAMP    │
                     │ UK  (user_id, event_id)            │
                     └─────────────────▲──────────────────┘
                                       │ 0..*
                                       │
                                       │ 1
                     ┌─────────────────┴──────────────────┐
                     │               events               │
                     ├────────────────────────────────────┤
                     │ PK  id                BIGINT       │
                     │     title             VARCHAR(200) │
                     │     description       TEXT         │
                     │ IDX category          VARCHAR(50)  │
                     │ IDX date_time         DATETIME     │
                     │     venue             VARCHAR(100) │
                     │     registration_link VARCHAR(500) │
                     │     image_url         VARCHAR(500) │
                     │ IDX status            VARCHAR(20)  │
                     │     created_at        TIMESTAMP    │
                     └────────────────────────────────────┘

                     ┌────────────────────────────────────┐
                     │           outbox_events            │
                     ├────────────────────────────────────┤
                     │ PK  id             BIGINT          │
                     │     aggregate_type VARCHAR(50)     │
                     │     aggregate_id   BIGINT          │
                     │     event_type     VARCHAR(50)     │
                     │     payload        JSON            │
                     │ IDX status         VARCHAR(20)     │
                     │ IDX created_at     TIMESTAMP       │
                     │     processed_at   TIMESTAMP       │
                     └────────────────────────────────────┘
```

---

## 3. Core Database Invariants & Enforcements

| Invariant / Business Rule | Enforcement Mechanism | Failure Mode Prevented |
|---|---|---|
| **Single Seat per Student** | `UNIQUE KEY uk_user_event (user_id, event_id)` | Prevents duplicate enrollments under high-concurrency race conditions. |
| **Referential Integrity** | `FOREIGN KEY ... ON DELETE CASCADE` | Eliminates orphaned registration records upon user or event removal. |
| **Event Lifecycle Integrity** | `CHECK (status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED'))` | Prevents corrupt or unauthorized event states. |
| **Non-Empty String Data** | `CHECK (CHAR_LENGTH(TRIM(title)) > 0)` and `CHECK (CHAR_LENGTH(TRIM(venue)) > 0)` | Prevents blank or whitespace-only records. |
| **Account Identity Uniqueness** | `UNIQUE KEY (email)` | Guarantees single account per academic email. |
| **Decoupled Asynchronous Events** | `outbox_events` table with JSON payload | Ensures reliable domain event publishing without fragile 2-Phase Commit (2PC). |

---

## 4. Indexing & Storage Engine Structure

All tables use the **InnoDB** storage engine:
* **Primary Key Indexing:** Every table possesses an explicit surrogate primary key (`id BIGINT AUTO_INCREMENT`), serving as the **Clustered Index**. Data rows are physically ordered by `id` on 16KB InnoDB pages.
* **Secondary Indexes:**
  * `uk_users_email`: Enforces email uniqueness and optimizes authentication lookups ($O(\log N)$).
  * `idx_events_category_date`: Composite B-Tree index on `(category, date_time)` powering category-filtered queries while eliminating external filesorts.
  * `idx_events_date_time`: Range index for upcoming timeline queries (`WHERE date_time >= NOW()`).
  * `idx_events_status_date_time`: Added in V4 migration to accelerate catalog queries for published events.
  * `idx_registrations_user_id` and `idx_registrations_event_id`: Accelerate student enrollment histories and attendee roster aggregations.

---

## 5. Directory Cross-Reference

* **Master DDL:** [`database/schema.sql`](../database/schema.sql)
* **Master Seed Dataset:** [`database/seed.sql`](../database/seed.sql)
* **Data Dictionary:** [`docs/data-dictionary.md`](data-dictionary.md)
* **Normalization Theory:** [`docs/normalization.md`](normalization.md)
* **Query Optimization & EXPLAIN:** [`docs/query-optimization.md`](query-optimization.md)
* **Distributed Architecture:** [`docs/distributed-database.md`](distributed-database.md)
* **ACID & Transactions:** [`docs/transaction-analysis.md`](transaction-analysis.md)
