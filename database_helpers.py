
import sqlite3
import pandas as pd
from config import SQL_DATABASE_PATH


def query_sql(cols_to_get,filter_col_name_to_condition): # condition, treatment, time_from_treatment_start, sample_type, sex)

    querys = ["WHERE"]
    params = []
    for key, value in filter_col_name_to_condition.items():
        if filter_col_name_to_condition[key] != "all":
            querys.append(key + " = ?")
            querys.append("AND")
            params.append(value)
    querys.pop()
    query_string = " ".join(querys)

    conn = sqlite3.connect(SQL_DATABASE_PATH)

    print("query and params", query_string, params)

    df = pd.read_sql_query(f"""SELECT {','.join(cols_to_get)} FROM subjects JOIN samples ON subjects.subject = samples.subject
                                {query_string} """, conn, params=params)#params=(condition, treatment, time_from_treatment_start, sample_type, sex))
    
    # if 'response' in cols_to_get:
    #     df["response"] = df['response'].astype(bool)
    conn.close()

    return df


def get_all_unique_values(db_path: str) -> dict:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    result = {}
    for table in tables:
        result[table] = {}
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]

        for col in columns:
            cursor.execute(f"SELECT DISTINCT [{col}] FROM [{table}] ORDER BY [{col}]")
            result[table][col] = [row[0] for row in cursor.fetchall()]

    conn.close()
    return result
