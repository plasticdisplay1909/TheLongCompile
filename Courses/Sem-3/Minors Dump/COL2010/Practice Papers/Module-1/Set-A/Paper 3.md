# COL2010 — Introduction to Data Science
## Mid-Term Examination — Mock Paper 3
**Module 1: Database Systems** | Instructor: Maya Ramanath | Diwali Semester, 2026

**Total Marks: 59** | **Time: 2 Hours**

### Instructions
- Attempt **all** questions.
- Marks for each question/part are indicated alongside it.
- Where a proof, algorithm, or multi-iteration derivation is required, you must show all intermediate steps — final answers alone will not receive full credit.
- A few questions (ISA hierarchies, MVDs/4NF) extend slightly beyond the core lecture slides into standard textbook material flagged for self-study; reason from first principles using the definitions given in the question.
- State any additional assumptions clearly.

---

**Q1.** [4 Marks]
Let $R(A,B) $ and $S(B,C)$. A student claims the following relational-algebra equivalence always holds:
$$\sigma_{A>10}(R \Join S) \;=\; \sigma_{A>10}(R) \Join S$$
(a) [2] Prove this equivalence holds whenever the selection condition refers only to attributes of $R$, using the definition of natural join and selection.
(b) [2] Give a concrete counterexample showing the equivalence **fails** if the condition is instead $\sigma_{A>10 \,\wedge\, C<5}(R \Join S)$ pushed entirely to $\sigma_{A>10\,\wedge\,C<5}(R) \Join S$ — i.e., explain precisely why a condition spanning both relations cannot be pushed below the join in this way.

---

**Q2.** [2 Marks]
Naive (bottom-up) evaluation of a recursive Datalog program over a database with a **finite** domain of constants is guaranteed to terminate. Give a short, formal argument for this, referencing (i) the monotonicity of the rules (no negation) and (ii) the finiteness of the space of possible IDB tuples.

---

**Q3.** [6 Marks]
Consider `OrderRouting(OrderID, WarehouseID, RegionID, CountryID)` with the functional dependencies:
$$OrderID \rightarrow WarehouseID, \qquad WarehouseID \rightarrow RegionID, \qquad RegionID \rightarrow CountryID$$
Consider the decomposition $D = \{\, R_1(OrderID, WarehouseID),\ R_2(WarehouseID, RegionID),\ R_3(RegionID, CountryID) \,\}$.
For each $R_i \in D$, compute the projection of $F$ onto $R_i$'s attributes, $\Pi_{R_i}(F)$ (i.e., attribute closure restricted to that schema). Using these projections, determine whether $D$ is **dependency-preserving**, showing your closure computations explicitly.

---

**Q4.** [3 Marks]
An entity set `Machine(MachineID, Type)` is related to `Technician(TechID, Name)` via a relationship `Services`, carrying attributes `ServiceDate` and `Cost`. Every machine must be serviced by **at least one** technician at some point (total participation of `Machine` in `Services`), but a technician need not service any machine (partial participation of `Technician`). Draw (describe in words) how you would annotate this ER diagram with participation constraints, and give the relational schema(s) that result from mapping `Services` to a relation, following the convention taught in class.

---

**Q5.** [6 Marks]
The EDB relation `Prereq(Course, Requires)` records direct prerequisites:
$$\text{(CS301, CS201), (CS201, CS101), (CS401, CS301)}$$
Two IDB predicates are defined:
```
AllPrereqs(C, P) :- Prereq(C, P).
AllPrereqs(C, P) :- Prereq(C, X), AllPrereqs(X, P).

DeepCourse(C) :- AllPrereqs(C, P1), AllPrereqs(P1, P2).
```
Using naive least-fixedpoint evaluation, compute `AllPrereqs` after each iteration until it stabilizes, and then compute the final contents of `DeepCourse` (which depends on the fully-evaluated `AllPrereqs`). Show all intermediate iterations.

---

**Q6.** [2 Marks]
`GymVisit(MemberID, VisitMonth)` records which members visited the gym in a given month. Write a single SQL query using `EXCEPT` to find all members who visited in `'Jan'` but did **not** visit in `'Feb'`.

---

**Q7.** [4 Marks]
An `AutoRent` rental agency models its fleet with entity set `Vehicle(VIN, Make, Model)` specialized (ISA) into three subclasses: `Car(NumDoors)`, `Truck(CargoCapacity)`, and `Motorcycle(EngineCC)` — every vehicle in the fleet is exactly one of these three types.
(a) [2] State, with justification, whether this ISA hierarchy should be modelled as **disjoint or overlapping**, and as **total or partial** participation.
(b) [2] Give the relational schema(s) that result from mapping this ISA hierarchy, following the standard convention of one relation per subclass linked by a shared key to the superclass relation.

