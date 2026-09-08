import subprocess
import os

os.makedirs('database/explain/before', exist_ok=True)
os.makedirs('database/explain/after', exist_ok=True)

def run_query(sql):
    cmd = ['docker', 'exec', '-i', 'campus_events_db', 'mysql', '-u', 'campus_app', '-pcampus_app_password', 'campus_events', '-e', sql]
    p = subprocess.run(cmd, capture_output=True, text=True)
    # clean out any mysql warning header
    lines = [line for line in p.stdout.splitlines() if not line.startswith('mysql: [Warning]')]
    return '\n'.join(lines).strip()

# 1. Query 1: Category + Date
q1_b_sql = "EXPLAIN FORMAT=JSON SELECT id, title, venue, date_time FROM events IGNORE INDEX (idx_events_category_date_time, idx_events_date_time) WHERE category = 'Technical' AND date_time >= '2025-01-01 00:00:00' ORDER BY date_time ASC;"
q1_a_sql = "EXPLAIN FORMAT=JSON SELECT id, title, venue, date_time FROM events FORCE INDEX (idx_events_category_date_time) WHERE category = 'Technical' AND date_time >= '2025-01-01 00:00:00' ORDER BY date_time ASC;"
q1_b_an_sql = "EXPLAIN ANALYZE SELECT id, title, venue, date_time FROM events IGNORE INDEX (idx_events_category_date_time, idx_events_date_time) WHERE category = 'Technical' AND date_time >= '2025-01-01 00:00:00' ORDER BY date_time ASC;"
q1_a_an_sql = "EXPLAIN ANALYZE SELECT id, title, venue, date_time FROM events FORCE INDEX (idx_events_category_date_time) WHERE category = 'Technical' AND date_time >= '2025-01-01 00:00:00' ORDER BY date_time ASC;"

with open('database/explain/before/q1_category_date_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q1_b_sql))
with open('database/explain/after/q1_category_date_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q1_a_sql))
with open('database/explain/before/q1_category_date_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q1_b_an_sql))
with open('database/explain/after/q1_category_date_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q1_a_an_sql))

# 2. Query 2: Upcoming Events
q2_b_sql = "EXPLAIN FORMAT=JSON SELECT id, title, date_time, category FROM events IGNORE INDEX (idx_events_date_time, idx_events_category_date_time) WHERE date_time >= '2026-01-01 00:00:00' ORDER BY date_time ASC;"
q2_a_sql = "EXPLAIN FORMAT=JSON SELECT id, title, date_time, category FROM events FORCE INDEX (idx_events_date_time) WHERE date_time >= '2026-01-01 00:00:00' ORDER BY date_time ASC;"
q2_b_an_sql = "EXPLAIN ANALYZE SELECT id, title, date_time, category FROM events IGNORE INDEX (idx_events_date_time, idx_events_category_date_time) WHERE date_time >= '2026-01-01 00:00:00' ORDER BY date_time ASC;"
q2_a_an_sql = "EXPLAIN ANALYZE SELECT id, title, date_time, category FROM events FORCE INDEX (idx_events_date_time) WHERE date_time >= '2026-01-01 00:00:00' ORDER BY date_time ASC;"

with open('database/explain/before/q2_upcoming_events_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q2_b_sql))
with open('database/explain/after/q2_upcoming_events_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q2_a_sql))
with open('database/explain/before/q2_upcoming_events_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q2_b_an_sql))
with open('database/explain/after/q2_upcoming_events_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q2_a_an_sql))

# 3. Query 3: User Registration History
q3_b_sql = "EXPLAIN FORMAT=JSON SELECT r.id, r.registration_date, r.status, e.title FROM registrations r IGNORE INDEX (idx_registrations_user_status, uk_user_event) JOIN events e ON r.event_id = e.id WHERE r.user_id = 2;"
q3_a_sql = "EXPLAIN FORMAT=JSON SELECT r.id, r.registration_date, r.status, e.title FROM registrations r FORCE INDEX (idx_registrations_user_status) JOIN events e ON r.event_id = e.id WHERE r.user_id = 2;"
q3_b_an_sql = "EXPLAIN ANALYZE SELECT r.id, r.registration_date, r.status, e.title FROM registrations r IGNORE INDEX (idx_registrations_user_status, uk_user_event) JOIN events e ON r.event_id = e.id WHERE r.user_id = 2;"
q3_a_an_sql = "EXPLAIN ANALYZE SELECT r.id, r.registration_date, r.status, e.title FROM registrations r FORCE INDEX (idx_registrations_user_status) JOIN events e ON r.event_id = e.id WHERE r.user_id = 2;"

with open('database/explain/before/q3_user_history_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q3_b_sql))
with open('database/explain/after/q3_user_history_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q3_a_sql))
with open('database/explain/before/q3_user_history_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q3_b_an_sql))
with open('database/explain/after/q3_user_history_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q3_a_an_sql))

# 4. Query 4: Low Selectivity Example (Why Index is NOT Used)
q4_sql = "EXPLAIN FORMAT=JSON SELECT id, title, status FROM events WHERE status = 'PUBLISHED';"
q4_an_sql = "EXPLAIN ANALYZE SELECT id, title, status FROM events WHERE status = 'PUBLISHED';"

with open('database/explain/after/q4_low_selectivity_explain.json', 'w', encoding='utf-8') as f: f.write(run_query(q4_sql))
with open('database/explain/after/q4_low_selectivity_analyze.txt', 'w', encoding='utf-8') as f: f.write(run_query(q4_an_sql))

print('ALL EXPLAIN QUERY EVIDENCE CAPTURED SUCCESSFULLY!')
