import pandas as pd
from collections import Counter
df = pd.read_csv("result2.csv",skiprows=1,index_col=False)

criterias = df.columns[1:]

highest_per_criteria = []

for criteria in criterias:

    numeric_column = pd.to_numeric(df[criteria], errors='coerce')
    if numeric_column.any():
        # Get the index of the maximum value
        highest_index = numeric_column.idxmax()

        # Get the team name from the first column
        team_name = df.iloc[highest_index,1]
        highest_per_criteria.append(team_name)

print(f"The best perfoming team in the 2024-2025 Premier League season is {max(Counter(highest_per_criteria))}")