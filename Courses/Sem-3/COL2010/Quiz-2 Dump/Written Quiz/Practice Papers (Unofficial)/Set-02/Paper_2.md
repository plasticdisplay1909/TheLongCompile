# COL2010 — Data Cleaning & Preprocessing: 5 Sample Practice Papers

*Format and difficulty benchmarked against Quiz 1 (short-answer / prove-or-disprove / step-by-step computation, 2–3 points each). Content drawn from the Data Cleaning lecture notes (quality dimensions, profiling & validation, similarity & distance, entity resolution, missing data, and outlier detection / transformation).*

---

## Sample Paper 1

**Questions Only — 15 questions**

1. **(2 points)** A customer table contains a duplicate entry for the same person written two ways, an income value of −50,000, and a missing city value. For each of these three problems, name the data-quality dimension it violates and state the typical response to it.

2. **(2 points)** Prove or disprove: completeness and validity are independent dimensions — a column can be 100% complete (no missing values) yet 0% valid (every present value violates the domain rule).

3. **(2 points)** A column profile for Annual_Income reports that the mean substantially exceeds the median. What does this indicate about the shape of the distribution? Justify your answer.

4. **(2 points)** For a table containing BirthDate and GraduationDate, write one single-field validation rule and one cross-field validation rule. State, for each, an example input that would PASS and one that would FLAG.

5. **(2 points)** In a weighted entity-resolution score, the field weights are Name = 0.30, DOB = 0.30, City = 0.15, Email = 0.25. For a given candidate pair, Email evidence is unavailable. Renormalize the remaining three weights, then compute the aggregate score if Name similarity = 0.90, DOB similarity = 1.00, and City similarity = 0.50. Show all steps.

6. **(2 points)** Two strings are compared with the Jaro measure: m = 5 matching characters, t = 0 transpositions, s₁ = 6, s₂ = 7, and a shared prefix of length ℓ = 2 (Winkler p = 0.1). Compute the Jaro similarity and then the Jaro–Winkler similarity, showing all steps.

7. **(2 points)** Prove that for any two points x, y ∈ ℝ², the Minkowski L∞ distance is always less than or equal to the L2 distance between them.

8. **(2 points)** Two customers' binary purchase records give M₁₁ = 3, M₁₀ = 2, M₀₁ = 1, M₀₀ = 4. Compute the Simple Matching Coefficient and the Jaccard similarity. Explain why the two values differ so much.

9. **(3 points)** The Fellegi–Sunter agreement weight is w = log(m/u). For the Email field, m = 0.92 and u = 0.02; for the City field, m = 0.85 and u = 0.30. Compute the weight contributed by each field. Which field contributes stronger evidence for a match, and why does this model weight rare agreements more heavily than common ones?

10. **(2 points)** A database of 10,000 records is partitioned by a blocking key into 4 disjoint blocks of sizes 3,000, 2,500, 2,500, and 2,000. Using C(n,2) = n(n−1)/2, compute the total number of within-block candidate pairs generated, and compare this to the number of pairs required by exhaustive (unblocked) comparison.

11. **(2 points)** A candidate pair falls into the "clerical review" zone of the three-zone decision framework. Explain what this zone represents and why it exists, referring to the roles of T_lower and T_upper.

12. **(2 points)** Three pairwise decisions are made: (A,B) match, (B,C) match, (A,C) non-match. Explain the transitivity problem this creates for forming entity clusters, and name two approaches to resolving pairwise decisions into a coherent partition.

13. **(2 points)** A MAR check compares the mean Age of rows where Income is observed against rows where Income is missing, and finds a large difference. What does this suggest about the missingness mechanism for Income? Can this test alone prove that Income is MNAR? Justify your answer.

14. **(2 points)** Give one example of a column where mean imputation would be appropriate, one where median imputation would be preferred, and one where a constant fill is more meaningful than either. Justify each choice.

15. **(3 points)** A numeric column has median = 500,000 and MAD = 40,000. For a candidate value x = 700,000, compute the modified z-score z_mod = 0.6745 × (x − median)/MAD. Using the rule of thumb |z_mod| > 3.5, state whether x should be flagged as a candidate outlier. Show all working.

---

## Sample Paper 2

**Questions Only — 15 questions**

1. **(2 points)** A profile of Annual_Income reports "5.4% missing," "mean substantially exceeds median," and "extreme minimum and maximum values." For each of these three observations, state the question it raises about the data — recall that a profile identifies questions, it does not decide repairs.

2. **(2 points)** Prove or disprove: if a dataset satisfies uniqueness (each real-world entity appears only once), it must also satisfy accuracy (stored values correctly represent reality).

3. **(2 points)** Completeness is defined as non-missing / expected values. A table expects 12,000 customer income values; profiling finds 780 missing. Compute the completeness metric as a percentage.

4. **(2 points)** The notes give "GraduationDate ≥ BirthDate + 15 years" as a cross-field rule and "every DepartmentID in Employee exists in Department" as a cross-table rule. Propose one additional rule of your own choosing, classify it as single-field, cross-field, or cross-table, and give one PASS and one FLAG example for it.

5. **(2 points)** Using the recurrence D(i,0) = i, D(0,j) = j, D(i,j) = min(D(i−1,j)+1, D(i,j−1)+1, D(i−1,j−1)+[xᵢ≠yⱼ]), compute the edit distance between "CAT" and "CART." State the minimal edit sequence.

