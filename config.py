
CSV_DATA_PATH = "cell-count.csv"
SQL_DATABASE_PATH = "cell-count.db"

CELL_TYPES = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]

SUBJECT_TABLE_COLS = ["subject", 
                      "project", 
                      "condition", 
                      "age", 
                      "sex", 
                      "treatment", 
                      "response"]
    
SAMPLE_TABLE_COLS = ["sample", 
                    "subject", 
                    "sample_type", 
                    "time_from_treatment_start", 
                    "b_cell", 
                    "cd8_t_cell", 
                    "cd4_t_cell", 
                    "nk_cell", 
                    "monocyte"]


"""Identify all melanoma PBMC samples at baseline (time_from_treatment_start is 0) from patients who have been treated with miraclib. 

Among these samples, extend the query to determine:

How many samples from each project

How many subjects were responders/non-responders 

How many subjects were males/females"""

DASHBOARD_BUTTON_OPTION_COLS = ["project", 
                               "condition", 
                               "treatment", 
                               "response",
                               "time_from_treatment_start",
                               "sample_type", ] #+ CELL_TYPES

DASHBOARD_BOX_OPTION_COLS = []