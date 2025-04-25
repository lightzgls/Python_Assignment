from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv("result.csv")

#get the criteria except name, team, pos, nation
criterias = ["Shooting_SoT%", "Shooting_SoT/90", "Shooting_G/Sh","Defense_Att","Defense_Lost","Defense_Blocks"]

for criteria in criterias:

    #change all the value to to numberic, "N/a" string to NaN
    df[criteria] = pd.to_numeric(df[criteria],errors='coerce').dropna()

    #get the data of that column as panda array
    data = df[criteria]

    #configure histogram
    plt.hist(data, bins=30, edgecolor='black', alpha=0.7)


    # Set the title, x-label, and y-label
    plt.title(f"Distribution of {criteria}")
    plt.xlabel("Value")
    plt.ylabel("Number of player")

    #show histogram
    plt.show()
