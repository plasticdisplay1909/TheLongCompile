# COL2010 — Introduction to Data Science
## Mid-Term Examination — Mock Paper 1
**Module 1: Database Systems** | Instructor: Maya Ramanath | Diwali Semester, 2026

**Total Marks: 55** | **Time: 2 Hours**

### Instructions
- Attempt **all** questions.
- Marks for each question/part are indicated alongside it.
- Where an algorithm is required (attribute closure, BCNF decomposition, fixedpoint evaluation), you must show all intermediate steps — final answers alone will not receive full credit.
- State any additional assumptions clearly.

---

**Q1.** [2 Marks]
Consider a ternary relationship **Enrolls** among the entity sets `Student`, `Course`, and `Semester` (i.e., a student enrolls in a course during a specific semester). Using the technique discussed in class for converting an *n*-ary relationship to a set of binary relationships, describe how you would redraw this ER fragment. Name the new connector entity set you introduce and list the binary relationships (with roles) that replace `Enrolls`.

---

**Q2.** [6 Marks]
You are given the following set of functional dependencies on a relation with attributes $\{A,B,C,D,E\}$:

$$A \rightarrow B, \quad BC \rightarrow D, \quad D \rightarrow E, \quad CE \rightarrow A$$

Does $BC \rightarrow E$ hold? Compute the closure $\{B,C\}^+$ step by step using the attribute-closure algorithm taught in class (show the value of $Z$ after each pass), and state your conclusion with justification.

---

**Q3.** [6 Marks]
The EDB relation `Edge(from, to)` contains the tuples:

$$\text{(Delhi, Mumbai), (Mumbai, Pune), (Pune, Goa)}$$

The IDB predicate `Reach` is defined by the recursive Datalog rules:

```
Reach(X,Y) :- Edge(X,Y).
Reach(X,Y) :- Edge(X,Z), Reach(Z,Y).
```

Using **naive least-fixedpoint evaluation** (as taught in class), list the contents of `Reach` after each iteration — $Reach^0$ (initial, empty), $Reach^1$, $Reach^2$, $Reach^3$ — until the fixedpoint is reached. State clearly which iteration first reaches the fixedpoint and why.

---

**Q4.** [2 Marks]
Consider `Movie(Title, Year, Language, Length, ActorName)` with the single (minimal) candidate key $\{Title, Year, ActorName\}$, which functionally determines all other attributes. Define **key**, **superkey**, and **candidate key**. Give an example of a superkey of `Movie` that is *not* a key, and justify why it fails to be a key.

---

**Q5.** [3 Marks]
Let `Actors(Name, Age, Addr)` and `Movies(Name, Year, Title)`, where `Movies.Name` records the actor who starred in the movie. Convert the following relational algebra expression into an equivalent SQL query:

$$\Pi_{Name}\big(\sigma_{Age<40 \,\wedge\, Year=2023}(Actors \Join_{Actors.Name = Movies.Name} Movies)\big)$$

---

**Q6.** [2 Marks]
The entity sets `Courses` and `Students` are related by `Registers`, with the constraint that a student may register in **at most 4** courses, and `Students.Age` has a domain constraint of $0$–$100$. You are given two rows from a database instance:

(i) a `Registers` tuple referencing a `CourseID` that does not exist in `Courses`;
(ii) a `Students` tuple with `Age = 150`.

Identify, by name, which kind of constraint each row violates, and briefly explain why.

---

**Q7.** [5 Marks]
Consider `CourseEnrollment(StudentID, StudentName, CourseCode, CourseTitle, Instructor, Grade)` with the following functional dependencies:

$$StudentID \rightarrow StudentName, \qquad CourseCode \rightarrow CourseTitle,\ Instructor, \qquad StudentID,\ CourseCode \rightarrow Grade$$

Assume $\{StudentID, CourseCode\}$ is the only candidate key.
(a) [2] Is `CourseEnrollment` in 2NF? If not, precisely identify the violation using the 2NF definition.
(b) [3] Decompose `CourseEnrollment` into a set of relations that are each in 3NF, and state the resulting schemas.

---

**Q8.** [5 Marks]
Let `Actors(Name, Age, Addr)` and `Movies(ActorName, Year, Title)`. Write a single SQL query, using a **correlated subquery**, that returns the names of actors who have acted in *more* movies than the average number of movies per actor (i.e., more than the average value of "movie count per actor" computed across all actors).