---

**Q8.** [3 Marks]
Consider the three Datalog rules:
```
P(X) :- Q(X), NOT R(X).
R(X) :- S(X), NOT T(X).
T(X) :- U(X).
```
Construct the predicate dependency graph (nodes = IDB predicates `P, R, T`; edges labelled `+`/`−`). Is this program stratifiable? If so, compute the **stratum number** of each IDB predicate explicitly, using the definition taught in class (stratum of $P$ = largest number of negated edges on any path starting at $P$).

---

**Q9.** [5 Marks]
`Employee(EmpID, Skill, Hobby)` is used to record that an employee has a given skill and a given hobby, where an employee's skills and hobbies are **independent** of one another (an employee with 2 skills and 3 hobbies must appear as $2 \times 3 = 6$ rows to record every skill-hobby combination).
(a) [2] Write out a sample instance for one employee with 2 skills and 2 hobbies, and point out the redundancy this forces.
(b) [1] State the multivalued dependencies that hold: $EmpID \twoheadrightarrow Skill$ and $EmpID \twoheadrightarrow Hobby$.
(c) [2] `Employee` is in BCNF (its only FDs are trivial) but not in **4NF**. Give the two relations that result from decomposing it into 4NF, and explain briefly why this removes the redundancy identified in (a).

---

**Q10.** [4 Marks]
`Sales(SalesRepID, Region, Amount)` records individual sale amounts by region. Write a relational algebra expression, using $\gamma$ (grouping/aggregation) applied **twice** in sequence, that computes: *the average, across all regions, of each region's maximum single-sale `Amount`*. (I.e., first compute the per-region maximum, then average those maxima.) State both intermediate and final RA expressions.

---

**Q11.** [5 Marks]
**True or False:** *"Every relation that is in 3NF is also in BCNF."*
Consider `ExamSchedule(Room, Course, Instructor)` with the functional dependencies:
$$Instructor \rightarrow Course, \qquad Room,\ Course \rightarrow Instructor$$
(a) [2] Determine all candidate keys of `ExamSchedule`.
(b) [1] Show that `ExamSchedule` satisfies the **3NF** definition (for every non-trivial FD $X\to Y$, either $X$ is a superkey or $Y$ is prime).
(c) [2] Show that `ExamSchedule` nonetheless **violates BCNF**, thereby disproving the claim above. Identify the specific violating FD.

---

**Q12.** [4 Marks]
Extend the recursive rules from Q5. Suppose the `Prereq` table is corrupted by a data-entry bug, introducing the cycle $(CS501, CS502), (CS502, CS501)$. Write a Datalog rule (using the existing `AllPrereqs` IDB) whose non-empty result would indicate that the `Prereq` relation contains a cycle. Explain, in one or two sentences, why this rule correctly flags a cycle for **any** finite recursive graph, not just this specific instance.

---

**Q13.** [5 Marks]
`RestaurantRating(RestID, Year, AvgRating)` stores one row per restaurant per year. Write a single SQL query (using a correlated subquery) to find every `RestID` whose rating in the year **2026** is strictly greater than the **average** of that *same* restaurant's ratings across all of its **other** (non-2026) years on record. A restaurant with no prior-year ratings should **not** appear in the result.

---

**Q14.** [2 Marks]
State the **Decomposition Rule** of functional dependency theory: *if $A \rightarrow BC$, then $A \rightarrow B$ and $A \rightarrow C$.* Give a formal step-by-step proof of this rule using *only* Armstrong's three axioms (Reflexivity, Augmentation, Transitivity).

---

**Q15.** [4 Marks]
Convert the recursive Datalog program from Q5 (the `AllPrereqs` IDB only) into an equivalent SQL query using `WITH RECURSIVE`, following the translation pattern taught in class.

---
---

# Answer Key
*(Grading criterion in brackets after each part shows how marks should be distributed.)*

