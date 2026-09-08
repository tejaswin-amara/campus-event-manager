# CampusConnect — Database Data Dictionary

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Authoritative Runtime Database:** MySQL 8.4 LTS (InnoDB Engine)  
**PostgreSQL Equivalent:** Fully documented in `database/schema.sql`

---

## 1. Overview & Entity Summary

CampusConnect operates an ACID-compliant relational schema comprising 4 core tables:

| Table Name | Description | Engine | Primary Key | Foreign Keys | Status |
|---|---|---|---|---|---|
| `users` | Authenticated campus members (STUDENT, ADMIN) | InnoDB | `id` (BIGINT) | None | Implemented Runtime |
| `events` | Aggregated campus events with lifecycle status | InnoDB | `id` (BIGINT) | None | Implemented Runtime |
| `registrations` | Student registration intent / attendance record | InnoDB | `id` (BIGINT) | `user_id`, `event_id` | Implemented Runtime |
| `outbox_events` | Transactional outbox for reliable event publishing | InnoDB | `id` (BIGINT) | None | Implemented Runtime (V4) |

---

## 2. Table: `users`

Stores authentication credentials, university email identities, and role-based access control flags.

### 2.1 Column Definitions

| Column Name | Data Type | Nullable | Default | Key | Constraints | Description | Example |
|---|---|---|---|---|---|---|---|
| `id` | `BIGINT` | `NO` | `AUTO_INCREMENT` | `PK` | `PRIMARY KEY` | Surrogate primary key | `1` |
| `username` | `VARCHAR(50)` | `NO` | None | `UNI` | `NOT NULL UNIQUE` | Login identifier | `'aarav_sharma'` |
| `password` | `VARCHAR(255)` | `NO` | None | None | Bcrypt hash (length 60) | Salted & hashed password | `'$2a$10$7R3...'` |
| `role` | `VARCHAR(20)` | `NO` | None | None | None | Role authorization claim | `'STUDENT'` |
| `email` | `VARCHAR(254)` | `YES` | `NULL` | `UNI` | `UNIQUE` | Academic campus email address | `'aarav.sharma@campus.edu'` |

### 2.2 Keys and Constraints

* **Primary Key:** `PRIMARY KEY (id)` — Clustered B-Tree index.
* **Candidate Keys:**
  * `id`
  * `username` (UNIQUE)
  * `email` (UNIQUE)
* **Indexes:**
  * `PRIMARY` on `(id)` — Unique, Clustered.
  * Implicit unique index on `(username)` — Unique, Non-clustered B-Tree.
  * Implicit unique index on `(email)` — Unique, Non-clustered B-Tree.

---

## 3. Table: `events`

Stores campus events aggregated across clubs, departments, and hackathons. Includes event metadata, venue, schedule, external registration link, and lifecycle status.

### 3.1 Column Definitions

| Column Name | Data Type | Nullable | Default | Key | Constraints | Description | Example |
|---|---|---|---|---|---|---|---|
| `id` | `BIGINT` | `NO` | `AUTO_INCREMENT` | `PK` | `PRIMARY KEY` | Surrogate primary key | `1` |
| `title` | `VARCHAR(200)` | `NO` | None | None | `CHAR_LENGTH(TRIM(title)) > 0` | Official title of the campus event | `'ACM Hackathon 2026'` |
| `description` | `TEXT` | `YES` | `NULL` | None | None | Detailed markdown/prose description | `'Annual 24-hour campus hackathon'` |
| `category` | `VARCHAR(50)` | `NO` | None | `IDX` | None | Classification (Technical, Cultural, Sports, Workshop) | `'Technical'` |
| `date_time` | `DATETIME` | `NO` | None | `IDX` | None | Scheduled start date and time | `'2026-10-15 09:00:00'` |
| `venue` | `VARCHAR(100)` | `NO` | None | None | `CHAR_LENGTH(TRIM(venue)) > 0` | Physical auditorium or laboratory venue | `'Main Auditorium'` |
| `registration_link` | `VARCHAR(500)` | `YES` | `NULL` | None | Valid URI scheme | External registration form or ticket link | `'https://forms.campus.edu/hack2026'` |
| `image_url` | `VARCHAR(500)` | `YES` | `NULL` | None | Valid URI scheme | Event promotional poster banner | `'https://images.campus.edu/posters/hack.jpg'` |
| `status` | `VARCHAR(20)` | `NO` | `'PUBLISHED'` | `IDX` | `CHECK (status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED'))` | Lifecycle stage | `'PUBLISHED'` |
| `created_at` | `TIMESTAMP` | `YES` | `CURRENT_TIMESTAMP` | None | None | Event record creation timestamp | `'2026-09-01 10:00:00'` |

### 3.2 Keys and Constraints

* **Primary Key:** `PRIMARY KEY (id)` — Clustered B-Tree index.
* **Candidate Keys:**
  * `id`
  * Composite candidate key: `(title, venue, date_time)` (natural operational key preventing duplicate venue bookings).
* **Indexes:**
  * `PRIMARY` on `(id)` — Unique, Clustered.
  * `idx_events_category_date` on `(category, date_time)` — Composite B-Tree index supporting category filtering with chronological sort.
  * `idx_events_date_time` on `(date_time)` — B-Tree index for upcoming event timeline lookups.
  * `idx_events_status_date_time` on `(status, date_time)` — Composite B-Tree index supporting active published event discovery without table scans.

---