6. **(2 points)** Two strings of length 5 and 6 are compared with Jaro similarity: m = 4 matches, t = 0 transpositions, and a shared prefix of length ℓ = 2 (p = 0.1). Compute the Jaro similarity and the Jaro–Winkler similarity, showing all steps.

7. **(2 points)** Two customers' binary purchase records give M₁₁ = 2, M₁₀ = 3, M₀₁ = 1, M₀₀ = 5. Compute the SMC and the Jaccard similarity. If "did not purchase" is not informative (shared absences should not count as evidence of similarity), which measure is more appropriate, and why?

8. **(3 points)** Prove that Mahalanobis distance reduces to ordinary Euclidean distance in standardized coordinates when the covariance matrix Σ = I, starting from d_M(x, μ) = √((x−μ)ᵀΣ⁻¹(x−μ)).

9. **(2 points)** A candidate pair has field-comparison evidence γ(a,b) = (Name = 0.88, DOB = 1.00, City = 0.60, Phone = 1.00, Email = 0.75) and all fields are present, with weights (0.25, 0.25, 0.10, 0.20, 0.20). Compute the aggregate similarity score S(a,b).

10. **(2 points)** Explain why Soundex(last name) equality is a weaker blocking key than an exact postal-code match, in terms of the recall/precision trade-off, and why "a blocking rule creates a candidate pair; it is not sufficient evidence for a match."

11. **(2 points)** A dataset shows that rows where Salary is missing are disproportionately from respondents in a high self-reported wealth bracket, even after conditioning on Gender and Age. Classify this missingness mechanism and justify your classification using Rubin's taxonomy.

12. **(2 points)** State one advantage and one disadvantage of listwise deletion versus attribute (column) deletion, and identify the condition under which each is statistically defensible.

13. **(2 points)** A missing Income value is imputed using KNN with k = 5 nearest neighbours (matched on Age and City), whose income values are ₹7,20,000; ₹6,90,000; ₹8,10,000; ₹7,50,000; and ₹7,00,000. Compute the imputed value using a plain (unweighted) average.

14. **(2 points)** Explain why evaluating an imputation method must mask only cells whose true value is already known, rather than checking directly on the originally missing cells. Name two error metrics proposed for numeric columns and explain how they differ in penalizing large errors.

15. **(2 points)** A telemetry record shows a host reporting 3% CPU utilization while serving 40,000 requests/second. Neither value alone is extreme. Classify this as a univariate, multivariate, or contextual outlier, and name one detector suited to catching this kind of anomaly.

---

## Sample Paper 3

**Questions Only — 15 questions**

1. **(2 points)** Explain the difference between data profiling and data validation, using the statement "a profile identifies questions; it does not decide repairs" to frame your answer.

2. **(2 points)** Prove or disprove: consistency and uniqueness are the same data-quality dimension, since both concern how records relate to one another.

3. **(2 points)** Validity is defined as valid values / observed values. A column of 40,000 observed Age values contains 38,200 values within the allowed range [0, 120]. Compute the validity metric.

4. **(2 points)** Give an example of a single value that could simultaneously violate two different data-quality dimensions, and name both dimensions it violates.

5. **(2 points)** Compute d₁ (L1), d₂ (L2), and d∞ (L∞) between the points x = (2, 9) and y = (7, 5).

6. **(2 points)** Prove that for any x, y ∈ ℝ², d∞(x,y) ≤ d₂(x,y) ≤ d₁(x,y).

7. **(2 points)** Two count vectors are a = (2, 0, 4) and b = (1, 0, 2). Compute the cosine similarity between them, and explain — using the property that cosine is insensitive to positive rescaling — why it takes the value it does.

8. **(2 points)** A record has fields Age (numeric), Country (categorical), Purchased (binary), and Interests (set-valued). For each field type, state the comparison method the notes recommend, and justify one of your four choices.

9. **(2 points)** Compute m/u for the City field (m = 0.90, u = 0.25) and the Phone field (m = 0.95, u = 0.00001). Explain, in Fellegi–Sunter terms, why "weak" and "very strong" evidence differ by orders of magnitude here.

10. **(2 points)** A weighted match score uses Name = 0.40, Phone = 0.30, Email = 0.20, City = 0.10. For a candidate pair, Phone evidence is unavailable. Renormalize the remaining weights and state the new weight assigned to each remaining field.

11. **(2 points)** Explain why a golden record produced by consolidation must preserve provenance rather than simply overwrite conflicting field values with the most recent source.

12. **(2 points)** A Test_Score column has values missing only when this depends on the observed variable Attendance, not on the (unobserved) score itself. Classify the missingness mechanism, and state whether deleting incomplete rows would introduce systematic bias.

13. **(3 points)** An iterative (round-robin) imputation procedure updates Income, then Age, then Height, then Weight, cycling until convergence. Explain, step by step, why later cycles typically improve on the first cycle's imputed values, and state which cells are updated on each pass.

14. **(2 points)** Given Q1 = 40 and Q3 = 76 for a numeric column, compute the IQR, and the lower and upper boxplot fences (Q1 − 1.5×IQR, Q3 + 1.5×IQR). Is a value of 140 flagged as an outlier candidate?

15. **(2 points)** State one weakness of z-score outlier detection related to non-robust estimators, and explain concretely how the modified z-score (using median and MAD) addresses this weakness.

---

## Sample Paper 4

**Questions Only — 15 questions**

