-- ============================================================================
-- CampusConnect — SQL Fluency: Common Table Expressions (CTE)
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. SINGLE CTE: EVENT REGISTRATION DENSITY ANALYSIS
-- Purpose: Compute registration counts per event and identify over-subscribed events.
-- ----------------------------------------------------------------------------
WITH EventRegistrationCounts AS (
    SELECT
        e.id AS event_id,
        e.title AS event_title,
        e.category AS category,
        e.max_capacity AS capacity,
        COUNT(r.id) AS confirmed_attendees
    FROM events e
    LEFT JOIN registrations r ON e.id = r.event_id AND r.status = 'CONFIRMED'
    WHERE e.status = 'PUBLISHED'
    GROUP BY e.id, e.title, e.category, e.max_capacity
)
SELECT
    event_id,
    event_title,
    category,
    capacity,
    confirmed_attendees,
    ROUND((confirmed_attendees / NULLIF(capacity, 0)) * 100, 1) AS occupancy_percentage,
    CASE
        WHEN confirmed_attendees >= capacity THEN 'AT_CAPACITY'
        WHEN (confirmed_attendees / NULLIF(capacity, 0)) >= 0.75 THEN 'NEAR_CAPACITY'
        ELSE 'SEATS_AVAILABLE'
    END AS capacity_status
FROM EventRegistrationCounts
ORDER BY occupancy_percentage DESC;

-- ----------------------------------------------------------------------------
-- 2. MULTI-CTE PIPELINE: UNIVERSITY STUDENT ENGAGEMENT INDEX
-- Purpose: Multi-stage data pipeline calculating user registration velocity,
-- filtering out inactive students, and computing departmental percentiles.
-- ----------------------------------------------------------------------------
WITH
-- Stage 1: Aggregate registrations per student
StudentRegistrations AS (
    SELECT
        u.id AS student_id,
        u.username,
        u.email,
        COUNT(r.id) AS total_registrations,
        COUNT(CASE WHEN r.status = 'CONFIRMED' THEN 1 END) AS confirmed_registrations
    FROM users u
    LEFT JOIN registrations r ON u.id = r.user_id
    WHERE u.role = 'STUDENT'
    GROUP BY u.id, u.username, u.email
),
-- Stage 2: Calculate engagement statistics
EngagementMetrics AS (
    SELECT
        AVG(total_registrations) AS avg_regs,
        MAX(total_registrations) AS max_regs
    FROM StudentRegistrations
)
-- Stage 3: Project student leaderboard relative to campus baseline
SELECT
    sr.student_id,
    sr.username,
    sr.email,
    sr.total_registrations,
    sr.confirmed_registrations,
    ROUND(em.avg_regs, 2) AS campus_average_regs,
    ROUND((sr.total_registrations - em.avg_regs), 2) AS delta_from_average
FROM StudentRegistrations sr
CROSS JOIN EngagementMetrics em
WHERE sr.total_registrations > 0
ORDER BY sr.total_registrations DESC, sr.username ASC;
