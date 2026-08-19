-- V3__Add_event_query_indexes_and_integrity_checks.sql
-- Supports CO1 evidence: normalized relational design, constraints, and query-aware indexing.

CREATE INDEX idx_events_date_time ON events (date_time);
CREATE INDEX idx_events_category_date_time ON events (category, date_time);
CREATE INDEX idx_registrations_event_status ON registrations (event_id, status);
CREATE INDEX idx_registrations_user_status ON registrations (user_id, status);

ALTER TABLE events
    ADD CONSTRAINT chk_event_end_after_start
    CHECK (end_date_time IS NULL OR end_date_time > date_time);

ALTER TABLE registrations
    ADD CONSTRAINT chk_registration_status
    CHECK (status IN ('INTERESTED', 'CONFIRMED', 'CANCELLED', 'WAITLISTED'));