**A1.** [4 Marks]
(a) [2 — 1 mark for correctly unfolding the join definition, 1 mark for the containment/equality argument] By definition, $R \Join S = \{t : t[A,B]\in R,\ t[B,C]\in S,\ t.B \text{ agrees}\}$. Applying $\sigma_{A>10}$ to this set keeps exactly the joined tuples whose $A$-value exceeds 10. Since $A$ is an attribute of $R$ alone, whether a tuple survives the selection depends only on its $R$-portion — so we can equivalently first discard from $R$ every tuple with $A \le 10$ (giving $\sigma_{A>10}(R)$) and *then* join with the (unfiltered) $S$: the set of surviving joined tuples is identical either way. Formally, $t \in \sigma_{A>10}(R\Join S) \iff t[A,B]\in R \wedge t[B,C]\in S \wedge t.A>10 \iff t[A,B]\in \sigma_{A>10}(R) \wedge t[B,C]\in S \iff t\in \sigma_{A>10}(R)\Join S$.
(b) [2] Counterexample reasoning: once the condition also constrains $C$ (an attribute of $S$), the condition $A>10 \wedge C<5$ cannot be evaluated using $R$'s attributes alone — pushing $\sigma_{A>10\wedge C<5}$ below the join and applying it to $R$ (which has no column $C$) is not even syntactically well-formed, and applying only the $A>10$ part to $R$ while leaving $C<5$ unchecked would incorrectly retain tuples of $R$ that pair with an $S$-tuple having $C\ge5$. Correct push-down instead splits the condition: $\sigma_{A>10}(R) \Join \sigma_{C<5}(S)$ — each half of a **conjunctive, single-relation** condition may be pushed to its own relation, but the joint condition as a whole cannot be pushed to one side only.

**A2.** [2 Marks]
[Full marks for citing both (i) monotonicity and (ii) a finite tuple-space bound] Since the rules contain no negation, each application of a rule can only **add** tuples to an IDB relation, never remove any (monotonicity) — so the sequence of IDB instances across iterations is non-decreasing (with respect to $\subseteq$). The number of distinct tuples any IDB predicate of arity $k$ can ever contain is bounded above by $|dom|^k$, where $dom$ is the (finite) set of constants appearing in the EDB — a finite number. A non-decreasing sequence of subsets of a finite set must stabilize after finitely many steps (it cannot grow forever), so naive evaluation is guaranteed to reach a fixedpoint in finitely many iterations.

**A3.** [6 Marks]
Full attribute closures under $F$: $\{OrderID\}^+=\{OrderID,WarehouseID,RegionID,CountryID\}$; $\{WarehouseID\}^+=\{WarehouseID,RegionID,CountryID\}$; $\{RegionID\}^+=\{RegionID,CountryID\}$.
- $\Pi_{R_1}(F)$, attributes $\{OrderID,WarehouseID\}$: restrict $\{OrderID\}^+$ to this schema $\to \{OrderID,WarehouseID\}$, giving $OrderID \to WarehouseID$. [2]
- $\Pi_{R_2}(F)$, attributes $\{WarehouseID,RegionID\}$: restrict $\{WarehouseID\}^+$ to this schema $\to \{WarehouseID,RegionID\}$, giving $WarehouseID \to RegionID$. [2]
- $\Pi_{R_3}(F)$, attributes $\{RegionID,CountryID\}$: restrict $\{RegionID\}^+$ to this schema $\to \{RegionID,CountryID\}$, giving $RegionID \to CountryID$. [1]

The union $\Pi_{R_1}(F)\cup\Pi_{R_2}(F)\cup\Pi_{R_3}(F) = \{OrderID\to WarehouseID,\ WarehouseID\to RegionID,\ RegionID \to CountryID\} = F$ exactly. Since every original FD is recovered directly from a single relation's projection (no join needed), **$D$ is dependency-preserving**. [1]

**A4.** [3 Marks]
Participation constraints: draw a **double line** (or equivalent thick edge, per convention) between `Machine` and `Services` to denote **total participation** (every machine must appear in at least one `Services` tuple), and a regular **single line** between `Technician` and `Services` to denote **partial participation** (a technician may have zero `Services` tuples). [1.5]
Relational schema (relationship → relation, per the standard mapping):
```
Services (MachineID, TechID, ServiceDate, Cost)
```
with `MachineID` referencing `Machine` and `TechID` referencing `Technician` as foreign keys; the total-participation constraint on `Machine` cannot itself be expressed by the schema alone (it is enforced procedurally / via a check outside plain FK constraints), while partial participation on `Technician` requires no special enforcement. [1.5]

