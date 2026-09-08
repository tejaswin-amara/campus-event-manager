-- ============================================================================
-- CampusConnect — SQL Fluency: Data Manipulation Language (DML)
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. SINGLE-ROW INSERT
-- Purpose: Admin registers a new flagship technical symposium.
-- Invariant: Preserves check constraints on capacity and future end_date_time.
-- ----------------------------------------------------------------------------
INSERT INTO events (
    title,
    description,
    date_time,
    end_date_time,
    venue,
    category,
    status,
    registration_link,
    max_capacity,
    image_url
) VALUES (
    'Cloud Native Summit 2026',
    'Deep dive into Kubernetes, service meshes, and distributed database sharding patterns.',
    '2026-10-15 09:30:00',
    '2026-10-15 17:30:00',
    'APJ Abdul Kalam Auditorium',
    'Technical',
    'PUBLISHED',
    'https://forms.campus.edu/cloud2026',
    150,
    '/images/cloud-summit.jpg'
);

-- ----------------------------------------------------------------------------
-- 2. MULTI-ROW INSERT (BATCH INGESTION)
-- Purpose: Bulk student onboarding during orientation semester.
-- Benefit: Minimizes round-trip network latency and transaction log commits.
-- ----------------------------------------------------------------------------
INSERT INTO users (username, password, role, email) VALUES
('siddharth_m', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'siddharth.m@campus.edu'),
('sneha_rao',   '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'sneha.r@campus.edu'),
('tanya_sen',   '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'tanya.s@campus.edu')
ON DUPLICATE KEY UPDATE email = VALUES(email);

-- PostgreSQL 16 Equivalent:
-- INSERT INTO users (username, password, role, email) VALUES (...)
-- ON CONFLICT (username) DO UPDATE SET email = EXCLUDED.email;

-- ----------------------------------------------------------------------------
-- 3. CONDITIONAL UPDATE (LIFECYCLE STATE TRANSITIONS)
-- Purpose: Event organizer marks an ongoing workshop as COMPLETED.
-- Precondition: Only currently PUBLISHED events whose end_date_time has elapsed.
-- ----------------------------------------------------------------------------
UPDATE events e
SET e.status = 'COMPLETED'
WHERE e.status = 'PUBLISHED'
  AND e.end_date_time IS NOT NULL
  AND e.end_date_time < NOW();

-- ----------------------------------------------------------------------------
-- 4. CONDITIONAL REGISTRATION STATUS UPDATE
-- Purpose: Promote waitlisted students to confirmed status when capacity expands.
-- ----------------------------------------------------------------------------
UPDATE registrations r
JOIN events e ON r.event_id = e.id
SET r.status = 'CONFIRMED'
WHERE r.status = 'WAITLISTED'
  AND e.id = 6
  AND (
      SELECT COUNT(*)
      FROM (SELECT * FROM registrations) AS sub
      WHERE sub.event_id = 6 AND sub.status = 'CONFIRMED'
  ) < e.max_capacity;

-- ----------------------------------------------------------------------------
-- 5. SAFE CASCADING DELETE
-- Purpose: Administrative removal of an obsolete event.
-- Behavior: Foreign key constraints (ON DELETE CASCADE) ensure all associated
-- registration records are purged atomically, preventing orphaned records.
-- ----------------------------------------------------------------------------
DELETE FROM events
WHERE id = 12
  AND status = 'CANCELLED';
