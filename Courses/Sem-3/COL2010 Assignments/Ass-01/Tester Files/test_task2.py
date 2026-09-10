from pathlib import Path
import json
import io
import contextlib
import traceback
import pandas as pd

# Your solution file should be named solutions.py
try:
    import solutions
except ImportError:
    print("ERROR: solutions.py not found.")
    print("Rename skeleton-solutions.py to solutions.py")
    print("and keep test.py in the same folder.")
    raise SystemExit(1)


DB_PATH = "logistics_network.db"
INPUT_PATH = "hw1_query_inputs.json"


def load_task_2_inputs():
    """Prefer setup.py-generated inputs; otherwise use manual test values."""
    if Path(INPUT_PATH).exists():
        try:
            with open(INPUT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            task = data["task_02"]
            return (
                task["db_path"],
                float(task["min_cap"]),
                float(task["max_cap"]),
            )
        except Exception as e:
            print(f"WARNING: Could not read generated inputs: {e}")
            print("Using manual test values instead.\n")

    return DB_PATH, 50000.0, 1200000.0


def test_task_2():
    print("=" * 60)
    print("TASK 2 TEST")
    print("extract_bounded_capacity_nodes")
    print("=" * 60)

    # Check database
    if not Path(DB_PATH).exists():
        print(f"ERROR: {DB_PATH} not found.")
        print("Run setup.py first.")
        return

    # Check function
    if not hasattr(solutions, "extract_bounded_capacity_nodes"):
        print("ERROR: extract_bounded_capacity_nodes() not found.")
        return

    db_path, min_cap, max_cap = load_task_2_inputs()

    print(f"min_cap = {min_cap}")
    print(f"max_cap = {max_cap}")
    print()

    # Capture what your function prints
    captured = io.StringIO()

    try:
        with contextlib.redirect_stdout(captured):
            result = solutions.extract_bounded_capacity_nodes(
                db_path, min_cap, max_cap
            )
    except Exception as e:
        print("❌ FUNCTION CRASHED")
        print(f"{type(e).__name__}: {e}")
        traceback.print_exc()
        return

    printed = captured.getvalue()

    # 1. Return type
    if isinstance(result, pd.DataFrame):
        print("✅ Return type is DataFrame")
    else:
        print("❌ Return type is NOT DataFrame")
        print(f"   Got: {type(result).__name__}")

    # 2. Columns
    expected = [
        "node_id",
        "node_name",
        "capacity_cubic_meters",
    ]

    if list(result.columns) == expected:
        print("✅ Columns are correct")
    else:
        print("❌ Columns are incorrect")
        print(f"   Expected: {expected}")
        print(f"   Got:      {list(result.columns)}")

    # 3. Check WHERE condition independently
    if len(result) > 0:
        valid = result["capacity_cubic_meters"].between(
            min_cap, max_cap
        ).all()

        if valid:
            print("✅ All returned rows satisfy the bounds")
        else:
            print("❌ Some rows violate the bounds")
    else:
        print("⚠️ Query returned 0 rows")

    # 4. Required print statements
    if "FILTERED_RECORDS_COUNT:" in printed:
        print("✅ FILTERED_RECORDS_COUNT printed")
    else:
        print("❌ FILTERED_RECORDS_COUNT missing")

    if "MEAN_EXTRACTED_CAPACITY:" in printed:
        print("✅ MEAN_EXTRACTED_CAPACITY printed")
    else:
        print("❌ MEAN_EXTRACTED_CAPACITY missing")

    # 5. Show results
    print("\n--- What your function printed ---")
    print(printed.strip() if printed.strip() else "(nothing)")

    print("\n--- DataFrame returned by your function ---")
    print(result)

    # Independent calculation, useful for checking your print values
    print("\n--- Independent verification ---")
    print(f"Expected row count : {len(result)}")

    if len(result) > 0:
        mean_value = result["capacity_cubic_meters"].mean()
        print(f"Expected mean       : {mean_value:.2f}")
    else:
        print("Expected mean       : N/A")

    print("\n" + "=" * 60)
    print("TEST FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    test_task_2()
