-- ============================================================================
-- CampusConnect — Master Seed Dataset (Development & Demonstration)
-- Academic Subject: 25CS1302E Database Systems Engineering & Distributed Backend
-- Target Engine: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- 1. SEED USERS
-- BCrypt hashed passwords (cost 10) for standard personas:
-- admin / admin123  -> $2a$10$7EqJtq98hPqEX7fNZaFWoO...
-- student / pass123 -> $2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012
-- ----------------------------------------------------------------------------
INSERT INTO users (id, username, password, role, email) VALUES
(1, 'admin', '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy', 'ADMIN', 'admin@campus.edu'),
(2, 'arun_kumar', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'arun.k@campus.edu'),
(3, 'priya_sharma', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'priya.s@campus.edu'),
(4, 'rohit_verma', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'rohit.v@campus.edu'),
(5, 'ananya_iyer', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'ananya.i@campus.edu'),
(6, 'kavita_patel', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'kavita.p@campus.edu'),
(7, 'tech_club_lead', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'ORGANIZER', 'techclub@campus.edu'),
(8, 'cultural_coord', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'ORGANIZER', 'cultural@campus.edu'),
(9, 'sports_council', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'ORGANIZER', 'sports@campus.edu'),
(10, 'vikram_singh', '$2a$10$abcdefghijklmnopqrstuvwxyz1234567890123456789012', 'STUDENT', 'vikram.s@campus.edu')
ON DUPLICATE KEY UPDATE role=VALUES(role), email=VALUES(email);

-- ----------------------------------------------------------------------------
-- 2. SEED EVENTS (Past, Ongoing, Upcoming Across Categories & Statuses)
-- ----------------------------------------------------------------------------
INSERT INTO events (id, title, description, date_time, end_date_time, venue, category, status, registration_link, max_capacity, image_url) VALUES
-- Past Events
(1, 'Campus Hackathon 2025', 'Annual 24-hour national hackathon focused on distributed systems and AI applications.', '2025-11-15 09:00:00', '2025-11-16 09:00:00', 'Main Auditorium & CS Labs', 'Technical', 'COMPLETED', 'https://forms.campus.edu/hack2025', 200, '/images/hackathon.jpg'),
(2, 'Autumn Cultural Fest — Tarang', 'Inter-collegiate cultural festival featuring music, theater, and dance competitions.', '2025-10-20 17:00:00', '2025-10-22 22:00:00', 'Open Air Theater', 'Cultural', 'COMPLETED', 'https://forms.campus.edu/tarang25', 500, '/images/tarang.jpg'),
(3, 'Intra-University Badminton Cup', 'Singles and doubles knockout badminton championship.', '2025-12-05 08:00:00', '2025-12-06 18:00:00', 'Indoor Sports Complex', 'Sports', 'COMPLETED', 'https://forms.campus.edu/badminton', 64, '/images/badminton.jpg'),

-- Ongoing / Current Events
(4, 'Distributed Systems & Cloud Workshop', 'Hands-on training covering Spring Boot microservices, replication lag, and high-concurrency database design.', DATE_SUB(NOW(), INTERVAL 1 HOUR), DATE_ADD(NOW(), INTERVAL 3 HOUR), 'Turing Hall, Block C', 'Workshop', 'PUBLISHED', 'https://forms.campus.edu/dist-systems', 75, '/images/workshop.jpg'),
(5, 'Campus Art & Photography Exhibition', 'Showcasing contemporary student photography and fine arts.', DATE_SUB(NOW(), INTERVAL 2 HOUR), DATE_ADD(NOW(), INTERVAL 6 HOUR), 'Student Activity Center', 'Cultural', 'PUBLISHED', 'https://forms.campus.edu/artexpo', 150, '/images/art.jpg'),

-- Upcoming Events
(6, 'National Technical Symposium 2026', 'Flagship engineering conference featuring paper presentations, robotics showdowns, and algorithmic trading challenges.', DATE_ADD(NOW(), INTERVAL 7 DAY), DATE_ADD(NOW(), INTERVAL 8 DAY), 'Convention Center', 'Technical', 'PUBLISHED', 'https://forms.campus.edu/symposium2026', 350, '/images/symposium.jpg'),
(7, 'Spring Classical & Fusion Music Night', 'Evening of classical carnatic, hindustani, and western fusion ensemble performances.', DATE_ADD(NOW(), INTERVAL 10 DAY), DATE_ADD(NOW(), INTERVAL 10 DAY) + INTERVAL 4 HOUR, 'Amphitheater', 'Cultural', 'PUBLISHED', 'https://forms.campus.edu/musicnight', 250, '/images/music.jpg'),
(8, 'Inter-College Football Premier League', 'Annual 11-a-side inter-college tournament spanning two weekends.', DATE_ADD(NOW(), INTERVAL 14 DAY), DATE_ADD(NOW(), INTERVAL 21 DAY), 'Central Sports Ground', 'Sports', 'PUBLISHED', 'https://forms.campus.edu/football2026', 120, '/images/football.jpg'),
(9, 'Generative AI & Agentic Workflows Seminar', 'Guest lecture by industry research engineers on multi-agent architectures and neural retrieval.', DATE_ADD(NOW(), INTERVAL 18 DAY), DATE_ADD(NOW(), INTERVAL 18 DAY) + INTERVAL 2 HOUR, 'Seminar Hall 1', 'Seminar', 'PUBLISHED', 'https://forms.campus.edu/genai-seminar', 120, '/images/genai.jpg'),
(10, 'Full-Stack Web & Next.js Masterclass', 'Weekend intensive bootcamp covering React Server Components and modern API design.', DATE_ADD(NOW(), INTERVAL 25 DAY), DATE_ADD(NOW(), INTERVAL 26 DAY), 'Lab 3, Department of IT', 'Workshop', 'PUBLISHED', 'https://forms.campus.edu/web-bootcamp', 60, '/images/webbootcamp.jpg'),

