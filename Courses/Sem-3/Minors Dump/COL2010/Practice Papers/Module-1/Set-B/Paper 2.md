# COL2010 — Introduction to Data Science
## Mid-Semester Examination (Practice) — Module 1: Database Systems
### Set B

**Instructor:** Prof. Maya Ramanath &nbsp;|&nbsp; **Semester:** Diwali Semester, 2026
**Total Marks: 68** &nbsp;|&nbsp; **Time: 90 minutes**

**Instructions:**
- Answer all 15 questions. Marks for each question are indicated alongside it.
- Show all intermediate steps (derivations, closures, traces, query plans) — final answers alone will not receive full credit.
- Write SQL in standard ANSI syntax unless a dialect-specific function is explicitly required.
- Be concise and mathematically precise; avoid long descriptive paragraphs.

---

**Q1. (4 marks) Self-Join — Siblings Query**

Given `People(Name, Age, City, Parent)` (as used for the parent–child relationship discussed in class), write a SQL query using a **self-join** to return all pairs of **siblings** — i.e., pairs of distinct people who share the same value of `Parent`. Make sure each sibling pair is returned only once (not twice in both orders).

---

**Q2. (3 marks) Weak Entity Sets**

Consider an entity set **Treatment** (weak entity, partial key `TreatmentDate`) that exists only in the context of a strong entity set **Patient** (key `PatientID`), connected by an identifying relationship `Undergoes`.

(a) Convert this ER fragment into relational schema(s). Clearly indicate the full (composite) key of the relation corresponding to `Treatment`.
(b) In one line, explain why a weak entity set cannot have a key of its own without reference to its owning strong entity set.

---

**Q3. (5 marks) Datalog Safety**

Consider the following Datalog rule:

```
P(x, y)  :-  R(x, z), x > 5
```

(a) Is this rule **safe**, according to the safety condition discussed in class (every variable in the rule must appear in some non-negated, relational — i.e., non-arithmetic — subgoal)? Justify your answer by checking each variable individually.
(b) If it is unsafe, rewrite the rule (adding at most one relational subgoal) to make it safe, without changing the intended meaning as much as possible.

---

**Q4. (4 marks) UNION vs UNION ALL**

Given `WarehouseInventory(ItemID)` and `ShipmentManifest(ItemID)`:

(a) Write a SQL query using `EXCEPT` (equivalently `MINUS`) to return item IDs that appear in `WarehouseInventory` but **never** in `ShipmentManifest`.
(b) A colleague replaces `UNION` with `UNION ALL` in an unrelated query that combines `WarehouseInventory` and `ShipmentManifest` item IDs. Explain precisely how the result set changes, using the notion of tuple multiplicity.

---

**Q5. (4 marks) First Normal Form**

A poorly designed table `Course(CourseID, CourseName, Instructors)` stores multiple instructor names in a single comma-separated string in the `Instructors` column (e.g., `'Ramanath, Sharma'`).

(a) Explain precisely which part of the definition of 1NF this design violates.
(b) Propose a corrected schema (one or more relations) that resolves the violation, stating the key(s) of each relation.

---

**Q6. (6 marks) Equivalence of Functional Dependency Sets**

Let $S = \{A \to B,\ B \to C\}$ and $T = \{A \to B,\ A \to C,\ B \to C\}$ be two sets of FDs over relation $R(A,B,C)$.

Determine whether $S$ and $T$ are **equivalent** (i.e., $S^+ = T^+$) by checking whether $S \models T$ and $T \models S$. Show the relevant attribute-closure computations used to justify each direction.

---

**Q7. (3 marks) Extensional vs Intensional Predicates**

Given the Datalog rules:

```
Ancestor(x, y)  :-  Parent(x, y)
Ancestor(x, y)  :-  Parent(x, z), Ancestor(z, y)
```

Identify which predicate(s) above are **EDB** (extensional) and which are **IDB** (intensional), and justify each classification in one line.

---

**Q8. (3 marks) NULL Handling**

Given `Shipments(ShipmentID, DepartTime, ArrivalTime)` where `ArrivalTime` may be `NULL` for shipments still in transit, write a SQL query that returns `ShipmentID` and `ArrivalTime`, replacing any `NULL` arrival time with the fixed placeholder timestamp `'9999-12-31 00:00:00'`.

---

**Q9. (6 marks) BCNF vs. 3NF — Overlapping Candidate Keys**

Consider relation `Screening(Movie, Theatre, City)` with the following functional dependencies:

$$Theatre \to City, \qquad Movie,\ City \to Theatre$$

