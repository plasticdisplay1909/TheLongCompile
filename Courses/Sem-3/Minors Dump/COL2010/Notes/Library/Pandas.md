# Pandas Quick Reference — COL2010 Data Cleaning

## 1. Import

```python
import pandas as pd
```

`pd` is the standard short name for Pandas.

The main object you will use is a **DataFrame**.

```text
DataFrame = table
Series    = single column
```

---

# 2. Creating a DataFrame

```python
data = {
    "Name": ["Aman", "Rahul", "Priya"],
    "Age": [20, 21, 19],
    "Marks": [85, 90, 78]
}

df = pd.DataFrame(data)
```

Think of `df` as your table.

---

# 3. Reading Data

## CSV

```python
df = pd.read_csv("data.csv")
```

## Excel

```python
df = pd.read_excel("data.xlsx")
```

## JSON

```python
df = pd.read_json("data.json")
```

---

# 4. Inspecting the Data

## First rows

```python
df.head()
df.head(10)
```

## Last rows

```python
df.tail()
df.tail(10)
```

## Shape

```python
df.shape
```

Returns:

```text
(number_of_rows, number_of_columns)
```

## Column names

```python
df.columns
```

## Data types

```python
df.dtypes
```

## Summary information

```python
df.info()
```

## Statistical summary

```python
df.describe()
```

---

# 5. Selecting Columns

## One column

```python
df["Age"]
```

Returns a Series.

## Multiple columns

```python
df[["Name", "Age"]]
```

Returns a DataFrame.

### Remember

```python
df["Age"]        # Series
df[["Age"]]      # DataFrame
```

---

# 6. Selecting Rows

## `.iloc[]` — position based

```python
df.iloc[0]
```

First row.

```python
df.iloc[0:3]
```

First 3 rows.

```python
df.iloc[0, 1]
```

Row 0, column 1.

```python
df.iloc[:, 0]
```

All rows, first column.

```python
df.iloc[:, 1:3]
```

All rows, columns 1 and 2.

### Mental model

```text
iloc = integer/location/position
```

---

# 7. `.loc[]` — label based

```python
df.loc[0]
```

Row with index label `0`.

```python
df.loc[0, "Age"]
```

Value at row label `0`, column `"Age"`.

```python
df.loc[:, "Age"]
```

All rows of Age.

### Conditional selection

```python
df.loc[df["Age"] > 20]
```

Rows where Age > 20.

---

# 8. Filtering Rows

```python
df[df["Age"] > 20]
```

Multiple conditions:

```python
df[(df["Age"] > 18) & (df["Marks"] >= 80)]
```

OR:

```python
df[(df["Age"] > 20) | (df["Marks"] >= 90)]
```

NOT:

```python
df[~(df["Age"] > 20)]
```

### Important

Use:

```text
& → AND
| → OR
~ → NOT
```

Do NOT use Python `and` / `or` between Series.

---

# 9. Missing Values

## Detect missing values

```python
df.isna()
```

or:

```python
df.isnull()
```

Both are commonly used.

## Count missing values

```python
df.isna().sum()
```

For one column:

```python
df["Age"].isna().sum()
```

## Detect non-missing values

```python
df.notna()
```

---

# 10. Removing Missing Values

## Remove rows containing any NaN

```python
df.dropna()
```

## Remove rows only if a particular column is missing

```python
df.dropna(subset=["Age"])
```

## Remove columns containing NaN

```python
df.dropna(axis=1)
```

### Important

Many Pandas functions return a modified copy.

So:

```python
df = df.dropna()
```

is safer when you want to keep the change.

---

# 11. Filling Missing Values

## Fill with a constant

```python
df["Age"] = df["Age"].fillna(0)
```

## Fill with mean

```python
df["Age"] = df["Age"].fillna(df["Age"].mean())
```

## Fill with median

```python
df["Age"] = df["Age"].fillna(df["Age"].median())
```

## Forward fill

```python
df["Age"] = df["Age"].ffill()
```

## Backward fill

```python
df["Age"] = df["Age"].bfill()
```

---

# 12. Duplicates

## Check duplicates

```python
df.duplicated()
```

Count:

```python
df.duplicated().sum()
```

## Remove duplicates

```python
df = df.drop_duplicates()
```

For specific columns:

```python
df = df.drop_duplicates(subset=["Name"])
```

---

# 13. Unique Values

## `unique()`

```python
df["Department"].unique()
```

Returns unique values.

## `nunique()`

```python
df["Department"].nunique()
```

Returns the number of unique values.

## `value_counts()`

```python
df["Department"].value_counts()
```

Counts how often each value appears.

Example:

```text
CSE    50
ECE    35
ME     20
```

---