**A5.** [6 Marks]
- $AllPrereqs^1$ (base case, direct `Prereq` facts): $\{(CS301,CS201),(CS201,CS101),(CS401,CS301)\}$. [1]
- $AllPrereqs^2$: extend each pair by one more `Prereq` hop: $CS301\to CS201\to CS101$ gives $(CS301,CS101)$; $CS401\to CS301\to CS201$ gives $(CS401,CS201)$. New total: previous 3 plus $(CS301,CS101),(CS401,CS201)$. [1.5]
- $AllPrereqs^3$: $CS401 \to CS301 \to CS201 \to CS101$ gives $(CS401,CS101)$ (new). No other new pairs arise. [1]
- $AllPrereqs^4$: no new tuples — **fixedpoint reached at iteration 3**. Final `AllPrereqs` = $\{(CS301,CS201),(CS201,CS101),(CS401,CS301),(CS301,CS101),(CS401,CS201),(CS401,CS101)\}$. [1]
- `DeepCourse(C)` requires $C$ to have *two* chained `AllPrereqs` facts, $AllPrereqs(C,P_1)$ and $AllPrereqs(P_1,P_2)$ for some $P_1,P_2$. Checking each course: $CS301$: $AllPrereqs(CS301,CS201)$ and $AllPrereqs(CS201,CS101)$ both hold $\Rightarrow$ `DeepCourse(CS301)`. $CS401$: $AllPrereqs(CS401,CS301)$ and $AllPrereqs(CS301,CS201)$ both hold $\Rightarrow$ `DeepCourse(CS401)`. $CS201$: only $AllPrereqs(CS201,CS101)$ exists, no further chaining from $CS101$ $\Rightarrow$ not deep. **`DeepCourse` = $\{CS301, CS401\}$.** [1.5]

**A6.** [2 Marks]
```sql
SELECT MemberID FROM GymVisit WHERE VisitMonth = 'Jan'
EXCEPT
SELECT MemberID FROM GymVisit WHERE VisitMonth = 'Feb';
```

**A7.** [4 Marks]
(a) [2] **Disjoint**, because a given `VIN` is exactly one of `Car`, `Truck`, or `Motorcycle` — it cannot simultaneously belong to two subclasses (a vehicle is never both a car and a truck). **Total**, because every vehicle in the fleet must belong to one of the three subclasses (there is no "generic" vehicle instance with none of the specialized attributes).
(b) [2]
```
Vehicle (VIN, Make, Model)
Car (VIN, NumDoors)
Truck (VIN, CargoCapacity)
Motorcycle (VIN, EngineCC)
```
Each subclass relation shares its key (`VIN`) with `Vehicle`, functioning as both primary key and foreign key referencing `Vehicle`.

