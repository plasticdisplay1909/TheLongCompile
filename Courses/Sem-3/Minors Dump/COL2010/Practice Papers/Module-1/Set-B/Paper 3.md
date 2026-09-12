# COL2010 — Introduction to Data Science
## Mid-Semester Examination (Practice) — Module 1: Database Systems
### Set C

**Instructor:** Prof. Maya Ramanath &nbsp;|&nbsp; **Semester:** Diwali Semester, 2026
**Total Marks: 68** &nbsp;|&nbsp; **Time: 90 minutes**

**Instructions:**
- Answer all 15 questions. Marks for each question are indicated alongside it.
- Show all intermediate steps (derivations, closures, traces, query plans) — final answers alone will not receive full credit.
- Write SQL in standard ANSI syntax unless a dialect-specific function is explicitly required.
- Be concise and mathematically precise; avoid long descriptive paragraphs.

---

**Q1. (7 marks) Recursive Datalog — Same-Generation Query**

Consider `Parent(parent, child)` representing a family tree. Define `SameGen(x, y)` to mean "$x$ and $y$ are at the same generation" (e.g., two cousins, or two siblings, are the same generation; a parent and child are not).

(a) Write Datalog rules for `SameGen(x, y)`, using a base case (every person is the same generation as themself) and a recursive case (in terms of `Parent`).
(b) Translate your Datalog rules into an equivalent `WITH RECURSIVE` SQL query over `Parent(parent, child)`.

---

**Q2. (3 marks) General ER Constraints**

The relationship `Register(Students, Courses)` in the lecture slides was annotated with a constraint "≤ 4", meaning **each student may register for at most 4 courses**.

(a) Explain why this constraint is a **general constraint** and not simply a key constraint or a referential-integrity constraint.
(b) Give one example each (for any schema of your choice) of a **domain constraint** and a **referential integrity constraint**, clearly distinguishing the two.

---

**Q3. (4 marks) INTERSECT vs. AND**

Given `Shipments(ShipmentID, DepartTime, ArrivalTime)`:

(a) Write a query using `INTERSECT` that returns shipments departing after `'2026-01-01'` **and** arriving before `'2026-06-01'`, by intersecting two separate `SELECT` statements.
(b) Rewrite the same query as a single `SELECT` using `AND` in the `WHERE` clause.
(c) Describe one situation (in terms of the columns being selected, or the tables involved) where an `INTERSECT` of two queries is **not** equivalent to combining their conditions with `AND` in a single query.

---

**Q4. (6 marks) Negation and Recursion — Non-Unique Fixpoints**

Let `R(ATTR)` be an EDB relation with a single fact `R(0)`. Consider the following recursive Datalog rules involving negation:

```
P(x)  :-  R(x), NOT Q(x)
Q(x)  :-  R(x), NOT P(x)
```

(a) Is `0` in `P`, in `Q`, or in neither, according to the least-fixpoint semantics? Show that **more than one fixpoint** is consistent with these rules (i.e., that the least fixpoint is not uniquely determined).
(b) Explain, using the definition of **stratified negation**, why this particular rule set cannot be stratified, and how stratification (when it is possible) guarantees a unique result.

---

**Q5. (3 marks) SQL — CASE WHEN Classification**

Given `Employees(EmpID, YearsOfService)`, write a SQL query that returns `EmpID` and a new column `Tenure_Tier`, using `CASE WHEN` to label each employee as `'Senior'` if `YearsOfService >= 10`, `'Mid-Level'` if between 3 and 9 (inclusive), and `'Junior'` otherwise.

---

**Q6. (5 marks) Referential Integrity Check via EXISTS**

Given `Shipments(ShipmentID, RouteID, ...)` and `Routes(RouteID, ...)`, suppose the database was populated carelessly and some `Shipments.RouteID` values do not exist in `Routes` (a referential-integrity violation, even though no `FOREIGN KEY` constraint was declared). Write a SQL query using `NOT EXISTS` (a correlated subquery) that returns all `ShipmentID`s with such **dangling** `RouteID` references.