(a) List all candidate keys of `Screening`.
(b) Show that `Screening` satisfies **3NF** but violates **BCNF**. Identify precisely which FD causes the BCNF violation and why the same FD does not violate 3NF.

---

**Q10. (4 marks) Rename in Relational Algebra**

Given `Employee(EmpID, Name, ManagerID)`, where `ManagerID` refers to the `EmpID` of another row in the same table, write a relational algebra expression (using $\rho$, $\pi$, $\bowtie$) to return the **names of managers together with the names of the employees who report to them**. You must use the rename operator to distinguish the two "roles" of the `Employee` relation.

---

**Q11. (3 marks) Relational Algebra → SQL**

Translate the following relational algebra expression into an equivalent SQL query:

$$\pi_{Title}\Big(\sigma_{Language='Telugu' \;\wedge\; Year>2015}(Movie)\Big)$$

---

**Q12. (6 marks) Multivalued Dependencies (4NF) — Conceptual**

A relation `StudentActivity(StudentID, Club, Sport)` records, independently, which clubs a student belongs to and which sports they play (a student's set of clubs has nothing to do with their set of sports). To represent every (club, sport) combination for a student, the table stores one row per (club, sport) pair.

(a) Explain, using the notion of a **multivalued dependency**, why this design causes redundancy even though **no non-trivial functional dependency** holds on `StudentID`. Write the MVD(s) that hold.
(b) Propose a decomposition into two relations that eliminates the redundancy (informally justify why this is a lossless decomposition into 4NF).

---

**Q13. (5 marks) Correlated Subquery — NOT EXISTS vs. NOT IN**

Given `Employees(EmpID, Name)` and `ProjectAssignments(EmpID, ProjectID)`:

(a) Write a correlated subquery using `NOT EXISTS` to find employees who are **not assigned to any project**.
(b) A student instead writes the equivalent query using `NOT IN (SELECT EmpID FROM ProjectAssignments)`. Explain precisely the edge case under which this `NOT IN` version can silently return **zero rows** even when unassigned employees exist, and why `NOT EXISTS` does not have this problem.

---

**Q14. (7 marks) Recursive CTE with Cycle Avoidance**

Consider `ReportsTo(EmployeeID, ManagerID)` representing an organizational hierarchy, where — due to a data-entry error — the table may contain a **cycle** (e.g., X reports to Y, Y reports to Z, and Z reports to X).

Write a `WITH RECURSIVE` SQL query that returns all **downstream subordinates** of a given `start_manager_id`, while guaranteeing termination even if a cycle exists in the data. Your query must explicitly track the path visited so far and must not revisit an `EmployeeID` already on the current path. Briefly explain, in one or two lines, why simple unbounded recursion (without this check) would fail to terminate on cyclic data.

---

**Q15. (5 marks) Armstrong's Axioms — Derivation**

Using only the three basic Armstrong's Axioms (**Reflexivity**, **Augmentation**, **Transitivity**), formally derive the **Union Rule**:

$$\text{If } A \to B \text{ and } A \to C, \text{ then } A \to BC$$

Show each derivation step and state which axiom justifies it.

---

# End of Set B

---

## Answer Key & Marking Scheme

**Q1 (4 marks).**
```sql
SELECT DISTINCT p1.Name AS Sibling1, p2.Name AS Sibling2
FROM People p1 JOIN People p2
  ON p1.Parent = p2.Parent
WHERE p1.Name < p2.Name;
```
- 2 marks correct self-join on `Parent`; 2 marks correct de-duplication technique (e.g., `p1.Name < p2.Name` or equivalent) preventing both orders / self-pairing.

**Q2 (3 marks).**
(a) `Treatment(PatientID, TreatmentDate, ...)` with composite key `(PatientID, TreatmentDate)`; `Patient(PatientID, ...)` with key `PatientID`.
(b) A weak entity's partial key only distinguishes it among treatments *of the same patient* — it is not globally unique, so the owning entity's key must be included to form a full identifying key.
- 1.5 marks each part.

**Q3 (5 marks).**
(a) **Unsafe.** Variable `y` appears only in the head `P(x,y)` and never in any subgoal — it is unbounded (could range over infinitely many values), violating the safety condition. `x` appears in the relational subgoal `R(x,z)` (safe), and the arithmetic atom `x>5` does not by itself make `x` safe (arithmetic atoms don't bind), but `x` is already safe via `R(x,z)`. `z` also appears in `R(x,z)`, safe.
(b) Rewrite: `P(x, y) :- R(x, z), R(x, y), x > 5` (introducing a relational subgoal that binds `y`) — or more generally, any relational subgoal containing `y`.
- 3 marks correct identification of unsafe variable with reasoning per-variable; 2 marks valid fix.

**Q4 (4 marks).**
(a)
```sql
SELECT ItemID FROM WarehouseInventory
EXCEPT
SELECT ItemID FROM ShipmentManifest;
```
(b) `UNION` eliminates duplicate tuples across and within the two input sets (set semantics), so an ItemID appearing in both tables appears **once** in the result. `UNION ALL` uses bag semantics — it does not eliminate duplicates, so the same ItemID would appear **twice** (once from each source), and any ItemID duplicated within a single source retains all its copies too.
- 2 marks correct EXCEPT query; 2 marks correct multiplicity explanation.

**Q5 (4 marks).**
(a) Violates 1NF because the `Instructors` attribute does not hold an **atomic value** — it packs multiple instructor names into a single field, so a tuple does not contain one atomic value per attribute.
(b) Decompose into `Course(CourseID, CourseName)` [key: `CourseID`] and `Teaches(CourseID, InstructorName)` [key: `(CourseID, InstructorName)`].
- 2 marks each part.

**Q6 (6 marks).**
Check $S \models T$: Does $S^+$ contain $A \to C$? Compute $\{A\}^+$ under $S$: start $\{A\}$; apply $A\to B$: $\{A,B\}$; apply $B \to C$: $\{A,B,C\}$. So $A \to C$ is derivable from $S$ ⇒ $S \models A\to C$. The other FDs of $T$ ($A\to B$, $B\to C$) are already in $S$. So $S \models T$.
Check $T \models S$: $S = \{A\to B, B\to C\}$, both of which are explicitly present in $T$. So trivially $T \models S$.
Since $S \models T$ and $T \models S$, $S^+ = T^+$ ⇒ **$S$ and $T$ are equivalent.**
- 3 marks per direction (closure computation + correct conclusion).

**Q7 (3 marks).**
`Parent` is **EDB** — it corresponds to a stored/base relation with actual data. `Ancestor` is **IDB** — it is a derived/virtual relation, defined recursively via rules, and not directly stored.
- 1.5 marks each, with correct one-line justification.

**Q8 (3 marks).**
```sql
SELECT ShipmentID, COALESCE(ArrivalTime, '9999-12-31 00:00:00') AS ArrivalTime
FROM Shipments;
```
- Full marks for correct use of `COALESCE` with the given placeholder.

**Q9 (6 marks).**
(a) Candidate keys: $\{Theatre, Movie\}$ (since $Theatre \to City$, closure of $\{Theatre,Movie\}$ = all attributes) and $\{Movie, City\}$ (since $Movie,City \to Theatre$, closure = all attributes). Both are minimal ⇒ two candidate keys.
(b) For 3NF: check $Theatre \to City$ — $Theatre$ alone is not a superkey, **but** $City$ is a prime attribute (it is part of the candidate key $\{Movie, City\}$), so the FD satisfies the 3NF exception clause ("Y is prime") ⇒ **3NF is not violated**. For BCNF: the same FD $Theatre \to City$ requires $Theatre$ itself to be a superkey (BCNF has no "prime attribute" exception) — since $Theatre$ alone is not a superkey, this **violates BCNF**.
- 3 marks candidate keys; 3 marks correct 3NF-satisfied / BCNF-violated distinction with the specific FD and reasoning.

**Q10 (4 marks).**
$$\pi_{ManagerName,\ EmpName}\Big(\rho_{Mgr(ManagerID,\,ManagerName,\,\_)}(Employee) \;\bowtie_{Mgr.ManagerID = Emp.ManagerID}\; \rho_{Emp(EmpID,\,EmpName,\,ManagerID)}(Employee)\Big)$$
(Accept any equivalent expression that renames `Employee` twice — once playing the "manager" role via `EmpID`, once playing the "subordinate" role via `ManagerID` — and joins on `Mgr.EmpID = Emp.ManagerID`.)
- 2 marks correct use of $\rho$ to create two roles; 2 marks correct join condition and projection.

**Q11 (3 marks).**
```sql
SELECT Title
FROM Movie
WHERE Language = 'Telugu' AND Year > 2015;
```
- Full marks for correct WHERE clause and projection.

**Q12 (6 marks).**
(a) `StudentID` multi-determines `Club` and, independently, multi-determines `Sport`: this is written as the multivalued dependency $StudentID \twoheadrightarrow Club$ (equivalently $StudentID \twoheadrightarrow Sport$, since they are complementary). Because `Club` and `Sport` vary independently for a given student, storing every combination in one table forces every club to be paired with every sport for that student, producing redundant rows (this is exactly the "clubbing together many-many relationships" scenario flagged in class as a source of redundancy even with no non-trivial FD present).
(b) Decompose into `StudentClub(StudentID, Club)` and `StudentSport(StudentID, Sport)`. This is lossless because rejoining the two relations via natural join on `StudentID` reconstructs exactly the original Cartesian combinations per student (the defining property of an MVD-based decomposition), and each resulting relation is trivially in 4NF (only trivial MVDs remain).
- 3 marks correct MVD identification/notation and reasoning; 3 marks correct decomposition with lossless justification.

**Q13 (5 marks).**
(a)
```sql
SELECT e.EmpID, e.Name
FROM Employees e
WHERE NOT EXISTS (
  SELECT 1 FROM ProjectAssignments pa WHERE pa.EmpID = e.EmpID
);
```
(b) If the subquery's result set `(SELECT EmpID FROM ProjectAssignments)` contains **even a single NULL** `EmpID` value, then for *every* outer row, the `NOT IN` comparison becomes `EmpID <> value1 AND EmpID <> ... AND EmpID <> NULL`; the comparison against `NULL` evaluates to `UNKNOWN`, which makes the entire `AND` chain `UNKNOWN` rather than `TRUE`, so **no rows at all** satisfy the `WHERE` clause — silently returning zero rows regardless of the actual data. `NOT EXISTS` does not have this problem because it only checks for the existence of matching rows and never compares against a `NULL` value directly.
- 2 marks correct `NOT EXISTS` query; 3 marks correct and precise NULL-related explanation of the `NOT IN` failure mode.

**Q14 (7 marks).**
```sql
WITH RECURSIVE Downstream(EmployeeID, ManagerID, path) AS (
  SELECT EmployeeID, ManagerID, CAST(EmployeeID AS VARCHAR(1000))
  FROM ReportsTo
  WHERE ManagerID = :start_manager_id

  UNION ALL

  SELECT r.EmployeeID, r.ManagerID, d.path || ',' || r.EmployeeID
  FROM ReportsTo r
  JOIN Downstream d ON r.ManagerID = d.EmployeeID
  WHERE d.path NOT LIKE '%' || r.EmployeeID || '%'
)
SELECT DISTINCT EmployeeID FROM Downstream;
```
Explanation: without the `path`-tracking / "not already visited" check, a cycle (X→Y→Z→X) would cause the recursive term to keep re-deriving the same rows indefinitely (each pass along the cycle produces "new" path-extended tuples even though the set of `EmployeeID`s stabilizes), so the recursive CTE would never reach a fixpoint and would run forever (or hit an engine-imposed recursion limit).
- 4 marks correct recursive query with explicit path tracking and cycle check; 3 marks correct explanation of non-termination without it.

**Q15 (5 marks).**
Given: $A \to B$ and $A \to C$.
1. From $A \to B$, apply **Augmentation** (add $A$ to both sides): $AA \to AB$, i.e., $A \to AB$.
2. From $A \to C$, apply **Augmentation** (add $B$ to both sides): $AB \to BC$.
3. From step 1 ($A \to AB$) and step 2 ($AB \to BC$), apply **Transitivity**: $A \to BC$. $\blacksquare$
- 2 marks correct use of Augmentation (both applications); 2 marks correct use of Transitivity to combine; 1 mark for correctly stating which axiom justifies each step.

---

### Topic/Difficulty Coverage Log (cumulative — for Set C onward)

| # | Topic | Set |
|---|---|---|
| Self-join for siblings/parallel relationship | B |
| Weak entity set conversion | B |
| Datalog safety (arithmetic atom, unbound variable) | B |
| UNION vs UNION ALL / EXCEPT | B |
| 1NF violation (non-atomic multi-valued field) | B |
| FD-set equivalence via mutual closure | B |
| EDB vs IDB classification | B |
| NULL handling with COALESCE | B |
| BCNF vs 3NF with overlapping candidate keys | B |
| Rename operator for self-referential role-join | B |
| RA → SQL translation | B |
| Multivalued dependency / 4NF reasoning | B |
| NOT EXISTS vs NOT IN (NULL pitfall) | B |
| Recursive CTE with explicit cycle avoidance | B |
| Armstrong's Axioms formal derivation (Union rule) | B |

*(Set A topics — ER many-one w/ relationship attribute, attribute-closure/candidate-key check, bag algebra union/difference identity, RA composition, candidate vs primary key, GROUP BY/HAVING + scalar subquery, BCNF decomposition (single-key case), SQL join+ORDER BY, N-ary→binary conversion, recursive CTE fixpoint trace (acyclic), DDL CREATE TABLE, window functions, Datalog stratification, join tuple-count bounds, 2NF/3NF diagnosis — are excluded from Set B and should likewise be excluded from Set C.)*
