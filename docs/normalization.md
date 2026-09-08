# CampusConnect — Database Normalization & Dependency Theory Report

**Course:** 25CS1302E — Database Systems Engineering And Distributed Backend Development  
**Course Outcome Alignment:** **CO2** — Formulate conceptually sound ER models and map them to normalized relational schemas.  
**Authoritative Relational Schema:** `users`, `events`, `registrations`, `outbox_events`

---

## 1. Universal Relation Formulation

To demonstrate formal normalization from first principles, we define the unnormalized universal relation representing campus event management prior to relational decomposition:

$$\mathcal{U} = (\text{user\_id}, \text{user\_name}, \text{user\_email}, \text{user\_password}, \text{user\_role}, \text{user\_dept}, \text{event\_id}, \text{event\_title}, \text{event\_desc}, \text{event\_cat}, \text{event\_dt}, \text{venue}, \text{reg\_link}, \text{img\_url}, \text{status}, \text{reg\_id}, \text{reg\_date})$$

---

## 2. Functional Dependencies ($\mathcal{F}$)

Analysis of campus domain invariants yields the following minimal cover of functional dependencies:

### 2.1 User Entity Sub-schema
1. $\text{user\_id} \rightarrow \text{user\_name}, \text{user\_email}, \text{user\_password}, \text{user\_role}, \text{user\_dept}$
2. $\text{user\_email} \rightarrow \text{user\_id}, \text{user\_name}, \text{user\_password}, \text{user\_role}, \text{user\_dept}$

### 2.2 Event Entity Sub-schema
3. $\text{event\_id} \rightarrow \text{event\_title}, \text{event\_desc}, \text{event\_cat}, \text{event\_dt}, \text{venue}, \text{reg\_link}, \text{img\_url}, \text{status}$
4. $\text{event\_title}, \text{venue}, \text{event\_dt} \rightarrow \text{event\_id}$ (Natural operational business key: an auditorium cannot host two events with the same title at the exact same time).

### 2.3 Registration Relationship Sub-schema
5. $\text{reg\_id} \rightarrow \text{user\_id}, \text{event\_id}, \text{reg\_date}$
6. $\text{user\_id}, \text{event\_id} \rightarrow \text{reg\_id}, \text{reg\_date}$ (A student can register for a given event at most once).

---

## 3. Candidate Keys of Universal Relation $\mathcal{U}$

Computing the attribute closure under $\mathcal{F}$:
* $\{ \text{user\_id}, \text{event\_id} \}^+ = \mathcal{U}$
* $\{ \text{user\_email}, \text{event\_id} \}^+ = \mathcal{U}$
* $\{ \text{reg\_id} \}^+$ only determines user and event attributes if they are bound, but for unregistered events or users with no registrations, $\mathcal{U}$ produces NULLs.

Hence, the primary composite candidate key of $\mathcal{U}$ is $(\text{user\_id}, \text{event\_id})$.

---

## 4. Normal Form Step-by-Step Proofs

### 4.1 First Normal Form (1NF)

**Definition:** A relation $R$ is in 1NF if and only if all underlying domains contain only atomic (indivisible) values, and there are no repeating groups or multivalued arrays.

* **Audit of Legacy State:** In legacy flat architectures, students attending an event might be stored as comma-separated student IDs or JSON arrays within the event record (e.g., `attendee_ids: "1,4,7,12"`).
* **CampusConnect Compliance:**
  * Every attribute holds strictly scalar, atomic values (`BIGINT`, `VARCHAR`, `DATETIME`, `TIMESTAMP`).
  * Repeating attendance lists are decoupled into an independent associative relation (`registrations`), where each tuple represents exactly one atomic binding between a single user and a single event.
* **Conclusion:** The relational schema satisfies **1NF**.

---

### 4.2 Second Normal Form (2NF)

**Definition:** A relation $R$ is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on every candidate key (i.e., no partial dependency on a proper subset of any candidate key).

* **Violation in Universal Relation $\mathcal{U}$:**
  * Candidate key: $\{ \text{user\_id}, \text{event\_id} \}$
  * Non-prime attributes: $\text{user\_name}, \text{user\_email}, \text{event\_title}, \text{venue}, \dots$
  * Observe: $\text{user\_id} \rightarrow \text{user\_name}$ is a partial dependency ($\text{user\_id} \subset \{ \text{user\_id}, \text{event\_id} \}$).
  * Observe: $\text{event\_id} \rightarrow \text{event\_title}$ is a partial dependency ($\text{event\_id} \subset \{ \text{user\_id}, \text{event\_id} \}$).
  * **Anomalies Produced:**
    * *Insertion Anomaly:* Cannot register a new student before they enroll in an event without setting event attributes to NULL.
    * *Deletion Anomaly:* Deleting the last attendee from an event erases the event description and venue.
    * *Update Anomaly:* Modifying a user's department requires updating hundreds of rows across all event enrollments.