---

**Q7. (6 marks) Lossless-Join Decomposition Test**

Let $R(A, B, C, D)$ have functional dependencies $A \to B$ and $A \to C$. It is decomposed into $R_1(A, B)$ and $R_2(A, C, D)$.

Apply the formal **lossless-join test**: a decomposition of $R$ into $R_1, R_2$ is lossless if and only if $(R_1 \cap R_2) \to R_1$ or $(R_1 \cap R_2) \to R_2$ holds (i.e., the common attributes functionally determine at least one of the two pieces). Compute $R_1 \cap R_2$, check both directions using attribute closure, and state your final conclusion.

---

**Q8. (3 marks) Relational Algebra — Grouping/Aggregation Notation**

Given `Routes(RouteID, transport_mode, distance_km)`, write a relational algebra expression using the grouping operator $\gamma$ to compute the **average distance per transport mode**. Then write the equivalent SQL query.

---

**Q9. (5 marks) Theta Join — Budget Violation Detection**

Given `Employees(EmpID, Salary, DeptID)` and `DeptBudget(DeptID, MaxSalary)`, write:

(a) A relational algebra expression using a **theta join** ($\bowtie_\theta$, with a non-equality condition) to find all (Employee, DeptBudget) pairs where the employee's salary **exceeds** the maximum salary allowed for their department.
(b) The equivalent SQL query.

---

**Q10. (7 marks) Recursive CTE — Minimum-Cost Bounded Path**

Given `RouteEdge(source, dest, cost)`:

| source | dest | cost |
|---|---|---|
| X | Y | 10 |
| Y | Z | 15 |
| X | Z | 30 |
| Y | W | 5 |
| W | Z | 8 |

Write a `WITH RECURSIVE` SQL query that computes the **minimum cumulative cost** to travel from node `X` to node `Z`, considering paths of **at most 3 hops**. Trace your query on the data above and state the resulting minimum cost, showing which path achieves it.

---

**Q11. (4 marks) Trivial vs. Non-Trivial Functional Dependencies**

For relation $R(A, B, C)$ with the functional dependency set $\{AB \to ABC,\ B \to B,\ AB \to C\}$, classify **each** of the three FDs as **trivial** or **non-trivial**, using the formal definition: an FD $X \to Y$ is trivial if and only if $Y \subseteq X$.

---

**Q12. (4 marks) Domain and Single-Value Constraints**

Given `Actor(Name, Age, Birthplace)`:

(a) State a **domain constraint** on `Age` and show how it would be expressed as a SQL `CHECK` constraint in a `CREATE TABLE` statement.
(b) Explain what it means for `Birthplace` to satisfy a **single-value constraint**, and why the basic relational model already enforces this for every attribute by definition (i.e., what would have to be true of the data for this constraint to be violated).

---

**Q13. (4 marks) SQL — String Manipulation**

Given `Employees(EmpID INT, DeptName VARCHAR, FullName VARCHAR)`, write a SQL query that builds an `EmployeeCode` column by concatenating: the **first 3 uppercase letters** of `DeptName`, a hyphen, and `EmpID` **zero-padded to 5 digits** (e.g., Department `'sales'`, EmpID `42` → `'SAL-00042'`). You may use `UPPER`, `SUBSTR`/`SUBSTRING`, `LPAD` (or equivalent string functions), and `||` (or `CONCAT`).

---

**Q14. (3 marks) Superkey vs. Key — Formal Justification**

For relation $R(A, B, C, D)$ with the single functional dependency $A \to BCD$, give **one** superkey that is **not** minimal and **one** superkey that **is** minimal (i.e., a key), and formally justify each using the definition of "functionally determines all attributes" and "minimality."

---

**Q15. (4 marks) Cross Join — Cardinality and Pitfalls**

Given `Node` with 5 rows and `Item` with 8 rows:

