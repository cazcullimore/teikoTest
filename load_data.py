import pandas as pd
import sqlite3
from config import CSV_DATA_PATH, SAMPLE_TABLE_COLS, SQL_DATABASE_PATH, SUBJECT_TABLE_COLS


def make_db():

    conn = sqlite3.connect(SQL_DATABASE_PATH)
    cursor = conn.cursor()

    df = pd.read_csv(CSV_DATA_PATH)
    patient_info = df[SUBJECT_TABLE_COLS].drop_duplicates()# extract patient info 


    patient_info.to_sql("subjects", conn, if_exists='replace', index=False)

    cursor.execute("CREATE INDEX subjects_subject_index ON subjects(subject)")

    

    # extract sample info
    sample_info = df[SAMPLE_TABLE_COLS].drop_duplicates()

    sample_info.to_sql("samples", conn, if_exists='replace', index=False)

    cursor.execute("CREATE INDEX sample_index ON samples(sample)")
    cursor.execute("CREATE INDEX samples_subject_index ON samples(subject)")
    
    
    conn.commit()
    conn.close()
    print("SUCCESS")


if __name__ == "__main__":
    make_db()