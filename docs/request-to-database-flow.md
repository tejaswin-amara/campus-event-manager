# CampusConnect — Request-to-Database End-to-End Execution Flow

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Course Outcome Alignment:** **CO1** — Analyze backend services as systems interacting with database layers.  
**Target Transactional Route:** `POST /student/register` (Student Event Registration & Attendance Interest)

---

## 1. Architectural Flow Diagram

The diagram below traces an incoming HTTP registration request through every layer of the distributed backend stack down to the physical storage engine and transactional commit:

```mermaid
sequenceDiagram
    autonumber
    actor Client as Browser / HTTP Client
    participant Sec as Spring Security Filter Chain
    participant Ctrl as StudentController
    participant Svc as EventService (@Transactional)
    participant RepoE as EventRepository
    participant RepoR as RegistrationRepository
    participant Outbox as OutboxRepository (CO6)
    participant Hikari as HikariCP Connection Pool
    participant MySQL as MySQL 8.4 Server (InnoDB)
    participant Disk as Physical Storage (Redo Log/Tablespace)

    Client->>Sec: POST /student/register?eventId=1 (Session Cookie: JSESSIONID)
    Note over Sec: Authenticates session, verifies ROLE_STUDENT authorization
    Sec->>Ctrl: Dispatch to registerForEvent(@RequestParam Long eventId, Principal)
    
    Ctrl->>Svc: registerStudent(eventId, email)
    Note over Svc: Open Spring Transaction (Propagation.REQUIRED)
    Svc->>Hikari: Borrow active physical connection
    Hikari->>MySQL: BEGIN TRANSACTION (ISOLATION LEVEL REPEATABLE READ)
    
    Svc->>RepoE: findByIdForUpdate(eventId)
    Note over RepoE: Pessimistic Write Lock (SELECT ... FOR UPDATE)
    RepoE->>MySQL: SELECT * FROM events WHERE id = 1 FOR UPDATE
    MySQL->>Disk: Read clustered index page into InnoDB Buffer Pool
    MySQL-->>RepoE: Return locked Event entity (status: 'PUBLISHED')
    
    Svc->>RepoR: existsByUserIdAndEventId(user.getId(), eventId)
    RepoR->>MySQL: SELECT COUNT(*) > 0 FROM registrations WHERE user_id = 1 AND event_id = 1
    MySQL-->>RepoR: false (user not yet registered)
    
    Svc->>RepoR: save(new Registration(user, event))
    RepoR->>MySQL: INSERT INTO registrations (user_id, event_id, registration_date) VALUES (1, 1, NOW())
    Note over MySQL: InnoDB checks UNIQUE constraint (uk_user_event) via B-Tree
    MySQL-->>RepoR: Insert OK (Generated ID = 29)
    
    opt Asynchronous Event Decoupling (CO6 Outbox)
        Svc->>Outbox: save(new OutboxEvent("REGISTRATION", 29, "EVENT_REGISTERED", payload))
        Outbox->>MySQL: INSERT INTO outbox_events (...) VALUES (...)
        MySQL-->>Outbox: Insert OK
    end
    
    Note over Svc: Method exits successfully; Spring triggers Transaction Commit
    Svc->>MySQL: COMMIT
    MySQL->>Disk: Write transaction undo/redo log to ib_logfile0 (WAL flush)
    MySQL-->>Hikari: Commit confirmed; release row lock on events
    Hikari-->>Svc: Return connection to pool
    
    Svc-->>Ctrl: Return updated Registration entity
    Ctrl-->>Client: 302 Redirect to /student/dashboard?registered=true
```

---

## 2. Step-by-Step Execution Mechanics

### 2.1 Layer 1: HTTP Client & Transport
* **Protocol:** HTTP/1.1 or HTTP/2 over TLS.
* **Payload:** `POST /student/register` with URL-encoded parameter `eventId=1`.
* **Headers:** `Cookie: JSESSIONID=B263F...` identifying the authenticated student session.
* **CSRF Verification:** Spring Security CSRF token validated from request header or form parameter (`_csrf`).

---

### 2.2 Layer 2: Spring Security Filter Chain
* **Filter:** `UsernamePasswordAuthenticationToken` is resolved from `SecurityContextPersistenceFilter`.
* **Authorization Check:** Evaluates ant matchers:
  ```java
  .requestMatchers("/student/**").hasRole("STUDENT")
  ```
* **Principal Resolution:** Extracts the current user identity (`user@campus.edu`). If unauthenticated, the filter chain redirects to `/login` with HTTP 302.

---

### 2.3 Layer 3: Web Controller (`StudentController`)
* **Endpoint:** `@PostMapping("/student/register")`
* **Input Validation:**
  * Checks that `eventId` is a non-null positive integer (`Long`).
  * Resolves user details via `userService.getUserByEmail(principal.getName())`.
* **Delegation:** Invokes `eventService.registerStudent(eventId, user.getEmail())`.