(a) State the number of rows produced by `Node CROSS JOIN Item`.
(b) Give one legitimate use case for a deliberate `CROSS JOIN` in this schema (e.g., enumerating theoretical allocation pairs), and one common **pitfall** where a query unintentionally becomes a cross join (in terms of a missing clause).

---

# End of Set C

---

## Answer Key & Marking Scheme

**Q1 (7 marks).**
(a)
```
SameGen(x, x)  :-  Parent(_, x)          % base case: everyone is same-gen as self
SameGen(x, y)  :-  Parent(px, x), Parent(py, y), SameGen(px, py)
```
(b)
```sql
WITH RECURSIVE SameGen(x, y) AS (
  SELECT DISTINCT child AS x, child AS y FROM Parent
  UNION
  SELECT p1.child, p2.child
  FROM Parent p1, Parent p2, SameGen sg
  WHERE p1.parent = sg.x AND p2.parent = sg.y
)
SELECT * FROM SameGen;
```
- 3 marks correct base + recursive Datalog rules; 4 marks correct recursive SQL translation (correct join pattern between `Parent` and the recursive `SameGen` relation).

**Q2 (3 marks).**
(a) It is neither a key constraint (it doesn't identify entities uniquely) nor referential integrity (it doesn't concern existence of a referenced value) — it restricts the **cardinality of a relationship instance** (how many `Courses` a given `Student` may participate in), which falls outside the standard "key / single-value / referential integrity / domain" categories and must be captured as a **general constraint**.
(b) Domain constraint example: `Age` must be between 0 and 100. Referential integrity example: every `DeptCode` in `Employee` must exist in `Department`. The domain constraint restricts a single attribute's value range; referential integrity restricts a value to match an existing key elsewhere.
- 1.5 marks each part.

**Q3 (4 marks).**
(a)
```sql
SELECT * FROM Shipments WHERE DepartTime > '2026-01-01'
INTERSECT
SELECT * FROM Shipments WHERE ArrivalTime < '2026-06-01';
```
(b)
```sql
SELECT * FROM Shipments
WHERE DepartTime > '2026-01-01' AND ArrivalTime < '2026-06-01';
```
(c) They stop being equivalent once the two `SELECT`s project **different columns** (INTERSECT requires identical, union-compatible schemas, so it cannot combine conditions from queries returning different attribute sets) or draw from **different tables** entirely — a single `AND`-combined query only works when all conditions apply to the *same* row of the *same* table/join.
- 1 mark each for (a) and (b); 2 marks for a valid non-equivalence scenario in (c).

**Q4 (6 marks).**
(a) Two fixpoints are both self-consistent: **Fixpoint 1** — $P = \{0\}, Q = \{\}$: check rule for `P`: `R(0)` true, `NOT Q(0)` true (since $Q=\emptyset$) ⇒ $0\in P$ consistent. Check rule for `Q`: `R(0)` true, `NOT P(0)` false (since $0\in P$) ⇒ $0\notin Q$ consistent. **Fixpoint 2** — $P=\{\}, Q=\{0\}$: symmetric argument also self-consistent. Since both assignments simultaneously satisfy the rules, the least fixpoint is **not unique** — the semantics is ambiguous without further restriction.
(b) The predicate-dependency graph has $P \to Q$ (labelled `–`, since `Q` is negated in `P`'s rule) and $Q \to P$ (labelled `–`, since `P` is negated in `Q`'s rule) — this is a cycle **containing a negated edge**, which stratified negation explicitly disallows (no negation is permitted within a mutually recursive cycle). Because no valid stratum ordering exists, the rules cannot be stratified. When stratification *is* possible, each stratum is evaluated fully before moving to the next, so every negated predicate is completely and unambiguously computed before it is referenced — guaranteeing a single, unique fixpoint.
- 3 marks for correctly demonstrating both fixpoints with justification; 3 marks for correct stratification argument.