* **Decomposition to Achieve 2NF:**
  Decompose $\mathcal{U}$ into:
  1. $R_1(\text{user\_id}, \text{user\_name}, \text{user\_email}, \text{user\_password}, \text{user\_role}, \text{user\_dept})$
  2. $R_2(\text{event\_id}, \text{event\_title}, \text{event\_desc}, \text{event\_cat}, \text{event\_dt}, \text{venue}, \text{reg\_link}, \text{img\_url}, \text{status})$
  3. $R_3(\text{reg\_id}, \text{user\_id}, \text{event\_id}, \text{reg\_date})$

* **Verification:**
  * In $R_1$, candidate keys are $\{ \text{user\_id} \}$ and $\{ \text{user\_email} \}$. Both are single attributes; hence no partial dependency can exist.
  * In $R_2$, candidate key is $\{ \text{event\_id} \}$. Single attribute; no partial dependency can exist.
  * In $R_3$, candidate keys are $\{ \text{reg\_id} \}$ and $\{ \text{user\_id}, \text{event\_id} \}$. The only non-prime attribute is $\text{reg\_date}$, which depends on the full pair $(\text{user\_id}, \text{event\_id})$ (the timestamp when that specific student enrolled in that specific event).
* **Conclusion:** The decomposition strictly satisfies **2NF**.

---

### 4.3 Third Normal Form (3NF)

**Definition:** A relation $R$ is in 3NF if it is in 2NF and for every non-trivial functional dependency $X \rightarrow Y$, at least one of the following conditions holds:
1. $X$ is a superkey of $R$, OR
2. $Y$ is a prime attribute (member of a candidate key) of $R$.

* **Transitive Dependency Check:**
  * In $R_1$: Functional dependencies are $\text{user\_id} \rightarrow \text{user\_dept}$ and $\text{user\_dept} \not\rightarrow \text{user\_id}$. If department had associated attributes like `dept_head_name` or `dept_building`, then $\text{user\_id} \rightarrow \text{dept\_name} \rightarrow \text{dept\_head}$ would create a transitive dependency. However, CampusConnect treats `department` as a scalar classification string on the user entity, exactly like a title. No secondary functional dependency exists among non-prime attributes.
  * In $R_2$: Every dependency $X \rightarrow Y$ has $X = \text{event\_id}$ or $X = \{ \text{event\_title}, \text{venue}, \text{event\_dt} \}$. Both determinants are superkeys.
  * In $R_3$: Dependencies are $\text{reg\_id} \rightarrow \text{user\_id}, \text{event\_id}, \text{reg\_date}$ and $\{ \text{user\_id}, \text{event\_id} \} \rightarrow \text{reg\_id}, \text{reg\_date}$. Both determinants are superkeys.
* **Conclusion:** The schema strictly satisfies **3NF**.

---

### 4.4 Boyce-Codd Normal Form (BCNF)

**Definition:** A relation $R$ is in BCNF if for every non-trivial functional dependency $X \rightarrow Y$, $X$ is a **superkey** of $R$. (Unlike 3NF, BCNF does not permit the exception where $Y$ is a prime attribute).

* **Verification of All Functional Dependencies:**
  * In `users`:
    * $\text{id} \rightarrow \text{name}, \text{email}, \text{password}, \text{role}, \text{department}$ ($\text{id}$ is a superkey $\checkmark$).
    * $\text{email} \rightarrow \text{id}, \text{name}, \text{password}, \text{role}, \text{department}$ ($\text{email}$ is a unique key, therefore a superkey $\checkmark$).
  * In `events`:
    * $\text{id} \rightarrow \text{title}, \text{description}, \text{category}, \text{date\_time}, \text{venue}, \text{registration\_link}, \text{image\_url}, \text{status}$ ($\text{id}$ is a superkey $\checkmark$).
    * $\{ \text{title}, \text{venue}, \text{date\_time} \} \rightarrow \text{id}, \dots$ (Composite determinant is a superkey $\checkmark$).
  * In `registrations`:
    * $\text{id} \rightarrow \text{user\_id}, \text{event\_id}, \text{registration\_date}$ ($\text{id}$ is a superkey $\checkmark$).
    * $\{ \text{user\_id}, \text{event\_id} \} \rightarrow \text{id}, \text{registration\_date}$ ($\{ \text{user\_id}, \text{event\_id} \}$ is backed by `UNIQUE KEY uk_user_event`, hence a superkey $\checkmark$).
