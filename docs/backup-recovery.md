# CampusConnect — Database Backup, Disaster Recovery & PITR Runbook

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Target Engine:** MySQL 8.4 LTS (InnoDB Storage Engine)

---

## 1. Disaster Recovery Metrics & Service Level Objectives

| Metric | Business Definition | Target SLO (Registration Window) | Target SLO (Standard Semester) |
|---|---|---|---|
| **RPO (Recovery Point Objective)** | Maximum acceptable data loss duration | **$\le$ 1 Minute** (near-zero data loss) | **$\le$ 1 Hour** |
| **RTO (Recovery Time Objective)** | Maximum allowable downtime until service restoration | **$\le$ 15 Minutes** | **$\le$ 1 Hour** |

---

## 2. Backup Strategy Architecture

CampusConnect implements a tiered backup topology combining daily consistent logical snapshots with continuous Binary Log (binlog) streaming:

```
               ┌────────────────────────────────────────────────────────┐
               │              Continuous Binary Log Streaming           │
               │  (Captures every COMMIT, DDL, DML transaction)         │
               └──────────────────────────┬─────────────────────────────┘
                                          │
 ┌────────────────────────────────────────▼────────────────────────────────────────┐
 │ Snapshot Baseline (Daily at 02:00 UTC)                                          │
 │ mysqldump --single-transaction --flush-logs --master-data=2                     │
 └────────────────────────────────────────┬────────────────────────────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │ Encrypted Remote Object Storage (S3) │
                      │ Retention: 30 Daily / 12 Monthly      │
                      └───────────────────────────────────────┘
```

---

## 3. Operational Backup Procedures

### 3.1 Consistent Logical Snapshot (`mysqldump`)

The following command executes a consistent snapshot without taking read locks on InnoDB tables:

```bash
mysqldump \
  --host=127.0.0.1 \
  --port=3307 \
  --user=campus_app \
  --password=campus_app_password \
  --single-transaction \
  --quick \
  --routines \
  --triggers \
  --source-data=2 \
  --databases campus_events \
  | gzip > /backups/campus_events_$(date +%Y%m%d_%H%M%S).sql.gz
```

* **`--single-transaction`:** Sets transaction isolation level to `REPEATABLE READ` before dumping, creating an MVCC consistent read snapshot without blocking concurrent writes.
* **`--quick`:** Forces `mysqldump` to retrieve rows from the server row-by-row rather than buffering all rows in client memory.
* **`--source-data=2` (formerly `--master-data`):** Records the exact binary log file name and log position in SQL comment header for seamless PITR stitching.

---

## 4. Point-In-Time Recovery (PITR) Execution Runbook

When catastrophic failure or accidental table truncation occurs (e.g., accidental `DROP TABLE` at `2026-09-08 14:35:00`), perform Point-In-Time Recovery to restore the database to `2026-09-08 14:34:59`.

### Step 1: Isolate the Host & Stop Application Traffic
```bash
docker stop campus_connect_app
```

### Step 2: Restore the Base Snapshot
Extract and apply the most recent daily base snapshot (e.g., taken at `02:00:00`):

```bash
gunzip < /backups/campus_events_20260908_020000.sql.gz | mysql \
  -h 127.0.0.1 -P 3307 -u campus_app -p campus_events
```

### Step 3: Extract Binary Log Coordinates
Inspect the comment in the top 25 lines of the uncompressed dump:
```text
-- CHANGE MASTER TO MASTER_LOG_FILE='binlog.000042', MASTER_LOG_POS=1048576;
```

### Step 4: Replay Binary Logs Up to the Exact Second Before Corruption
Use `mysqlbinlog` to extract and replay all transactions committed between the snapshot position and `14:34:59`:

```bash
mysqlbinlog \
  --start-position=1048576 \
  --stop-datetime="2026-09-08 14:34:59" \
  /var/lib/mysql/binlog.000042 /var/lib/mysql/binlog.000043 \
  | mysql -h 127.0.0.1 -P 3307 -u campus_app -p campus_events
```

### Step 5: Verify Data Consistency
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM events;
SELECT COUNT(*) FROM registrations;
-- Confirm row counts match pre-incident audit logs
```

### Step 6: Resume Application Services
```bash
docker start campus_connect_app
```

---

## 5. Automated Verification Drill Schedule

1. **Daily Automated Check:** Automated cron job spins up a disposable test container, restores the previous night's `.sql.gz` dump, and verifies table checksums (`CHECKSUM TABLE events, registrations`).
2. **Monthly Full Recovery Drill:** Simulated disaster drill executing PITR against a sandbox environment, recording actual elapsed time to prove compliance with the 15-minute RTO target.