1. **(2 points)** List the seven stages of the data-cleaning pipeline given in the module map, and state which stage most directly consumes the outputs of "Resolve entities."

2. **(2 points)** Distinguish preventive controls from corrective controls in data-quality management, giving two examples of each.

3. **(2 points)** Prove or disprove: a completeness score of 100% guarantees a validity score of 100%.

4. **(2 points)** A relationship profile reports that a functional-dependency-like pattern "RollNumber → StudentName" is violated in 40 of 10,000 rows. What does a violation of this kind typically signal about the underlying records, and which cleaning stage would you use to investigate it?

5. **(2 points)** Compute the L1, L2, and L∞ distances between the vectors x = (15, 3, 8) and y = (10, 9, 5).

6. **(2 points)** The strings "Meera" and "Mira" are compared with edit distance. List a minimal sequence of edit operations transforming one into the other, and state the resulting edit distance.

7. **(2 points)** Given Jaro parameters m = 3, t = 1, s₁ = 6, s₂ = 6, and prefix length ℓ = 0 (p = 0.1), compute the Jaro similarity and the Jaro–Winkler similarity. Explain why the Winkler boost has no effect here.

8. **(2 points)** Customer X has interests {AI, DB, ML} and customer Y has {DB, ML, Cloud}. Compute the generalized Jaccard similarity J(X, Y).

9. **(2 points)** Distinguish deduplication, record linkage, and entity resolution as terms, and state which one applies when matching a CRM customer table against a separate KYC table with no shared identifier.

10. **(2 points)** Given m/u ratios Phone = 95,000, DOB = 323, City = 3.6, rank the three fields from strongest to weakest evidence using w = log(m/u), and explain why a rare agreement (matching phone numbers) contributes more evidence than a common one (matching city).

11. **(2 points)** A missingness diagnostic finds that, for target column Email, the difference in missingness rate between rows with observed vs. missing Email is close to zero for every supplied conditioning column. What does this pattern suggest about the missingness mechanism, and what deletion method might this justify?

12. **(2 points)** Explain why "distortion" occurs after mean imputation, and describe what an artificial spike in the post-imputation distribution indicates about the imputed column.

13. **(3 points)** A numeric column has mean = 52 and standard deviation = 9. Using the rule |z| ≥ 3, determine whether a value of 25 is flagged. Now suppose several extreme values elsewhere in the column have already inflated σ. Explain, using the concept of "masking," why the z-score rule might fail to catch a genuine outlier in this column.

14. **(2 points)** Distinguish min-max normalization from z-score standardization in terms of (a) whether the result is bounded, and (b) sensitivity to outliers. Name one algorithm for which each scaling method is typically preferred.

15. **(2 points)** A pipeline fits an imputer and a scaler on the entire dataset (train and test together) before splitting. Name the error this constitutes and describe the correct order of operations to avoid it.

---

## Sample Paper 5

**Questions Only — 15 questions**

1. **(2 points)** A raw City column contains "Bengaluru" (18,420), "Bangalore" (7,910), "BENGALURU" (1,105), "Bengluru" (316), and "Banglore" (73). Describe the three-step normalization flow that would canonicalize all of these to one value, and name the canonical value.

2. **(2 points)** Prove or disprove: profiling a dataset is unnecessary once it has passed all validation rules, since profiling and validation test the same thing.

3. **(2 points)** A Phone column has 9,000 expected values, of which 8,550 are present, and of those, 8,200 pass the phone-format validation rule. Compute both the completeness metric and the validity metric for this column.

4. **(2 points)** A record profile flags "Ananya Rao" / "A. Rao" as a duplicate candidate, and separately flags Age = 240 and Income = −50,000 as rule violations. Explain the difference between what a "duplicate candidate" flag and a "rule violation" flag each indicate, and which downstream cleaning stage each feeds into.

5. **(2 points)** Two standardized customer vectors are A = (0.5, 1.2, −0.3) and B = (0.9, 0.7, −0.1). Compute the L1 and L2 distances between A and B.

6. **(2 points)** Using the diamond / circle / square geometric interpretation of L1, L2, and L∞, explain why two points that are equally far apart under L1 need not be equally far apart under L∞.

7. **(2 points)** Two phone-number records "+91-98450-12345" and "9845012345" are compared using "normalize, then exact match." After standardization, do these values match? Explain why standardization (Step 1 of the entity-resolution pipeline) is necessary before this comparison can succeed.

8. **(2 points)** Given m = 6 matches, t = 1 transposition, s₁ = s₂ = 6, shared prefix ℓ = 3, and p = 0.1, compute the Jaro similarity and the Jaro–Winkler similarity from first principles.

9. **(2 points)** A blocking scheme uses "email domain + birth year" as its key. Give one advantage and one risk of this key compared to using "same postal code," in terms of which true duplicate pairs might be missed.

10. **(2 points)** Explain why narrowing the gap between T_lower and T_upper (shrinking the clerical-review zone) increases the risk of both false matches and missed matches, compared to a wider review zone.

11. **(2 points)** An Age field is MCAR, and only 2% of its rows are missing. Using the deletion-methods comparison from the notes, justify using listwise deletion here rather than KNN imputation, referencing cost and bias considerations.

12. **(2 points)** Explain why adding an Income_missing_flag alongside an imputed Income_imputed column can improve a downstream model even after every gap has already been filled.

13. **(3 points)** Five numeric cells with true values [100, 150, 120, 90, 200] are imputed as [110, 140, 130, 95, 180]. Compute the RMSE of this imputation.

