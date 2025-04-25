from matplotlib import pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv("results.csv")

# List of criteria columns
criterias = ["Shooting_SoT%", "Shooting_SoT/90", "Shooting_G/Sh", "Defense_Att", "Defense_Lost", "Defense_Blocks"]

# Set of all team names
teams_name = sorted(set(df['Team']))

# Iterate over each team
for team in teams_name:
    # Create a 2x3 grid for 6 subplots (2 rows, 3 columns)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Flatten axes for easy iteration
    axes = axes.flatten()

    # Iterate over each criterion and plot its histogram for the current team
    for i, criteria in enumerate(criterias):
        # Convert the criteria column to numeric values (coerce errors to NaN)
        numeric_col = pd.to_numeric(df[criteria], errors='coerce')

        # Filter the data for the specific team and drop NaN values
        data = numeric_col[df["Team"] == team].dropna()

        # Plot the histogram for the current criteria
        axes[i].hist(data, bins=30, edgecolor='black', alpha=0.7)
        axes[i].grid(axis="y", alpha=0.7, linestyle="--")

        # Set the title, x-label, and y-label for the plot
        axes[i].set_title(f"{criteria} for {team}")
        axes[i].set_xlabel("Value")
        axes[i].set_ylabel("Number of players")

    # Adjust the layout to avoid overlap
    plt.tight_layout()

    # Show the plots
    plt.show()
