-- ============================================================================
-- CampusConnect — SQL Fluency: Data Definition Language (DDL)
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS (with PostgreSQL 16 equivalents in comments)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. DATABASE & SCHEMA CREATION
-- Purpose: Establish UTF-8 multi-byte Unicode database environment
-- Context: Initial system bootstrap
-- ----------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS campus_events
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE campus_events;

-- PostgreSQL 16:
-- CREATE DATABASE campus_events WITH ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8';

-- ----------------------------------------------------------------------------
-- 2. TABLE CREATION WITH CONSTRAINTS
-- Purpose: Formal table definition with PK, FK, UNIQUE, and CHECK constraints.
-- Invariant: Preserves domain integrity at the database layer (Zero-Trust design).
-- ----------------------------------------------------------------------------

-- A. USERS Table
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

-- B. EVENTS Table
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

-- C. REGISTRATIONS Table (Junction Table for M:N Relationship)
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

-- D. OUTBOX_EVENTS Table (Transactional Outbox for CO6 Distributed Decoupling)
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

-- ----------------------------------------------------------------------------
-- 3. INDEX CREATION (CO5 Query Performance)
-- Purpose: Enable $O(\log N)$ B-Tree lookups for frequent access paths.
-- ----------------------------------------------------------------------------
CREATE INDEX idx_events_date_time ON events (date_time);
CREATE INDEX idx_events_category_date_time ON events (category, date_time);
CREATE INDEX idx_events_status_date_time ON events (status, date_time);
CREATE INDEX idx_registrations_event_status ON registrations (event_id, status);
CREATE INDEX idx_registrations_user_status ON registrations (user_id, status);
CREATE INDEX idx_outbox_status_created ON outbox_events (status, created_at);

-- ----------------------------------------------------------------------------
-- 4. ALTER TABLE OPERATIONS
-- Purpose: Schema evolution demonstration (adding audit columns, modifying types).
-- ----------------------------------------------------------------------------
-- Add audit timestamp to users table
ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL;

-- Modify column length for future OAuth identity providers
ALTER TABLE users MODIFY COLUMN email VARCHAR(320) NULL;

-- Add optional check constraint for external registration URLs
ALTER TABLE events ADD CONSTRAINT chk_event_reg_link_protocol
    CHECK (registration_link IS NULL OR registration_link LIKE 'http://%' OR registration_link LIKE 'https://%');

-- ----------------------------------------------------------------------------
-- 5. ISOLATED SAFE DROP DEMONSTRATION
-- Purpose: Safe teardown of temporary or deprecated analytics staging tables.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS temp_registration_import (
    temp_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    raw_payload TEXT,
    imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Verify existence then drop safely
DROP TABLE IF EXISTS temp_registration_import;
