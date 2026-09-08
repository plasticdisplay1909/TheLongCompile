# Preprocessing & Data Cleaning — 5 Sample Practice Papers
### Modeled on the format, style, and difficulty of Quiz 1 (COL2010) — 15 questions each, 2–3 points per question
### Content drawn from: Missing Data, Model-Based Imputation, Outlier Detection, Data Transformation

---

# SAMPLE PAPER 1

**Questions Only — 15 Questions**

1. (2 points) Explain why a NULL value should be treated as "an observation to be explained" rather than simply an empty cell. Give one example of how ignoring this distinction could bias an analysis.

2. (2 points) A hospital's blood-test dataset has missing "Cholesterol" readings only for patients above age 70, because the device used for older patients frequently malfunctioned regardless of their actual cholesterol level. Identify the missingness mechanism (MCAR / MAR / MNAR) and justify your answer using Rubin's taxonomy.

3. (3 points) A table of 800 rows has a column "Marital_Status" missing in 15 rows (determined to be MCAR) and a column "Secondary_Phone" missing in 540 rows (67.5%) with little analytical value. State which deletion method — listwise, pairwise, or attribute — is appropriate for each column, and justify each choice.

4. (2 points) Prove or disprove: replacing every missing value in a numeric column with the column mean leaves the variance of that column unchanged.

5. (3 points) A record's "Income" (₹'000) is missing. Its three nearest neighbours (already identified by distance in standardized feature space) have Income values 640, 615, and 655. Compute the KNN-imputed value using k = 3 with a plain (unweighted) average. Show your work.

6. (3 points) During evaluation of an imputation method, four originally-observed values were masked and then re-imputed. True values: [58, 71, 44, 93]. Imputed values: [55, 75, 50, 90]. Compute the RMSE and the MAE for this imputation. Show all steps.

7. (2 points) Explain why the pair of columns "Income" and "Income_missing_flag" should both be kept in the final dataset, rather than discarding the flag once imputation is complete.

8. (2 points) Classify each of the following as a univariate, multivariate, or contextual outlier, and justify each in one sentence:
   (a) A recorded resting heart rate of 350 bpm.
   (b) A person recorded as 55 kg with a height of 195 cm.
   (c) A recorded rainfall of 2 mm in Chennai during peak monsoon month.

9. (3 points) A feature's first and third quartiles are Q1 = 22 and Q3 = 48. Compute the IQR and the lower and upper boxplot fences. Would a value of 95 be flagged as an outlier? Justify.

10. (3 points) For the two points x = (3, 9) and y = (7, 2), compute the L1 (Manhattan), L2 (Euclidean), and L∞ (Chebyshev) distances between them. Show your work for each.

11. (3 points) A feature has mean μ = 50, standard deviation σ = 6, median = 49, and MAD = 4. For a value x = 71, compute (a) the ordinary z-score and (b) the modified z-score (using the constant 0.6745). Using thresholds |z| ≥ 3 and |z_mod| > 3.5, state whether the point would be flagged as an outlier under each method.

12. (2 points) Using the idea of a covariance matrix, explain why Mahalanobis distance can treat a "tall and heavy" record as less unusual than an equally-far (in raw Euclidean terms) "tall and light" record.

13. (2 points) State, for each of the following algorithms, whether feature scaling is required, and give one reason: (a) K-Means, (b) Random Forests, (c) Gradient descent–based neural networks, (d) Naïve Bayes.

14. (3 points) A feature has values: 10, 15, 20, 30, 45. Apply Min-Max normalization to rescale these values into [0, 1]. Show your calculations.

15. (2 points) A right-skewed "Revenue" column ranges from ₹18,000 to ₹4,50,00,000. Explain, with reference to the general behaviour of a log transform, why applying log10 to this column would help before feeding it into a distance-based model. You do not need to compute exact log values.

---

# SAMPLE PAPER 2

**Questions Only — 15 Questions**

1. (2 points) A university's course-feedback survey has a missing "Overall_Rating" field only for students who received a low midterm grade — the probability of skipping the rating rises specifically as the (unseen) rating itself would have been lower. Identify the missingness mechanism and justify using Rubin's taxonomy.

