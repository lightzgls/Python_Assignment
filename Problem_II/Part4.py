import pandas as pd

# Read the CSV file
df = pd.read_csv("result2.csv", skiprows=1, index_col=False)

# Get the criteria columns (starting from the 8th column)
criterias = df.columns[8:]

# Initialize a dictionary to store the scores for each team
score_check = {}

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    team_name = row.iloc[1]  # Replace with the actual column name for the team
    if team_name not in score_check:
        score_check[team_name] = 0  # Initialize the team's score

    # Sum the numeric values for the criteria columns
    for criteria in criterias:
        numeric_value = pd.to_numeric(row[criteria], errors='coerce')  # Convert to numeric
        if not pd.isna(numeric_value):  # Ignore NaN values
            score_check[team_name] += numeric_value

# Find the best-performing team
best_team = max(score_check, key=score_check.get)
print(f"The best-performing team in the 2024-2025 Premier League season is {best_team}")