14. **(2 points)** A Mahalanobis-distance calculation gives a smaller distance for a customer who deviates in the direction of high natural covariance (taller-and-heavier) than for one with the same raw Euclidean displacement in a direction of low natural covariance (taller-but-lighter). Explain why Mahalanobis distance treats these two displacements differently even though their raw displacements from the mean are equal.

15. **(2 points)** State the intuition behind Local Outlier Factor (LOF) and Isolation Forest as two different multivariate outlier-detection strategies, and describe one scenario where LOF would catch an anomaly that a single global Mahalanobis-distance threshold might miss.

---

## Sample Paper 6

**Questions Only — 15 questions**
*(Each question asks you to prove a general claim and then confirm it against specific numbers — show all algebraic and arithmetic steps.)*

1. **(3 points)** Prove that the min–max normalized value x′ = (x − x_min)/(x_max − x_min) is a strictly increasing (order-preserving) function of x whenever x_max > x_min. Then, for a column with x_min = 12, x_max = 30, compute x′ for x = 18 and x = 24, and verify x′(24) > x′(18).

2. **(3 points)** Prove that z-score standardization z = (x − μ)/σ (σ > 0) preserves the ordering of any two values x₁ < x₂. Then, for μ = 50, σ = 8, compute z for x₁ = 42 and x₂ = 58, and verify z₁ < z₂.

3. **(3 points)** Prove that the L1 distance on the real line satisfies the triangle inequality: |a − c| ≤ |a − b| + |b − c| for any real a, b, c. Then verify this numerically for a = 5, b = 20, c = 9.

4. **(3 points)** Prove that the L∞ distance between two points in ℝ² is the limit of the Lp distance as p → ∞. Then, for x = (3, 11) and y = (9, 15), compute d_p for p = 1, 2, and 4, and show that these values decrease toward d∞ = max(|Δx|, |Δy|).

5. **(3 points)** Prove that cosine similarity is invariant to scaling either vector by a positive constant: cos(x, c·y) = cos(x, y) for any c > 0. Then verify numerically using x = (3, 4) and y = (1.5, 2), where y = 0.5·x.

6. **(3 points)** Prove that Jaccard similarity J(A,B) = |A∩B| / |A∪B| always lies in the closed interval [0, 1] for any two nonempty finite sets A and B. Then compute J(A,B) for A = {AI, DB, ML, Cloud} and B = {DB, ML, Security}.

7. **(3 points)** Prove that a weighted aggregate score S(a,b) = Σ wⱼsⱼ(a,b), where the weights wⱼ sum to 1 and each field similarity sⱼ ∈ [0,1], must itself lie in [0,1]. Then verify this bound using weights Name = 0.4, DOB = 0.3, City = 0.3 and similarities 0.9, 1.0, 0.2 respectively.

8. **(3 points)** Prove that renormalizing a subset of weights after dropping a missing field — replacing each remaining weight wⱼ with wⱼ divided by the sum of the remaining weights — always produces new weights that sum exactly to 1, regardless of which field was dropped. Then verify this using original weights Name = 0.35, DOB = 0.30, City = 0.20, Phone = 0.15, with Phone missing.

9. **(3 points)** Prove that the arithmetic mean of k values minimizes the sum of squared deviations Σ(xᵢ − c)² over all choices of constant c (the property that justifies averaging the k nearest neighbours for imputation). Then, for neighbour values 640,000; 700,000; 660,000; 720,000, compute the mean and show its sum of squared deviations is smaller than the sum of squared deviations from c = 750,000.

10. **(3 points)** Prove that RMSE ≥ MAE for any nonzero vector of errors e₁,…,eₙ. Then, for imputation errors [4, 6, 2, 8], compute RMSE and MAE and confirm RMSE ≥ MAE.

11. **(3 points)** Prove that the modified z-score z_mod = 0.6745(x − median)/MAD is an affine, order-preserving transformation of x whenever MAD > 0, so ranking records by z_mod gives the same order as ranking by raw distance from the median. Then, for median = 300,000 and MAD = 25,000, compute z_mod for x = 340,000 and x = 410,000, and confirm the ranking matches the raw ordering.

12. **(3 points)** Prove that for a diagonal covariance matrix Σ = diag(σ₁², σ₂²), the Mahalanobis distance reduces to d_M(x,μ) = √(Σᵢ (xᵢ−μᵢ)²/σᵢ²). Then compute d_M for x = (180, 42), μ = (170, 65), σ_Height = 10, σ_Weight = 12.

13. **(3 points)** Prove that log₁₀ is a strictly increasing (order-preserving) function on x > 0, and hence a log transform never reorders a positive column. Then, for Income values 25,000 and 250,000, compute log₁₀ of each and verify that the tenfold gap in raw units compresses to a difference of exactly 1 in log-space.

14. **(3 points)** Prove that the Simple Matching Coefficient SMC = (M₁₁+M₀₀)/(M₁₁+M₁₀+M₀₁+M₀₀) always equals 1 when two binary records are identical (M₁₀ = M₀₁ = 0), regardless of how many attributes are compared. Then verify with M₁₁ = 4, M₀₀ = 6, M₁₀ = M₀₁ = 0.