-- Lifecycle States: Draft & Cancelled
(11, 'Spring Track & Field Athletics Meet', 'Inter-department 100m, 400m, relay, and field track events.', DATE_ADD(NOW(), INTERVAL 30 DAY), DATE_ADD(NOW(), INTERVAL 31 DAY), 'University Stadium', 'Sports', 'DRAFT', NULL, 150, NULL),
(12, 'Cancelled Winter Robotics Challenge', 'Postponed due to lab renovation.', DATE_ADD(NOW(), INTERVAL 5 DAY), DATE_ADD(NOW(), INTERVAL 6 DAY), 'Robotics Arena', 'Technical', 'CANCELLED', NULL, 50, NULL)
ON DUPLICATE KEY UPDATE title=VALUES(title), status=VALUES(status);

-- ----------------------------------------------------------------------------
-- 3. SEED REGISTRATIONS (User Interest & Invariant Demonstration)
-- ----------------------------------------------------------------------------
INSERT INTO registrations (id, registration_date, status, user_id, event_id) VALUES
(1, '2025-11-01 10:15:00', 'CONFIRMED', 2, 1),
(2, '2025-11-01 11:30:00', 'CONFIRMED', 3, 1),
(3, '2025-11-02 09:45:00', 'CONFIRMED', 4, 1),
(4, '2025-10-05 14:20:00', 'CONFIRMED', 2, 2),
(5, '2025-10-06 16:10:00', 'CONFIRMED', 5, 2),
(6, '2025-12-01 12:00:00', 'CONFIRMED', 4, 3),
(7, NOW() - INTERVAL 3 DAY, 'INTERESTED', 2, 4),
(8, NOW() - INTERVAL 3 DAY, 'INTERESTED', 3, 4),
(9, NOW() - INTERVAL 2 DAY, 'INTERESTED', 6, 4),
(10, NOW() - INTERVAL 2 DAY, 'INTERESTED', 10, 4),
(11, NOW() - INTERVAL 1 DAY, 'INTERESTED', 5, 5),
(12, NOW() - INTERVAL 1 DAY, 'INTERESTED', 6, 5),
(13, NOW() - INTERVAL 12 HOUR, 'CONFIRMED', 2, 6),
(14, NOW() - INTERVAL 10 HOUR, 'CONFIRMED', 3, 6),
(15, NOW() - INTERVAL 8 HOUR, 'INTERESTED', 4, 6),
(16, NOW() - INTERVAL 6 HOUR, 'INTERESTED', 5, 6),
(17, NOW() - INTERVAL 4 HOUR, 'WAITLISTED', 6, 6),
(18, NOW() - INTERVAL 2 HOUR, 'INTERESTED', 10, 6),
(19, NOW() - INTERVAL 5 HOUR, 'INTERESTED', 3, 7),
(20, NOW() - INTERVAL 4 HOUR, 'INTERESTED', 5, 7),
(21, NOW() - INTERVAL 8 HOUR, 'CONFIRMED', 4, 8),
(22, NOW() - INTERVAL 6 HOUR, 'CONFIRMED', 10, 8),
(23, NOW() - INTERVAL 3 HOUR, 'INTERESTED', 2, 9),
(24, NOW() - INTERVAL 2 HOUR, 'INTERESTED', 3, 9),
(25, NOW() - INTERVAL 1 HOUR, 'INTERESTED', 4, 9),
(26, NOW() - INTERVAL 30 MINUTE, 'INTERESTED', 6, 10),
(27, NOW() - INTERVAL 20 MINUTE, 'CANCELLED', 2, 8)
ON DUPLICATE KEY UPDATE status=VALUES(status);

-- ----------------------------------------------------------------------------
-- 4. SEED OUTBOX EVENTS (CO6 Asynchronous Event Decoupling)
-- ----------------------------------------------------------------------------
INSERT INTO outbox_events (id, aggregate_type, aggregate_id, event_type, payload, created_at, processed_at, status) VALUES
(1, 'EVENT', '6', 'EVENT_PUBLISHED', '{"eventId": 6, "title": "National Technical Symposium 2026", "category": "Technical", "venue": "Convention Center"}', NOW() - INTERVAL 7 DAY, NOW() - INTERVAL 7 DAY, 'PROCESSED'),
(2, 'REGISTRATION', '13', 'STUDENT_REGISTERED', '{"registrationId": 13, "userId": 2, "eventId": 6, "status": "CONFIRMED"}', NOW() - INTERVAL 12 HOUR, NOW() - INTERVAL 12 HOUR, 'PROCESSED'),
(3, 'REGISTRATION', '26', 'STUDENT_REGISTERED', '{"registrationId": 26, "userId": 6, "eventId": 10, "status": "INTERESTED"}', NOW() - INTERVAL 30 MINUTE, NULL, 'PENDING');