2. (2 points) Prove or disprove: under an MAR mechanism, listwise deletion of incomplete rows produces an unbiased estimate of the population mean.

3. (3 points) You are given the raw heterogeneous record: Age = 27, Income = 620000, City = Chennai (one of {Chennai, Delhi, Mumbai}), Purchased = No, Interests = {DB, ML} (from universe {AI, DB, ML}). Construct one possible feature-vector encoding φ(r) for this record, following the style discussed in the notes. State any assumptions about your encoding order.

4. (3 points) For the vectors x = (1, 3, 0) and y = (2, 1, 0), compute the cosine similarity between them. Show your work, and state one type of data for which cosine similarity is typically preferred over Euclidean distance.

5. (2 points) Explain the phenomenon of "masking" in outlier detection using the z-score method — that is, why several extreme points together can prevent any of them from crossing the 3σ threshold.

6. (3 points) A feature has median = 35 and IQR = 12. Apply robust scaling to the value x = 71 using the formula x' = (x − median) / IQR. Show your work.

7. (3 points) A dataset column has mean = 42, standard deviation = 5, median = 41, and MAD = 3.5. For x = 60, compute (a) the ordinary z-score and (b) the modified z-score (constant 0.6745). State which of the two methods you would trust more if the column were known to be heavy-tailed, and why.

8. (3 points) For two records represented as vectors x = (4, 4) and y = (1, 8), compute the L1, L2, and L∞ distances. Which of the three distances is most influenced by the single largest coordinate difference, and why?

9. (2 points) A dataset has four incomplete columns: Income, Age, Height, and Weight. Describe, step by step, how iterative (cyclic) predictive imputation would proceed across these columns, including how the process is initialized and when it stops.

10. (2 points) Explain why training a model-based imputer only on complete cases (rather than all rows) is necessary when the target column itself has missing values, and name one risk of this approach if complete cases are not representative of incomplete ones.

11. (2 points) Complete the following table by stating, for each mechanism, one appropriate class of imputation/repair method: (a) MCAR, (b) MAR, (c) MNAR. Briefly justify each.

12. (2 points) State, with one reason each, whether the following transformations preserve the original ordering of values: (a) log transform, (b) one-hot encoding, (c) equal-width discretization, (d) z-score standardization.

13. (2 points) Explain why the preprocessing pipeline (imputation → scaling → encoding → feature construction) must be fit on the training set only and then reused unchanged on the validation/test sets. Name the problem this practice prevents.

14. (3 points) A feature has values: 8, 12, 16, 24, 40. Apply Min-Max normalization to rescale these into [0, 1]. Show your calculations.

15. (2 points) Give one example each of a legitimate rare event and a data error that could both produce a statistically extreme value in a dataset, and explain why a purely statistical detector cannot, by itself, tell them apart.

---

# SAMPLE PAPER 3

**Questions Only — 15 Questions**

1. (2 points) A retail chain's dataset has "Customer_Age" missing at a rate that does not depend on any observed or unobserved variable — the field is simply skipped uniformly at random due to a rotating survey design. Identify the missingness mechanism and state one consequence for deletion-based repairs under this mechanism.

2. (3 points) A table of 1,200 rows has "Email" missing in 30 rows (MCAR) and "Secondary_Address" missing in 900 rows (75%) with negligible predictive value. Recommend a deletion method for each column and justify your choice with reference to the advantages/disadvantages discussed in the notes.

3. (2 points) Prove or disprove: mode imputation for a categorical column can distort the class balance of that column.

4. (3 points) A missing "Score" value's four nearest neighbours (already identified by distance) have values 72, 68, 75, and 65. Using k = 4 with a plain average, compute the KNN-imputed value. Then briefly explain, without recomputing, how the imputed value might have changed if k had instead been set to 2 using only the two closest neighbours (68 and 72).

5. (3 points) Four masked values and their imputed counterparts are: True = [200, 340, 150, 410], Imputed = [210, 320, 170, 400]. Compute the MAE and RMSE. Which metric penalizes large individual errors more heavily, and why?

6. (2 points) Explain why keeping a "Missing_flag" column can sometimes improve a downstream model's performance even after the missing values have been numerically filled in.