---

**Q9.** [4 Marks]
An entity set `Employee(EmpID, Name, Salary)` participates in a relationship `Supervises` with itself, distinguishing the roles `supervisor` and `subordinate`; the relationship also carries an attribute `StartDate`. Following the ER-to-relational mapping convention used in class for relationships on an entity set with roles, write the relational schema(s) produced from this ER fragment. Clearly show how the role names are used to disambiguate the two references to `Employee`.

---

**Q10.** [2 Marks]
Define what it means for a Datalog rule to be **safe**. Consider the rule:

```
Rich(X) :- Person(X), NOT Poor(X).
```

Is this rule safe as written? If not, explain precisely why, and state the general principle (in one line) that explains why negation in recursive Datalog programs requires **stratification** rather than being permitted unrestrictedly.

---

**Q11.** [3 Marks]
Consider `TheatreShow(Title, Theatre, City)` with the functional dependencies:

$$Theatre \rightarrow City, \qquad Title,\ City \rightarrow Theatre$$

Show that `TheatreShow` violates **BCNF** (identify the violating FD explicitly, and confirm it is not merely a 3NF violation). Then apply the lossless-decomposition algorithm taught in class to decompose `TheatreShow` into a set of relations that are all in BCNF; state the resulting schemas.

---

**Q12.** [6 Marks]
Consider an ER fragment with entity set `Book(ISBN, Title, Genre)` and entity set `Publisher(PubName, PubAddress)`, related by a many-to-one relationship `PublishedBy` (many books are published by at most one publisher).

(a) [2] Convert this ER fragment into a relational schema by **combining relations**, following the approach used in class for many-one relationships (i.e., merge `PublishedBy` into `Book`). State the resulting schema(s).
(b) [2] Using the merged relation `Book(ISBN, Title, Genre, PubName, PubAddress)`, identify one instance each of a redundancy, an update anomaly, and a deletion anomaly that this schema can exhibit.
(c) [2] State the functional dependency responsible for the anomalies in (b), and propose a lossless decomposition of `Book` that removes it.

---

**Q13.** [2 Marks]
Consider a relation `Student(RollNo, Name, Dept, DeptHead)` with the functional dependency $Dept \rightarrow DeptHead$. For each of the following FDs, state whether it is **trivial** or **non-trivial**, with a one-line justification:

(a) $RollNo,\ Name \rightarrow Name$
(b) $Dept \rightarrow DeptHead$

---

**Q14.** [3 Marks]
Given `Movies(Title, City, Boxoffice)`, write a SQL query that returns, for each movie, the **total** boxoffice returns summed across all cities — but only for movies whose total exceeds 2,000,000 — and orders the result by this total in descending order.

---

**Q15.** [4 Marks]
Given a table `Edge(from, to)` representing direct flight routes, write a `WITH RECURSIVE` SQL query (following the recursive-Datalog-to-SQL translation pattern taught in class) that computes all pairs `(origin, destination)` reachable via one or more flights, i.e., the transitive closure of `Edge`.

---
---

# Answer Key

**A1.** [2 Marks]
Introduce a connector entity set, e.g. `EnrollmentEvent`, with no attributes of its own (or a synthetic key `EnrollID`), and three binary many-one relationships from `EnrollmentEvent` to each of `Student` (role: `enrolledStudent`), `Course` (role: `enrolledCourse`), and `Semester` (role: `enrolledSemester`). Each triple in the original ternary `Enrolls` relationship corresponds to exactly one `EnrollmentEvent` entity connected to the three participating entities. This mirrors the `MovieRoles` construction shown for the ternary `plays` relationship.

**A2.** [6 Marks]
Compute $Z = \{B,C\}$.
- Pass 1: $A \to B$ (LHS $\not\subseteq Z$, skip); $BC \to D$ (LHS $\subseteq Z$): $Z = \{B,C,D\}$; $D \to E$ (LHS $\subseteq Z$): $Z = \{B,C,D,E\}$; $CE \to A$ (LHS $\subseteq Z$): $Z = \{A,B,C,D,E\}$.
- $Z$ is now the full attribute set; further passes leave $Z$ unchanged, so the algorithm halts.
- $\{B,C\}^+ = \{A,B,C,D,E\}$, and since $E \in \{B,C\}^+$, **$BC \rightarrow E$ holds**.

