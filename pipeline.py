from collections.abc import Iterable

from config import CSV_DATA_PATH, SQL_DATABASE_PATH, CELL_TYPES
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from scipy import stats
from statannotations.Annotator import Annotator


import seaborn as sns



def pivot_summary_table(df, pivot_on,):
    df_cell_types = df.set_index(pivot_on)[CELL_TYPES]
    totals = df_cell_types.sum(axis=1)

    df_summary = df_cell_types.stack() # Slow should fix if time

    df_summary.name = "count"

    if isinstance(pivot_on, (list, tuple)):
        df_summary.index.names = (*pivot_on, "population",)
    else:
        df_summary.index.names = (pivot_on, "population",)

    df_summary = df_summary.reset_index().set_index(pivot_on)
    df_summary["total_count"] = totals
    df_summary["percentage"] = 100 * df_summary["count"] / df_summary["total_count"]
    return df_summary


def make_boxplot(df):
    pivoted = pivot_summary_table(df, ["response", "subject"]).reset_index()
    pivoted["proportion"] = pivoted["count"] / pivoted["total_count"]

    pop_stats = {}

    for cell_pop in pivoted["population"].unique():
        data = df[[cell_pop, "response"]]

        stat, p_dist = stats.mannwhitneyu(data.loc[data["response"] == 'yes', cell_pop], data.loc[data["response"] == 'no', cell_pop], alternative='two-sided')

        pop_stats[cell_pop] =  p_dist

    pop_stats = pd.Series(stats.false_discovery_control(list(pop_stats.values())), index=pop_stats.keys())
    fig, bp = plt.subplots()
    sns.boxplot(
        data=pivoted,
        x="population",
        y="proportion",
        hue="response",
        ax=bp
    )

    annotator = Annotator(bp, [((elt, 'no',), (elt, 'yes')) for elt in pop_stats.index], data=pivoted, x="population", y="proportion", hue="response")
    annotator.configure(text_format="simple", loc="outside")

    annotator.set_pvalues_and_annotate(pop_stats)

    plt.savefig("responder_nonresponder_boxplot.png")
   
    return fig

def get_filter_stats(df, cat1, cat2):
    if df[cat2].dtype == "object":
        output = df.groupby(cat1)[cat2].nunique()
    else:
        output = df.groupby(cat1)[cat2].mean()
        output.name = "mean_" + output.name
    return output

import sqlite3
import pandas as pd
from config import SQL_DATABASE_PATH


def query_sql(cols_to_get,filter_col_name_to_condition): 

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

    df = pd.read_sql_query(f"""SELECT {','.join(cols_to_get)} FROM subjects JOIN samples USING(subject)
                                {query_string} """, conn, params=params)
    
    conn.close()

    return df


# main pipeline funcs
def part2_make_summary_table():
    # I would get samples from SQL
    conn = sqlite3.connect(SQL_DATABASE_PATH)

    df = pd.read_sql_query(f"SELECT sample,{','.join(CELL_TYPES)} FROM samples",conn,)
    conn.close()

    df_summary = pivot_summary_table(df, "sample")
    return df_summary


def part3_data_analysis():
    subject_condition = "melanoma"
    treatment = "miraclib"
    conn = sqlite3.connect(SQL_DATABASE_PATH) 
    df = pd.read_sql_query(f"""SELECT subjects.subject,response,{','.join(CELL_TYPES)} FROM subjects JOIN samples ON subjects.subject = samples.subject
                                WHERE condition = '{subject_condition}' AND
                                treatment = '{treatment}' AND
                                time_from_treatment_start = 0 AND
                                sample_type = "PBMC"
                                
                                """,conn,)

    make_boxplot(df)
    conn.close()


def part4_filter_stats():

    mel_mirc_PBMC = query_sql("*", {"sample_type": "PBMC",  "time_from_treatment_start":0, "treatment": "miraclib"})
    mel_mirc_PBMC.to_csv("mel_mirc_PBMC.csv")
    get_filter_stats(mel_mirc_PBMC, "project", "sample").to_csv("samples_per_project_mel_mirc_PBMC.csv")
    get_filter_stats(mel_mirc_PBMC, "response", "subject").to_csv("subjects_per_response_mel_mirc_PBMC.csv")
    get_filter_stats(mel_mirc_PBMC, "sex", "subject").to_csv("subjects_per_sex_mel_mirc_PBMC.csv")



if __name__ == "__main__":
    df_summary = part2_make_summary_table()
    df_summary.to_csv("summary_table.csv")


    output = part3_data_analysis()

    part4_filter_stats()