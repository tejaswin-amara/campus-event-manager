-- V4__Hardening_and_audit.sql
-- CampusConnect DBMS/PBL Hardening: Lifecycle states, check constraints, and transactional outbox

-- 1. Add status column with lifecycle constraints to events
ALTER TABLE events
    ADD COLUMN status VARCHAR(20) DEFAULT 'PUBLISHED' NOT NULL;

ALTER TABLE events
    ADD CONSTRAINT chk_event_status
    CHECK (status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED'));

-- 2. Domain check constraints: Ensure non-empty strings for critical event attributes
ALTER TABLE events
    ADD CONSTRAINT chk_event_title_nonempty
    CHECK (CHAR_LENGTH(TRIM(title)) > 0);

ALTER TABLE events
    ADD CONSTRAINT chk_event_venue_nonempty
    CHECK (CHAR_LENGTH(TRIM(venue)) > 0);

-- 3. High-selectivity composite index for status and event chronology
CREATE INDEX idx_events_status_date_time ON events (status, date_time);

-- 4. Transactional Outbox table for reliable distributed event propagation (CO6)
CREATE TABLE IF NOT EXISTS outbox_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    payload JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT chk_outbox_status CHECK (status IN ('PENDING', 'PROCESSED', 'FAILED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_outbox_status_created ON outbox_events (status, created_at);
