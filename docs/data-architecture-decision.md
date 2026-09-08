# CampusConnect — Data Architecture Decision Record (ADR)

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Document Status:** Approved & Authoritative  
**Decision Scope:** Core Transactional Engine Selection, Polyglot Complementarity, and Search Paradigms

---

## 1. Context & Problem Statement

CampusConnect serves as an integrated event aggregation and student registration platform. The operational requirements demand:
1. Strict ACID transactions to prevent overselling and duplicate registrations.
2. Relational integrity across users, events, and registrations with cascading constraints.
3. Sub-millisecond indexed queries for event catalog browsing and filtering.
4. Seamless compatibility with containerized development environments and standard enterprise Java frameworks (Spring Boot 3.4, Hibernate 6.6, Flyway 10.20).

We evaluated four primary architectural paradigms:
1. **Relational RDBMS: MySQL 8.4 LTS (InnoDB)**
2. **Relational RDBMS: PostgreSQL 16**
3. **Document Store: MongoDB 7.0**
4. **Vector Database / Extension: pgvector / Dedicated Vector Store**

---

## 2. Evaluation Matrix

| Decision Criteria | MySQL 8.4 LTS (InnoDB) | PostgreSQL 16 | MongoDB 7.0 | Vector Engine (pgvector) |
|---|---|---|---|---|
| **ACID Guarantees** | Full ACID (InnoDB WAL + MVCC) | Full ACID (WAL + MVCC) | Document-level ACID (Multi-doc via wiredTiger transactions with high latency overhead) | Typically eventual consistency / approximate nearest neighbor |
| **Integrity Enforcement** | Declarative PK, FK (`CASCADE`), UNIQUE, CHECK constraints | Declarative PK, FK (`CASCADE`), UNIQUE, CHECK, Domain types | Application-level validation or JSON Schema validators (No cross-collection FKs) | External metadata tables required |
| **Concurrency Under Contention** | Pessimistic Record/Gap locking (`SELECT FOR UPDATE`), low row-level overhead | Strong row-level locking (`FOR UPDATE`, `FOR SHARE`), SSI | Optimistic concurrency / write lock per collection shard | Index rebuild contention |
| **Dialect & Portability** | MySQL 8.4 dialect; standard SQL-92/99/2016 support | Highly expressive SQL, rich window functions, CTEs | Aggregation pipelines (JSON MQL) | Vector similarity operators (`<->`, `<#>`) |
| **Existing Repository Alignment** | **100% Native:** Existing schema, Flyway migrations V1–V4, and 65 tests build natively | Requires dialect translation and custom SQL changes | Requires complete ORM replacement (Spring Data MongoDB) | Irrelevant for core transactional catalog |

---

## 3. Decision & Trade-Off Rationale

### 3.1 Decision 1: Retention of MySQL 8.4 LTS as Authoritative Runtime Engine
* **Verdict:** **SELECTED (Authoritative Runtime Engine)**.
* **Rationale:**
  1. The existing repository codebase, database initialization scripts, connection pooling, and Flyway migration baseline are built on MySQL.
  2. MySQL 8.4 LTS introduces modern SQL features required for academic compliance (Window functions, Common Table Expressions, Recursive CTEs, native JSON column support, and domain `CHECK` constraints).
  3. Preserving MySQL 8.4 eliminates disruptive migration risk, allowing all 65 automated tests and multi-threaded concurrency suites to pass with 100% reliability.

### 3.2 Decision 2: PostgreSQL 16 Support as Documented Equivalent
* **Verdict:** **DOCUMENTED EQUIVALENT (Full Side-by-Side DDL/DML Support)**.
* **Rationale:**
  1. For academic rigor and portability, every DDL migration, DML statement, and analytical query has been verified and provided with its native PostgreSQL 16 equivalent in `database/schema.sql` and `database/sql/`.
  2. For instance, PostgreSQL's native `FULL OUTER JOIN` is documented alongside MySQL's ANSI-compliant `LEFT JOIN ... UNION ... RIGHT JOIN` emulation pattern.

### 3.3 Decision 3: Rejection of Document Store (MongoDB) for Core Catalog
* **Verdict:** **REJECTED for Transactional Core**.
* **Rationale:**
  1. Event registration inherently represents an $M:N$ relational association between `users` and `events`.
  2. In a document model, embedding registration lists inside event documents creates document growth limits (BSON 16MB cap) and severe write contention when hundreds of students register concurrently.
  3. Referencing IDs across collections without foreign key cascading constraints invites orphaned data and data anomalies during user or event deletions.
  4. MongoDB multi-document transactions introduce significant lock contention and performance degradation compared to InnoDB row-level locking.

### 3.4 Decision 4: Role of Vector Databases for Campus Event Discovery
* **Verdict:** **OPTIONAL / FUTURE EXTENSION (Recommended for Semantic Search)**.
* **Rationale:**
  1. Keyword search (e.g., `LIKE '%hackathon%'` or MySQL Full-Text Search) is sufficient for categorical lookups but fails to capture semantic student intents (e.g., "beginner friendly AI coding contests").
  2. As detailed in `database/sql/analytics.sql`, modern campus platforms benefit from an asynchronous vector pipeline:
     * When an event is published, an Outbox worker generates text embeddings (e.g., 768-dimensional vectors via Vertex AI or Ollama).
     * Embeddings are stored in a dedicated vector index (or pgvector) for semantic similarity retrieval.
     * Core registrations, seat quotas, and attendee rosters remain strictly anchored in the relational MySQL ACID engine.

---

## 4. Architectural Summary

$$\text{Architecture} = \underbrace{\text{MySQL 8.4 (InnoDB)}}_{\text{ACID Core (Users, Events, Registrations, Outbox)}} + \underbrace{\text{Outbox Pattern}}_{\text{Decoupled Event Streaming}} + \underbrace{\text{Redis / Vector Store (Future)}}_{\text{Cache & Semantic Search}}$$
