setup:
	pip install -e . # Installs all necessary dependencies for your project (e.g., from a requirements.txt, environment.yml, or pyproject.toml).

# pipeline:
# # Executes your entire data pipeline sequentially from start to finish without any manual intervention. When our grader runs this command, it should initialize the database, load the data (Part 1), and generate all required output tables and plots (Parts 2-4). (Note: You may use pure Python, bash scripts, Snakemake, or any other orchestration tool, as long as make pipeline triggers the complete execution).

# dashboard:
# # sarts the local server for your interactive dashboard.