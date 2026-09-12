# COL2010 — Introduction to Data Science
## Mid-Term Examination — Mock Paper 2
**Module 1: Database Systems** | Instructor: Maya Ramanath | Diwali Semester, 2026

**Total Marks: 59** | **Time: 2 Hours**

### Instructions
- Attempt **all** questions.
- Marks for each question/part are indicated alongside it.
- Where an algorithm or proof is required (minimal cover, BCNF decomposition, Armstrong's axioms, fixedpoint evaluation), you must show all intermediate steps — final answers alone will not receive full credit.
- State any additional assumptions clearly.

---

**Q1.** [3 Marks]
Consider `Orders(OrderID, CustomerID, ProductID)`, where `CustomerID` may be `NULL` for orders placed as a guest checkout. A student writes the following query intending to find all customers who have never placed an order:

```sql
SELECT CustomerID FROM Customers
WHERE CustomerID NOT IN (SELECT CustomerID FROM Orders);
```

Explain precisely, in terms of SQL's three-valued logic, why this query can return an **empty result set** even when such customers exist, the moment `Orders.CustomerID` contains at least one `NULL`. Rewrite the query using `NOT EXISTS` so that it is correct regardless of `NULL`s in `Orders.CustomerID`.

---

**Q2.** [2 Marks]
Consider a ternary relationship **Supplies** among entity sets `Supplier`, `Part`, and `Project` (i.e., a supplier supplies a part to a project, in a given quantity). Using the technique taught in class for converting an *n*-ary relationship into binary relationships, describe the connector entity set you would introduce, and list the binary many-one relationships (with roles) that replace `Supplies`.

---

**Q3.** [6 Marks]
The EDB relation `Follows(follower, followee)` in a social network contains the tuples:

$$\text{(Alice, Bob), (Bob, Carol), (Carol, Alice), (Carol, Dave)}$$

Note that this graph contains a **cycle**: Alice → Bob → Carol → Alice. The IDB predicate `Reachable` is defined by:

```
Reachable(X,Y) :- Follows(X,Y).
Reachable(X,Y) :- Follows(X,Z), Reachable(Z,Y).
```

Using naive least-fixedpoint evaluation, compute $Reachable^1, Reachable^2, Reachable^3, Reachable^4$, and state at which iteration the fixedpoint is reached. Explain, with reference to the semantics of Datalog evaluation, why the presence of a cycle does **not** cause the evaluation to grow without bound.

---

**Q4.** [2 Marks]
Consider `R(P, Q, S, T, U)` with functional dependencies:

$$P \rightarrow Q, \qquad Q,S \rightarrow T, \qquad T \rightarrow U$$

Classify each attribute of $R$ as (i) appearing only on the left of some FD, (ii) appearing only on the right, (iii) appearing on both sides, or (iv) appearing in no FD. Using this classification, determine **all** candidate keys of $R$, briefly justifying why no smaller set can be a key.

---

**Q5.** [4 Marks]
Let `Orders(OrderID, ProductID, Category, Qty, Price)`, where each row records one line item (`Price` is the unit price). Write a relational algebra expression using $\gamma$ (grouping/aggregation) that returns, for each `Category`, the **total revenue** (i.e., $\sum Qty \times Price$) — assume a derived attribute `LineTotal = Qty \times Price` is already available as part of the schema for this question. State your expression using standard RA notation ($\sigma, \Pi, \gamma$).

---

**Q6.** [3 Marks]
Two Datalog rules are given for a hospital risk-flagging system:

```
HighRisk(X) :- Patient(X), NOT LowRisk(X).
LowRisk(X)  :- Screened(X), NOT HighRisk(X).
```

Construct the predicate dependency graph for `HighRisk` and `LowRisk` (nodes = IDB predicates, edges labelled `+`/`−` for non-negated/negated occurrence). Based on this graph, is this program **stratifiable**? Justify your answer using the definition of stratification taught in class.

---

**Q7.** [6 Marks]
Given the functional dependency set $F$ on relation $R(W,X,Y,Z)$:

$$W \rightarrow X, \qquad WX \rightarrow Y, \qquad Y \rightarrow Z, \qquad Y \rightarrow X$$

Compute a **minimal (canonical) cover** $F_c$ of $F$. Show your work in the standard three stages: (a) reduce all left-hand sides to remove extraneous attributes, (b) reduce right-hand sides to single attributes if not already so, (c) eliminate any FD that is redundant given the others. State the final minimal cover.

---

**Q8.** [2 Marks]
Let `Product(PID, Price, Category)`. Write a SQL query using `> ALL` (not a bare aggregate) that returns the products whose `Price` is strictly greater than the price of **every** product in category `'Budget'`.

---

**Q9.** [4 Marks]
An entity set `Product(PID, Name, Price)` participates in a relationship `BundledWith` with itself: each bundle pairs a `primary` product with a `secondary` product, and the relationship carries an attribute `DiscountPercent`. Following the ER-to-relational mapping convention used in class for role-based relationships on a single entity set, write the relational schema produced from this ER fragment, clearly showing how the two roles are used to disambiguate the two references to `Product`.

---

**Q10.** [5 Marks]
State **Armstrong's Axioms** (Reflexivity, Augmentation, Transitivity). Using *only* these three axioms (no other "derived" rules), give a formal step-by-step proof of the **Union Rule**:

> If $A \rightarrow B$ and $A \rightarrow C$, then $A \rightarrow BC$.

---

**Q11.** [3 Marks]
Consider two bag (multiset) relations over the same schema $(X,Y)$:

$$R = \{(1,a)^{\times 3}, (2,b)^{\times 1}\}, \qquad S = \{(1,a)^{\times 1}, (2,b)^{\times 2}, (3,c)^{\times 1}\}$$

(where the exponent denotes multiplicity.) Give the multiplicity of each tuple in (a) $R \cup S$ (bag union), (b) $R \cap S$ (bag intersection), and (c) $R - S$ (bag difference), following the bag-semantics rules taught in class.

---

**Q12.** [4 Marks]
Consider the Datalog rule:

```
BigBonus(Name, Bonus) :- Employee(Name, Salary), Bonus > 10000.
```

Is this rule **safe**? If not, identify exactly which variable violates the safety condition and why, and rewrite the rule (adding at most one additional subgoal referencing an existing EDB predicate `Employee(Name, Salary, Bonus)`) so that it becomes safe.

---

**Q13.** [6 Marks]
Consider `Person(SSN, City, State, Zip)` with the functional dependencies:

$$SSN \rightarrow City,\ State,\ Zip, \qquad Zip \rightarrow City,\ State$$

(a) [2] Identify the candidate key of `Person`, and show that $Zip \rightarrow City,\ State$ violates BCNF.
(b) [2] Apply the BCNF decomposition algorithm on this violating FD and give the two resulting relation schemas.
(c) [2] Show that this decomposition is **lossless** but **not dependency-preserving** — specifically, identify the original FD that can no longer be checked without a join across the two decomposed relations, and briefly explain why this is an unavoidable trade-off of the BCNF algorithm in this case.

---

**Q14.** [4 Marks]
Given `Employee(EmpID, DeptID, Salary)`, write a single SQL query that returns each `DeptID` along with its average salary, but only for departments that satisfy **both** of the following conditions: (i) the department has **at least 3 employees**, and (ii) the department's average salary is **strictly greater than** the company-wide average salary (computed across all employees, all departments).

---

**Q15.** [5 Marks]
Given `Customer(CustID)`, `Product(PID, Category)`, and `Bought(CustID, PID)` (a customer-product purchase-history table), write a SQL query using `NOT EXISTS` (double negation, i.e., relational division) to find all customers who have bought **every** product in the `'Electronics'` category.

---
---

# Answer Key

**A1.** [3 Marks]
SQL's `NOT IN` is defined via a chain of `<>` comparisons combined with `AND`. If the subquery `(SELECT CustomerID FROM Orders)` returns even one `NULL`, then for *any* candidate `CustomerID` value $c$, the comparison $c \neq NULL$ evaluates to `UNKNOWN` (not `TRUE`) under three-valued logic. Since the whole `AND`-chain becomes `UNKNOWN` whenever any single comparison is `UNKNOWN`, and a `WHERE` clause only keeps rows where the condition is `TRUE`, **every** row of `Customers` is excluded — the query silently returns an empty set, even if some customers genuinely never ordered anything. Corrected query:
```sql
SELECT C.CustomerID
FROM Customers C
WHERE NOT EXISTS (
    SELECT 1 FROM Orders O WHERE O.CustomerID = C.CustomerID
);
```
`NOT EXISTS` only checks row-existence via equality matches and is unaffected by unrelated `NULL`s in the subquery result.

**A2.** [2 Marks]
Introduce a connector entity set, e.g. `SupplyRecord(Qty)`, with three binary many-one relationships to the participating entity sets: `suppliedBy` (to `Supplier`), `suppliesPart` (to `Part`), and `suppliesTo` (to `Project`). Each triple of the original ternary `Supplies` relationship corresponds to exactly one `SupplyRecord` entity linked to the three participants — the same construction used for `MovieRoles` on the ternary `plays` relationship in class.

**A3.** [6 Marks]
Using initials A, B, C, D for Alice, Bob, Carol, Dave:
- $Reachable^1$ (base case): $\{(A,B),(B,C),(C,A),(C,D)\}$.
- $Reachable^2$: extend each pair by one more `Follows` hop: adds $(A,C)$ [A→B→C], $(B,A)$ [B→C→A], $(B,D)$ [B→C→D], $(C,B)$ [C→A→B]. So $Reachable^2 = \{(A,B),(B,C),(C,A),(C,D),(A,C),(B,A),(B,D),(C,B)\}$.
- $Reachable^3$: adds $(A,A)$ [A→C→A? via C,A already present — check systematically: A→B→C→A gives (A,A); A→B→C→D gives (A,D); B→A→B gives (B,B); C→B→C gives (C,C)]. So new tuples: $(A,A),(A,D),(B,B),(C,C)$.
- $Reachable^4$: every pair among $\{A,B,C\}$ and reachability of $D$ from each is already covered; no new tuples are generated.
- **Fixedpoint reached at iteration 4** (i.e. $Reachable^4 = Reachable^5$). The relation stabilizes to the *set* of all pairs reachable within the cycle $\{A,B,C\}$ (all $3\times3=9$ pairs) plus $(A,D),(B,D),(C,D)$.
Because `Reachable` is evaluated under **set semantics**, revisiting an already-derived tuple through the cycle adds no new information — the relation can only grow up to a bound of $|dom|^2$ distinct pairs, so naive evaluation is guaranteed to converge to a unique least fixedpoint despite the cycle.

**A4.** [2 Marks]
- Only on LHS: $P$ (appears in $P \to Q$ only as source).
- Only on RHS: $U$ (appears only as target of $T \to U$).
- Both sides: $Q$ (RHS of $P\to Q$, LHS of $QS\to T$), $T$ (RHS of $QS\to T$, LHS of $T\to U$).
- Neither side: $S$ (never appears in any FD).

Since $S$ appears in no FD, it must be in **every** candidate key (nothing else can ever determine it). Since $P$ appears only on the left, it must also be in every candidate key (nothing determines $P$). So every candidate key contains $\{P,S\}$. Compute $\{P,S\}^+$: $P\to Q$ gives $\{P,Q,S\}$; $QS \to T$ gives $\{P,Q,S,T\}$; $T\to U$ gives $\{P,Q,S,T,U\}$ — the full attribute set. So $\{P,S\}$ is a superkey, and since both $P$ and $S$ are individually required, it is **minimal**. **The unique candidate key is $\{P,S\}$.**

**A5.** [4 Marks]
$$\gamma_{Category,\ SUM(LineTotal)\rightarrow TotalRevenue}(Orders)$$
Equivalently expanded with the grouping attribute and the aggregate function applied over the remaining rows within each group, as taught: the expression groups all tuples of `Orders` by `Category` and computes $\Sigma(Qty \times Price)$ within each group, producing one output tuple `(Category, TotalRevenue)` per distinct category.

**A6.** [3 Marks]
Dependency graph: `HighRisk` has a `−` edge to `LowRisk` (since `LowRisk` is negated in `HighRisk`'s body), and `LowRisk` has a `−` edge to `HighRisk` (since `HighRisk` is negated in `LowRisk`'s body). This forms a cycle **containing a negated edge in both directions** — `HighRisk` depends negatively on `LowRisk`, which depends negatively back on `HighRisk`.
This program is **not stratifiable**. Stratification requires that no predicate be part of a cycle that includes a negated edge (a predicate cannot negatively depend, even indirectly, on itself), since this makes the least fixedpoint ill-defined/non-unique (as flagged in the "Negation and Recursion" discussion in class) — there is no way to assign a linear order of strata to `HighRisk` and `LowRisk` that respects "negated predicates must be evaluated at a strictly lower stratum" in both directions simultaneously.

**A7.** [6 Marks]
$F = \{W\to X,\ WX\to Y,\ Y\to Z,\ Y\to X\}$.
(a) **Remove extraneous LHS attributes.** Check $WX\to Y$: is $X$ extraneous, i.e. does $W\to Y$ already hold via $F$? $\{W\}^+$ using $F$: $W\to X$ gives $\{W,X\}$; now $WX\to Y$ applies (since $\{W,X\}\subseteq\{W,X\}$) giving $\{W,X,Y\}$; $Y\to Z$ gives $\{W,X,Y,Z\}$; $Y\to X$ adds nothing new. So $\{W\}^+ = \{W,X,Y,Z\}$, which includes $Y$ — so $X$ **is** extraneous in $WX\to Y$; replace it with $W \to Y$.
Updated set: $\{W\to X,\ W\to Y,\ Y\to Z,\ Y\to X\}$.
(b) **Right-hand sides** are already singleton attributes — no change needed.
(c) **Remove redundant FDs.** Test each FD by checking if it's derivable from the rest:
 - $W\to X$: closure of $\{W\}$ under $\{W\to Y, Y\to Z, Y\to X\}$ alone: $W\to Y$ gives $\{W,Y\}$; $Y\to Z$ gives $\{W,Y,Z\}$; $Y\to X$ gives $\{W,X,Y,Z\}$ — includes $X$, so **$W\to X$ is redundant**; drop it.
 - Remaining: $\{W\to Y,\ Y\to Z,\ Y\to X\}$. Test $W\to Y$: closure of $\{W\}$ under $\{Y\to Z, Y\to X\}$ alone is just $\{W\}$ (no FD has LHS $\subseteq \{W\}$) — $Y \notin \{W\}^+$, so $W\to Y$ is **not** redundant; keep it.
 - Test $Y\to Z$: closure of $\{Y\}$ under $\{W\to Y, Y\to X\}$ is $\{Y,X\}$ — $Z\notin$, not redundant; keep.
 - Test $Y\to X$: closure of $\{Y\}$ under $\{W\to Y, Y\to Z\}$ is $\{Y,Z\}$ — $X\notin$, not redundant; keep.

**Minimal cover: $F_c = \{\,W\to Y,\ \ Y\to Z,\ \ Y\to X\,\}$.**

**A8.** [2 Marks]
```sql
SELECT PID
FROM Product
WHERE Price > ALL (
    SELECT Price FROM Product WHERE Category = 'Budget'
);
```

**A9.** [4 Marks]
```
BundledWith (primary_PID, primary_Name, primary_Price,
             secondary_PID, secondary_Name, secondary_Price,
             DiscountPercent)
```
Since both roles reference the same entity set `Product`, every attribute of `Product` must appear twice, each copy prefixed by its role name (`primary_`, `secondary_`) to avoid ambiguity — directly analogous to the `parentName, parentDOB, childName, childDOB` construction for the self-relationship `parentOf` shown in class.

**A10.** [5 Marks]
**Axioms:**
- *Reflexivity*: If $B \subseteq A$, then $A \to B$.
- *Augmentation*: If $A \to B$, then $AC \to BC$ for any $C$.
- *Transitivity*: If $A \to B$ and $B \to C$, then $A \to C$.

**Proof of the Union Rule** ($A\to B$ and $A\to C$ $\Rightarrow$ $A \to BC$):
1. Given: $A \to B$. By Augmentation (adding $A$ to both sides): $AA \to BA$, i.e. $A \to AB$. — (i)
2. Given: $A \to C$. By Augmentation (adding $B$ to both sides): $AB \to CB$, i.e. $AB \to BC$. — (ii)
3. From (i), $A \to AB$, and from (ii), $AB \to BC$. By Transitivity applied to (i) and (ii): $A \to BC$. $\blacksquare$

**A11.** [3 Marks]
Bag semantics: multiplicity in $R\cup S$ = sum of multiplicities; in $R\cap S$ = minimum of multiplicities; in $R-S$ = $\max(0, \text{mult}_R - \text{mult}_S)$.

| Tuple | mult in $R$ | mult in $S$ | $R\cup S$ | $R\cap S$ | $R-S$ |
|---|---|---|---|---|---|
| $(1,a)$ | 3 | 1 | 4 | 1 | 2 |
| $(2,b)$ | 1 | 2 | 3 | 1 | 0 |
| $(3,c)$ | 0 | 1 | 1 | 0 | 0 |

**A12.** [4 Marks]
This rule is **unsafe**. The variable `Bonus` appears only in the **arithmetic atom** `Bonus > 10000`, and not in any non-negated relational subgoal — arithmetic atoms do not bind variables (they only test already-bound values), so `Bonus` is unbound, violating the safety condition. Fix, given the (now-assumed) EDB predicate `Employee(Name, Salary, Bonus)`:
```
BigBonus(Name, Bonus) :- Employee(Name, Salary, Bonus), Bonus > 10000.
```
Now `Bonus` is bound by the relational subgoal `Employee(Name, Salary, Bonus)` before the arithmetic atom tests it, making the rule safe.

**A13.** [6 Marks]
(a) $\{SSN\}^+$ = all attributes (given directly), and no proper subset of $\{SSN\}$ can be a key since it is a single attribute — so $\{SSN\}$ is the candidate key. $Zip \to City, State$ has LHS $\{Zip\}$, and $\{Zip\}^+ = \{Zip, City, State\} \neq$ all attributes (missing $SSN$), so $\{Zip\}$ is **not** a superkey — this FD violates BCNF.
(b) Decomposing on $Zip \to City, State$:
 - $R_1(Zip, City, State)$ — attributes $X \cup Y$
 - $R_2(SSN, Zip)$ — attributes $X \cup (\text{all} - X - Y)$
(c) The decomposition is lossless because $Zip$ (the common attribute) is a key of $R_1$. However, it is **not dependency-preserving**: the original FD $SSN \to City, State$ cannot be verified by examining $R_1$ or $R_2$ in isolation — $R_2$ has no `City`/`State` columns, and $R_1$ has no `SSN` column, so checking this FD requires **joining** $R_1 \bowtie R_2$ back together. This is an intrinsic trade-off of the BCNF algorithm: it always guarantees losslessness, but (unlike 3NF decomposition via minimal cover) it does not guarantee that every original FD remains checkable without a join.

**A14.** [4 Marks]
```sql
SELECT DeptID, AVG(Salary) AS AvgDeptSalary
FROM Employee
GROUP BY DeptID
HAVING COUNT(*) >= 3
   AND AVG(Salary) > (SELECT AVG(Salary) FROM Employee);
```

**A15.** [5 Marks]
```sql
SELECT C.CustID
FROM Customer C
WHERE NOT EXISTS (
    SELECT P.PID
    FROM Product P
    WHERE P.Category = 'Electronics'
      AND NOT EXISTS (
          SELECT 1 FROM Bought B
          WHERE B.CustID = C.CustID AND B.PID = P.PID
      )
);
```
The inner `NOT EXISTS` finds Electronics products the customer has *not* bought; the outer `NOT EXISTS` keeps only customers for whom no such "not bought" product exists — i.e., customers who bought **every** Electronics product. This is the standard double-negation (relational division) pattern.
