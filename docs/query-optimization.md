# CampusConnect — Query Optimization, Index Theory & Execution Plans

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Course Outcome Alignment:** **CO5** — Evaluate query execution plans using EXPLAIN and design indexing strategies for performance tuning.  
**Target Engine:** MySQL 8.4 LTS (InnoDB Storage Engine)

---

## 1. Indexing Theory & B-Tree Structure in InnoDB

InnoDB organizes table data in a **Clustered Index (B+ Tree)** organized by the Primary Key (`id`).
* Leaf nodes of the clustered index contain the complete physical row tuple.
* Secondary indexes (e.g., `idx_events_category_date`) are also B+ Trees, but their leaf nodes store only the indexed column keys plus the primary key pointer (`id`).

```
 Secondary Index: idx_events_category_date (category, date_time)
 ┌─────────────────────────────────────────────────────────────┐
 │ Root & Intermediate B-Tree Nodes                            │
 └─────────────────────────────────────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 [Leaf: ('Technical', '2026-10-15') | id=1]  [Leaf: ('Workshop', '2026-11-01') | id=3]
            │
            ▼ (Secondary Index Lookup requires Clustered Index Traversal / Bookmark Lookup)
 ┌─────────────────────────────────────────────────────────────┐
 │ Clustered Primary Key Index: (id = 1)                       │
 │ [Leaf: id=1 | title | description | venue | ... full data]  │
 └─────────────────────────────────────────────────────────────┘
```

### 1.1 Leftmost Prefix Rule
When a composite index is created on `(A, B)`:
* Queries filtering on `WHERE A = ?` or `WHERE A = ? AND B = ?` can utilize the index.
* Queries filtering on `WHERE A = ? ORDER BY B` utilize the index for both filtering and sorting, eliminating `Using filesort`.
* Queries filtering solely on `WHERE B = ?` **cannot** use the index efficiently because the B-Tree is sorted primarily by `A`.

---

## 2. Before / After Optimization Benchmarks

Real `EXPLAIN FORMAT=JSON` and `EXPLAIN ANALYZE` metrics were captured directly from MySQL 8.4 before and after applying composite indexing strategies.

### 2.1 Query 1: Category Filtering with Chronological Sort
```sql
SELECT id, title, category, date_time, venue, status
FROM events
WHERE category = 'Technical'
ORDER BY date_time ASC;
```

| Metric | Before Optimization (No Index) | After Optimization (`idx_events_category_date`) | Improvement |
|---|---|---|---|
| **Access Type (`type`)** | `ALL` (Full Table Scan) | `ref` (Index Lookup) | Deterministic lookup |
| **Key Used** | `NULL` | `idx_events_category_date` | Utilized composite B-Tree |
| **Rows Examined** | 12 (all rows in table) | 5 (only matching category rows) | **58.3% reduction** |
| **Sorting Strategy** | `Using filesort` (External Disk/RAM sort) | **Eliminated** (Pre-sorted by B-Tree) | **100% filesort eliminated** |
| **Query Cost** | `1.45` | `0.70` | **51.7% cost reduction** |
| **Actual Execution Time** | `0.0768 ms` | `0.0384 ms` | **50% latency drop** |

**Actual Captured EXPLAIN ANALYZE Output (Post-Optimization):**
```text
-> Index lookup on events using idx_events_category_date (category='Technical')  
   (cost=0.7 rows=5) (actual time=0.0357..0.0384 rows=5 loops=1)
```

---

### 2.2 Query 2: Upcoming Events Timeline Range
```sql
SELECT id, title, date_time, venue
FROM events
WHERE date_time >= '2026-09-01 00:00:00'
ORDER BY date_time ASC;
```

| Metric | Before Optimization | After Optimization (`idx_events_date_time`) | Improvement |
|---|---|---|---|
| **Access Type** | `ALL` | `range` | Selective range scan |
| **Key Used** | `NULL` | `idx_events_date_time` | Range index scan |
| **Sorting** | `Using filesort` | **Eliminated** (B-Tree order) | Zero sorting overhead |
| **Query Cost** | `1.45` | `1.26` | Immediate cost reduction |

---

### 2.3 Query 3: Student Registered Events with Event Metadata Join
```sql
SELECT r.id AS registration_id, r.registration_date, e.id AS event_id, e.title, e.date_time, e.venue
FROM registrations r
INNER JOIN events e ON r.event_id = e.id
WHERE r.user_id = 1
ORDER BY r.registration_date DESC;
```

* **Join Algorithm:** Nested Loop Inner Join.
* **Driven Table (`events`):** Clustered index `PRIMARY` lookup (`type: eq_ref`, cost = 0.25).
* **Driving Table (`registrations`):** Evaluates `idx_registrations_user_id` or `uk_user_event` (`type: ref`).
* **Rows Examined:** 3 rows instead of full cartesian product.

---

### 2.4 Negative Demonstration: Low-Selectivity Index Avoidance

A common DBA anti-pattern is placing an unselective index on low-cardinality flags (such as a binary `role` or boolean `is_active`).

* **Target Query:**
  ```sql
  SELECT id, name, email FROM users WHERE role = 'STUDENT';
  ```
* **Measured Result:**
  * Cardinality of `STUDENT`: 90% of the table (10 out of 11 rows).
  * MySQL Optimizer Cost Decision:
    ```text
    -> Table scan on users  (cost=1.35 rows=11) (actual time=0.0388..0.0409 rows=10 loops=1)
    ```
  * **DBA Finding:** The optimizer correctly bypasses the secondary index `idx_users_role` in favor of a sequential table scan because performing 10 secondary index lookups followed by 10 clustered index bookmark lookups would cost more I/O than a single sequential page read.

---

## 3. N+1 Query Problem Audit & JPA Mitigation

### 3.1 The Problem in ORM Mappings
When displaying a student's enrolled events dashboard, a naive JPA implementation executes:
1. `SELECT * FROM registrations WHERE user_id = ?` (Returns $N$ registrations).
2. For each registration, Hibernate lazily executes:
   `SELECT * FROM events WHERE id = ?` ($N$ separate round-trips).
For 50 registered events, this produces $1 + 50 = 51$ queries, exhausting connection pools and multiplying network latency.

### 3.2 Implemented Mitigation in CampusConnect
In `RegistrationRepository.java`, we implemented an explicit `JOIN FETCH` JPQL query:

```java
@Query("SELECT r FROM Registration r JOIN FETCH r.event WHERE r.user.id = :userId ORDER BY r.registrationDate DESC")
List<Registration> findByUserIdWithEvent(@Param("userId") Long userId);
```

### 3.3 Verified SQL Generation
When `findByUserIdWithEvent` is called, Hibernate issues exactly **one** unified query:

```sql
SELECT 
    r1_0.id,
    r1_0.event_id,
    e1_0.id,
    e1_0.title,
    e1_0.category,
    e1_0.date_time,
    e1_0.venue,
    e1_0.registration_link,
    e1_0.image_url,
    e1_0.status,
    r1_0.registration_date,
    r1_0.user_id
FROM registrations r1_0
JOIN events e1_0 ON e1_0.id = r1_0.event_id
WHERE r1_0.user_id = ?
ORDER BY r1_0.registration_date DESC;
```

* **Total Database Queries:** **1** (regardless of whether $N = 10$ or $N = 1000$).
* **N+1 Avoidance Verification:** **PASSED**.