**A3.** [6 Marks]
- $Reach^0 = \emptyset$.
- $Reach^1$ (base case, `Edge(X,Y)`): $\{(D,M),(M,P),(P,G)\}$ (using initials for Delhi, Mumbai, Pune, Goa).
- $Reach^2$: add pairs via one join of `Edge` with `Reach^1`: $\{(D,M),(M,P),(P,G),(D,P),(M,G)\}$.
- $Reach^3$: joining `Edge` with `Reach^2` adds $(D,G)$: $\{(D,M),(M,P),(P,G),(D,P),(M,G),(D,G)\}$.
- $Reach^4$ produces no new tuples, so the **fixedpoint is reached at iteration 3** (i.e., $Reach^3 = Reach^4$); the final `Reach` relation is the transitive closure of `Edge` over the given chain.

**A4.** [2 Marks]
- **Key**: a minimal set of attributes that functionally determines all other attributes of the relation.
- **Superkey**: any set of attributes that functionally determines all other attributes, not necessarily minimal.
- **Candidate key**: a key (i.e., a minimal superkey); a relation may have more than one.
- Example non-minimal superkey: $\{Title, Year, ActorName, Length\}$ — it still determines all attributes but is not minimal, since dropping `Length` (itself determined by the key) leaves a still-determining, smaller set $\{Title,Year,ActorName\}$; hence it is a superkey but not a key.

**A5.** [3 Marks]
```sql
SELECT Actors.Name
FROM Actors, Movies
WHERE Age < 40
  AND Year = 2023
  AND Actors.Name = Movies.Name;
```
The selection condition maps directly to the `WHERE` clause, the join condition to the equality on `Actors.Name = Movies.Name`, and the projection to the `SELECT` list.

**A6.** [2 Marks]
(i) Violates **referential integrity** — the `Registers` tuple references a `CourseID` that does not exist in `Courses`, so the reference cannot be resolved to an existing entity.
(ii) Violates a **domain constraint** — `Age = 150` falls outside the declared valid range $[0,100]$ for the `Age` attribute.
(The "at most 4 courses" restriction is a general/cardinality constraint, not directly violated by either given row, and is not required for this answer.)

**A7.** [5 Marks]
(a) `CourseEnrollment` is **not in 2NF**. The key is $\{StudentID, CourseCode\}$; the non-prime attribute `StudentName` depends only on $StudentID$, a *proper subset* of the key (similarly `CourseTitle`, `Instructor` depend only on `CourseCode`). This is a direct violation of the 2NF definition (no non-prime attribute may depend on a proper subset of a candidate key).
(b) Decompose by projecting each partial dependency into its own relation:
- `StudentInfo(StudentID, StudentName)`
- `CourseInfo(CourseCode, CourseTitle, Instructor)`
- `Enrollment(StudentID, CourseCode, Grade)`

