import pandas as pd

# Read the CSV file
df = pd.read_csv("results2.csv", index_col=False)

#remove the "all" rwo and reset the index
df = df.drop(0).reset_index(drop=True)


# Get the criteria columns (only get the mean of each criteria)
criterias = df.columns[3::3]

# Initialize a dictionary to store the scores for each team
teams_names = set(df.iloc[:,1])
score_check = {team: 0 for team in teams_names}
highest_per_criteria = {criteria: "" for criteria in criterias}

# Sum the scores for each criteria by finding the index of the maximum per column
for criteria in criterias:

    numeric_cols = pd.to_numeric(df[criteria], errors='coerce')  # Convert to numeric
    # Skip this criteria if all values are NaN
    if numeric_cols.isna().all():
        continue


    idx_max = numeric_cols.idxmax()  # Get index of maximum value in the column
    team_name = df.iloc[idx_max, 1]  # Get the team name from the "Team" column at that index
    score_check[team_name] += 1
    highest_per_criteria[criteria] = team_name


#print out the team with the highest score per criteria
for criteria, team in highest_per_criteria.items():
    print(f"Team with the highest {criteria.split()[2]} is {team}")


# Find the best-performing team
best_team = max(score_check, key=score_check.get)
print("Score check")
for key, value in score_check.items():
    print(f"{key}: {value} scored")

print(f"The best-performing team in the 2024-2025 Premier League season is {best_team}")