15. **(3 points)** Prove that the completeness metric (non-missing / expected) and the validity metric (valid / observed) can each independently range from 0 to 1, and that validity depends only on the observed subset, not on how many values were expected. Then, for a column with expected = 1,000, non-missing (observed) = 850, and valid = 816, compute completeness and validity, and confirm they need not move together.

---

## Sample Paper 7

**Questions Only — 15 questions**
*(Each question asks you to prove a general claim and then confirm it against specific numbers — show all algebraic and arithmetic steps.)*

1. **(3 points)** Prove that the L2 distance satisfies the triangle inequality, and verify with the collinear points a = (0,0), b = (1,1), c = (2,2) that equality d(a,c) = d(a,b) + d(b,c) holds when b lies directly between a and c.

2. **(3 points)** Prove that Jaro similarity J(x,y) = ⅓(m/s₁ + m/s₂ + (m−t)/m) is symmetric, i.e., J(x,y) = J(y,x). Then verify with s₁ = 6, s₂ = 8, m = 5, t = 1 by computing J using (s₁,s₂) and again using (s₂,s₁).

3. **(3 points)** Prove that the Jaro–Winkler score JW = J + ℓp(1−J) is always ≥ J whenever ℓ > 0 and 0 < p ≤ 0.25, i.e., the prefix boost never decreases similarity. Then verify with J = 0.70, ℓ = 4, p = 0.1.

4. **(3 points)** Prove that Mahalanobis distance is invariant to shifting both x and μ by the same constant vector a. Then verify numerically for x = (50,20), μ = (40,10), Σ = diag(25,4), by computing d_M before and after adding a = (100,100) to both x and μ.

5. **(3 points)** Prove that SMC and Jaccard similarity coincide exactly when M₀₀ = 0 (no shared absences). Then verify with M₁₁ = 3, M₁₀ = 1, M₀₁ = 2, M₀₀ = 0.

6. **(3 points)** Prove that for any two positive reals p < q, log₁₀(q) − log₁₀(p) = log₁₀(q/p), so the log-space gap between two values depends only on their ratio, not their absolute difference. Then verify using the pairs (20, 200) and (200, 2000), both with ratio 10, and show both give the same log-gap despite very different raw gaps.

7. **(3 points)** Prove that a Fellegi–Sunter score for k independent fields, W = Σ log(mⱼ/uⱼ), equals the logarithm of the product Π(mⱼ/uⱼ). Then, for three fields with m/u ratios 95,000, 323, and 3.6, compute the product of the ratios and confirm that log₁₀ of that product equals the sum of the individual log₁₀(mⱼ/uⱼ) values.

8. **(3 points)** Prove that min–max normalization maps the minimum of a column to exactly 0 and the maximum to exactly 1 whenever x_max > x_min. Then, for the column {12, 15, 18, 24, 30}, compute the normalized value at both endpoints and at x = 18.

9. **(3 points)** Prove algebraically that replacing the largest value in a small, sorted dataset with an extreme value leaves the median unchanged but can shift the mean arbitrarily far. Using {10, 12, 14, 16, 18}, compute the mean and median before and after replacing 18 with 1000, and confirm the median is unaffected while the mean shifts substantially.

10. **(3 points)** Prove that, since 1.5×IQR ≥ 0, any value strictly between Q1 and Q3 must lie inside the boxplot fences [Q1 − 1.5×IQR, Q3 + 1.5×IQR] — the interquartile region is always a subset of the fenced "normal" region. Then, for Q1 = 25 and Q3 = 65, compute the fences and confirm the midpoint of Q1 and Q3 lies well inside them.

11. **(3 points)** Prove that KNN imputation with k = 1 always reproduces exactly one observed neighbour's value, while averaging over a larger k smooths the imputed value toward the local mean (reducing its distance from typical values). Then compute the imputed value for k = 2 (neighbours 500,000 and 900,000) and for k = 4 (neighbours 500,000; 900,000; 650,000; 700,000), and confirm the k = 4 estimate sits closer to the bulk of the neighbourhood, further from the extreme 900,000, than the k = 2 estimate.

12. **(3 points)** Prove that any convex combination S = w·s₁ + (1−w)·s₂ of two similarity scores s₁, s₂ ∈ [0,1], with 0 ≤ w ≤ 1, itself lies in [0,1]. Then compute S for w = 0.7, s₁ = 0.95, s₂ = 0.10, and confirm it lies between s₂ and s₁.

13. **(3 points)** Prove that renormalizing a set of weights preserves the ratio between any two remaining weights (since all remaining weights are divided by the same constant). Then verify using original weights Name = 0.30, DOB = 0.20, City = 0.10 (Phone = 0.40 missing): compute the renormalized weights and confirm the Name : DOB ratio is still 3 : 2.

14. **(3 points)** Prove that RMSE is a strictly increasing function of the sum of squared errors (SSE) for a fixed number of masked cells n, so the method with lower SSE always has the lower RMSE. Then, given SSE = 480 for Method A and SSE = 650 for Method B on n = 5 masked cells, compute RMSE for each and confirm the ordering matches.

15. **(3 points)** Prove that adding a constant c to every value in a column leaves its standard deviation unchanged, and hence leaves every z-score (and therefore every z-score-based outlier flag) unchanged. Then verify using {40, 50, 60} versus the shifted set {140, 150, 160}, showing the z-score of the smallest value is identical in both cases.

---

## Sample Paper 8

**Questions Only — 15 questions**
*(Prove each general claim, then verify it on the specific numbers given — show all steps.)*

