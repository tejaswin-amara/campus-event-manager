-- ============================================================================
-- CampusConnect — Master Relational Database Schema
-- Academic Subject: 25CS1302E Database Systems Engineering & Distributed Backend
-- Target Database: MySQL 8.4 LTS (InnoDB Engine)
-- Cross-Compatibility: Annotated with PostgreSQL 16 Equivalents
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. DATABASE INITIALIZATION
-- ----------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS campus_events
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE campus_events;

-- PostgreSQL 16 Equivalent:
-- CREATE DATABASE campus_events WITH ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8';

-- ----------------------------------------------------------------------------
-- 2. USERS TABLE
-- Stores authenticated actors (STUDENT, ORGANIZER, ADMIN) with bcrypt credentials.
-- Candidate Keys: (id), (username), (email)
-- Primary Key: id
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    email VARCHAR(254) NULL,
    CONSTRAINT uk_users_username UNIQUE (username),
    CONSTRAINT uk_users_email UNIQUE (email),
    CONSTRAINT chk_users_role CHECK (role IN ('ADMIN', 'STUDENT', 'ORGANIZER')),
    CONSTRAINT chk_users_username_nonempty CHECK (CHAR_LENGTH(TRIM(username)) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- PostgreSQL 16 Equivalent:
-- CREATE TABLE users (
--     id BIGSERIAL PRIMARY KEY,
--     username VARCHAR(50) NOT NULL UNIQUE,
--     password VARCHAR(255) NOT NULL,
--     role VARCHAR(20) NOT NULL CHECK (role IN ('ADMIN', 'STUDENT', 'ORGANIZER')),
--     email VARCHAR(254) UNIQUE,
--     CONSTRAINT chk_users_username_nonempty CHECK (LENGTH(TRIM(username)) > 0)
-- );

-- ----------------------------------------------------------------------------
-- 3. EVENTS TABLE
-- Stores campus event catalog, metadata, lifecycle states, and media blobs.
-- Primary Key: id
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    date_time DATETIME NOT NULL,
    end_date_time DATETIME NULL,
    venue VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'PUBLISHED' NOT NULL,
    registration_link VARCHAR(1000) NULL,
    max_capacity INT NULL,
    image_url VARCHAR(1000) NULL,
    responses_link VARCHAR(1000) NULL,
    image_data MEDIUMBLOB NULL,
    image_mime_type VARCHAR(255) NULL,
    CONSTRAINT chk_events_max_capacity_positive CHECK (max_capacity IS NULL OR max_capacity > 0),
    CONSTRAINT chk_events_end_after_start CHECK (end_date_time IS NULL OR end_date_time > date_time),
    CONSTRAINT chk_events_status CHECK (status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED')),
    CONSTRAINT chk_events_title_nonempty CHECK (CHAR_LENGTH(TRIM(title)) > 0),
    CONSTRAINT chk_events_venue_nonempty CHECK (CHAR_LENGTH(TRIM(venue)) > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- PostgreSQL 16 Equivalent:
-- CREATE TABLE events (
--     id BIGSERIAL PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     description TEXT,
--     date_time TIMESTAMPTZ NOT NULL,
--     end_date_time TIMESTAMPTZ,
--     venue VARCHAR(255) NOT NULL,
--     category VARCHAR(50) NOT NULL,
--     status VARCHAR(20) DEFAULT 'PUBLISHED' NOT NULL CHECK (status IN ('DRAFT', 'PUBLISHED', 'CANCELLED', 'COMPLETED')),
--     registration_link VARCHAR(1000),
--     max_capacity INT CHECK (max_capacity IS NULL OR max_capacity > 0),
--     image_url VARCHAR(1000),
--     responses_link VARCHAR(1000),
--     image_data BYTEA,
--     image_mime_type VARCHAR(255),
--     CONSTRAINT chk_events_end_after_start CHECK (end_date_time IS NULL OR end_date_time > date_time),
--     CONSTRAINT chk_events_title_nonempty CHECK (LENGTH(TRIM(title)) > 0),
--     CONSTRAINT chk_events_venue_nonempty CHECK (LENGTH(TRIM(venue)) > 0)
-- );

-- ----------------------------------------------------------------------------
-- 4. REGISTRATIONS TABLE
-- M:N relationship junction table between Users and Events.
-- Candidate Keys: (id), (user_id, event_id)
-- Primary Key: id
-- Unique Invariant: uk_user_event (prevents duplicate registrations)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS registrations (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'INTERESTED' NOT NULL,
    user_id BIGINT NOT NULL,
    event_id BIGINT NOT NULL,
    CONSTRAINT uk_user_event UNIQUE (user_id, event_id),
    CONSTRAINT fk_registration_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_registration_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT chk_registration_status CHECK (status IN ('INTERESTED', 'CONFIRMED', 'CANCELLED', 'WAITLISTED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- PostgreSQL 16 Equivalent:
-- CREATE TABLE registrations (
--     id BIGSERIAL PRIMARY KEY,
--     registration_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     status VARCHAR(20) DEFAULT 'INTERESTED' NOT NULL CHECK (status IN ('INTERESTED', 'CONFIRMED', 'CANCELLED', 'WAITLISTED')),
--     user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
--     CONSTRAINT uk_user_event UNIQUE (user_id, event_id)
-- );

-- ----------------------------------------------------------------------------
-- 5. TRANSACTIONAL OUTBOX TABLE (CO6 Distributed Fundamentals)
-- Provides reliable asynchronous event delivery without distributed 2PC locking.
-- Primary Key: id
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS outbox_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(100) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    payload JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    processed_at DATETIME NULL,
    status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
    CONSTRAINT chk_outbox_status CHECK (status IN ('PENDING', 'PROCESSED', 'FAILED'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- PostgreSQL 16 Equivalent:
-- CREATE TABLE outbox_events (
--     id BIGSERIAL PRIMARY KEY,
--     aggregate_type VARCHAR(50) NOT NULL,
--     aggregate_id VARCHAR(100) NOT NULL,
--     event_type VARCHAR(50) NOT NULL,
--     payload JSONB NOT NULL,
--     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
--     processed_at TIMESTAMPTZ,
--     status VARCHAR(20) DEFAULT 'PENDING' NOT NULL CHECK (status IN ('PENDING', 'PROCESSED', 'FAILED'))
-- );

-- ----------------------------------------------------------------------------
-- 6. SECONDARY B-TREE INDEXES (CO5 Optimization)
-- ----------------------------------------------------------------------------
-- Chronological event feed indexing (range queries on event start time)
CREATE INDEX idx_events_date_time ON events (date_time);

-- Composite index supporting category filtering sorted by date (leftmost prefix)
CREATE INDEX idx_events_category_date_time ON events (category, date_time);

-- Composite index supporting status + timeline filtering (published upcoming events)
CREATE INDEX idx_events_status_date_time ON events (status, date_time);

-- Composite index supporting event attendee list queries by status
CREATE INDEX idx_registrations_event_status ON registrations (event_id, status);

-- Composite index supporting student registered events dashboard by status
CREATE INDEX idx_registrations_user_status ON registrations (user_id, status);

-- Outbox poller queue index for unprocessed events
CREATE INDEX idx_outbox_status_created ON outbox_events (status, created_at);