# 14. Sorting

## Sort by column

```python
df.sort_values("Age")
```

Descending:

```python
df.sort_values("Age", ascending=False)
```

Multiple columns:

```python
df.sort_values(["Department", "Marks"])
```

Different directions:

```python
df.sort_values(
    ["Department", "Marks"],
    ascending=[True, False]
)
```

## Sort by index

```python
df.sort_index()
```

---

# 15. Copying a DataFrame

Use:

```python
df2 = df.copy()
```

Instead of:

```python
df2 = df
```

Why?

```python
df2 = df
```

usually makes both variables refer to the same DataFrame.

`copy()` creates an independent copy.

---

# 16. Adding a Column

```python
df["Passed"] = df["Marks"] >= 40
```

Or:

```python
df["Bonus"] = df["Marks"] + 5
```

Using NumPy:

```python
import numpy as np

df["Result"] = np.where(
    df["Marks"] >= 40,
    "Pass",
    "Fail"
)
```

---

# 17. Removing Columns

```python
df = df.drop(columns=["Age"])
```

Multiple:

```python
df = df.drop(columns=["Age", "Marks"])
```

---

# 18. Renaming Columns

```python
df = df.rename(
    columns={"Marks": "Score"}
)
```

Multiple:

```python
df = df.rename(
    columns={
        "Marks": "Score",
        "Name": "Student_Name"
    }
)
```

---

# 19. Changing Data Types

Check:

```python
df.dtypes
```

Convert:

```python
df["Age"] = df["Age"].astype(int)
```

String:

```python
df["Name"] = df["Name"].astype(str)
```

Numeric conversion:

```python
df["Marks"] = pd.to_numeric(
    df["Marks"],
    errors="coerce"
)
```

`errors="coerce"` converts invalid values to `NaN`.

---

# 20. Strings

String operations usually use `.str`.

Lowercase:

```python
df["Name"] = df["Name"].str.lower()
```

Uppercase:

```python
df["Name"] = df["Name"].str.upper()
```

Remove leading/trailing spaces:

```python
df["Name"] = df["Name"].str.strip()
```

Replace text:

```python
df["Name"] = df["Name"].str.replace(
    "old",
    "new"
)
```

Check whether string contains something:

```python
df["Name"].str.contains("rahul")
```

Case-insensitive:

```python
df["Name"].str.contains(
    "rahul",
    case=False,
    na=False
)
```

---

# 21. Dates

Convert a column to datetime:

```python
df["Date"] = pd.to_datetime(df["Date"])
```

Invalid dates:

```python
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)
```

Extract year:

```python
df["Date"].dt.year
```

Month:

```python
df["Date"].dt.month
```

Day:

```python
df["Date"].dt.day
```

Day of week:

```python
df["Date"].dt.dayofweek
```

---

# 22. `groupby()` ⭐ VERY IMPORTANT

Used to group data and calculate statistics.

Example:

```python
df.groupby("Department")["Marks"].mean()
```

Meaning:

> For each department, calculate average marks.

Multiple statistics:

```python
df.groupby("Department")["Marks"].agg(
    ["mean", "median", "min", "max", "count"]
)
```

Multiple columns:

```python
df.groupby("Department").agg({
    "Marks": "mean",
    "Age": "median"
})
```

---

# 23. `iterrows()`

Loops through rows.

```python
for index, row in df.iterrows():
    print(index, row["Name"])
```

Useful for understanding row-wise processing, but usually slower than vectorized Pandas operations.

---

# 24. `itertuples()`

Another way to iterate through rows.

```python
for row in df.itertuples():
    print(row)
```

Generally faster than `iterrows()`.

---

# 25. `apply()`

Applies a function.

Example:

```python
df["Marks"] = df["Marks"].apply(
    lambda x: x + 5
)
```

Custom function:

```python
def grade(x):
    if x >= 80:
        return "A"
    elif x >= 60:
        return "B"
    else:
        return "C"

df["Grade"] = df["Marks"].apply(grade)
```

---

# 26. `replace()`

Replace specific values.

```python
df["Gender"] = df["Gender"].replace(
    "M",
    "Male"
)
```

Multiple:

```python
df["Gender"] = df["Gender"].replace({
    "M": "Male",
    "F": "Female"
})
```

Replace missing-like values:

```python
df = df.replace(["NA", "N/A", "missing"], np.nan)
```

---

# 27. `drop()` vs `dropna()` vs `fillna()`

Very important distinction:

```python
df.drop(...)
```

Remove rows/columns explicitly.

```python
df.dropna(...)
```

Remove missing values.

```python
df.fillna(...)
```

Replace missing values.

---

# 28. Combining DataFrames

## `pd.concat()`

