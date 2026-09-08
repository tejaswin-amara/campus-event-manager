-- ============================================================================
-- CampusConnect — SQL Fluency: Subqueries & Nested Evaluations
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. SCALAR SUBQUERY
-- Purpose: Find all events whose capacity exceeds the campus-wide average.
-- Context: Resource allocation for high-capacity venue logistics.
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.category,
    e.venue,
    e.max_capacity,
    ROUND((SELECT AVG(sub.max_capacity) FROM events sub WHERE sub.status = 'PUBLISHED'), 1) AS campus_avg_capacity
FROM events e
WHERE e.status = 'PUBLISHED'
  AND e.max_capacity > (
      SELECT AVG(sub.max_capacity)
      FROM events sub
      WHERE sub.status = 'PUBLISHED'
  )
ORDER BY e.max_capacity DESC;

-- ----------------------------------------------------------------------------
-- 2. IN SUBQUERY
-- Purpose: Identify all students enrolled in at least one 'Technical' event.
-- ----------------------------------------------------------------------------
SELECT
    u.id AS student_id,
    u.username AS student_username,
    u.email AS contact_email
FROM users u
WHERE u.id IN (
    SELECT r.user_id
    FROM registrations r
    JOIN events e ON r.event_id = e.id
    WHERE e.category = 'Technical'
      AND r.status IN ('INTERESTED', 'CONFIRMED')
)
ORDER BY u.username ASC;

-- ----------------------------------------------------------------------------
-- 3. EXISTS SUBQUERY
-- Purpose: Find events that have at least one active student registration.
-- Performance: EXISTS short-circuits on the first matching index record, avoiding
-- full table join materialization.
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.category AS event_category,
    e.date_time AS scheduled_date
FROM events e
WHERE e.status = 'PUBLISHED'
  AND EXISTS (
      SELECT 1
      FROM registrations r
      WHERE r.event_id = e.id
        AND r.status IN ('CONFIRMED', 'INTERESTED')
  )
ORDER BY e.date_time ASC;

-- ----------------------------------------------------------------------------
-- 4. NOT EXISTS SUBQUERY
-- Purpose: Identify events with zero registered students (cold events).
-- Context: Automated notification to event organizers to boost promotional outreach.
-- ----------------------------------------------------------------------------
SELECT
    e.id AS cold_event_id,
    e.title AS cold_event_title,
    e.category AS category,
    e.venue,
    e.date_time
FROM events e
WHERE e.status = 'PUBLISHED'
  AND NOT EXISTS (
      SELECT 1
      FROM registrations r
      WHERE r.event_id = e.id
  )
ORDER BY e.date_time ASC;

-- ----------------------------------------------------------------------------
-- 5. CORRELATED SUBQUERY
-- Purpose: For each user, calculate their registration count and compare it to
-- the global student average.
-- ----------------------------------------------------------------------------
SELECT
    u.id AS user_id,
    u.username,
    u.email,
    (
        SELECT COUNT(r.id)
        FROM registrations r
        WHERE r.user_id = u.id
    ) AS user_registration_count,
    CASE
        WHEN (SELECT COUNT(r.id) FROM registrations r WHERE r.user_id = u.id) >= 3 THEN 'HIGHLY_ENGAGED'
        WHEN (SELECT COUNT(r.id) FROM registrations r WHERE r.user_id = u.id) > 0  THEN 'MODERATELY_ENGAGED'
        ELSE 'INACTIVE'
    END AS engagement_tier
FROM users u
WHERE u.role = 'STUDENT'
ORDER BY user_registration_count DESC;