1. **(3 points)** Prove that after z-score standardization, a column has mean exactly 0 and variance exactly 1. Then verify with {2, 4, 6, 8, 10}: compute the mean and (population) standard deviation, standardize each value, and confirm the standardized mean is 0 and variance is 1.

2. **(3 points)** Prove that scaling every value in a column by a positive constant c multiplies its standard deviation by c, so z-scores are invariant to positive linear rescaling of units. Then verify using {10, 20, 30} versus {30, 60, 90} (scaled by c = 3): compute σ for both, confirm the ratio is 3, and confirm the z-score of 10 (original) equals the z-score of 30 (scaled).

3. **(3 points)** Prove that C(n,2) = n(n−1)/2 grows quadratically, so doubling n roughly quadruples the number of candidate pairs under exhaustive matching. Then compute C(n,2) for n = 2,000 and n = 4,000 and confirm the ratio is approximately 4.

4. **(3 points)** Prove that splitting n records into b disjoint equal-sized blocks reduces the number of within-block candidate pairs to b·C(n/b, 2), and that this is smaller than C(n,2) by roughly a factor of b for large n. Then, for n = 1,000,000 split into b = 100 equal blocks, compute the number of blocked candidate pairs and compare it to the ≈500 billion pairs required without blocking.

5. **(3 points)** Prove that edit (Levenshtein) distance satisfies the triangle inequality: d(x,z) ≤ d(x,y) + d(y,z) for any strings x, y, z. Then verify with x = "CAT", y = "CART", z = "CARTS": compute d(x,y), d(y,z), and d(x,z), and confirm the inequality (note whether it holds with equality).

6. **(3 points)** Prove that the Winkler prefix-boost term ℓp(1−J) is maximized, for fixed J and p, at the capped value ℓ = 4, regardless of how long the true common prefix actually is. Then compute JW for J = 0.80, p = 0.1 at ℓ = 2 and at ℓ = 4, and confirm the boost is larger at ℓ = 4.

7. **(3 points)** Prove that robust scaling's center (median) and scale (IQR) are unaffected by changing an existing extreme value to an even more extreme one, as long as it remains the maximum (or minimum) of the data. Then, for a 9-point dataset with median = 50 and IQR = 40, compute the robust-scaled value of the maximum point when it equals 90, and again when that same point is changed to 900 — noting that its own scaled value changes sharply while the median and IQR used for every other point do not.

8. **(3 points)** Prove that discretization (binning) is not injective — two distinct values can map to the same bin — and therefore loses ordering information at the resolution of the original variable even though it preserves the coarse order between bins. Then verify using bins Young (<30), Middle (30–45), Senior (>45): confirm ages 31 and 44 fall into the same bin despite being different values.

9. **(3 points)** Prove that aggregating n independent daily values (each with standard deviation σ) into a monthly sum reduces the *relative* noise (coefficient of variation) by a factor of √n, since Var(sum) = nσ² while the sum's mean scales as n. Then, for daily purchases with σ = ₹200 and mean ₹1,000 over a 30-day month, compute the CV of a single day and the CV of the monthly total, and confirm their ratio is √30.

10. **(3 points)** Prove that a feature-construction ratio such as debt-to-income is invariant to converting both numerator and denominator by the same positive exchange-rate factor c. Then verify with debt = ₹200,000, income = ₹800,000 (ratio 0.25), converted to USD at ₹80/$ (debt = $2,500, income = $10,000), and confirm the ratio is unchanged.

11. **(3 points)** Prove that fitting a scaler's parameters on the training set only and applying them unchanged to the test set does not, in general, make the transformed test-set mean exactly 0 (this is expected, not evidence of leakage). Then, given train mean = 50 and train σ = 10, compute the standardized values of test points x = 55 and x = 70, and confirm their average is not 0.

12. **(3 points)** Prove that the pooled "OVERALL" RMSE across several columns (computed from the combined squared errors of all masked cells) is generally not equal to the simple average of the per-column RMSEs. Then, given column A has 2 masked cells with squared errors 4 and 16, and column B has 3 masked cells with squared errors 9, 9, and 36, compute RMSE_A, RMSE_B, their simple average, and the pooled OVERALL RMSE across all 5 cells — and show the two summary numbers differ.

13. **(3 points)** Prove that Σ(xᵢ − c)² is minimized uniquely at c = mean(x), and that this minimum value equals (n−1) times the sample variance. Then, for {5, 10, 15}, compute the mean, the minimal sum of squared deviations, and confirm it equals (n−1) × sample variance.

14. **(3 points)** Prove that the Pearson correlation coefficient between two variables is unchanged by independently standardizing each variable (correlation is scale- and location-invariant). Then, for X = (2, 4, 6) and Y = (3, 7, 5), compute corr(X,Y) directly, standardize both variables, recompute the correlation on the standardized values, and confirm they match.

15. **(3 points)** Prove that SMC and Jaccard similarity are undefined and defined, respectively, in the edge case where M₁₁ = M₁₀ = M₀₁ = 0 and M₀₀ > 0 (all shared absences), while both equal exactly 1 when M₁₀ = M₀₁ = M₀₀ = 0 and M₁₁ > 0 (all shared presences). Verify both edge cases numerically with M₀₀ = 5 (case a) and M₁₁ = 5 (case b).

---

## Sample Paper 9

**Questions Only — 15 questions**
*(Prove each general claim, then verify it on the specific numbers given — show all steps.)*