7. (2 points) Classify each as a univariate, multivariate, or contextual outlier and justify: (a) A car's recorded speed of −40 km/h. (b) A product priced at ₹5 with a recorded weight of 800 kg. (c) A recorded AC usage of 8 hours in Delhi in December.

8. (3 points) A feature has Q1 = 30 and Q3 = 66. Compute the IQR and the lower/upper boxplot fences. State whether a value of 15 would be flagged as a low-end outlier.

9. (3 points) For points x = (0, 0) and y = (6, 8), compute the L1, L2, and L∞ distances. Verify that the L2 distance corresponds to the straight-line distance between the two points.

10. (3 points) A column has mean = 100, standard deviation = 12, median = 98, MAD = 9. For x = 145, compute the ordinary z-score and the modified z-score (constant 0.6745). Using thresholds |z| ≥ 3 and |z_mod| > 3.5, would this point be flagged as an outlier under each rule?

11. (2 points) Two features, Height and Weight, are positively correlated. Explain, in terms of the covariance matrix Σ, why Mahalanobis distance can assign a small distance to a point that is far from the mean in raw Euclidean terms but consistent with the correlation between Height and Weight.

12. (2 points) State whether scaling is required for each of the following, with a brief reason: (a) PCA, (b) Decision trees, (c) SVM, (d) K-Means.

13. (3 points) A feature has values: 5, 9, 14, 22, 38. Apply z-score standardization is not requested here — instead, apply robust scaling using median = 14 and IQR = 13. Compute the robust-scaled value for each of the five points. Show your work.

14. (2 points) Explain, using the idea of "gaps and isolated bars" or "points beyond the whiskers," how a histogram and a boxplot can each visually reveal outliers that a single numeric threshold might miss.

15. (2 points) Explain the difference between equal-width and equal-frequency discretization, and give one weakness of each, using the Age-into-bins example style from the notes.

---

# SAMPLE PAPER 4

**Questions Only — 15 Questions**

1. (2 points) A loan-application dataset has "Employment_Type" missing more often for applicants who report being self-employed than for salaried applicants — that is, the probability of missingness depends on the (observed) applicant category itself. Identify the missingness mechanism and justify.

2. (2 points) Prove or disprove: pairwise deletion always uses the same subset of rows to compute every statistic in a correlation matrix.

3. (3 points) Construct a feature-vector encoding φ(r) for the record: Age = 45, Income = 910000, City = Mumbai (from {Chennai, Delhi, Mumbai}), Purchased = Yes, Interests = {AI} (from universe {AI, DB, ML}). State your encoding scheme clearly before writing the final vector.

4. (2 points) Explain why Euclidean distance cannot be directly applied to a raw heterogeneous tuple containing numbers, categories, binary values, and sets, and describe the general pipeline used to make such comparisons possible.

5. (3 points) A missing "Weight" value's three nearest neighbours (by standardized distance) are 58, 63, and 60 kg. Compute the KNN-imputed value for k = 3 using a plain average. Then explain in one sentence why standardizing features before this computation matters.

6. (2 points) Describe the "Train → Test split → Fit → Evaluate" workflow used for model-based (predictive) imputation, and explain why the test set is necessary even though the ultimate goal is to fill missing cells rather than to deploy a predictive model.

7. (3 points) Four masked/true and imputed value pairs are: True = [12, 25, 18, 40], Imputed = [15, 22, 20, 33]. Compute the RMSE and the MAE. Show your work.

8. (2 points) Complete and justify: for each mechanism (MCAR, MAR, MNAR), name one method from the notes that is inappropriate to use and explain why it would introduce bias.

9. (2 points) Classify each as a univariate, multivariate, or contextual outlier: (a) An exam score recorded as 130 out of 100. (b) A patient with systolic BP = 90 and heart rate = 180. (c) A heating-bill spike recorded for a house in July in a country with a June–September winter.

10. (3 points) A feature has Q1 = 55 and Q3 = 95. Compute the IQR, the lower and upper boxplot fences, and state whether a value of 200 is flagged as an outlier.

11. (3 points) For points x = (5, 1) and y = (2, 9), compute the L1, L2, and L∞ distances. Sketch (in words) how the "unit circle" for each of these three metrics differs in shape.

