# NumPy Quick Reference — COL2010 Data Cleaning

## 1. Import

```python
import numpy as np
```

`np` is the standard short name for NumPy.

---

## 2. Creating Arrays

### `np.array()`

```python
a = np.array([1, 2, 3, 4])
b = np.array([[1, 2], [3, 4]])
```

Useful properties:

```python
a.shape
a.ndim
a.size
a.dtype
```

### `np.zeros()`

```python
np.zeros(5)
np.zeros((2, 3))
```

Creates arrays containing only `0`.

### `np.ones()`

```python
np.ones(5)
np.ones((2, 3))
```

Creates arrays containing only `1`.

### `np.full()`

```python
np.full(5, 7)
np.full((2, 3), 9)
```

Creates an array filled with a chosen value.

---

# 3. Missing and Special Values

## `np.nan`

Represents a missing numerical value.

```python
x = np.nan
a = np.array([1, 2, np.nan, 4])
```

## `np.isnan()`

Checks which values are NaN.

```python
np.isnan(a)
```

Result:

```text
[False False  True False]
```

Count NaNs:

```python
np.isnan(a).sum()
```

## `np.isfinite()`

Checks whether values are finite.

```python
a = np.array([1, np.inf, -np.inf, np.nan, 5])
np.isfinite(a)
```

Result:

```text
[ True False False False  True]
```

## `np.inf`

Positive infinity.

```python
np.inf
-np.inf
```

---

# 4. Basic Statistics

Given:

```python
a = np.array([10, 20, 30, 40, 50])
```

## Mean

```python
np.mean(a)
```

Average.

## Median

```python
np.median(a)
```

Middle value after sorting.

## Standard deviation

```python
np.std(a)
```

Measures spread/variation.

## Minimum / Maximum

```python
np.min(a)
np.max(a)
```

## Sum

```python
np.sum(a)
```

Adds all values.

---

# 5. Handling NaN in Statistics

Normal functions can return `nan` if the array contains NaN:

```python
a = np.array([10, 20, np.nan, 40])

np.mean(a)       # nan
```

Use NaN-aware versions:

```python
np.nanmean(a)
np.nanmedian(a)
np.nanstd(a)
np.nansum(a)
np.nanmin(a)
np.nanmax(a)
```

These ignore NaN values.

---

# 6. Percentiles

```python
a = np.array([10, 20, 30, 40, 50])

np.percentile(a, 25)
np.percentile(a, 50)
np.percentile(a, 75)
```

Important:

```text
25th percentile = Q1
50th percentile = Q2 = median
75th percentile = Q3
```

### IQR

```python
Q1 = np.percentile(a, 25)
Q3 = np.percentile(a, 75)

IQR = Q3 - Q1
```

### Outlier rule

```python
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
```

Values below `lower` or above `upper` are commonly treated as outliers.

---

# 7. Absolute Value

## `np.abs()`

```python
np.abs(-5)
```

Result:

```text
5
```

For arrays:

```python
a = np.array([-5, -2, 3])
np.abs(a)
```

Result:

```text
[5 2 3]
```

---

# 8. Square Root

## `np.sqrt()`

```python
np.sqrt(25)
```

Result:

```text
5
```

Element-wise:

```python
a = np.array([4, 9, 16])
np.sqrt(a)
```

---

# 9. Conditional Operations

## `np.where()`

One of the most useful NumPy functions for data cleaning.

Syntax:

```python
np.where(condition, value_if_true, value_if_false)
```

Example:

```python
a = np.array([10, 20, 30, 40])

np.where(a > 25, "High", "Low")
```

Result:

```text
['Low' 'Low' 'High' 'High']
```

### Replace invalid values

```python
df["Age"] = np.where(
    df["Age"] < 0,
    np.nan,
    df["Age"]
)
```

Meaning:

> Negative age → NaN; otherwise keep the original age.

### Multiple conditions

```python
np.where(
    a >= 80,
    "A",
    np.where(a >= 60, "B", "C")
)
```

---

# 10. Unique Values

## `np.unique()`

```python
a = np.array([1, 2, 2, 3, 3, 3])

np.unique(a)
```

