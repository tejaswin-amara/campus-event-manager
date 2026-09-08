# CampusConnect — Entity-Relationship (ER) Architecture (CO2)

This document specifies the conceptual and logical data model for **CampusConnect** (Course 25CS1302E).

---

## 1. Formal Entity-Relationship Diagram (Mermaid)

```mermaid
erDiagram
    USERS ||--o{ REGISTRATIONS : "places / registers (1:N)"
    EVENTS ||--o{ REGISTRATIONS : "receives (1:N)"
    EVENTS ||--o{ OUTBOX_EVENTS : "emits domain events (1:N)"

    USERS {
        bigint id PK "Autoincrement Primary Key"
        varchar_50 username UK "Unique student/admin handle"
        varchar_255 password "BCrypt hashed credential"
        varchar_20 role "Domain: ADMIN, STUDENT, ORGANIZER"
        varchar_254 email UK "Nullable unique institutional email"
        datetime created_at "Audit creation timestamp"
    }

    EVENTS {
        bigint id PK "Autoincrement Primary Key"
        varchar_255 title "Event Title (non-empty)"
        text description "Markdown/text event description"
        datetime date_time "Event start timestamp"
        datetime end_date_time "Event conclusion (end > start)"
        varchar_255 venue "Physical campus room / hall"
        varchar_50 category "Domain: Technical, Cultural, Sports..."
        varchar_20 status "Lifecycle: DRAFT, PUBLISHED, CANCELLED, COMPLETED"
        varchar_1000 registration_link "External authoritative URL"
        int max_capacity "Seating capacity limit (> 0)"
        varchar_1000 image_url "Thumbnail image URI"
        varchar_1000 responses_link "Admin feedback spreadsheet URL"
        mediumblob image_data "Binary image payload"
        varchar_255 image_mime_type "MIME header: image/png, image/jpeg"
    }

    REGISTRATIONS {
        bigint id PK "Autoincrement Primary Key"
        datetime registration_date "Timestamp of interest recording"
        varchar_20 status "State: INTERESTED, CONFIRMED, WAITLISTED, CANCELLED"
        bigint user_id FK "References USERS(id) ON DELETE CASCADE"
        bigint event_id FK "References EVENTS(id) ON DELETE CASCADE"
    }

    OUTBOX_EVENTS {
        bigint id PK "Autoincrement Primary Key"
        varchar_50 aggregate_type "Entity name: EVENT, REGISTRATION"
        varchar_100 aggregate_id "Identifier of mutated entity"
        varchar_50 event_type "Action: STUDENT_REGISTERED, EVENT_PUBLISHED"
        json payload "Complete event payload"
        datetime created_at "Timestamp of transaction commit"
        datetime processed_at "Timestamp dispatched by outbox poller"
        varchar_20 status "State: PENDING, PROCESSED, FAILED"
    }
```

---

## 2. Structural Characteristics & Invariants

### A. Cardinality and Multiplicity
- **USERS to REGISTRATIONS**: $1:N$ (One user can register for zero, one, or multiple events).
- **EVENTS to REGISTRATIONS**: $1:N$ (One event can receive zero, one, or many student registrations).
- **USERS to EVENTS**: $M:N$ (Resolved into two $1:N$ relationships via the `REGISTRATIONS` associative junction entity).
- **EVENTS to OUTBOX_EVENTS**: $1:N$ (An event modification produces one or more asynchronous outbox events).

### B. Participation Constraints
| Entity | Relationship | Participation | Rationale |
|---|---|---|---|
| **USERS** | `REGISTRATIONS` | **Partial** | A user can register on the platform without immediately signing up for an event. |
| **EVENTS** | `REGISTRATIONS` | **Partial** | Newly published events initially have zero registered students. |
| **REGISTRATIONS** | `USERS` | **Total (Mandatory)** | A registration record cannot exist without a valid associated `user_id` ($FK \to users.id$). |
| **REGISTRATIONS** | `EVENTS` | **Total (Mandatory)** | A registration record cannot exist without a valid associated `event_id` ($FK \to events.id$). |

### C. Candidate Keys & Integrity Constraints
1. **USERS**:
   - **Primary Key**: `id`
   - **Alternate Candidate Keys**: `username`, `email`
   - **Domain Constraint**: `role IN ('ADMIN', 'STUDENT', 'ORGANIZER')`
2. **EVENTS**:
   - **Primary Key**: `id`
   - **Domain Constraints**:
     - `max_capacity IS NULL OR max_capacity > 0`
     - `end_date_time IS NULL OR end_date_time > date_time`
     - `status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED')`
     - `CHAR_LENGTH(TRIM(title)) > 0`
     - `CHAR_LENGTH(TRIM(venue)) > 0`
3. **REGISTRATIONS**:
   - **Primary Key**: `id`
   - **Candidate Key / Unique Invariant**: `(user_id, event_id)` via `CONSTRAINT uk_user_event UNIQUE (user_id, event_id)`
   - **Referential Integrity**: Cascading deletion ensures zero orphaned junction records when a parent user or event is purged.
   - **Domain Constraint**: `status IN ('INTERESTED', 'CONFIRMED', 'CANCELLED', 'WAITLISTED')`
4. **OUTBOX_EVENTS**:
   - **Primary Key**: `id`
   - **Domain Constraint**: `status IN ('PENDING', 'PROCESSED', 'FAILED')`