12. (3 points) A column has mean = 75, standard deviation = 10, median = 74, MAD = 7. For x = 40 (a low outlier candidate), compute the ordinary z-score and the modified z-score (constant 0.6745). Would this point be flagged under |z| ≥ 3? Under |z_mod| > 3.5?

13. (2 points) Explain why the sample mean and standard deviation used in the ordinary z-score are described as "non-robust estimators" in the context of outlier detection.

14. (3 points) A feature has values: 4, 6, 9, 15, 25. Apply Min-Max normalization to scale these values into [0, 1]. Show your calculations.

15. (2 points) Explain, with reference to the preprocessing pipeline diagram in the notes, why encoding categorical fields typically happens after scaling numeric fields rather than before, and what could go wrong if the pipeline were fit on the full dataset (train + test) instead of the training set alone.

---

# SAMPLE PAPER 5

**Questions Only — 15 Questions**

1. (2 points) A national census has "Disability_Status" missing at a constant, uniform rate across every demographic group and every possible (unobserved) disability status. Identify the missingness mechanism and state one reason it is described as "the friendliest and rarest case."

2. (3 points) A table of 2,000 rows has "Middle_Name" missing in 25 rows (MCAR, low importance) and "Alternate_Contact" missing in 1,300 rows (65%). For each column, recommend listwise, pairwise, or attribute deletion, and justify using the trade-offs discussed in the notes.

3. (2 points) Prove or disprove: median imputation is generally preferable to mean imputation for a numeric column that is heavily right-skewed. Justify your answer with reference to the properties of the median.

4. (3 points) A missing "Test_Score" value has five candidate neighbours identified by standardized distance: 82, 79, 85, 91, 77. Using k = 5 and a plain average, compute the KNN-imputed value. Show your work.

5. (3 points) True (masked) values = [65, 90, 40, 120], Imputed values = [70, 85, 55, 110]. Compute the RMSE and MAE for this imputation and show your working.

6. (2 points) Explain the purpose of the "Income_imputed" and "Income_missing_flag" columns together, and describe one scenario in which the missingness itself carries predictive signal.

7. (2 points) Classify as univariate, multivariate, or contextual, with justification: (a) A recorded body temperature of 60°C. (b) A car recorded as travelling 5 km/h with an engine RPM of 6,500. (c) A recorded ice-cream sales spike in a city during a heatwave in what is normally its coldest month.

8. (3 points) A feature has Q1 = 18 and Q3 = 42. Compute the IQR and the lower/upper boxplot fences. Would a value of 4 be flagged as a low-end outlier? Justify.

9. (3 points) For the points x = (10, 2) and y = (4, 6), compute the L1, L2, and L∞ distances. State which metric would be most appropriate if you cared primarily about the single worst-case coordinate difference, and why.

10. (3 points) A column has mean = 88, standard deviation = 9, median = 87, MAD = 6. For x = 61, compute the ordinary z-score and the modified z-score (constant 0.6745). Would the point be flagged under each of the two thresholds discussed in the notes?

11. (2 points) Two features X and Y are uncorrelated. Using the notes' derivation z = D^{-1/2}(x − μ) for uncorrelated variables, explain why the Mahalanobis distance reduces to a simple sum of squared, individually standardized z-scores in this special case.

12. (2 points) State whether scaling is needed and give one reason, for: (a) Linear regression trained with gradient descent, (b) Naïve Bayes, (c) Neural networks, (d) Random forests.

13. (3 points) A feature has values: 12, 18, 24, 36, 60. Apply robust scaling using median = 24 and IQR = 18. Compute the robust-scaled value for each point. Show your work.

14. (2 points) Explain, using the ₹20,000-to-₹20,000,000 style example from the notes, why a log transform compresses a long right tail, and what happens to the transformed range compared to the raw range.

15. (2 points) Explain why "detection is only the middle of the pipeline — never the final decision" in the context of outlier handling, and describe briefly what the "Investigate" and "Treat" steps involve after a candidate outlier has been flagged.

---

*End of practice paper set. All content drawn from: Missing Data (Lecture 3), Model-Based Imputation (Lecture 3), Outlier Detection (Lecture 4), and Data Transformation (Lecture 4/5).*
