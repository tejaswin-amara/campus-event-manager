-- ============================================================================
-- CampusConnect — SQL Fluency: Aggregations & Grouped Analytics
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. BASIC AGGREGATIONS (COUNT, SUM, AVG, MIN, MAX)
-- Purpose: University executive event portfolio summary.
-- ----------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_events_catalogued,
    COUNT(CASE WHEN e.status = 'PUBLISHED' THEN 1 END) AS active_events,
    SUM(e.max_capacity) AS total_campus_seating_capacity,
    ROUND(AVG(e.max_capacity), 1) AS average_event_capacity,
    MIN(e.max_capacity) AS smallest_capacity,
    MAX(e.max_capacity) AS largest_capacity
FROM events e
WHERE e.status <> 'CANCELLED';

-- ----------------------------------------------------------------------------
-- 2. GROUP BY WITH MULTIPLE DIMENSIONS
-- Purpose: Category and status distribution analysis.
-- Context: Admin dashboard metric cards.
-- ----------------------------------------------------------------------------
SELECT
    e.category AS event_category,
    e.status AS lifecycle_state,
    COUNT(e.id) AS event_count,
    COALESCE(SUM(e.max_capacity), 0) AS aggregate_capacity
FROM events e
GROUP BY e.category, e.status
ORDER BY e.category ASC, event_count DESC;

-- ----------------------------------------------------------------------------
-- 3. HAVING CLAUSE (FILTERING ON AGGREGATE VALUES)
-- Purpose: Identify high-demand categories where average capacity exceeds 100
-- and at least 2 events are offered.
-- ----------------------------------------------------------------------------
SELECT
    e.category AS popular_category,
    COUNT(e.id) AS total_events,
    ROUND(AVG(e.max_capacity), 1) AS avg_capacity,
    COUNT(r.id) AS total_registrations
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
GROUP BY e.category
HAVING COUNT(e.id) >= 2
   AND AVG(e.max_capacity) > 100
ORDER BY total_registrations DESC;

-- ----------------------------------------------------------------------------
-- 4. PIVOTED / CONDITIONAL AGGREGATIONS (SINGLE-SCAN DASHBOARD QUERY)
-- Purpose: Consolidate 4 separate dashboard count queries into 1 single-pass scan.
-- Performance: Eliminates multiple round trips and table re-scans (CO5 optimization).
-- ----------------------------------------------------------------------------
SELECT
    COUNT(*) AS total_events,
    COUNT(CASE WHEN e.date_time > NOW() THEN 1 END) AS upcoming_count,
    COUNT(CASE WHEN e.date_time <= NOW() AND (e.end_date_time IS NULL OR e.end_date_time > NOW()) THEN 1 END) AS ongoing_count,
    COUNT(CASE WHEN (e.end_date_time IS NOT NULL AND e.end_date_time < NOW()) OR (e.end_date_time IS NULL AND e.date_time < NOW()) THEN 1 END) AS past_count,
    COUNT(CASE WHEN e.status = 'CANCELLED' THEN 1 END) AS cancelled_count
FROM events e;

-- ----------------------------------------------------------------------------
-- 5. REGISTRATION STATUS ENROLLMENT MATRIX PER EVENT
-- Purpose: Breakdown of student registration states (Interested, Confirmed, Waitlisted).
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.max_capacity,
    COUNT(CASE WHEN r.status = 'CONFIRMED' THEN 1 END) AS confirmed_count,
    COUNT(CASE WHEN r.status = 'INTERESTED' THEN 1 END) AS interested_count,
    COUNT(CASE WHEN r.status = 'WAITLISTED' THEN 1 END) AS waitlisted_count,
    COUNT(CASE WHEN r.status = 'CANCELLED' THEN 1 END) AS user_cancelled_count
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
WHERE e.status = 'PUBLISHED'
GROUP BY e.id, e.title, e.max_capacity
ORDER BY confirmed_count DESC, interested_count DESC;
