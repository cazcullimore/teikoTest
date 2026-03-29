from config import DASHBOARD_BOX_OPTION_COLS, DASHBOARD_BUTTON_OPTION_COLS
from flask import Flask, render_template, request
from database_helpers import query_sql


app = Flask(__name__)

# option_dict = {}
# def load_summary_box():
    # results = query_sql("*",{}) # get everything to get rows


@app.route("/", methods=["GET", "POST"])
def home():

    selected = []
    
    
    results = query_sql("*",{}) # get everything to get rows
    

    # I need to get all the columns make a SQL query with 

    # option_dict = {"col1": ["option1_c1", "o2_c1"], "col2": ["o1_c2", "dfjadlk"]}
    option_dict = {col: results[col].astype(str).unique().tolist() + ["all"] for col in DASHBOARD_BUTTON_OPTION_COLS}
    selected = {col: "all" for col in option_dict}
    if request.method == "POST":
        for col in option_dict:
            selected[col] = request.form.get(f"{col}")  
        print("selected",selected)
    
    results = query_sql("*", selected)
    items = []
    for idx, row in results.iterrows():
        items.append(row.to_string())
    print(results)
    return render_template("index.html", table=results.to_html(index=False), option_dict=option_dict, selected=selected)

if __name__ == "__main__":
    app.run(debug=True)

