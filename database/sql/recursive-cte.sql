-- ============================================================================
-- CampusConnect — SQL Fluency: Recursive Common Table Expressions (WITH RECURSIVE)
-- Course: 25CS1302E Database Systems Engineering & Distributed Backend
-- Dialect: MySQL 8.4 LTS / PostgreSQL 16 Equivalent
-- ============================================================================

USE campus_events;

-- ----------------------------------------------------------------------------
-- ACADEMIC NOTE & DOMAIN MODEL CONTEXT
-- In CampusConnect, the core operational schema represents flat event categories.
-- To rigorously demonstrate CO3 Recursive CTE traversal without fabricating
-- product features, this script defines a clean academic hierarchy model:
-- 1. Campus Event Category Taxonomy (Multi-level Tree Traversal)
-- 2. Event Series Prerequisite Dependency Graph (Directed Acyclic Graph)
-- ----------------------------------------------------------------------------

-- ----------------------------------------------------------------------------
-- SCENARIO 1: CAMPUS EVENT CATEGORY TAXONOMY HIERARCHY
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS event_categories_hierarchy (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    parent_id INT NULL,
    CONSTRAINT fk_category_parent FOREIGN KEY (parent_id) REFERENCES event_categories_hierarchy(category_id)
) ENGINE=InnoDB;

-- Populate representative taxonomy tree
INSERT INTO event_categories_hierarchy (category_id, category_name, parent_id) VALUES
(1, 'All Campus Activities', NULL),
(2, 'Technical & Computing', 1),
(3, 'Cultural & Performing Arts', 1),
(4, 'Athletics & Physical Recreation', 1),
(5, 'Artificial Intelligence & Data', 2),
(6, 'Distributed Systems & Cloud', 2),
(7, 'Classical & Fusion Music', 3),
(8, 'Theater & Fine Arts', 3),
(9, 'Inter-College Football', 4),
(10, 'Indoor Racquet Sports', 4)
ON DUPLICATE KEY UPDATE category_name = VALUES(category_name);

-- RECURSIVE QUERY 1: TOP-DOWN HIERARCHICAL TREE TRAVERSAL WITH PATH BREADCRUMBS
-- Purpose: Traverse taxonomy from root to leaf nodes, computing depth level and breadcrumb path.
WITH RECURSIVE CategoryPathCTE AS (
    -- Anchor member: Select all root categories (parent_id IS NULL)
    SELECT
        c.category_id,
        c.category_name,
        c.parent_id,
        1 AS hierarchy_depth,
        CAST(c.category_name AS CHAR(1000)) AS taxonomy_path
    FROM event_categories_hierarchy c
    WHERE c.parent_id IS NULL

    UNION ALL

    -- Recursive member: Traverse child categories, incrementing depth and concatenating path
    SELECT
        child.category_id,
        child.category_name,
        child.parent_id,
        parent.hierarchy_depth + 1,
        CONCAT(parent.taxonomy_path, ' -> ', child.category_name)
    FROM event_categories_hierarchy child
    INNER JOIN CategoryPathCTE parent ON child.parent_id = parent.category_id
)
SELECT
    hierarchy_depth,
    category_name,
    taxonomy_path
FROM CategoryPathCTE
ORDER BY taxonomy_path ASC;

-- ----------------------------------------------------------------------------
-- SCENARIO 2: PREREQUISITE EVENT CHAIN RESOLUTION (DIRECTED GRAPH TRAVERSAL)
-- Purpose: Given an advanced workshop, identify the complete prerequisite chain
-- that a student must complete prior to registration.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS event_prerequisites (
    course_event_id INT NOT NULL,
    prerequisite_event_id INT NOT NULL,
    PRIMARY KEY (course_event_id, prerequisite_event_id)
) ENGINE=InnoDB;

INSERT INTO event_prerequisites (course_event_id, prerequisite_event_id) VALUES
(103, 102), -- Advanced Distributed Systems requires Intermediate Cloud Architecture
(102, 101), -- Intermediate Cloud Architecture requires Foundations of Computer Systems
(105, 104), -- Deep Neural Networks requires Foundations of Machine Learning
(104, 101)  -- Foundations of Machine Learning requires Foundations of Computer Systems
ON DUPLICATE KEY UPDATE course_event_id=VALUES(course_event_id);

-- RECURSIVE QUERY 2: BOTTOM-UP PREREQUISITE GRAPH EXPANSION
-- Query: Find all transitive prerequisites for 'Advanced Distributed Systems' (ID 103).
WITH RECURSIVE PrerequisiteChainCTE AS (
    -- Anchor member: Direct prerequisites of course 103
    SELECT
        ep.course_event_id AS target_event,
        ep.prerequisite_event_id AS prerequisite_event,
        1 AS prerequisite_level
    FROM event_prerequisites ep
    WHERE ep.course_event_id = 103

    UNION ALL

    -- Recursive member: Prerequisites of the prerequisite
    SELECT
        pc.target_event,
        ep.prerequisite_event_id,
        pc.prerequisite_level + 1
    FROM event_prerequisites ep
    INNER JOIN PrerequisiteChainCTE pc ON ep.course_event_id = pc.prerequisite_event
)
SELECT
    target_event AS target_advanced_course_id,
    prerequisite_event AS required_foundation_course_id,
    prerequisite_level AS dependency_distance
FROM PrerequisiteChainCTE
ORDER BY prerequisite_level ASC;