**Q5 (3 marks).**
```sql
SELECT EmpID,
  CASE
    WHEN YearsOfService >= 10 THEN 'Senior'
    WHEN YearsOfService >= 3  THEN 'Mid-Level'
    ELSE 'Junior'
  END AS Tenure_Tier
FROM Employees;
```
- Full marks for correct `CASE WHEN` ordering and boundary handling.

**Q6 (5 marks).**
```sql
SELECT s.ShipmentID
FROM Shipments s
WHERE NOT EXISTS (
  SELECT 1 FROM Routes r WHERE r.RouteID = s.RouteID
);
```
- Full marks for correct correlated `NOT EXISTS` structure identifying dangling references.

**Q7 (6 marks).**
$R_1 \cap R_2 = \{A\}$. Check direction 1: does $A \to R_1$ (i.e., $A \to \{A,B\}$)? Compute $\{A\}^+$: given $A\to B$, $\{A\}^+ \supseteq \{A,B\}$ ⇒ yes, $A \to \{A,B\}$ holds, so $A \to R_1$. (Direction 2 need not even be checked, since one direction already suffices, but for completeness: does $A \to R_2$, i.e., $A \to \{A,C,D\}$? We have $A \to C$ but no FD gives $A \to D$, so this direction fails — consistent with direction 1 already succeeding.)
**Conclusion: the decomposition is lossless**, since $(R_1\cap R_2) \to R_1$ holds.
- 2 marks correct intersection; 3 marks correct closure computation for at least one direction; 1 mark correct final conclusion.

**Q8 (3 marks).**
$$\gamma_{transport\_mode,\ AVG(distance\_km)}(Routes)$$
```sql
SELECT transport_mode, AVG(distance_km)
FROM Routes
GROUP BY transport_mode;
```
- 1.5 marks each for correct RA and SQL.

**Q9 (5 marks).**
(a)
$$Employees \bowtie_{Employees.DeptID = DeptBudget.DeptID \;\wedge\; Salary > MaxSalary} DeptBudget$$
(b)
```sql
SELECT e.*, d.*
FROM Employees e JOIN DeptBudget d
  ON e.DeptID = d.DeptID
WHERE e.Salary > d.MaxSalary;
```
- 2.5 marks each for correct RA theta-join notation and correct SQL with matching join + inequality condition.

**Q10 (7 marks).**
```sql
WITH RECURSIVE PathCost(node, cost, hops) AS (
  SELECT dest, cost, 1 FROM RouteEdge WHERE source = 'X'
  UNION ALL
  SELECT re.dest, pc.cost + re.cost, pc.hops + 1
  FROM RouteEdge re
  JOIN PathCost pc ON re.source = pc.node
  WHERE pc.hops < 3
)
SELECT MIN(cost) FROM PathCost WHERE node = 'Z';
```
Trace: hop 1: X→Y (10), X→Z (30). Hop 2 (from Y, hops<3): Y→Z (10+15=25), Y→W (10+5=15). Hop 3 (from W, hops<3): W→Z (15+8=23). Candidates reaching `Z`: 30 (direct), 25 (via Y), 23 (via Y→W). **Minimum cost = 23**, achieved by path **X → Y → W → Z**.
- 4 marks correct recursive query with hop bound; 3 marks correct trace identifying minimum cost and path.

**Q11 (4 marks).**
- $AB \to ABC$: **non-trivial** — RHS $\{A,B,C\} \not\subseteq$ LHS $\{A,B\}$ (specifically $C$ is not in the LHS).
- $B \to B$: **trivial** — RHS $\{B\} \subseteq$ LHS $\{B\}$.
- $AB \to C$: **non-trivial** — RHS $\{C\} \not\subseteq$ LHS $\{A,B\}$.
- ~1.3 marks per correct classification with justification.

