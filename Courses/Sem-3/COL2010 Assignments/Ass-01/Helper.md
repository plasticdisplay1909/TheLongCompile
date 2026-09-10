## Question 1
Give we have to create a table

- Syntax goes like ```CREATE TABLE name```
- We are given the name ```operational audit logs```

### For the IDs
##### audit_id
Write it as 
```sql
audit INTEGER PRIMARY KEY AUTOINCREMENT
```
-   audit_id is the column name, 
-   ```INTEGER``` specify Data-type
-   ```AUTOINCREMENT``` automatically generates new ID when a row is generated


``` sql
event_time TEXT NOT NULL,
```
- Here DATE or DATETIME or TIME could have also been used as data types
- NOT NULL ensures that no column table is left empty


```sql
payload_json TEXT,
```
- NOT NULL is not required here

    - For example ```action_code='LOGIN'``` here actor_id and event_time tells us enough info
    - For ```action_code= "UPDATE" ```  we need to know what has changed and to know what value, here playload_json stores the exact details of 

    - If we force it to be null every time, we do some task, we would be forced to use ``` {} or ' '``` just to satisfy the data-base constraint


```sql
UNIQUE(actor_id, action_code, entity_name, entity_key, event_time)
```
    - Trailing commas are not required 
    

---
---


Now continue filling the other tables for question number 1

---

Althought it does not really matters which of column names are written first, it is just readability to write PRIMARY KEY first

#### Final code
```sql

def build_operational_audit_schema() -> str:
    """
    TODO: Write the raw SQL for this task, execute it using sqlite3/pandas,
    print the required summary line(s), and return the specified object.
    """


    query = """
    CREATE TABLE operational_audit_logs (
        audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time DATETIME NOT NULL,
        actor_id INTEGER NOT NULL,
        action_code TEXT NOT NULL,
        entity_name TEXT NOT NULL,
        entity_key TEXT NOT NULL,
        payload_json TEXT,

        UNIQUE(actor_id, action_code, entity_name, entity_key)
    )
    """
    print("SCHEMA_VERIFICATION_IS_VALID: TRUE")
    return query
```

