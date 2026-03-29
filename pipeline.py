from collections.abc import Iterable

from config import CSV_DATA_PATH, SQL_DATABASE_PATH, CELL_TYPES
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from scipy import stats
from statannotations.Annotator import Annotator


import seaborn as sns

def part2_make_summary_table():
    # I would get samples from SQL
    conn = sqlite3.connect(SQL_DATABASE_PATH)

    df = pd.read_sql_query(f"SELECT sample,{','.join(CELL_TYPES)} FROM samples",conn,)
    conn.close()

    df_summary = pivot_summary_table(df, "sample")

def pivot_summary_table(df, pivot_on,):
    df_cell_types = df.set_index(pivot_on)
    totals = df_cell_types.sum(axis=1)

    df_summary = df_cell_types.stack() # Slow should fix if time

    df_summary.name = "count"

    if isinstance(pivot_on, (list, tuple)):
        df_summary.index.names = (*pivot_on, "population",)
    else:
        df_summary.index.names = (pivot_on, "population",)

    df_summary = df_summary.reset_index().set_index(pivot_on)
    df_summary["total_count"] = totals
    return df_summary

def part3_data_analysis():
    """As the trial progresses, Bob wants to identify patterns that might predict treatment response and
      share those findings with his colleague, Yah D’yada. Using the data reported in the summary table,
        your program should provide functionality to:

    Compare the differences in cell population relative frequencies of melanoma patients 
    receiving miraclib who respond (responders) versus those who do not (non-responders), with the overarching aim of predicting response to the treatment miraclib. Response information can be found in column "response", with value "yes" for responding and value "no" for non-responding. Please only include PBMC samples.

Visualize the population relative frequencies comparing responders versus non-responders using a boxplot of for each immune cell population.

Report which cell populations have a significant difference in relative frequencies between responders and non-responders. Statistics are needed to support any conclusion to convince Yah of Bob’s findings. 
"""
   
    subject_condition = "melanoma"
    treatment = "miraclib"
    conn = sqlite3.connect(SQL_DATABASE_PATH) # 
    df = pd.read_sql_query(f"""SELECT subjects.subject,response,{','.join(CELL_TYPES)} FROM subjects JOIN samples ON subjects.subject = samples.subject
                                WHERE condition = '{subject_condition}' AND
                                treatment = '{treatment}' AND
                                time_from_treatment_start = 0 AND
                                sample_type = "PBMC"
                                
                                """,conn,)

    # df["t_cells"] = df[["cd8_t_cell", "cd4_t_cell"]].sum(axis=1)
    pivoted = pivot_summary_table(df, ["response", "subject"]).reset_index()
    pivoted["proportion"] = pivoted["count"] / pivoted["total_count"]
    
    
    # print(p
    # t_cells = pivoted[(pivoted["population"].isin(["cd8_t_cell","cd4_t_cell"]))].groupby(["response", "subject"])["proportion"].sum().reset_index()
    # t_cells["population"] = "t_cells"
    # pivoted = pd.concat([pivoted, t_cells], ignore_index=True)
    pop_stats = {}

    for cell_pop in pivoted["population"].unique():
        data = df[[cell_pop, "response"]]
        # stat, p_normal = stats.shapiro(data)

        stat, p_dist = stats.mannwhitneyu(data.loc[data["response"] == 1, cell_pop], data.loc[data["response"] == 0, cell_pop], alternative='two-sided')

        pop_stats[cell_pop] =  p_dist

    # pop_stats = {key: stats.false_discovery_control(value) for key, value in pop_stats.items()}
    print(pop_stats)
    print(pop_stats.values())
    pop_stats = pd.Series(stats.false_discovery_control(list(pop_stats.values())), index=pop_stats.keys())

    bp = sns.boxplot(
        data=pivoted,
        x="population",
        y="proportion",
        hue="response"
    )

    annotator = Annotator(bp, [((elt, 0,), (elt, 1)) for elt in pop_stats.index], data=pivoted, x="population", y="proportion", hue="response")
    annotator.configure(text_format="simple", loc="outside")

    annotator.set_pvalues_and_annotate(pop_stats)

    plt.savefig("Bonferroni-corrected_p-values_between_responders_and_nonresponders.png")
    plt.show()
    conn.close()
    plt.show()
    conn.close()

if __name__ == "__main__":
    df_summary = part2_make_summary_table()
    print(df_summary)


    output = part3_data_analysis()
    print(output)