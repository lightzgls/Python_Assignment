from matplotlib import pyplot as plt
import pandas as pd


df = pd.read_csv("results.csv")

criterias = ["Shooting_SoT%", "Shooting_SoT/90", "Shooting_G/Sh","Defense_Att","Defense_Lost","Defense_Blocks"]  # List of criteria columns
  # List of criteria columns

teams_name = sorted(set(df['Team']))  # Set of all team names

# Iterate over each team and criteria
for team in teams_name:
    for criteria in criterias:
        # Convert the criteria column to numeric values (coerce errors to NaN)
        numeric_col = pd.to_numeric(df[criteria], errors='coerce')

        # Filter the data for the specific team and drop NaN values
        data = numeric_col[df["Team"] == team].dropna()

        # Create a new figure for each plot
        plt.figure()

        # Plot the histogram for the current team's data for this criteria
        plt.hist(data, bins=30, edgecolor='black', alpha=1)
        plt.grid(axis="y",alpha=1,linestyle= "--")

        # Set the title, x-label, and y-label
        plt.title(f"Distribution of {criteria} for {team}")
        plt.xlabel("Value")
        plt.ylabel("Number of players")

        # Show the plot
        plt.show()
