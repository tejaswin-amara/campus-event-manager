-- ============================================================================
-- CampusConnect — SQL Fluency: Relational Joins
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. INNER JOIN
-- Purpose: Match students with their registered events.
-- Context: Event check-in roster generation for organizers.
-- Invariant: Excludes users without registrations and events without attendees.
-- ----------------------------------------------------------------------------
SELECT
    r.id AS registration_id,
    u.id AS user_id,
    u.username AS student_username,
    u.email AS student_email,
    e.id AS event_id,
    e.title AS event_title,
    e.category AS event_category,
    r.registration_date AS registered_at,
    r.status AS enrollment_status
FROM registrations r
INNER JOIN users u ON r.user_id = u.id
INNER JOIN events e ON r.event_id = e.id
WHERE e.status = 'PUBLISHED'
ORDER BY e.date_time ASC, r.registration_date ASC;

-- ----------------------------------------------------------------------------
-- 2. LEFT OUTER JOIN
-- Purpose: Show ALL events in the catalog regardless of whether anyone registered.
-- Context: Admin catalog health audit to detect low-engagement events (0 signups).
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.category AS category,
    e.date_time AS scheduled_time,
    e.status AS event_status,
    COUNT(r.id) AS total_interested_students
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
GROUP BY
    e.id,
    e.title,
    e.category,
    e.date_time,
    e.status
ORDER BY total_interested_students ASC, e.date_time ASC;

-- ----------------------------------------------------------------------------
-- 3. RIGHT OUTER JOIN
-- Purpose: Identify all students in the database and their active registrations.
-- Context: Student engagement office finding passive students with zero activity.
-- ----------------------------------------------------------------------------
SELECT
    u.id AS student_id,
    u.username AS student_name,
    u.email AS student_email,
    e.title AS registered_event_title,
    r.status AS registration_status
FROM registrations r
RIGHT JOIN users u ON r.user_id = u.id
LEFT JOIN events e ON r.event_id = e.id
WHERE u.role = 'STUDENT'
ORDER BY u.id ASC;

-- ----------------------------------------------------------------------------
-- 4. FULL OUTER JOIN (ACADEMIC DEMONSTRATION & ENGINE COMPARISON)
-- Purpose: Comprehensive audit of all users and all events simultaneously,
-- showing matched pairs, un-registered students, and events with no signups.
--
-- Dialect Note:
-- MySQL 8.4 does not support the native FULL OUTER JOIN syntax.
-- Standard SQL pattern: LEFT JOIN combined with RIGHT JOIN via UNION.
-- ----------------------------------------------------------------------------

-- MySQL 8.4 Implementation (Emulated via UNION):
SELECT
    u.username AS student_name,
    r.status AS reg_status,
    e.title AS event_title
FROM users u
LEFT JOIN registrations r ON u.id = r.user_id
LEFT JOIN events e ON r.event_id = e.id

UNION

SELECT
    u.username AS student_name,
    r.status AS reg_status,
    e.title AS event_title
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
LEFT JOIN users u ON r.user_id = u.id;

-- PostgreSQL 16 Native Syntax:
-- SELECT
--     u.username AS student_name,
--     r.status AS reg_status,
--     e.title AS event_title
-- FROM users u
-- FULL OUTER JOIN registrations r ON u.id = r.user_id
-- FULL OUTER JOIN events e ON r.event_id = e.id;