**A8.** [3 Marks]
Edges: $P \xrightarrow{-} R$ (since `R` is negated in `P`'s body), $R \xrightarrow{-} T$ (since `T` is negated in `R`'s body), $T \xrightarrow{+} $ (only depends on EDB `U`, no IDB edge onward). No cycles exist in this graph (it's a simple chain $P\to R\to T$), so the program **is stratifiable**. [1]
Stratum computation (largest count of negated edges on any path starting at the predicate): $stratum(T) = 0$ (no outgoing edges). $stratum(R) = 1$ (one negated edge, $R\to T$, and $T$ itself is at stratum 0). $stratum(P) = 2$ (path $P\xrightarrow{-}R\xrightarrow{-}T$ crosses two negated edges). [2]

**A9.** [5 Marks]
(a) [2] Sample instance for `EmpID = E1` with skills $\{Python, SQL\}$ and hobbies $\{Chess, Running\}$:
```
EmpID  Skill    Hobby
E1     Python   Chess
E1     Python   Running
E1     SQL      Chess
E1     SQL      Running
```
Every skill must be paired with every hobby, forcing $2\times2=4$ rows to represent just 2 facts about E1's skills and 2 facts about E1's hobbies — this cross-product blow-up is the redundancy.
(b) [1] $EmpID \twoheadrightarrow Skill$ and $EmpID \twoheadrightarrow Hobby$ (equivalently $EmpID \twoheadrightarrow Skill \mid Hobby$).
(c) [2]
```
EmpSkill (EmpID, Skill)
EmpHobby (EmpID, Hobby)
```
Each relation now stores one independent fact per row (2 rows for skills, 2 rows for hobbies — 4 rows total instead of 4 *redundant* combined rows growing multiplicatively), eliminating the forced cross-product redundancy since skills and hobbies no longer need to be co-listed.

**A10.** [4 Marks]
Step 1 — per-region maximum:
$$T_1 \;=\; \gamma_{Region,\ MAX(Amount)\rightarrow MaxAmt}(Sales)$$
Step 2 — average of those per-region maxima (grouping on no attributes, i.e. a single aggregate over all of $T_1$):
$$T_2 \;=\; \gamma_{AVG(MaxAmt)\rightarrow AvgOfMax}(T_1)$$
Final expression: $\gamma_{AVG(MaxAmt)\rightarrow AvgOfMax}\big(\gamma_{Region,\ MAX(Amount)\rightarrow MaxAmt}(Sales)\big)$.

**A11.** [5 Marks]
(a) [2] $\{Instructor\}^+ = \{Instructor, Course\}$ — not all attributes (missing `Room`), so `Instructor` alone is not a key. $\{Room,Course\}^+ = \{Room,Course,Instructor\}$ (via $Room,Course\to Instructor$) — all attributes, so $\{Room,Course\}$ is a candidate key. Also check $\{Room,Instructor\}^+$: $Instructor\to Course$ gives $\{Room,Instructor,Course\}$ — all attributes, so $\{Room,Instructor\}$ is **also** a candidate key. **Candidate keys: $\{Room,Course\}$ and $\{Room,Instructor\}$.**
(b) [1] For $Instructor \to Course$: LHS `Instructor` is not a superkey, **but** `Course` is a prime attribute (it belongs to the candidate key $\{Room,Course\}$) — so this FD does not violate 3NF (satisfies the "Y is prime" exception). For $Room,Course \to Instructor$: LHS is a superkey — trivially satisfies 3NF. **All FDs satisfy 3NF, so `ExamSchedule` is in 3NF.**
(c) [2] For BCNF, the "Y is prime" exception does not apply — only "X is a superkey" is allowed. $Instructor \to Course$ has LHS `Instructor`, which is **not** a superkey (shown in (a)) — this is a genuine **BCNF violation**. Hence `ExamSchedule` is a relation that is in 3NF but not in BCNF, **disproving** the claim that 3NF always implies BCNF.

**A12.** [4 Marks]
```
CycleDetected() :- AllPrereqs(X, X).
```
(or equivalently, existentially: $\exists X.\ AllPrereqs(X,X)$.) Since $AllPrereqs$ is the *transitive closure* of `Prereq`, a course $X$ satisfies $AllPrereqs(X,X)$ if and only if there is a non-empty directed path from $X$ back to itself in the `Prereq` graph — i.e., a cycle. This works for **any** finite graph because transitive closure captures reachability along paths of any length, and a self-reachable node is by definition on a cycle, regardless of the cycle's length or position in the graph.

**A13.** [5 Marks]
```sql
SELECT R1.RestID
FROM RestaurantRating R1
WHERE R1.Year = 2026
  AND R1.AvgRating > (
        SELECT AVG(R2.AvgRating)
        FROM RestaurantRating R2
        WHERE R2.RestID = R1.RestID
          AND R2.Year <> 2026
      )
  AND EXISTS (
        SELECT 1 FROM RestaurantRating R3
        WHERE R3.RestID = R1.RestID AND R3.Year <> 2026
      );
```
The correlated subquery computes each restaurant's average rating over its non-2026 years; the outer comparison keeps only restaurants whose 2026 rating exceeds that average. The additional `EXISTS` guard is required because, if a restaurant has **no** prior-year rows, the correlated `AVG` subquery returns `NULL`, and `AvgRating > NULL` evaluates to `UNKNOWN` — which already correctly excludes such restaurants — but the explicit `EXISTS` makes this exclusion unambiguous and self-documenting rather than relying on `NULL`-comparison behavior.

**A14.** [2 Marks]
Given $A \to BC$.
1. By Reflexivity, since $B \subseteq BC$: $BC \to B$.
2. By Transitivity applied to $A\to BC$ and $BC\to B$: $A \to B$. — (i)
3. By Reflexivity, since $C \subseteq BC$: $BC \to C$.
4. By Transitivity applied to $A\to BC$ and $BC\to C$: $A \to C$. — (ii)

From (i) and (ii), $A\to B$ and $A\to C$. $\blacksquare$

**A15.** [4 Marks]
```sql
WITH RECURSIVE AllPrereqs(Course, Requires) AS (
    SELECT Course, Requires
    FROM Prereq
    UNION
    SELECT Prereq.Course, AllPrereqs.Requires
    FROM Prereq, AllPrereqs
    WHERE Prereq.Requires = AllPrereqs.Course
)
SELECT * FROM AllPrereqs;
```
The base case seeds `AllPrereqs` with direct entries from `Prereq`; the recursive case extends a course's prerequisite set by chaining through one more `Prereq` hop, matching the `Edge`/`Path` recursive translation pattern taught in class. `UNION` (not `UNION ALL`) ensures duplicate elimination, guaranteeing termination even if the underlying prerequisite graph contains a cycle.
