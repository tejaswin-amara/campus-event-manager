-- ============================================================================
-- CampusConnect — SQL Fluency: Executive Campus Analytics Portfolio
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. CATEGORY DEMAND INDEX & MARKET SHARE
-- Purpose: Quantify which event genres attract the highest proportion of campus interest.
-- Context: University budget allocation and club sponsorship decisions.
-- ----------------------------------------------------------------------------
WITH CategoryMetrics AS (
    SELECT
        e.category,
        COUNT(DISTINCT e.id) AS event_count,
        COUNT(r.id) AS total_signups,
        COALESCE(SUM(e.max_capacity), 0) AS aggregate_capacity
    FROM events e
    LEFT JOIN registrations r ON e.id = r.event_id
    WHERE e.status = 'PUBLISHED'
    GROUP BY e.category
),
TotalMetrics AS (
    SELECT SUM(total_signups) AS grand_total_signups FROM CategoryMetrics
)
SELECT
    cm.category,
    cm.event_count,
    cm.total_signups,
    cm.aggregate_capacity,
    ROUND((cm.total_signups / NULLIF(tm.grand_total_signups, 0)) * 100, 2) AS demand_market_share_percent,
    ROUND((cm.total_signups / NULLIF(cm.event_count, 0)), 1) AS average_signups_per_event
FROM CategoryMetrics cm
CROSS JOIN TotalMetrics tm
ORDER BY cm.total_signups DESC;

-- ----------------------------------------------------------------------------
-- 2. CAPACITY UTILIZATION & WAITLIST PRESSURE METRIC
-- Purpose: Identify high-pressure events where student interest exceeds physical room capacity.
-- ----------------------------------------------------------------------------
SELECT
    e.id AS event_id,
    e.title AS event_title,
    e.venue,
    e.max_capacity,
    COUNT(CASE WHEN r.status = 'CONFIRMED' THEN 1 END) AS confirmed_count,
    COUNT(CASE WHEN r.status = 'WAITLISTED' THEN 1 END) AS waitlist_count,
    ROUND((COUNT(CASE WHEN r.status = 'CONFIRMED' THEN 1 END) / NULLIF(e.max_capacity, 0)) * 100, 1) AS confirmed_utilization_pct,
    CASE
        WHEN COUNT(CASE WHEN r.status = 'WAITLISTED' THEN 1 END) > 0 THEN 'OVER_SUBSCRIBED'
        WHEN COUNT(CASE WHEN r.status = 'CONFIRMED' THEN 1 END) >= e.max_capacity THEN 'AT_CAPACITY'
        WHEN (COUNT(CASE WHEN r.status = 'CONFIRMED' THEN 1 END) / NULLIF(e.max_capacity, 0)) >= 0.80 THEN 'HIGH_UTILIZATION'
        ELSE 'NORMAL'
    END AS enrollment_health
FROM events e
LEFT JOIN registrations r ON e.id = r.event_id
WHERE e.status = 'PUBLISHED'
GROUP BY e.id, e.title, e.venue, e.max_capacity
ORDER BY waitlist_count DESC, confirmed_utilization_pct DESC;

-- ----------------------------------------------------------------------------
-- 3. STUDENT ACTIVITY COHORT SEGMENTATION
-- Purpose: Categorize students into engagement cohorts (Super-Users, Active, Low, Dormant).
-- ----------------------------------------------------------------------------
WITH StudentActivity AS (
    SELECT
        u.id AS student_id,
        u.username,
        u.email,
        COUNT(r.id) AS activity_count,
        MAX(r.registration_date) AS most_recent_interaction
    FROM users u
    LEFT JOIN registrations r ON u.id = r.user_id
    WHERE u.role = 'STUDENT'
    GROUP BY u.id, u.username, u.email
)
SELECT
    student_id,
    username,
    email,
    activity_count,
    most_recent_interaction,
    CASE
        WHEN activity_count >= 5 THEN 'POWER_ATTENDEE'
        WHEN activity_count >= 2 THEN 'ACTIVE_STUDENT'
        WHEN activity_count = 1  THEN 'OCCASIONAL_VISITOR'
        ELSE 'DORMANT'
    END AS cohort_classification
FROM StudentActivity
ORDER BY activity_count DESC, username ASC;

-- ----------------------------------------------------------------------------
-- 4. VENUE UTILIZATION FREQUENCY
-- Purpose: Identify busiest campus facilities to avoid double-booking conflicts.
-- ----------------------------------------------------------------------------
SELECT
    e.venue AS facility_name,
    COUNT(e.id) AS hosted_events_count,
    COUNT(DISTINCT e.category) AS distinct_genres_hosted,
    MIN(e.date_time) AS earliest_scheduled,
    MAX(e.date_time) AS latest_scheduled
FROM events e
WHERE e.status <> 'CANCELLED'
GROUP BY e.venue
ORDER BY hosted_events_count DESC;

-- ----------------------------------------------------------------------------
-- 5. OUTBOX EVENT PIPELINE DIAGNOSTICS (CO6 OBSERVABILITY)
-- Purpose: Real-time health monitor of asynchronous event outbox dispatch.
-- Detects pending event backlogs and delivery failure rates.
-- ----------------------------------------------------------------------------
SELECT
    oe.status AS outbox_delivery_status,
    oe.event_type,
    COUNT(oe.id) AS event_count,
    MIN(oe.created_at) AS oldest_unprocessed_timestamp,
    MAX(oe.created_at) AS newest_event_timestamp
FROM outbox_events oe
GROUP BY oe.status, oe.event_type
ORDER BY oe.status ASC, event_count DESC;
