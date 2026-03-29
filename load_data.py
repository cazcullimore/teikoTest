import pandas as pd
import sqlite3

CSV_DATA_PATH = "cell-count.csv"
SQL_DATABASE_PATH = "cell-count.db"


def make_db():

    conn = sqlite3.connect(SQL_DATABASE_PATH)
    cursor = conn.cursor()


    patient_table_cols = ["subject", "project", "condition", "age", "sex", "treatment", "response"]
    # for table in 
    df = pd.read_csv(CSV_DATA_PATH)
    patient_info = df[patient_table_cols]# extract patient info 
    patient_info["response"] = patient_info["response"] == "yes" # convert bool
    
    cursor.execute("""
        CREATE TABLE patients (
            subject VARCHAR PRIMARY KEY,
            project VARCHAR,
            condition VARCHAR,
            age INTEGER, 
            sex CHAR, 
            treatment VARCHAR, 
            response BOOL
                       );""")
    


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
    sample_info = sample_table_cols

    cursor.execute("""
        CREATE TABLE samples (
            sample PRIMARY KEY,
            subject VARCHAR, 
            sample_type VARCHAR,
            time_from_treatment_start INTEGER,
            b_cell VARCHAR
            
                       );""")


    


    conn.commit()
    conn.close()



if __name__ == "__main__":
    