Each resulting relation has no partial or transitive dependency on its key, so all three are in 3NF (in fact BCNF here, since each non-trivial FD's LHS is a superkey of its own relation).

**A8.** [5 Marks]
```sql
SELECT A.Name
FROM Actors A
WHERE (SELECT COUNT(*) FROM Movies M WHERE M.ActorName = A.Name)
      >
      (SELECT AVG(cnt) FROM (
          SELECT COUNT(*) AS cnt
          FROM Movies M2
          GROUP BY M2.ActorName
       ) AS PerActorCounts);
```
The outer correlated subquery counts movies per candidate actor `A.Name`; the inner (non-correlated) subquery first computes the per-actor movie count for every actor via `GROUP BY`, then averages those counts, giving the required threshold.

**A9.** [4 Marks]
```
Supervises (supEmpID, supName, supSalary, subEmpID, subName, subSalary, StartDate)
```
equivalently written with role-qualified column names:
```
Supervises (supervisor_EmpID, supervisor_Name, supervisor_Salary,
            subordinate_EmpID, subordinate_Name, subordinate_Salary, StartDate)
```
Since both roles reference the same entity set `Employee`, each attribute of `Employee` must be duplicated and prefixed/renamed by its role (`supervisor_`, `subordinate_`) to avoid ambiguity — directly analogous to the `parentName, parentDOB, childName, childDOB` construction shown for the self-relationship `parentOf` on `People`.

**A10.** [2 Marks]
A rule is **safe** if every variable appearing anywhere in the rule (head or body) also appears in some non-negated, relational (not arithmetic) subgoal of the body. The given rule *is safe*: $X$ appears in the non-negated subgoal `Person(X)`, so it is bound before the negated subgoal `NOT Poor(X)` is evaluated. General principle: unrestricted negation in recursive rules can make the least fixedpoint non-unique/ill-defined (a predicate's truth value can flip depending on evaluation order), so recursive programs with negation must be stratified — negated subgoals may only refer to predicates from a strictly lower stratum, ensuring the negated relation is fully computed before it is used.

**A11.** [3 Marks]
Candidate keys of `TheatreShow` are $\{Title, City\}$ and $\{Theatre, Title\}$ (both determine all attributes). The FD $Theatre \rightarrow City$ has LHS $\{Theatre\}$, which is **not** a superkey (it does not functionally determine `Title`), so it violates BCNF. However, since `City` is a prime attribute (part of the candidate key $\{Title,City\}$), this same FD does *not* violate 3NF — confirming this is a BCNF-only violation, one of the scenarios flagged in class (candidate keys with intersecting elements).
Decomposition (BCNF algorithm on $Theatre \to City$):
- $R_1(Theatre, City)$ — attributes of $X \cup Y$
- $R_2(Theatre, Title)$ — attributes of $X \cup (\text{all} - X - Y)$

Both $R_1$ and $R_2$ are in BCNF: in $R_1$, $Theatre \to City$ with `Theatre` a key; $R_2$ has no non-trivial FDs beyond the key $\{Theatre,Title\}$.

**A12.** [6 Marks]
(a)
```
Book (ISBN, Title, Genre, PubName, PubAddress)
Publisher (PubName, PubAddress)
```
(merging the many-one `PublishedBy` relationship's key into `Book`, per the `Movie`/`Studio` pattern from class).
(b) Using `Book(ISBN, Title, Genre, PubName, PubAddress)` alone:
- **Redundancy**: `PubAddress` is repeated in every row for the same publisher, once per book they have published.
- **Update anomaly**: if a publisher's address changes, every book row for that publisher must be updated; missing even one row leaves the data inconsistent.
- **Deletion anomaly**: deleting the last remaining book from a publisher also deletes all record of that publisher's existence (including its address), even though the publisher itself has not ceased to exist.
(c) The responsible FD is $PubName \rightarrow PubAddress$ (non-trivial, with LHS not a superkey of the merged `Book` relation). Lossless decomposition:
- $Book(ISBN, Title, Genre, PubName)$
- $Publisher(PubName, PubAddress)$

This is lossless since `PubName` is a key of `Publisher` and a foreign key in `Book`.

**A13.** [2 Marks]
(a) **Trivial** — $\{Name\} \subseteq \{RollNo, Name\}$, so by Armstrong's reflexivity axiom this FD holds in every relation regardless of data.
(b) **Non-trivial** — $DeptHead \notin \{Dept\}$, so this is a genuine constraint on the data, not one that follows from reflexivity alone.

**A14.** [3 Marks]
```sql
SELECT Title, SUM(Boxoffice) AS TotalBoxoffice
FROM Movies
GROUP BY Title
HAVING SUM(Boxoffice) > 2000000
ORDER BY TotalBoxoffice DESC;
```

**A15.** [4 Marks]
```sql
WITH RECURSIVE Reach(origin, destination) AS (
    SELECT "from", "to"
    FROM Edge
    UNION
    SELECT Reach.origin, Edge."to"
    FROM Reach, Edge
    WHERE Edge."from" = Reach.destination
)
SELECT * FROM Reach;
```
The base case seeds `Reach` with direct edges; the recursive case extends any existing reachable pair by one more `Edge` hop, following exactly the `Path`/`Edge` translation pattern taught for recursive Datalog-to-SQL conversion. `UNION` (not `UNION ALL`) is used to avoid infinite growth on cyclic graphs, consistent with duplicate-elimination under set semantics.
