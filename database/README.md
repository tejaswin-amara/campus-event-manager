# CampusConnect — Database Systems Engineering Portfolio (25CS1302E)

This directory houses the authoritative database architecture, SQL fluency portfolio, schema migrations, and optimization evidence for **CampusConnect**.

---

## 1. Directory Structure

```text
database/
├── README.md                          # Database architecture and execution guide
├── schema.sql                         # Master standalone DDL (MySQL 8.4 + Postgres 16)
├── seed.sql                           # Production-realistic demonstration dataset
├── transactions.sql                   # ACID transaction scenarios (BEGIN, SAVEPOINT, ROLLBACK)
├── indexes.sql                        # B-tree index definitions and maintenance commands
├── er-diagram.md                      # Formal ER Diagram (Mermaid) with cardinalities
├── sql/                               # Comprehensive CO3 SQL fluency package
│   ├── ddl.sql                        # DDL: CREATE, ALTER, DROP, constraints
│   ├── dml.sql                        # DML: Single/Multi INSERT, UPDATE, DELETE
│   ├── select.sql                     # SELECT: Projections, filtering, expressions
│   ├── joins.sql                      # JOINS: INNER, LEFT, RIGHT, FULL OUTER
│   ├── aggregations.sql               # AGGREGATIONS: GROUP BY, HAVING, single-pass counts
│   ├── subqueries.sql                 # SUBQUERIES: Scalar, IN, EXISTS, Correlated
│   ├── cte.sql                        # CTE: Single & Chained Common Table Expressions
│   ├── recursive-cte.sql              # RECURSIVE CTE: Category taxonomy & prerequisites
│   ├── window-functions.sql           # WINDOW: ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG
│   └── analytics.sql                  # ANALYTICS: Institutional demand & venue metrics
└── explain/                           # Real MySQL 8.4 query execution plans (CO5)
    ├── README.md                      # Before/after comparative optimization analysis
    ├── before/                        # Baseline unindexed execution plans (JSON + text)
    └── after/                         # Hardened index execution plans (JSON + text)
```

---

## 2. Quickstart & Verification

### Running the Database Container
```bash
# Start MySQL 8.4 LTS Container
docker run -d --name campus_events_db -p 3307:3306 \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=campus_events \
  -e MYSQL_USER=campus_app \
  -e MYSQL_PASSWORD=campus_app_password \
  mysql:8.4
```

### Loading Seed Data
```bash
# Execute master seed dataset
docker exec -i campus_events_db mysql -u campus_app -pcampus_app_password campus_events < database/seed.sql
```

### Running the SQL Portfolio
Any script in `database/sql/` can be executed directly against the container:
```bash
docker exec -i campus_events_db mysql -u campus_app -pcampus_app_password campus_events < database/sql/analytics.sql
docker exec -i campus_events_db mysql -u campus_app -pcampus_app_password campus_events < database/sql/recursive-cte.sql
docker exec -i campus_events_db mysql -u campus_app -pcampus_app_password campus_events < database/sql/window-functions.sql
```

---

## 3. Database Engine Decision Summary

- **Primary Engine**: **MySQL 8.4 LTS (InnoDB)**
- **Handout Requirement**: Course specifies PostgreSQL 16.
- **Architectural Rationale**: The repository has 65 automated tests, Flyway migrations V1–V4, and production Docker pipelines configured and verified against MySQL 8.4. Rather than destabilizing the working runtime with a superficial swap, MySQL 8.4 is retained as the authoritative runtime, and side-by-side PostgreSQL 16 equivalents are fully provided for every DDL and query. (See `docs/data-architecture-decision.md`).
