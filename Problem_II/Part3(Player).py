from matplotlib import pyplot as plt
import pandas as pd
import os

# Load data
df = pd.read_csv("results.csv")

# Criteria to plot
criterias = ["Shooting_SoT%", "Shooting_SoT/90", "Shooting_G/Sh", "Defense_Att", "Defense_Lost", "Defense_Blocks"]

# Ensure all values are numeric
for criteria in criterias:
    df[criteria] = pd.to_numeric(df[criteria], errors='coerce')

# Create subplots
n = len(criterias)
rows = (n + 2) // 3  # up to 3 per row
fig, axes = plt.subplots(rows, 3, figsize=(15, 5 * rows))
axes = axes.flatten()  # flatten to make iteration easier

# Plot each histogram
for i, criteria in enumerate(criterias):
    data = df[criteria].dropna()
    axes[i].hist(data, bins=30, edgecolor='black', alpha=0.7)
    axes[i].set_title(f"Distribution of {criteria}")
    axes[i].set_xlabel("Value")
    axes[i].set_ylabel("Number of players")

# Hide any unused subplots
for j in range(len(criterias), len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()
plt.show()

