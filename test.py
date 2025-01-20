from flask import Flask, jsonify, render_template, request
import pandas as pd

app = Flask(__name__)

# Load and preprocess the data
csv_path = "csv_data/dezembro.csv"
data = pd.read_csv(csv_path, skiprows=8, delimiter=",")

# Renaming columns for easier access
data = data.rename(columns={
    "Billing account name": "billing_account",
    "Project name": "project",
    "Cost (R$)": "cost"
})

@app.route("/data")
def get_data():
    # Get the billing account filter from query parameters
    billing_account_filter = request.args.get("billing_account")

    if billing_account_filter:
        # Filter the data by Billing Account Name
        filtered_data = data[data["billing_account"] == billing_account_filter]
    else:
        # Use all data if no filter is provided
        filtered_data = data

    # Summarize costs by project
    project_costs = filtered_data.groupby("project")["cost"].sum().reset_index()

    # Convert data to a JSON-friendly format
    chart_data = {
        "projects": project_costs["project"].tolist(),
        "costs": project_costs["cost"].tolist(),
    }
    return jsonify(chart_data)

@app.route("/")
def index():
    return render_template("chart.html")

if __name__ == "__main__":
    app.run(debug=True)
