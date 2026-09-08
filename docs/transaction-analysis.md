# CampusConnect — Transaction Analysis, ACID Semantics & Concurrency Control

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Course Outcome Alignment:** **CO4** — Implement transactions and analyze isolation levels, concurrency anomalies, and locking protocols.  
**Target Engine:** MySQL 8.4 LTS (InnoDB Storage Engine)

---

## 1. ACID Properties in CampusConnect

CampusConnect enforces ACID guarantees across all state transitions, specifically during student registration and event administrative actions:

```
                      ┌───────────────────────────────────────┐
                      │             ACID Engine               │
                      └───────────────────────────────────────┘
                                         │
         ┌──────────────────┬────────────┴───────────┬──────────────────┐
         ▼                  ▼                        ▼                  ▼
    [Atomicity]        [Consistency]            [Isolation]        [Durability]
   Undo Log (Rollback) Integrity Constraints  REPEATABLE READ (MVCC)  Redo Log (WAL)
   Transaction Scope    Domain CHECK & FKs     Record/Gap Locking     innodb_flush_log
```

### 1.1 Atomicity
* **Definition:** A transaction is an indivisible unit of work; either all changes are committed, or none are.
* **Mechanism in CampusConnect:**
  * All composite operations (such as registering a student and writing to the `outbox_events` table) are enclosed within a single `@Transactional` method boundary.
  * If an exception occurs (e.g., unique constraint violation or validation failure), Spring triggers a rollback.
  * The InnoDB engine uses **Undo Logs** (`undo tablespace`) to revert all modified pages to their exact pre-transaction state.
* **Proof Script:** See `database/transactions.sql` Scenario 3 (Rollback Demonstration).

### 1.2 Consistency
* **Definition:** A transaction transforms the database from one valid state to another, satisfying all schema constraints, business invariants, and referential integrity.
* **Mechanism in CampusConnect:**
  * **Referential Integrity:** `FOREIGN KEY (user_id) REFERENCES users(id)` and `FOREIGN KEY (event_id) REFERENCES events(id)` with `ON DELETE CASCADE`.
  * **Entity Integrity:** Non-null primary keys on all tables.
  * **Domain Integrity:** MySQL CHECK constraints (`status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED')`, `CHAR_LENGTH(TRIM(title)) > 0`).
  * **Business Rule Integrity:** Unique constraint `uk_user_event` prevents duplicate event registrations.

### 1.3 Isolation
* **Definition:** Uncommitted changes in one transaction are invisible to concurrent transactions, preventing concurrency anomalies.
* **Mechanism in CampusConnect:**
  * Default Engine Isolation: `REPEATABLE READ`.
  * Read consistency powered by InnoDB **Multi-Version Concurrency Control (MVCC)** without read locks.
  * Write serialization achieved via **Pessimistic Locking** (`SELECT ... FOR UPDATE`).

### 1.4 Durability
* **Definition:** Once a transaction is committed, its changes survive system crashes, power failures, or server restarts.
* **Mechanism in CampusConnect:**
  * InnoDB **Write-Ahead Logging (WAL)**: All page modifications are written to the Redo Log buffer before being written to disk data files.
  * Production Setting: `innodb_flush_log_at_trx_commit = 1` flushes and fsyncs the redo log to physical disk upon every transaction commit.
  * Crash Recovery: On startup, InnoDB inspects the redo log checkpoint (`ib_logfile0`) and replays any committed transactions that were not yet flushed to data pages.

---

## 2. MySQL InnoDB Isolation Levels & Anomaly Matrix

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read (Select) | Phantom Read (Update) | Lost Update |
|---|---|---|---|---|---|
| **READ UNCOMMITTED** | Permitted | Permitted | Permitted | Permitted | Permitted |
| **READ COMMITTED** | Prevented | Permitted | Permitted | Permitted | Prevented (via locks) |
| **REPEATABLE READ (Default)** | **Prevented** | **Prevented** | **Prevented (via MVCC)** | Permitted (in raw SQL) | **Prevented (via FOR UPDATE)** |
| **SERIALIZABLE** | Prevented | Prevented | Prevented | Prevented | Prevented |

---

## 3. Deep Dive: Anomaly Prevention Mechanics

### 3.1 Dirty Read Prevention
* **Anomaly Definition:** Transaction $T_1$ modifies a row without committing. Transaction $T_2$ reads this uncommitted row. If $T_1$ subsequently rolls back, $T_2$ acted on invalid data.
* **How CampusConnect Prevents It:**
  Under `REPEATABLE READ` and `READ COMMITTED`, InnoDB never reads uncommitted dirty pages from memory. Instead, InnoDB inspects the row's `DB_TRX_ID` and `DB_ROLL_PTR`, traversing the Undo Log to reconstruct the latest committed version.

