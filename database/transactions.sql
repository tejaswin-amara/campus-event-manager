-- ============================================================================
-- CampusConnect — SQL Fluency: Transaction Control & ACID Execution
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. ISOLATION LEVEL CONFIGURATION
-- CampusConnect standard isolation: REPEATABLE READ
-- InnoDB guarantees repeatable reads within the transaction snapshot via MVCC,
-- and prevents phantom rows in range scans via Next-Key locking.
-- ----------------------------------------------------------------------------
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- ----------------------------------------------------------------------------
-- 2. SCENARIO A: ATOMIC REGISTRATION WITH PESSIMISTIC ROW LOCKING
-- Purpose: Complete registration sequence ensuring capacity is not exceeded.
-- Invariant: If capacity is full, rollback immediately; otherwise record interest.
-- ----------------------------------------------------------------------------
START TRANSACTION;

-- Step 1: Read and acquire exclusive row lock (X-Lock) on event to serialize capacity checks
SELECT id, title, max_capacity, status
FROM events
WHERE id = 6
FOR UPDATE;

-- Step 2: Verify current confirmed count under lock
SELECT COUNT(*) INTO @current_attendees
FROM registrations
WHERE event_id = 6 AND status = 'CONFIRMED';

-- Step 3: Insert registration record
INSERT INTO registrations (registration_date, status, user_id, event_id)
VALUES (NOW(), 'CONFIRMED', 10, 6);

-- Step 4: Write Outbox event in the EXACT SAME local transaction (CO6 atomicity)
INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, payload, status)
VALUES (
    'REGISTRATION',
    LAST_INSERT_ID(),
    'STUDENT_CONFIRMED',
    JSON_OBJECT('eventId', 6, 'userId', 10, 'status', 'CONFIRMED', 'timestamp', NOW()),
    'PENDING'
);

COMMIT;

-- ----------------------------------------------------------------------------
-- 3. SCENARIO B: SAVEPOINT & PARTIAL ROLLBACK (SAFE RETRY)
-- Purpose: Attempt primary registration; if secondary notification fails,
-- roll back to savepoint without aborting the core registration.
-- ----------------------------------------------------------------------------
START TRANSACTION;

-- Core business mutation
INSERT INTO registrations (registration_date, status, user_id, event_id)
VALUES (NOW(), 'INTERESTED', 5, 4);

-- Set intermediate transaction savepoint
SAVEPOINT RegistrationCreated;

-- Attempt secondary experimental outbox entry with deliberate syntax/domain check
-- If a failure occurs in an auxiliary task:
-- ROLLBACK TO SAVEPOINT RegistrationCreated;
-- Then the core registration record remains safe!

RELEASE SAVEPOINT RegistrationCreated;
COMMIT;

-- ----------------------------------------------------------------------------
-- 4. SCENARIO C: FULL ROLLBACK ON INVARIANT VIOLATION
-- Purpose: Demonstrate complete abort on failure to preserve relational consistency.
-- ----------------------------------------------------------------------------
START TRANSACTION;

-- Step 1: Attempt to register for a cancelled event
INSERT INTO registrations (registration_date, status, user_id, event_id)
VALUES (NOW(), 'INTERESTED', 2, 12);

-- Step 2: Validation check reveals event is CANCELLED
SELECT status INTO @event_state FROM events WHERE id = 12;

-- Step 3: Condition failed — issue explicit rollback
ROLLBACK;
-- Post-condition: Database state is completely unchanged.
