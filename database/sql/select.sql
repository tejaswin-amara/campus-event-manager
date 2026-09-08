-- ============================================================================
-- CampusConnect — SQL Fluency: SELECT Queries & Data Retrieval
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. CLEAN PROJECTION & FILTERING (UPCOMING ACTIVE EVENTS)
-- Purpose: Retrieve essential event details for student exploration catalog.
-- Best Practice: Strict column projection (never SELECT *) prevents unnecessary
-- memory bloat and enables future covering index scans (CO5).
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.category AS event_category,
    e.venue AS event_venue,
    e.date_time AS start_time,
    e.end_date_time AS end_time,
    e.max_capacity AS capacity,
    e.status AS lifecycle_status
FROM events e
WHERE e.status = 'PUBLISHED'
  AND e.date_time >= NOW()
ORDER BY e.date_time ASC;

-- ----------------------------------------------------------------------------
-- 2. PATTERN MATCHING & CATEGORY SEARCH
-- Purpose: Full-text case-insensitive discovery across title and venue.
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.category AS event_category,
    e.venue AS event_venue,
    e.date_time AS event_date
FROM events e
WHERE e.status = 'PUBLISHED'
  AND (
      LOWER(e.title) LIKE LOWER('%hackathon%')
      OR LOWER(e.venue) LIKE LOWER('%auditorium%')
  )
ORDER BY e.date_time DESC;

-- ----------------------------------------------------------------------------
-- 3. USER REGISTRATION STATUS AUDIT
-- Purpose: Retrieve student profile with distinct registration activity.
-- ----------------------------------------------------------------------------
SELECT
    u.id AS user_id,
    u.username AS student_username,
    u.email AS contact_email,
    u.role AS user_role
FROM users u
WHERE u.role = 'STUDENT'
  AND u.email IS NOT NULL
ORDER BY u.username ASC;

-- ----------------------------------------------------------------------------
-- 4. DEMONSTRATION: WHY "SELECT *" IS AN ANTIPATTERN (ACADEMIC EVIDENCE)
-- ----------------------------------------------------------------------------
-- POOR DESIGN (Anti-pattern):
-- SELECT * FROM events WHERE category = 'Technical';
-- FLAWS:
-- 1. Transmits `image_data` (MEDIUMBLOB, up to 16MB) over JDBC socket even if
--    the caller only needs the event title and date.
-- 2. Prevents the MySQL query optimizer from using Index-Only Scans (Using index).
-- 3. Breaks downstream ORM mappings if new columns are added without migration sync.

-- PERFORMANT DESIGN (Optimized):
SELECT
    e.id,
    e.title,
    e.date_time,
    e.venue
FROM events e
WHERE e.category = 'Technical';
