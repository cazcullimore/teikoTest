from config import DASHBOARD_BUTTON_OPTION_COLS
from flask import Flask, render_template, request
from pipeline import get_filter_stats, make_boxplot, pivot_summary_table, query_sql
import io, base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def get_bp_html(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return f'<img src="data:image/png;base64,{img_b64}">'

    

app = Flask(__name__)

with app.app_context():
    _schema_results = query_sql("*", {})
    OPTION_DICT = {col: _schema_results[col].astype(str).unique().tolist() + ["all"] 
                   for col in DASHBOARD_BUTTON_OPTION_COLS}

@app.route("/", methods=["GET", "POST"])
def home():

    selected = []
    selected = {col: "all" for col in OPTION_DICT}
    filter_stat1 = "response"
    filter_stat2 = "subject"
    if request.method == "POST":
        for col in OPTION_DICT:
            post_value = request.form.get(f"{col}")  
            print("col ",col," filtering got '",post_value,"'",sep="")
            if post_value is not None:
                selected[col] = post_value

        print("selected",selected)
        post_value = request.form.get(f"filter_stat1")
        if post_value is not None:
            filter_stat1 = post_value
        post_value = request.form.get(f"filter_stat2")
        if post_value is not None:
            filter_stat2 = post_value
        
    
    results = query_sql("*", selected)
    try:
        box_html = get_bp_html(make_boxplot(results))
    except (ValueError, TypeError):
        box_html = '<h3>Filtering Not Valid for Boxplot</h3>'

    print("filter_stat1, filter_stat2", filter_stat1, filter_stat2)
    print(results)
    summary_results = pivot_summary_table(results, "sample")
    
    filter_stat_output =  get_filter_stats(results, filter_stat1, filter_stat2).reset_index().to_html(index=False) 
    print(get_filter_stats(results, filter_stat1, filter_stat2).to_string())
    return render_template("index.html", 
                           table=summary_results.reset_index().to_html(index=False), 
                           option_dict=OPTION_DICT, 
                           selected=selected, 
                           filter_stat1=filter_stat1, 
                           filter_stat2=filter_stat2, 
                           stat1_columns=DASHBOARD_BUTTON_OPTION_COLS, 
                           stat2_columns=results.columns, 
                           filter_stat_output=filter_stat_output,
                           box_html=box_html)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

