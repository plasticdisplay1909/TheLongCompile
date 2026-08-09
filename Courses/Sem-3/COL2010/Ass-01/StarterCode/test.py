from solutions import build_operational_audit_schema

def main():
    try:
        result = build_operational_audit_schema()

        print("\nReturned SQL:")
        print(result)

        print("\nTASK 1 EXECUTION: PASSED")

    except Exception as e:
        print("TASK 1 FAILED:", e)


if __name__ == "__main__":
    main()