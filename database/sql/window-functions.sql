-- ============================================================================
-- CampusConnect — SQL Fluency: Analytical Window Functions
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. ROW_NUMBER(): EVENT SEQUENCE WITHIN CATEGORY
-- Purpose: Number events chronologically within each category partition.
-- Context: Event catalog pagination and category-specific scheduling.
-- ----------------------------------------------------------------------------
SELECT
    e.category,
    ROW_NUMBER() OVER (
        PARTITION BY e.category
        ORDER BY e.date_time ASC
    ) AS category_sequence_num,
    e.id AS event_id,
    e.title AS event_title,
    e.date_time AS scheduled_date,
    e.venue
FROM events e
WHERE e.status = 'PUBLISHED'
ORDER BY e.category ASC, category_sequence_num ASC;

-- ----------------------------------------------------------------------------
-- 2. RANK() VS DENSE_RANK(): EVENT POPULARITY LEADERBOARD
-- Purpose: Rank campus events based on student enrollment demand.
-- Demonstration: Illustrates behavior when two events tie in registration count
-- (RANK leaves a gap; DENSE_RANK assigns consecutive integers).
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.category,
    COUNT(r.id) AS total_registrations,
    RANK() OVER (
        ORDER BY COUNT(r.id) DESC
    ) AS standard_rank,
    DENSE_RANK() OVER (
        ORDER BY COUNT(r.id) DESC
    ) AS dense_popularity_rank
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id AND r.status IN ('INTERESTED', 'CONFIRMED')
WHERE e.status = 'PUBLISHED'
GROUP BY e.id, e.title, e.category
ORDER BY dense_popularity_rank ASC;

-- ----------------------------------------------------------------------------
-- 3. LAG() & LEAD(): INTER-EVENT SCHEDULING GAP ANALYSIS
-- Purpose: For each event in a category, compute:
--   LAG: Elapsed days since the previous event in the same category
--   LEAD: Days remaining until the next scheduled event in the same category
-- Context: Venue operations team identifying scheduling clusters vs scheduling droughts.
-- ----------------------------------------------------------------------------
SELECT
    e.category,
    e.title AS event_title,
    e.date_time AS current_event_date,
    LAG(e.date_time, 1) OVER (
        PARTITION BY e.category
        ORDER BY e.date_time ASC
    ) AS previous_event_date,
    DATEDIFF(
        e.date_time,
        LAG(e.date_time, 1) OVER (
            PARTITION BY e.category
            ORDER BY e.date_time ASC
        )
    ) AS days_since_last_event,
    LEAD(e.date_time, 1) OVER (
        PARTITION BY e.category
        ORDER BY e.date_time ASC
    ) AS next_event_date,
    DATEDIFF(
        LEAD(e.date_time, 1) OVER (
            PARTITION BY e.category
            ORDER BY e.date_time ASC
        ),
        e.date_time
    ) AS days_until_next_event
FROM events e
WHERE e.status = 'PUBLISHED'
ORDER BY e.category ASC, e.date_time ASC;

-- ----------------------------------------------------------------------------
-- 4. RUNNING TOTAL (CUMULATIVE REGISTRATIONS OVER TIME)
-- Purpose: Track the cumulative timeline of student interest over time.
-- ----------------------------------------------------------------------------
SELECT
    r.id AS registration_id,
    r.registration_date,
    u.username AS student_name,
    e.title AS event_title,
    COUNT(r.id) OVER (
        ORDER BY r.registration_date ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_campus_registrations
FROM registrations r
JOIN users u ON r.user_id = u.id
JOIN events e ON r.event_id = e.id
ORDER BY r.registration_date ASC;
