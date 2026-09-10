from pathlib import Path
import json
import io
import contextlib
import traceback
import sqlite3
import pandas as pd

# Keep this file in the same folder as solutions.py and logistics_network.db
try:
    import solutions
except ImportError:
    print("ERROR: solutions.py not found.")
    print("Rename your solution file to solutions.py and keep it beside this test file.")
    raise SystemExit(1)


DB_PATH = "logistics_network.db"
INPUT_PATH = "hw1_query_inputs.json"


def get_task_3_input():
    """Use setup.py-generated input when available."""
    if Path(INPUT_PATH).exists():
        try:
            with open(INPUT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Try common task-key formats.
            task = (
                data.get("task_03")
                or data.get("task3")
                or data.get("3")
            )

            if task:
                db_path = task.get("db_path", DB_PATH)
                status = (
                    task.get("status_flag")
                    or task.get("status")
                    or task.get("shipment_status")
                )

                if status is not None:
                    return db_path, status

        except Exception as e:
            print(f"WARNING: Could not read generated inputs: {e}")

    # Fallback for manual testing.
    return DB_PATH, "Delivered"


def independent_expected_result(db_path, status_flag):
    """
    Independently calculate what Task 3 should return.
    This does NOT use the student's SQL.
    """
    query = """
        SELECT
            shipment_id,
            carrier_name,
            (julianday(arrival_timestamp) -
             julianday(departure_timestamp)) * 24 AS duration
        FROM shipments
        WHERE shipment_status = ?
          AND arrival_timestamp IS NOT NULL
        ORDER BY duration DESC, shipment_id ASC;
    """

    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=(status_flag,))


def test_task_3():
    print("=" * 65)
    print("TASK 3 TEST")
    print("identify_highest_transit_delays")
    print("=" * 65)

    # ---------- Basic checks ----------
    if not Path(DB_PATH).exists():
        print(f"ERROR: {DB_PATH} not found.")
        print("Put the database beside this test file.")
        return

    if not hasattr(solutions, "identify_highest_transit_delays"):
        print("ERROR: identify_highest_transit_delays() not found.")
        return

    db_path, status_flag = get_task_3_input()

    print(f"status_flag = {status_flag}")
    print()

    # ---------- Run student's function ----------
    captured = io.StringIO()

    try:
        with contextlib.redirect_stdout(captured):
            result = solutions.identify_highest_transit_delays(
                db_path, status_flag
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
    required_columns = [
        "shipment_id",
        "carrier_name",
        "duration"
    ]

    missing = [c for c in required_columns if c not in result.columns]

    if not missing:
        print("✅ Required columns are present")
    else:
        print("❌ Missing columns:", missing)
        return

    # ---------- Independent verification ----------
    try:
        expected = independent_expected_result(db_path, status_flag)

        if len(result) == len(expected):
            print("✅ Correct number of rows")
        else:
            print("❌ Wrong number of rows")
            print(f"   Expected: {len(expected)}")
            print(f"   Got:      {len(result)}")

        # Check shipment ordering/results.
        if (
            result["shipment_id"].tolist()
            == expected["shipment_id"].tolist()
        ):
            print("✅ Shipment ordering/filtering is correct")
        else:
            print("❌ Shipment ordering/filtering is incorrect")

        # Check durations numerically.
        if len(result) == len(expected):
            if result["duration"].equals(expected["duration"]):
                print("✅ Duration values are correct")
            elif (
                result["duration"].sub(expected["duration"]).abs() < 1e-6
            ).all():
                print("✅ Duration values are correct")
            else:
                print("❌ Duration values are incorrect")

        # Check carrier values.
        if (
            result["carrier_name"].tolist()
            == expected["carrier_name"].tolist()
        ):
            print("✅ Carrier values are correct")
        else:
            print("❌ Carrier values are incorrect")

    except Exception as e:
        print("⚠️ Independent verification failed:")
        print(f"{type(e).__name__}: {e}")

    # ---------- Required output ----------
    if "LONGEST_TRANSIT_HOURS:" in printed:
        print("✅ LONGEST_TRANSIT_HOURS printed")
    else:
        print("❌ LONGEST_TRANSIT_HOURS missing")

    if "CARRIER_IDENTITY_STRING:" in printed:
        print("✅ CARRIER_IDENTITY_STRING printed")
    else:
        print("❌ CARRIER_IDENTITY_STRING missing")

    # ---------- Check output values ----------
    if len(expected) > 0:
        expected_hours = expected.loc[0, "duration"]
        expected_carrier = str(
            expected.loc[0, "carrier_name"]
        ).replace(" ", "_")

        expected_hours_text = f"{expected_hours:.2f}"

        if expected_hours_text in printed:
            print("✅ LONGEST_TRANSIT_HOURS value is correct")
        else:
            print("❌ LONGEST_TRANSIT_HOURS value may be incorrect")
            print(f"   Expected: {expected_hours_text}")

        if expected_carrier in printed:
            print("✅ CARRIER_IDENTITY_STRING value is correct")
        else:
            print("❌ CARRIER_IDENTITY_STRING value may be incorrect")
            print(f"   Expected: {expected_carrier}")

    # ---------- Show results ----------
    print("\n--- What your function printed ---")
    print(printed.strip() if printed.strip() else "(nothing)")

    print("\n--- First rows returned ---")
    print(result.head())

    print("\n--- Independent expected first row ---")
    if len(expected) > 0:
        print(expected.loc[0])
    else:
        print("No matching rows.")

    print("\n" + "=" * 65)
    print("TASK 3 TEST FINISHED")
    print("=" * 65)


if __name__ == "__main__":
    test_task_3()