Result:

```text
[1 2 3]
```

With counts:

```python
values, counts = np.unique(a, return_counts=True)
```

This is useful for categorical data.

---

# 11. Sorting

## `np.argsort()`

Returns the indices that would sort the array.

```python
a = np.array([30, 10, 20])

np.argsort(a)
```

Result:

```text
[1 2 0]
```

Because:

```text
a[1] = 10
a[2] = 20
a[0] = 30
```

Get sorted array:

```python
a[np.argsort(a)]
```

---

# 12. Combining Arrays

## `np.vstack()`

Vertical stacking:

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.vstack((a, b))
```

Result:

```text
[[1 2 3]
 [4 5 6]]
```

## `np.hstack()`

Horizontal stacking:

```python
np.hstack((a, b))
```

Result:

```text
[1 2 3 4 5 6]
```

## `np.column_stack()`

Combines 1D arrays as columns:

```python
np.column_stack((a, b))
```

Result:

```text
[[1 4]
 [2 5]
 [3 6]]
```

---

# 13. Array Indexing

```python
a = np.array([10, 20, 30, 40, 50])
```

First element:

```python
a[0]
```

Last element:

```python
a[-1]
```

Slice:

```python
a[1:4]
```

Result:

```text
[20 30 40]
```

2D:

```python
b = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

b[0, 1]     # 2
b[1, 2]     # 6
```

---

# 14. Boolean Filtering

```python
a = np.array([10, 20, 30, 40])

a > 20
```

Result:

```text
[False False True True]
```

Filter:

```python
a[a > 20]
```

Result:

```text
[30 40]
```

Multiple conditions:

```python
a[(a > 10) & (a < 40)]
```

Use:

```text
&  → AND
|  → OR
~  → NOT
```

Use parentheses around each condition.

---

# 15. Axis — Important

For:

```python
a = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```

Column-wise:

```python
np.sum(a, axis=0)
```

Result:

```text
[5 7 9]
```

Row-wise:

```python
np.sum(a, axis=1)
```

Result:

```text
[ 6 15]
```

Remember:

```text
axis=0 → operate down rows → result for each column
axis=1 → operate across columns → result for each row
```

---

# 16. NumPy + Pandas

NumPy and Pandas are commonly used together.

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")

df["marks"] = np.where(
    df["marks"] < 0,
    np.nan,
    df["marks"]
)
```

Useful examples:

```python
np.mean(df["marks"])
np.median(df["marks"])
np.percentile(df["marks"], 75)
np.unique(df["department"])
np.isnan(df["marks"]).sum()
```

---

# ⭐ Must-Know for COL2010

Prioritize these:

```python
np.array()
np.nan
np.isnan()
np.isfinite()

np.mean()
np.median()
np.std()
np.min()
np.max()
np.percentile()
np.sum()

np.abs()
np.where()
np.unique()
np.argsort()

np.vstack()
np.hstack()
np.column_stack()

np.zeros()
np.ones()
np.full()
np.inf
```

### Most important for data cleaning

```python
np.isnan()
np.isfinite()
np.nan
np.percentile()
np.where()
np.unique()
np.abs()
```

---

# Quick Cheat Sheet

| Function | Purpose |
|---|---|
| `np.array()` | Create array |
| `np.nan` | Missing numerical value |
| `np.isnan()` | Detect NaN |
| `np.isfinite()` | Detect finite values |
| `np.mean()` | Mean |
| `np.median()` | Median |
| `np.std()` | Standard deviation |
| `np.min()` | Minimum |
| `np.max()` | Maximum |
| `np.percentile()` | Percentile |
| `np.sum()` | Sum |
| `np.abs()` | Absolute value |
| `np.sqrt()` | Square root |
| `np.where()` | Conditional replacement |
| `np.unique()` | Unique values |
| `np.argsort()` | Sorting indices |
| `np.vstack()` | Stack vertically |
| `np.hstack()` | Stack horizontally |
| `np.column_stack()` | Combine as columns |
| `np.zeros()` | Array of zeros |
| `np.ones()` | Array of ones |
| `np.full()` | Array with chosen value |
| `np.inf` | Infinity |