---

### 2.4 Layer 4: Service Layer & Transaction Boundary (`EventService`)
* **Annotation:** `@Transactional(isolation = Isolation.REPEATABLE_READ, rollbackFor = Exception.class)`
* **Spring Transaction Manager (`JpaTransactionManager`):**
  1. Detects transaction boundary.
  2. Acquires a JDBC `Connection` from `HikariDataSource`.
  3. Executes `connection.setAutoCommit(false)`.
  4. Binds the connection to the current thread via `TransactionSynchronizationManager`.

---

### 2.5 Layer 5: Data Access & Pessimistic Locking (`EventRepository`)
* **Method:** `eventRepository.findByIdForUpdate(eventId)`
* **Generated SQL:**
  ```sql
  SELECT e.id, e.title, e.category, e.date_time, e.venue, e.registration_link, e.image_url, e.status, e.created_at
  FROM events e
  WHERE e.id = 1
  FOR UPDATE;
  ```
* **Locking Semantics:** InnoDB acquires an **exclusive record lock (X-lock)** on the primary key index leaf for `id = 1`. Any concurrent transaction attempting to modify or lock this event must wait until this transaction commits or aborts.
* **Domain Check:** Service verifies `event.getStatus().equals("PUBLISHED")`. If the event was cancelled or is in draft, an `IllegalStateException` is thrown, triggering a rollback.

---

### 2.6 Layer 6: Duplicate Check & Unique Index Enforcement
* **Application Level Check:**
  ```java
  if (registrationRepository.existsByUserIdAndEventId(user.getId(), eventId)) {
      throw new DuplicateRegistrationException("Student already registered for this event");
  }
  ```
* **Database Level Enforcement:**
  When `registrationRepository.save(registration)` executes:
  ```sql
  INSERT INTO registrations (user_id, event_id, registration_date)
  VALUES (1, 1, '2026-09-08 21:15:00');
  ```
* **InnoDB Concurrency Safety:**
  If two concurrent requests bypass the Java `existsBy...` check simultaneously:
  1. MySQL executes the duplicate key check on `UNIQUE KEY uk_user_event (user_id, event_id)`.
  2. The first thread acquires an exclusive index lock and inserts the tuple.
  3. The second thread detects key collision and MySQL throws:
     `ERROR 1062 (23000): Duplicate entry '1-1' for key 'registrations.uk_user_event'`.
  4. Spring's `PersistenceExceptionTranslationPostProcessor` converts this into a `DataIntegrityViolationException`, which rolls back the second transaction cleanly.

---

### 2.7 Layer 7: Transactional Outbox Pattern (CO6)
* Inside the **exact same database transaction**, an outbox event is persisted:
  ```sql
  INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, payload, status, created_at)
  VALUES ('REGISTRATION', 29, 'EVENT_REGISTERED', '{"userId":1,"eventId":1,"email":"aarav.sharma@campus.edu"}', 'PENDING', NOW());
  ```
* Because both the `registrations` record and the `outbox_events` record are saved in the same local transaction, atomicity is guaranteed without distributed 2-Phase Commit (2PC) overhead.

---

### 2.8 Layer 8: InnoDB Engine & Storage Subsystem Commit
* **Commit Trigger:** Service method returns; `JpaTransactionManager` invokes `connection.commit()`.
* **InnoDB Write-Ahead Logging (WAL):**
  1. Undo log records are written to keep MVCC read consistency for concurrent transactions.
  2. Redo log entries describing the page changes are written to the Redo Log Buffer.
  3. Per `innodb_flush_log_at_trx_commit = 1`, the Redo Log Buffer is flushed and fsync'd to physical disk (`ib_logfile0`).
  4. Clustered index pages in the InnoDB Buffer Pool are marked "dirty" and scheduled for asynchronous flushing by page cleaner threads.
* **Lock Release:** All record locks held on `events` and `registrations` are released immediately.
* **Connection Handback:** `connection.setAutoCommit(true)` is reset, and the physical JDBC connection is returned to the HikariCP pool.

---

## 3. Failure & Rollback Modes Matrix

| Failure Point | Trigger Condition | System Reaction | Database State |
|---|---|---|---|
| **Invalid Event ID** | Event ID does not exist | `ResourceNotFoundException` thrown | Transaction rolled back; no locks retained |
| **Non-Published Event** | Event status is `CANCELLED` or `DRAFT` | `IllegalStateException` thrown | Transaction rolled back; event remains unmodified |
| **Duplicate Registration** | Same student clicks register twice concurrently | `DataIntegrityViolationException` via `uk_user_event` | Second transaction rolled back; first registration intact |
| **Database Network Timeout** | DB crash or connection dropped during query | `CannotCreateTransactionException` | HikariCP marks connection broken; 500 error returned to client |
| **Outbox Insert Failure** | Disk full / payload serialization failure | Exception bubbles out of service | Entire transaction rolls back; neither registration nor outbox committed |
