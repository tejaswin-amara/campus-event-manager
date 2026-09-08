-- ============================================================================
-- CampusConnect — SQL Fluency: Index Engineering & Optimization
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. PRIMARY & UNIQUE ENFORCEMENT INDEXES
-- Automatically created by InnoDB as clustered (PK) and unique secondary indexes.
-- ----------------------------------------------------------------------------
-- Clustered Index: events.PRIMARY on (id)
-- Clustered Index: users.PRIMARY on (id)
-- Clustered Index: registrations.PRIMARY on (id)
-- Unique Index: users.uk_users_username on (username)
-- Unique Index: users.uk_users_email on (email)
-- Unique Index: registrations.uk_user_event on (user_id, event_id)

-- ----------------------------------------------------------------------------
-- 2. QUERY-DRIVEN SECONDARY B-TREE INDEXES
-- Designed specifically to eliminate Full Table Scans (type: ALL) and filesorts.
-- ----------------------------------------------------------------------------

-- A. Chronological Timeline Index
-- Query Pattern: WHERE date_time >= NOW() ORDER BY date_time ASC
-- Selectivity: High. Allows index range scans instead of full table scans.
CREATE INDEX idx_events_date_time
    ON events (date_time);

-- B. Composite Category + Chronological Index
-- Query Pattern: WHERE category = 'Technical' AND date_time >= NOW() ORDER BY date_time ASC
-- Optimization Rule: Leftmost Prefix. Matches both `category` alone AND `(category, date_time)`.
CREATE INDEX idx_events_category_date_time
    ON events (category, date_time);

-- C. Composite Status + Chronological Index
-- Query Pattern: WHERE status = 'PUBLISHED' AND date_time >= NOW()
-- Eliminates cancelled and draft events early in the B-tree traversal.
CREATE INDEX idx_events_status_date_time
    ON events (status, date_time);

-- D. Event Attendee Status Index
-- Query Pattern: WHERE event_id = 6 AND status = 'CONFIRMED'
-- Speeds up capacity validation and organizer attendee roster generation.
CREATE INDEX idx_registrations_event_status
    ON registrations (event_id, status);

-- E. Student Portal History Index
-- Query Pattern: WHERE user_id = 2 AND status = 'INTERESTED'
-- Eliminates N+1 query overhead when rendering student dashboard.
CREATE INDEX idx_registrations_user_status
    ON registrations (user_id, status);

-- F. Outbox Poller Index (CO6 Distributed Architecture)
-- Query Pattern: WHERE status = 'PENDING' ORDER BY created_at ASC
CREATE INDEX idx_outbox_status_created
    ON outbox_events (status, created_at);

-- ----------------------------------------------------------------------------
-- 3. INDEX MAINTENANCE & SELECTIVITY INSPECTION QUERIES
-- Purpose: Enable DBA to inspect index cardinality and fragmentation.
-- ----------------------------------------------------------------------------
SHOW INDEX FROM events;
SHOW INDEX FROM registrations;
SHOW INDEX FROM users;

-- Inspect index statistics from information_schema
SELECT
    table_name,
    index_name,
    seq_in_index,
    column_name,
    cardinality,
    nullable
FROM information_schema.statistics
WHERE table_schema = 'campus_events'
ORDER BY table_name, index_name, seq_in_index;