### 3.2 Non-Repeatable Read Prevention
* **Anomaly Definition:** Transaction $T_1$ reads row $R$. Transaction $T_2$ updates row $R$ and commits. When $T_1$ reads row $R$ again, it sees different values.
* **How CampusConnect Prevents It:**
  Under `REPEATABLE READ`, InnoDB establishes a **Consistent Read View** at the moment the first `SELECT` query executes in $T_1$. Any subsequent plain `SELECT` within $T_1$ uses this identical Read View, completely ignoring changes committed by $T_2$ after the Read View was established.

### 3.3 Phantom Read Prevention
* **Anomaly Definition:** Transaction $T_1$ executes a range query (e.g., `SELECT * FROM events WHERE category = 'Technical'`). Transaction $T_2$ inserts a new row matching the condition and commits. $T_1$ repeats the query and sees a new "phantom" row.
* **How CampusConnect Prevents It:**
  * **Consistent Read (MVCC):** Plain `SELECT` queries do not see phantoms because the snapshot was established at the start of the transaction.
  * **Locking Read (Next-Key Locks):** When a transaction executes `SELECT ... FOR UPDATE` over a range or index, InnoDB sets **Next-Key Locks** (a combination of a record lock on the index record plus a gap lock on the gap preceding the record). This physically blocks concurrent transactions from inserting into the locked interval.

### 3.4 Lost Update Prevention
* **Anomaly Definition:** Two transactions simultaneously read the same record, compute a new value based on that read, and write it back. The last writer overwrites the first writer's modification without including it.
* **How CampusConnect Prevents It:**
  In `EventService.java`, event retrieval for state-dependent operations uses pessimistic locking:
  ```java
  Event event = eventRepository.findByIdForUpdate(eventId)
      .orElseThrow(() -> new ResourceNotFoundException("Event not found"));
  ```
  This generates:
  ```sql
  SELECT * FROM events WHERE id = ? FOR UPDATE;
  ```
  The first transaction acquires an exclusive X-lock. Any concurrent transaction attempting to execute `findByIdForUpdate` on that same event blocks until the first transaction commits or rolls back, guaranteeing zero lost updates.

---

## 4. Multi-Version Concurrency Control (MVCC) Architecture

InnoDB implements MVCC by appending hidden system columns to every clustered index record:

1. `DB_TRX_ID` (6 bytes): Transaction ID of the last transaction that inserted or modified the row.
2. `DB_ROLL_PTR` (7 bytes): Roll pointer pointing to the undo log record in the undo tablespace containing the prior state of the row.
3. `DB_ROW_ID` (6 bytes): Monotonically increasing row identifier (if no explicit primary key exists).

```
 Clustered Index Record (events: id=1)
 ┌──────┬──────────────────────┬───────────┬──────────────┬───────────────┐
 │ id=1 │ title='ACM Hackathon'│ status='P'│ DB_TRX_ID=104│ DB_ROLL_PTR───┼──┐
 └──────┴──────────────────────┴───────────┴──────────────┴───────────────┘  │
                                                                             ▼
                             Undo Log Segment (Undo Tablespace)
                             ┌───────────────────────────────────────────┐
                             │ DB_TRX_ID=98 | status='DRAFT' | ptr ──────┼──► older version...
                             └───────────────────────────────────────────┘
```

When Transaction $T_{105}$ initiates a read under `REPEATABLE READ`, InnoDB creates a Read View containing:
* `m_low_limit_id`: Highest transaction ID created so far. Any transaction ID $\ge$ this is invisible.
* `m_up_limit_id`: Lowest active (uncommitted) transaction ID. Any transaction ID $<$ this is visible.
* `m_ids`: Set of active transaction IDs at snapshot creation time.

If a row's `DB_TRX_ID` is in `m_ids`, InnoDB follows `DB_ROLL_PTR` down the undo chain until it finds a record committed before $T_{105}$'s Read View was established. This allows non-blocking, lock-free reads while concurrent writes proceed.

---

## 5. Deadlock Detection and Resolution

### 5.1 Scenario Analysis
A deadlock occurs if:
* Transaction $A$ locks Event 1, then attempts to lock Event 2.
* Transaction $B$ locks Event 2, then attempts to lock Event 1.

### 5.2 InnoDB Deadlock Handling
* InnoDB runs an active **Deadlock Detector** (wait-for graph inspection).
* When a cycle in the wait-for graph is discovered, InnoDB automatically chooses the transaction with the smaller undo log footprint as the **victim** and rolls it back:
  `ERROR 1213 (40001): Deadlock found when trying to get lock; try restarting transaction`.
* **CampusConnect Mitigation:**
  1. All operations lock entities in consistent primary key order.
  2. The registration workflow only locks the single target event and the candidate registration tuple, avoiding multi-entity lock cross-dependencies.
