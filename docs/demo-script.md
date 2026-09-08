# CampusConnect — Live Evaluation & Faculty Presentation Demo Script

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Audience:** Project Evaluation Faculty / Review Committee  
**Estimated Duration:** 15 Minutes  
**Prerequisites:** Docker Engine running, Java 25 installed, Terminal open at repository root.

---

## Act 1: Infrastructure & Application Startup (Minutes 0–2)

### Step 1: Verify MySQL 8.4 Database Container
Demonstrate that the system connects to a genuine MySQL 8.4 LTS instance on port 3307:

```bash
docker ps --filter "name=campus_events_db"
```
*Expected Output:* Container `campus_events_db` is UP and healthy, port mapping `0.0.0.0:3307->3306/tcp`.

### Step 2: Verify Flyway Database Migration History
Demonstrate that the database schema is managed through version-controlled Flyway migrations (V1 through V4):

```bash
mysql -h 127.0.0.1 -P 3307 -u campus_app -pcampus_app_password campus_events -e "SELECT installed_rank, version, description, type, execution_time, success FROM flyway_schema_history;"
```
*Key Talking Point:* "Our schema is maintained in reproducible, idempotent migrations. V4 introduced table-level check constraints, composite B-Tree indexes, and the distributed transactional outbox."

### Step 3: Launch the Spring Boot 3.4 Application
```bash
./mvnw spring-boot:run
```
*Demonstrate:* Starts cleanly on port `8080`, connecting to MySQL on port `3307`.

---

## Act 2: Web Application & Role-Based Access (Minutes 2–5)

### Step 4: Student Flow (Browsing & Catalog Filtering)
1. Open Browser to `http://localhost:8080/login`.
2. Login with Student Credentials:
   * **Email:** `aarav.sharma@campus.edu`
   * **Password:** `password123`
3. View Student Dashboard (`/student/dashboard`):
   * Filter by category: Select **Technical**.
   * Note instant response time backed by index `idx_events_category_date`.
4. Click **Register** on Event 1 ("ACM Global Hackathon 2026"):
   * Shows registered badge; provides external registration link.
5. Attempt to Register Again:
   * System gracefully notifies student: "You are already registered for this event."

### Step 5: Admin Flow (Event Management & Roster Inspection)
1. Logout and login with Admin Credentials:
   * **Email:** `admin@campus.edu`
   * **Password:** `admin123`
2. View Admin Dashboard (`/admin/dashboard`):
   * Create a new event with status `PUBLISHED`.
   * View attendee rosters showing real-time enrollment counts.

---

## Act 3: Concurrency Stress Test & ACID Locking (Minutes 5–8)

### Step 6: Execute the Real Multi-Threaded Stress Test
Demonstrate live that duplicate registrations are physically impossible at the database engine level under multi-threaded contention:

```bash
./mvnw test -Dtest=EventServiceConcurrencyTest
```

*Faculty Demonstration Points:*
* Explain the dual `CountDownLatch` releasing 10 concurrent threads simultaneously.
* Highlight console output showing 1 thread acquiring the pessimistic write lock and committing, while 9 threads receive MySQL Error 1062:
  ```text
  SQL Error: 1062, SQLState: 23000: Duplicate entry '1-1' for key 'registrations.uk_user_event'
  ```
* Show the second test: 8 distinct users simultaneously registering for the same event with 8/8 successful commits and zero lost updates.

---

## Act 4: SQL Portfolio & Advanced Querying (Minutes 8–11)

### Step 7: Chained CTEs & Category Capacity Density
Demonstrate Common Table Expressions from `database/sql/cte.sql`:

```bash
mysql -h 127.0.0.1 -P 3307 -u campus_app -pcampus_app_password campus_events < database/sql/cte.sql
```
*Explain:* Computes multi-level aggregation comparing each category's enrollment against campus-wide average enrollment in a single scan.

### Step 8: Window Functions (Analytical Ranking & Moving Averages)
Execute `database/sql/window-functions.sql`:

```bash
mysql -h 127.0.0.1 -P 3307 -u campus_app -pcampus_app_password campus_events < database/sql/window-functions.sql
```
*Explain:* Demonstrates `DENSE_RANK() OVER (PARTITION BY category ORDER BY attendee_count DESC)` and 3-event rolling average attendance without subqueries.

---

## Act 5: Query Optimization & EXPLAIN ANALYZE Evidence (Minutes 11–13)

### Step 9: Live Before/After EXPLAIN ANALYZE Comparison
Show the measured query execution plans documented in `database/explain/README.md`:

```sql
-- Query Under Review:
EXPLAIN ANALYZE
SELECT id, title, category, date_time, venue 
FROM events 
WHERE category = 'Technical' 
ORDER BY date_time ASC;
```

*Highlight:*
* **Before Indexing:** `type: ALL` (Full Table Scan), `Using filesort`, Cost = `1.45`.
* **After Composite Index `idx_events_category_date`:** `type: ref`, **filesort eliminated**, Cost = `0.70` (**51.7% cost reduction**).
* Show negative demonstration: Explain why the optimizer intentionally skips `idx_users_role` due to 90% student cardinality.

---

## Act 6: Distributed Architecture & Automated Test Gate (Minutes 13–15)

### Step 10: Inspect the Transactional Outbox (CO6)
Demonstrate decoupled asynchronous event publishing:

```bash
mysql -h 127.0.0.1 -P 3307 -u campus_app -pcampus_app_password campus_events -e "SELECT id, aggregate_type, aggregate_id, event_type, status, created_at FROM outbox_events;"
```
*Explain:* "Rather than using fragile Two-Phase Commit (2PC) or risking dual-write inconsistencies, registration domain events are saved atomically in the same local transaction, ready for poller dispatch."

### Step 11: Execute the Full Automated Test Suite
Run the full test suite to prove 100% build health:

```bash
./mvnw test
```
*Expected Final Output:*
```text
[INFO] Tests run: 65, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

### Conclusion
"CampusConnect delivers a hardened, academically verified, and fully tested database systems engineering solution achieving complete compliance with all course outcomes CO1 through CO6."
