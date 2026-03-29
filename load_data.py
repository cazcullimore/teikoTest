import pandas as pd
import sqlite3
from config import CSV_DATA_PATH, SQL_DATABASE_PATH


def make_db():

    conn = sqlite3.connect(SQL_DATABASE_PATH)
    cursor = conn.cursor()


    patient_table_cols = ["subject", "project", "condition", "age", "sex", "treatment", "response"]
    # for table in 
    df = pd.read_csv(CSV_DATA_PATH)
    patient_info = df[patient_table_cols].drop_duplicates()# extract patient info 
    patient_info["response"] = patient_info["response"] == "yes" # convert bool
    
    # cursor.execute("""
    #     CREATE TABLE subjects (
    #         subject VARCHAR PRIMARY KEY,
    #         project VARCHAR,
    #         condition VARCHAR,
    #         age INTEGER, 
    #         sex CHAR, 
    #         treatment VARCHAR, 
    #         response BOOL
    #                    );""")

    patient_info.to_sql("subjects", conn, if_exists='replace', index=False)

    cursor.execute("CREATE INDEX subject_index ON subjects(subject)")

    sample_table_cols = ["sample", 
                         "subject", 
                         "sample_type", 
                         "time_from_treatment_start", 
                         "b_cell", 
                         "cd8_t_cell", 
                         "cd4_t_cell", 
                         "nk_cell", 
                         "monocyte"]

    # extract sample info
    # extract sample metadata - will combine fofr now
    sample_info = df[sample_table_cols].drop_duplicates()

    sample_info.to_sql("samples", conn, if_exists='replace', index=False)

    cursor.execute("CREATE INDEX sample_index ON samples(sample)")
    cursor.execute("CREATE INDEX patient_index ON samples(subject)")
    


    conn.commit()
    conn.close()
    print("SUCCESS")


if __name__ == "__main__":
    make_db()