## 4. Table: `registrations`

Associates students with events they have registered for or expressed intent to attend.

### 4.1 Column Definitions

| Column Name | Data Type | Nullable | Default | Key | Constraints | Description | Example |
|---|---|---|---|---|---|---|---|
| `id` | `BIGINT` | `NO` | `AUTO_INCREMENT` | `PK` | `PRIMARY KEY` | Surrogate primary key | `1` |
| `user_id` | `BIGINT` | `NO` | None | `MUL` | `FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE` | Registered student ID | `1` |
| `event_id` | `BIGINT` | `NO` | None | `MUL` | `FOREIGN KEY REFERENCES events(id) ON DELETE CASCADE` | Registered event ID | `1` |
| `registration_date` | `TIMESTAMP` | `YES` | `CURRENT_TIMESTAMP` | None | Non-updatable timestamp | Registration record timestamp | `'2026-09-05 14:22:10'` |

### 4.2 Keys and Constraints

* **Primary Key:** `PRIMARY KEY (id)` — Clustered B-Tree index.
* **Candidate Keys:**
  * `id`
  * `(user_id, event_id)` via `uk_user_event`
* **Foreign Keys:**
  * `fk_registrations_user`: `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`
  * `fk_registrations_event`: `FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE`
* **Unique Constraints:**
  * `uk_user_event`: `UNIQUE KEY (user_id, event_id)` — Enforces the critical business rule: a student can register for an event at most once. Tested under 10 concurrent threads.
* **Indexes:**
  * `PRIMARY` on `(id)` — Unique, Clustered.
  * `uk_user_event` on `(user_id, event_id)` — Composite Unique B-Tree index.
  * `idx_registrations_event_id` on `(event_id)` — Non-unique B-Tree index for attendee roster generation and enrollment counts.
  * `idx_registrations_user_id` on `(user_id)` — Non-unique B-Tree index for student registration history queries.

---

## 5. Table: `outbox_events`

Maintains asynchronous domain event messages produced inside application transactions for reliable decoupled distribution to notification, analytics, or search pipelines.

### 5.1 Column Definitions

| Column Name | Data Type | Nullable | Default | Key | Constraints | Description | Example |
|---|---|---|---|---|---|---|---|
| `id` | `BIGINT` | `NO` | `AUTO_INCREMENT` | `PK` | `PRIMARY KEY` | Surrogate primary key | `1` |
| `aggregate_type` | `VARCHAR(50)` | `NO` | None | None | None | Originating aggregate root | `'REGISTRATION'` |
| `aggregate_id` | `VARCHAR(100)` | `NO` | None | None | None | ID of the aggregate root | `'1'` |
| `event_type` | `VARCHAR(50)` | `NO` | None | None | None | Domain event identifier | `'EVENT_REGISTERED'` |
| `payload` | `JSON` | `NO` | None | None | Valid JSON structure | Serialized event payload | `'{"userId": 1, "eventId": 1}'` |
| `status` | `VARCHAR(20)` | `NO` | `'PENDING'` | `IDX` | `CHECK (status IN ('PENDING', 'PROCESSED', 'FAILED'))` | Outbox publishing status | `'PENDING'` |
| `created_at` | `TIMESTAMP` | `YES` | `CURRENT_TIMESTAMP` | `IDX` | None | Message queueing timestamp | `'2026-09-05 14:22:11'` |
| `processed_at` | `TIMESTAMP` | `YES` | `NULL` | None | None | Message dispatch timestamp | `'2026-09-05 14:22:12'` |

### 5.2 Keys and Constraints

* **Primary Key:** `PRIMARY KEY (id)` — Clustered B-Tree index.
* **Indexes:**
  * `PRIMARY` on `(id)` — Unique, Clustered.
  * `idx_outbox_status_created` on `(status, created_at)` — Composite index for efficient polling workers (`WHERE status = 'PENDING' ORDER BY created_at ASC`).

---

## 6. Referencing Entity Relationship Graph

```
 [users] 1 ────────── 0..* [registrations] *..0 ────────── 1 [events]
   │                              │
   │ (user_id)                    │ (event_id)
   └──────────────────────────────┘
               │
          [outbox_events] (Transactional decoupling)
```

## 7. Data Integrity Rules Matrix

| Rule Name | Target Table | Enforcement Mechanism | Severity if Violated | Academic Proof |
|---|---|---|---|---|
| Student Identity Uniqueness | `users` | `UNIQUE KEY (email)` | Data integrity violation / auth collision | 1NF / Candidate Key |
| Role Domain Boundary | `users` | `CHECK (role IN ('STUDENT', 'ADMIN'))` | Privilege escalation | Domain Constraint |
| Event Status State Machine | `events` | `CHECK (status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED'))` | Inconsistent event state | Domain Constraint |
| Empty String Protection | `events` | `CHECK (CHAR_LENGTH(TRIM(title)) > 0)` | Data quality degradation | Entity Integrity |
| Double Registration Prevention | `registrations` | `UNIQUE KEY uk_user_event (user_id, event_id)` | Duplicate seat reservation, overselling | CO4 Concurrency Protection |
| Cascading Deletion | `registrations` | `ON DELETE CASCADE` | Orphaned records | Referential Integrity |
| Outbox Message Integrity | `outbox_events` | `JSON` validation + `CHECK (status IN ('PENDING', 'PROCESSED', 'FAILED'))` | Broken asynchronous delivery | CO6 Distributed Decoupling |