1. **(3 points)** Prove that mean imputation preserves a column's overall mean but strictly reduces its variance below what the true (unobserved) variance would have been, whenever the missing values are not themselves equal to the mean. Then, for observed values {10, 20, 30} with two missing cells filled by the mean (20), compute the mean and variance of the completed column {10, 20, 30, 20, 20}, and compare that variance to the variance if the two missing values had actually been 5 and 35.

2. **(3 points)** Prove that cosine similarity between two vectors with strictly non-negative entries is always bounded in [0, 1] (a tighter bound than the general [−1, 1] range for arbitrary real vectors). Then verify with a = (0, 3, 4), b = (5, 0, 12): compute cos(a,b) and confirm it lies in [0, 1].

3. **(3 points)** Prove that if two comparison vectors agree on every field except one, the weighted aggregate scores differ by exactly wⱼ·Δsⱼ, where wⱼ is that field's weight and Δsⱼ is the similarity difference on that field. Then verify with weights (Name=0.3, DOB=0.3, City=0.2, Phone=0.2), DOB/City/Phone similarities fixed at 1.0/0.5/1.0, and Name similarity 0.9 versus 0.6 — compute both aggregate scores and confirm their difference equals 0.3×(0.9−0.6).

4. **(3 points)** Prove that under the Fellegi–Sunter model, a field with m = u contributes exactly zero weight (w = log(m/u) = 0) to the match score, i.e., a truly uninformative field drops out of the sum automatically. Then compute w for a field with m = 0.40, u = 0.40, and confirm w = 0.

5. **(3 points)** Prove that increasing the sliding-window width w in the sorted-neighbourhood method can only increase (never decrease) the raw number of candidate pairs generated, since every pair compared under width w is still compared under any w′ > w. Then, for n = 10 sorted records, compute the raw pair count using (n−w+1)·C(w,2) for w = 3 and w = 5, and confirm the count grows with w.

6. **(3 points)** Prove that the modified z-score constant 0.6745 makes z_mod approximately equal to the ordinary z-score when the data is close to normal, since MAD ≈ 0.6745σ under normality. Then, for σ = 12 and MAD = 8.1, compute z_mod and the ordinary z for x = 90, median = mean = 60, and confirm the two values are close.

7. **(3 points)** Prove that min–max normalization, being a strictly increasing transformation, cannot change the rank order of a feature's values (and therefore cannot change its rank correlation with any other variable). Then, for raw values {5, 20, 15} with rank order (1, 3, 2), compute the min–max normalized values (x_min=5, x_max=20) and confirm the same rank order is preserved.

8. **(3 points)** Prove algebraically that JW = J + ℓp(1−J) ≤ 1 whenever J ≤ 1, ℓ ≤ 4, and p ≤ 0.25 (the standard Winkler constraints), and that the boost term vanishes exactly when J = 1. Then verify with J = 0.95, ℓ = 4, p = 0.1: compute JW and confirm it is ≤ 1.

9. **(3 points)** Prove that Mahalanobis distance is non-negative for any x and equals zero only when x = μ, given that Σ is positive definite. Then verify with x = μ = (30, 500000) that d_M = 0, and compute a nonzero d_M for x = (32, 500000), μ = (30, 500000), Σ = diag(4, 1,000,000).

10. **(3 points)** Prove that the completeness metric (non-missing/expected) can never legitimately exceed 1, since non-missing values cannot exceed the expected count by definition. Then compute completeness for expected = 500, non-missing = 500 (fully complete), and for a second column where non-missing = 510 against the same expected = 500 — and explain what a value above 1 reveals about the "expected" count rather than about completeness itself.

11. **(3 points)** Prove, by constructing a small counterexample, that KNN imputation on raw (unscaled) features can select a different nearest neighbour than KNN imputation on standardized features, whenever the features have very different natural scales. Using target (Age=30, Income=500,000), candidate P=(Age=25, Income=505,000), and candidate Q=(Age=45, Income=500,000), compute the raw Euclidean distance from the target to P and to Q; then, using σ_Age=10 and σ_Income=50,000, compute the standardized distances to P and to Q, and show the nearest neighbour flips between the two calculations.

12. **(3 points)** Prove that the RMSE of a constant-fill imputation strategy (always filling with the same value c) is minimized, over all choices of c, exactly at c = mean of the true masked values. Then, for masked true values {200, 240, 260, 300}, compute the mean and show that filling with c = 250 (the mean) gives a lower RMSE than filling with c = 230.

13. **(3 points)** Prove that appending a 0/1 missingness-indicator column to a feature matrix does not change the Euclidean-distance contribution of any other column, since the indicator adds an independent term to the sum of squared differences. Then, for two records that differ only in Age (by 5, contributing 25 to the squared distance) and share the same flag value, compute the total squared distance with and without the flag column, and confirm they are equal.

14. **(3 points)** Prove that equal-frequency discretization guarantees each of k bins holds (as close as possible to) n/k records, regardless of the variable's distribution shape, unlike equal-width binning. Then, for n = 100 records split into k = 4 equal-frequency bins, state how many records each bin holds, and explain why an equal-width binning of a right-skewed distribution would not give this same balance.

15. **(3 points)** Prove that if a numeric column's IQR is exactly zero (Q1 = Q3), robust scaling x′ = (x − median)/IQR is undefined, and explain what this implies about the proportion of the data sharing the same value. Then give a small 8-value dataset where at least 6 of the 8 values are identical, causing Q1 = Q3, and identify the resulting division-by-zero issue.

