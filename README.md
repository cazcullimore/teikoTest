# Teiko Technical

## Instructions
- run `make setup` to install dependencies
- then run `python load_data.py` to load the database
- `make pipeline` generates the data analysis output files 
- `make dashboard` starts the server to the dashboard
    - local link: http://127.0.0.1:5000
    - codespaces link: https://\<codespace\>-5000.app.github.dev (go to the ports tab (next to terminal) in vscode and click on the link under forwarded address)



## SQL database schema
I decided to go with a simple schema of two tables:
- 'subjects' for patient metadata
- 'samples' for information on each sample

This allows us to reduce redundant columns of the patient metadata and reduces the size of our data. I indexed on samples and subjects. Indexing on subjects is probably the most important, so I can join efficiently when selecting specific patient populations. For 100s of projects, I probably would want to change some of the dashboard to not load everything at once. For a larger project, I might want to index on other columns in the subject table as well. However, the subject table will be much smaller than the sample table, so scanning would only become an issue later than it otherwise would be.




## Code Structure

`load_data.py` contains code to load the database.

`config.py` contains all the global constants that are used across files. 

`pipeline.py` contains all the data manipulation and analysis code as well as functions to generate the output tables and figures.

`dashboard.py` contains the HTML interface. It imports the analysis code from `pipeline.py`. 

`templates/index.html` contains the HTML for the dashboard.

This project has nice conceptual blocks that I chose to reflect in my code. By separating the data manipulation code and HTML interface, it forces me to make functions that only handle a single task. It also makes all the functions in the file related to a single task. I could have divided my pipeline.py into multiple files to separate the SQL and pandas code, but this project is small enough that it's unnecessary.


## Part 3 Statistical Analysis Results
Nothing is significant when looking at proportions. Some populations are close if looking at raw counts.

