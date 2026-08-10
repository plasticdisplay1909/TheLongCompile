"""
COL2010 Module 1: Database Systems skeleton.
Students must write raw SQL inside each function and execute it programmatically.
Run setup.py first to create logistics_network.db.
"""

##############################################################################################################
#################################               Imports         ##############################################
##############################################################################################################
from __future__ import annotations

import re
import sqlite3
from typing import Any

import pandas as pd

DB_FILENAME = "logistics_network.db"


##########################           No need to edit part           ##########################################
def _read_sql(db_path: str, query: str, params: tuple[Any, ...] = ()) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=params)

def _read_sql_with_regex(
    db_path: str,
    query: str,
    params: tuple[Any, ...] = ()
) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    conn.create_function(
        "REGEXP",
        2,
        lambda pattern, value: 1 if value is not None and re.search(pattern, value) else 0,
    )
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()


def _scalar(db_path: str, query: str, params: tuple[Any, ...] = ()) -> Any:
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        row = cur.fetchone()
    return None if row is None else row[0]


def sample_existing_sku(db_path: str = DB_FILENAME) -> str:
    """Convenience helper for local testing of SKU-parameterized queries."""
    return str(_scalar(db_path, "SELECT sku FROM inventory_items ORDER BY item_id LIMIT 1;"))


def sample_existing_employee(db_path: str = DB_FILENAME) -> int:
    """Convenience helper for local testing of recursive hierarchy queries."""
    return int(_scalar(db_path, "SELECT MAX(employee_id) FROM organizational_hierarchy;"))


############################################################################################################
###########################             Question Coding             ########################################
############################################################################################################


def build_operational_audit_schema() -> str:
    """
    TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, 
    print the required summary line(s), and return the specified object.
    """

    query = """
        CREATE TABLE operational_audit_logs (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time TEXT NOT NULL,
            actor_id INTEGER NOT NULL,
            action_code TEXT NOT NULL,
            entity_name TEXT NOT NULL,
            entity_key TEXT NOT NULL,
            payload_json TEXT,

            UNIQUE(actor_id,action_code,entity_name,entity_key)
        )
    """
    print("SCHEMA_VERIFICATION_IS_VALID: TRUE")
    return query
# build_operational_audit_schema()


##########################################################################################################
"""                                         Question 2                                                 """
##########################################################################################################
def extract_bounded_capacity_nodes(db_path: str, min_cap: float, max_cap: float) -> pd.DataFrame:
    """
    TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, 
    print the required summary line(s), and return the specified object.
    """
    query = """
        SELECT node_id,node_name,capacity_cubic_meters
        FROM nodes
        WHERE capacity_cubic_meters BETWEEN ? and ?;
    """
    df = _read_sql(db_path, query,(min_cap,max_cap))
    # TODO: print the exact target output lines from the homework.

    ## Counting average
    mean_cap=df["capacity_cubic_meters"].sum() / len(df)
    print("FILTERED_RECORDS_COUNT: ", len(df))
    print("MEAN_EXTRACTED_CAPACITY: {:.2f}", mean_cap)
    return df

# res=extract_bounded_capacity_nodes("logistics_network.db",5000,120000)
# print(res)


##############################################################################################################
###########################             Question 03         ##################################################
##############################################################################################################
def identify_highest_transit_delays(db_path: str, status_flag: str) -> pd.DataFrame:
    """
    TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, 
    print the required summary line(s), and return the specified object.
    """
    query = """
        SELECT shipment_id,carrier_name, (julianday(arrival_timestamp) - julianday(departure_timestamp)) *24 as DURATION
        FROM shipments
        where shipment_status=? AND arrival_timestamp IS NOT NULL
        ORDER BY duration DESC,shipment_id ASC;
    """
    df = _read_sql(db_path, query,(status_flag,))
    # TODO: print the exact target output lines from the homework.
    print("LONGEST_TRANSIT_HOURS: {:.2f}".format(df.at[0,"DURATION"]))
    print("CARRIER_IDENTITY_STRING: {}".format(df.at[0,"carrier_name"].replace(" ","_")))
    return df

identify_highest_transit_delays("logistics_network.db","Delivered")

def append_freight_risk_profiles(db_path: str, baseline_limit: float) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def verify_candidate_presence(db_path: str, sku_id: str, node_id: int) -> bool:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute query and compute boolean result.
    result = False
    return result

def calculate_shipment_manifest_mass(db_path: str, shipment_id: int) -> float:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute scalar SQL query and print the target line.
    return 0

def isolate_unreferenced_inventory_items(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def filter_sku_by_regex_pattern(db_path: str, exact_regex: str) -> list[str]:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql_with_regex(db_path, query, params=(exact_regex,))
    # TODO: convert the relevant column to a Python list and print the target line.
    return []

def sequence_carrier_allocations(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def identify_high_density_warehouses(db_path: str, asset_threshold: int) -> list[int]:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: convert the relevant column to a Python list and print the target line.
    return []

def filter_routes_by_source_inclusion(db_path: str, valid_source_types: list[str]) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def aggregate_carrier_performance(db_path: str, minimum_runs: int) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def locate_outlier_salaries_by_hub(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df


def extract_active_item_ids(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def compute_cartesian_density_space(db_path: str) -> float:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute scalar SQL query and print the target line.
    return 0

def isolate_overlapping_schedule_runs(db_path: str, start_bound: str, end_bound: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def calculate_manifest_deviation_variance(db_path: str) -> float:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute scalar SQL query and print the target line.
    return 0

def identify_high_inventory_nodes(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def remap_missing_timestamps(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def build_standardized_barcodes(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def project_metric_conversions(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def isolate_duplicate_skus(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def slice_top_salaries_per_node(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def cross_reference_route_intersections(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def evaluate_high_density_cost_centers(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def trace_management_hierarchy_chain(db_path: str, start_employee_id: int) -> list[int]:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: convert the relevant column to a Python list and print the target line.
    return []

def extract_downstream_subordinates(db_path: str, manager_id: int) -> list[int]:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: convert the relevant column to a Python list and print the target line.
    return []

def generate_multi_leg_connections(db_path: str, origin_id: int, terminal_id: int) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def find_shortest_distance_route(db_path: str, origin_id: int, terminal_id: int) -> float:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute scalar SQL query and print the target line.
    return 0

def scan_network_cyclic_dependencies(db_path: str) -> list[int]:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: convert the relevant column to a Python list and print the target line.
    return []

def evaluate_transitive_asset_flows(db_path: str, item_sku: str) -> int:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute scalar SQL query and print the target line.
    return 0

def compute_bom_packaging_mass(db_path: str, master_sku: str) -> float:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute scalar SQL query and print the target line.
    return 0

def evaluate_hub_reachability_matrix(db_path: str, source_node_id: int, target_node_id: int, blocked_node_id: int) -> bool:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    # TODO: execute query and compute boolean result.
    result = False
    return result

def trace_accumulated_transit_costs(db_path: str, start_node: int, end_node: int) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

def calculate_hierarchy_depth_matrix(db_path: str) -> pd.DataFrame:
    """TODO: Write the raw SQL for this task, execute it using sqlite3/pandas, print the required summary line(s), and return the specified object."""
    query = """
    -- TODO: SQL query goes here.
    """
    df = _read_sql(db_path, query)
    # TODO: print the exact target output lines from the homework.
    return df

