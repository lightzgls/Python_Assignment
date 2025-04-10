from matplotlib import pyplot as plt
import pandas as pd


df = pd.read_csv("result.csv")

criterias = df.columns[4:]  # List of criteria columns

teams_name = set(df['Squad'])  # Set of all team names

# Iterate over each team and criteria
for team in teams_name:
    for criteria in criterias:
        # Convert the criteria column to numeric values (coerce errors to NaN)
        numeric_col = pd.to_numeric(df[criteria], errors='coerce')

        # Filter the data for the specific team and drop NaN values
        data = numeric_col[df["Squad"] == team].dropna()

        # Create a new figure for each plot
        plt.figure()

        # Plot the histogram for the current team's data for this criteria
        plt.hist(data, bins=20, edgecolor='black', alpha=1)

        # Set the title, x-label, and y-label
        plt.title(f"Distribution of {criteria} for {team}")
        plt.xlabel("Value")
        plt.ylabel("Number of players")

        # Show the plot
        plt.show()