**Q12 (4 marks).**
(a) Domain constraint: `Age` must lie in $[0, 100]$.
```sql
CREATE TABLE Actor (
  Name VARCHAR(100),
  Age INT CHECK (Age >= 0 AND Age <= 100),
  Birthplace VARCHAR(100)
);
```
(b) A single-value constraint on `Birthplace` means each `Actor` tuple may record **exactly one** birthplace value, not a set of possible birthplaces. This is automatically enforced by the relational model's requirement that every attribute hold a single atomic value per tuple (1NF) — it would only be "violated" if someone tried to store multiple birthplaces for one actor in a single row (e.g., by packing them into one field or by allowing multiple rows to represent "alternatives" for the same actor without a clear semantic distinction).
- 2 marks each part.

**Q13 (4 marks).**
```sql
SELECT EmpID, DeptName, FullName,
  UPPER(SUBSTR(DeptName, 1, 3)) || '-' || LPAD(CAST(EmpID AS VARCHAR), 5, '0') AS EmployeeCode
FROM Employees;
```
- 2 marks correct department-prefix construction (`UPPER` + `SUBSTR`); 2 marks correct zero-padding of `EmpID` and correct concatenation.

**Q14 (3 marks).**
- Non-minimal superkey: $\{A, B\}$ — its closure $\{A,B\}^+ = \{A,B,C,D\}$ (via $A\to BCD$) covers all attributes, so it is a superkey, but the proper subset $\{A\}$ alone already has closure $\{A,B,C,D\}$, so $\{A,B\}$ is **not minimal**.
- Minimal superkey (a key): $\{A\}$ — $\{A\}^+ = \{A,B,C,D\}$ = all attributes, and no proper subset of $\{A\}$ (i.e., $\emptyset$) can determine all attributes, so $\{A\}$ is minimal ⇒ it is a **key**.
- 1.5 marks each, with correct closure-based justification.

**Q15 (4 marks).**
(a) $5 \times 8 = 40$ rows.
(b) Legitimate use: generating every theoretical `(Node, Item)` allocation pair as a candidate space before filtering by actual inventory/capacity constraints. Pitfall: omitting the `ON`/`WHERE` join condition between two tables in a query (e.g., writing `SELECT * FROM Node, Item` with no linking predicate) unintentionally produces a full cross join instead of the intended matched pairs.
- 1 mark cardinality; 1.5 marks each for use case and pitfall.

---

### Final Cumulative Topic Log — Sets A, B, C (Module 1: Databases)

All core sub-topics from the lecture notes, HW1, and Quiz 1 have now been distributed across three non-overlapping sets:

- **ER Modeling:** many-one w/ relationship attribute (A), weak entities (B), N-ary→binary conversion (A), general/domain/referential-integrity constraints (C).
- **Relational Model & Keys:** candidate vs. primary key (A), superkey vs. key formal proof (C), trivial/non-trivial FDs (C).
- **FD Theory:** attribute closure (A), Armstrong's Axioms derivation (B), FD-set equivalence (B), lossless-join test (C).
- **Normalization:** BCNF decomposition — single key (A), BCNF-vs-3NF overlapping keys (B), 1NF violation (B), MVD/4NF (B).
- **Relational Algebra:** composition/π-σ-⋈ (A), rename ρ (B), grouping γ (C), theta join (C), cross join semantics (C).
- **SQL — Core:** joins + sort (A), GROUP BY/HAVING + subquery (A), window functions (A), DDL (A), CASE WHEN (C), string functions (C).
- **SQL — Sets & Nulls:** UNION/EXCEPT (B), INTERSECT vs AND (C), COALESCE (B), NOT EXISTS vs NOT IN (B), EXISTS-based integrity check (C).
- **Recursive SQL / Datalog:** fixpoint trace — acyclic (A), cycle-avoidance in recursion (B), safety (B), stratification (A), EDB/IDB (B), same-generation query (C), non-unique fixpoints under negation (C), bounded shortest-path recursion (C).
- **Bag vs. Set Semantics:** bag algebra identity proof (A), join tuple-count bounds (A), cross-join cardinality (C).

No question, scenario, or numeric example is repeated across Sets A, B, and C.