Stack DataFrames.

Rows:

```python
pd.concat([df1, df2])
```

Columns:

```python
pd.concat([df1, df2], axis=1)
```

---

# 29. Merge

Similar to a database JOIN.

```python
pd.merge(
    df1,
    df2,
    on="ID"
)
```

Types:

```python
pd.merge(df1, df2, on="ID", how="inner")
pd.merge(df1, df2, on="ID", how="left")
pd.merge(df1, df2, on="ID", how="right")
pd.merge(df1, df2, on="ID", how="outer")
```

Mental model:

```text
inner → matching rows
left  → all rows from left
right → all rows from right
outer → everything
```

---

# 30. Index

View index:

```python
df.index
```

Reset:

```python
df = df.reset_index(drop=True)
```

Set a column as index:

```python
df = df.set_index("ID")
```

---

# 31. Reading and Writing Files

Read:

```python
df = pd.read_csv("data.csv")
```

Write:

```python
df.to_csv("output.csv", index=False)
```

Excel:

```python
df.to_excel("output.xlsx", index=False)
```

`index=False` prevents the DataFrame index from being written as an extra column.

---

# 32. Useful Data Inspection Commands

```python
df.head()
df.tail()
df.shape
df.columns
df.dtypes
df.info()
df.describe()

df["column"].unique()
df["column"].nunique()
df["column"].value_counts()

df.isna().sum()
df.duplicated().sum()
```

These are excellent commands to run at the beginning of a data-cleaning task.

---

# 33. Common Data Cleaning Workflow

A typical workflow:

```python
import pandas as pd
import numpy as np

# 1. Read
df = pd.read_csv("data.csv")

# 2. Inspect
print(df.head())
print(df.shape)
print(df.info())

# 3. Check missing values
print(df.isna().sum())

# 4. Check duplicates
print(df.duplicated().sum())

# 5. Clean strings
df["Name"] = df["Name"].str.strip()

# 6. Convert numeric values
df["Age"] = pd.to_numeric(
    df["Age"],
    errors="coerce"
)

# 7. Handle missing values
df["Age"] = df["Age"].fillna(
    df["Age"].median()
)

# 8. Remove duplicates
df = df.drop_duplicates()

# 9. Sort
df = df.sort_values("Age")

# 10. Save
df.to_csv("cleaned.csv", index=False)
```

---

# ⭐ Must-Know for COL2010

## 🔴 MUST KNOW

```python
pd.read_csv()

df["column"]

df.copy()

df.head()
df.tail()
df.shape
df.columns
df.dtypes
df.info()
df.describe()

df.isna()
df.notna()
df.dropna()
df.fillna()

df.nunique()
df.unique()
df.value_counts()

df.sort_values()
df.sort_index()

df.iloc[]
df.loc[]

df.groupby()

df.drop_duplicates()

df.rename()
df.drop()
df.replace()

pd.to_numeric()
pd.to_datetime()

df.str.strip()
df.str.lower()
df.str.upper()
df.str.contains()

df.iterrows()
df.itertuples()
```

## 🟡 Know the basic idea

```python
df.apply()

pd.concat()

pd.merge()

df.set_index()
df.reset_index()

df.to_csv()
df.to_excel()
```

---

# Pandas vs NumPy

| Task | Pandas | NumPy |
|---|---|---|
| Table/dataframe | `pd.DataFrame()` | — |
| Read CSV | `pd.read_csv()` | — |
| Select column | `df["Age"]` | — |
| Missing values | `df.isna()` | `np.isnan()` |
| Mean | `df["Age"].mean()` | `np.mean(a)` |
| Median | `df["Age"].median()` | `np.median(a)` |
| Percentile | — | `np.percentile()` |
| Conditional replacement | — | `np.where()` |
| Unique values | `df["x"].unique()` | `np.unique()` |
| Grouping | `df.groupby()` | — |
| Sorting | `df.sort_values()` | `np.argsort()` |
| Table manipulation | Excellent | Limited |
| Numerical arrays | Good | Excellent |

---

# 🧠 Mental Model

```text
                    DATA CLEANING
                         │
             ┌───────────┴───────────┐
             │                       │
          PANDAS                   NUMPY
             │                       │
          DataFrame                Arrays
             │                       │
       ┌─────┼─────┐          ┌──────┼──────┐
       │     │     │          │      │      │
     rows  cols  missing    stats  math   conditions
```

### Remember:

```python
df = your TABLE
df["Age"] = your COLUMN
np.array() = numerical ARRAY
pd = Pandas
np = NumPy
```

For COL2010, focus heavily on **missing values, duplicates, filtering, sorting, grouping, type conversion, strings, dates, percentiles, and `np.where()`**.