* **Conclusion:** Every left-hand side determinant across the entire relational schema is a superkey. Therefore, the CampusConnect production schema is in **Boyce-Codd Normal Form (BCNF)**.

---

## 5. Formal Proofs of Relational Properties

### 5.1 Lossless Join Decomposition Proof

Let $R = \mathcal{U}$ be decomposed into $R_1(\text{users})$, $R_2(\text{events})$, and $R_3(\text{registrations})$.

**Theorem (Lossless Join):** A decomposition of $R$ into $R_A$ and $R_B$ is lossless with respect to a set of functional dependencies $\mathcal{F}$ if and only if:
$$(R_A \cap R_B) \rightarrow R_A \quad \text{OR} \quad (R_A \cap R_B) \rightarrow R_B$$

1. **Step 1:** Consider $R_{12} = R_1 \cup R_2$ and $R_3$.
   * $R_1 \cap R_3 = \{ \text{user\_id} \}$.
   * Since $\text{user\_id} \rightarrow R_1$, $(R_1 \cap R_3) \rightarrow R_1$.
   * Therefore, natural join $R_1 \bowtie R_3$ is guaranteed lossless.
2. **Step 2:** Consider $(R_1 \bowtie R_3)$ and $R_2$.
   * $(R_1 \bowtie R_3) \cap R_2 = \{ \text{event\_id} \}$.
   * Since $\text{event\_id} \rightarrow R_2$, $((R_1 \bowtie R_3) \cap R_2) \rightarrow R_2$.
   * Therefore, natural join $(R_1 \bowtie R_3) \bowtie R_2$ is guaranteed lossless.

$$\Pi_{R_1}(\mathcal{U}) \bowtie \Pi_{R_2}(\mathcal{U}) \bowtie \Pi_{R_3}(\mathcal{U}) = \mathcal{U}$$
No spurious tuples can ever be generated.

---

### 5.2 Dependency Preservation Proof

**Theorem:** A decomposition $D = \{ R_1, R_2, \dots, R_k \}$ is dependency preserving if:
$$(\mathcal{F}_1 \cup \mathcal{F}_2 \cup \dots \cup \mathcal{F}_k)^+ = \mathcal{F}^+$$
where $\mathcal{F}_i = \pi_{R_i}(\mathcal{F})$ is the projection of functional dependencies onto $R_i$.

* $\mathcal{F}_1$ on `users` preserves:
  * $\text{id} \rightarrow \text{name}, \text{email}, \text{password}, \text{role}, \text{department}$
  * $\text{email} \rightarrow \text{id}, \dots$
* $\mathcal{F}_2$ on `events` preserves:
  * $\text{id} \rightarrow \text{title}, \text{description}, \text{category}, \text{date\_time}, \text{venue}, \text{registration\_link}, \text{image\_url}, \text{status}$
  * $\{ \text{title}, \text{venue}, \text{date\_time} \} \rightarrow \text{id}$
* $\mathcal{F}_3$ on `registrations` preserves:
  * $\text{id} \rightarrow \text{user\_id}, \text{event\_id}, \text{registration\_date}$
  * $\{ \text{user\_id}, \text{event\_id} \} \rightarrow \text{id}, \text{registration\_date}$

Every functional dependency in the minimal cover $\mathcal{F}$ is localized to a single relation and enforced by a `PRIMARY KEY` or `UNIQUE` constraint. No cross-table join is required to verify any functional dependency.
**Conclusion:** The decomposition is **100% dependency-preserving**.

---

## 6. Denormalization Evaluation for Read-Heavy Dashboards

While the core transactional schema is maintained in BCNF, high-traffic production aggregators frequently evaluate deliberate denormalization.

### Evaluated Pattern: Caching `attendee_count` on `events`

```sql
-- Potential Denormalized Schema Option:
ALTER TABLE events ADD COLUMN attendee_count INT DEFAULT 0;
```

* **Pros:** Replaces `COUNT(r.id)` aggregation with a simple scalar index lookup when rendering the catalog.
* **Cons (ACID Risk):** Every concurrent registration or cancellation would require acquiring an exclusive row lock on the `events` table row (`UPDATE events SET attendee_count = attendee_count + 1 WHERE id = ?`). This creates severe transaction serialization bottlenecks and increases deadlock frequency under concurrent registration rushes.
* **Design Decision:** CampusConnect **rejects** storing `attendee_count` as a mutable column on `events`. Instead, CampusConnect preserves strict BCNF and achieves high-performance aggregation through:
  1. Composite B-Tree index `idx_registrations_event_id` allowing index-only counts via `COUNT(id) WHERE event_id = ?`.
  2. Sub-millisecond execution plans verified in `database/sql/aggregations.sql`.
