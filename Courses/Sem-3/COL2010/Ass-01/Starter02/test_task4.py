from pathlib import Path
import json
import io
import contextlib
import traceback
import sqlite3
import pandas as pd

try:
    import solutions
except ImportError:
    print("ERROR: solutions.py not found.")
    print("Keep test_task4.py in the same folder as solutions.py.")
    raise SystemExit(1)


DB_PATH = "logistics_network.db"
INPUT_PATH = "hw1_query_inputs.json"


def get_task_4_input():
    """Use setup.py-generated input if available; otherwise use a manual value."""
    if Path(INPUT_PATH).exists():
        try:
            with open(INPUT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            task = (
                data.get("task_04")
                or data.get("task4")
                or data.get("4")
            )

            if task:
                db_path = task.get("db_path", DB_PATH)

                limit = (
                    task.get("baseline_limit")
                    or task.get("baseline")
                    or task.get("limit")
                )

                if limit is not None:
                    return db_path, float(limit)

        except Exception as e:
            print(f"WARNING: Could not read generated Task 4 input: {e}")

    return DB_PATH, 1000.0


def independent_expected_result(db_path, baseline_limit):
    """
    Independently calculate the expected Task 4 result.
    This does not call the student's function.
    """
    query = """
        SELECT
            base_cost_usd AS cost,
            CASE
                WHEN base_cost_usd >= ?
                THEN 'High-Cost-Tier'
                ELSE 'Standard-Cost-Tier'
            END AS risk_profile
        FROM routes
    """

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(
            query,
            conn,
            params=(baseline_limit,)
        )


def test_task_4():
    print("=" * 65)
    print("TASK 4 TEST")
    print("append_freight_risk_profiles")
    print("=" * 65)

    if not Path(DB_PATH).exists():
        print(f"ERROR: {DB_PATH} not found.")
        print("Put the database beside this test file.")
        return

    if not hasattr(solutions, "append_freight_risk_profiles"):
        print("ERROR: append_freight_risk_profiles() not found.")
        return

    db_path, baseline_limit = get_task_4_input()

    print(f"baseline_limit = {baseline_limit}")
    print()

    # ---------- Run student's function ----------
    captured = io.StringIO()

    try:
        with contextlib.redirect_stdout(captured):
            result = solutions.append_freight_risk_profiles(
                db_path,
                baseline_limit
            )
    except Exception as e:
        print("❌ FUNCTION CRASHED")
        print(f"{type(e).__name__}: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        return

    printed = captured.getvalue()

    # ---------- Return type ----------
    if isinstance(result, pd.DataFrame):
        print("✅ Return type is DataFrame")
    else:
        print("❌ Return type is NOT DataFrame")
        print(f"   Got: {type(result).__name__}")
        return

    # ---------- Required columns ----------
    required_columns = ["cost", "risk_profile"]

    missing = [c for c in required_columns if c not in result.columns]

    if not missing:
        print("✅ Required columns are present")
    else:
        print(f"❌ Missing columns: {missing}")
        return

    # ---------- Independent verification ----------
    try:
        expected = independent_expected_result(
            db_path,
            baseline_limit
        )

        # Row count
        if len(result) == len(expected):
            print("✅ Correct number of rows")
        else:
            print("❌ Wrong number of rows")
            print(f"   Expected: {len(expected)}")
            print(f"   Got:      {len(result)}")

        # Costs
        if len(result) == len(expected):
            costs_ok = (
                result["cost"].reset_index(drop=True)
                .equals(expected["cost"].reset_index(drop=True))
            )

            if costs_ok:
                print("✅ Cost values are correct")
            else:
                print("❌ Cost values are incorrect")

        # Risk classifications
        if len(result) == len(expected):
            risk_ok = (
                result["risk_profile"].reset_index(drop=True)
                .equals(expected["risk_profile"].reset_index(drop=True))
            )

            if risk_ok:
                print("✅ CASE classifications are correct")
            else:
                print("❌ CASE classifications are incorrect")

        # Independent count and ratio
        expected_count = (
            expected["risk_profile"] == "High-Cost-Tier"
        ).sum()

        expected_ratio = expected_count / len(expected)

        print("\n--- Independent verification ---")
        print(f"Expected high-risk count : {expected_count}")
        print(f"Expected ratio           : {expected_ratio:.4f}")

        # Check printed values
        if f"HIGH_RISK_ROUTE_COUNT: {expected_count}" in printed:
            print("✅ HIGH_RISK_ROUTE_COUNT value is correct")
        else:
            print("❌ HIGH_RISK_ROUTE_COUNT value is incorrect/missing")

        if f"RATIO_TO_TOTAL_SYSTEM: {expected_ratio:.4f}" in printed:
            print("✅ RATIO_TO_TOTAL_SYSTEM value is correct")
        else:
            print("❌ RATIO_TO_TOTAL_SYSTEM value is incorrect/missing")

    except Exception as e:
        print("⚠️ Independent verification failed:")
        print(f"{type(e).__name__}: {e}")

    # ---------- Required output labels ----------
    if "HIGH_RISK_ROUTE_COUNT:" in printed:
        print("✅ HIGH_RISK_ROUTE_COUNT printed")
    else:
        print("❌ HIGH_RISK_ROUTE_COUNT missing")

    if "RATIO_TO_TOTAL_SYSTEM:" in printed:
        print("✅ RATIO_TO_TOTAL_SYSTEM printed")
    else:
        print("❌ RATIO_TO_TOTAL_SYSTEM missing")

    # ---------- Show output ----------
    print("\n--- What your function printed ---")
    print(printed.strip() if printed.strip() else "(nothing)")

    print("\n--- First rows returned ---")
    print(result.head())

    print("\n" + "=" * 65)
    print("TASK 4 TEST FINISHED")
    print("=" * 65)


if __name__ == "__main__":
    test_task_4()