---

## Sample Paper 10

**Questions Only — 15 questions**
*(Prove each general claim, then verify it on the specific numbers given — show all steps.)*

1. **(3 points)** Prove that variance is invariant under reflection of the data about its mean — replacing each x with 2μ − x leaves the mean and variance unchanged, even though the sign of skew flips. Then verify with {8, 9, 13} (mean = 10): compute the variance, reflect each point about the mean, and confirm the reflected set {12, 11, 7} has the same mean and variance.

2. **(3 points)** Prove that sample variance computed with an (n−1) divisor is always ≥ the same sum of squared deviations divided by n, for any sample of size n ≥ 2. Then, for {4, 8, 12}, compute the population variance (n divisor) and the sample variance (n−1 divisor), and confirm the ordering.

3. **(3 points)** Prove that the total Fellegi–Sunter evidence W = Σ log(mⱼ/uⱼ) can be negative even when some individual field weights are positive, whenever disagreement weights (computed from (1−m)/(1−u)) are negative and large enough. Then, given Name agrees with weight +2.0 and DOB disagrees with weight −4.5, compute the total evidence W and state whether the pair leans toward MATCH or NON-MATCH.

4. **(3 points)** Prove that in one dimension, Mahalanobis distance equals the absolute ordinary z-score, d_M(x,μ) = |z|, so univariate Mahalanobis-based and z-score-based outlier flags always agree. Then verify with μ = 50, σ = 10, x = 75: compute the z-score and the 1-D Mahalanobis distance and confirm they are equal.

5. **(3 points)** Prove that if every field similarity in a comparison vector equals 1, the weighted aggregate score S = Σwⱼsⱼ equals exactly 1 regardless of the specific weight values, provided the weights sum to 1. Then verify with weights (0.5, 0.3, 0.2) and similarities (1, 1, 1).

6. **(3 points)** Prove that the number of pairs eliminated by blocking equals C(n,2) minus the sum of within-block C(nᵢ,2) over all blocks, and that this quantity is always non-negative. Then, for n = 20 split into blocks of size 12 and 8, compute the number of pairs eliminated by blocking.

7. **(3 points)** Using the worked Income example (raw values 20, 25, 30, 40, 50, 70, 100, 200, 500, 2000 with log₁₀ values 1.30, 1.40, 1.48, 1.60, 1.70, 1.85, 2.00, 2.30, 2.70, 3.30), compute the mean and median of the raw values and of the log-transformed values, and show the mean-to-median ratio moves from roughly 5:1 in raw space to close to 1:1 in log space — illustrating why log transforms tame right skew.

8. **(3 points)** Prove that Jaccard similarity between two disjoint sets (A ∩ B = ∅) is always exactly 0, using |A∪B| = |A|+|B| for disjoint sets. Then verify with A = {AI, DB} and B = {Cloud, Security}.

9. **(3 points)** Prove that if a comparison vector disagrees maximally on every field (similarity 0 everywhere), the weighted aggregate score S = 0 regardless of the weight distribution, provided the weights sum to 1. Then verify with weights (0.6, 0.4) and similarities (0, 0).

10. **(3 points)** Prove that plain-average KNN imputation is a special case of distance-weighted imputation in which every neighbour receives equal weight 1/k, and that the two coincide exactly when all k neighbours are equidistant from the target. Then verify with three equidistant neighbours (values 100, 120, 140) by showing the distance-weighted average equals the plain average.

11. **(3 points)** Prove that the boxplot fence width (upper fence − lower fence) equals exactly 4×IQR, independent of the median or the data's skew. Then, for Q1 = 30, Q3 = 70 (IQR = 40), compute the lower fence, the upper fence, and confirm their difference equals 4×40.

12. **(3 points)** Using {10, 14, 18, 50}, prove informally why including a candidate outlier in the calculation of its own mean and standard deviation dampens its z-score, by computing z(50) using the mean/σ of all four points, and then recomputing z(50) using the leave-one-out mean/σ of {10, 14, 18} only — and confirming the leave-one-out z-score is substantially larger in magnitude.

13. **(3 points)** Prove that adding the same constant to every field similarity in a comparison vector shifts the weighted aggregate score S by exactly that constant, whenever the weights sum to 1 (since S is then an affine function of the similarities). Then verify with weights (0.5, 0.5), original similarities (0.6, 0.8) giving S₁, and similarities shifted by +0.1 to (0.7, 0.9) giving S₂ — confirm S₂ − S₁ = 0.1.

14. **(3 points)** Prove that a typical (non-anomalous) point's expected Isolation Forest path length grows as O(log n), while an anomaly's path length stays roughly constant, so the contrast between the two sharpens as n grows. Illustrate (not a full derivation) using n = 1,000 (log₂1000 ≈ 9.97) and n = 1,000,000 (log₂1,000,000 ≈ 19.93), holding the anomaly's path length fixed at 2 splits in both cases, and compute the ratio of typical-to-anomalous path length for each n to show the contrast roughly doubles.

15. **(3 points)** Prove that two records at sort-order positions i and j (with gap k = |i−j|) are compared by the sorted-neighbourhood method if and only if the window width w satisfies w ≥ k+1. Then, for two duplicate records at positions 2 and 6 in a sorted list of 10, show that a window of width w = 3 fails to compare them while a window of width w = 5 succeeds, and state the minimum window width required in general.
