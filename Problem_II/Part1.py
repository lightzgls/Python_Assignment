import pandas as pd
from prettytable import PrettyTable

# Try reading CSV file
try:
    df = pd.read_csv("result.csv")
except FileNotFoundError:
    print("Result.csv file not found")
    exit()

if df.empty:
    print("Result.csv is empty")
    exit()
else:
    print("Result.csv read!")

    criterias = df.columns[4:]  # get all criteria starting from the 5th column

    # Replace "N/a" and similar with pd.NA
    df = df.replace(["N/a", "NA", "na", ""], pd.NA)

    with open("top_3.txt", mode="w", encoding="utf-8") as output:
        for criteria in criterias:
            df_temp = df.copy()
            df_temp[criteria] = pd.to_numeric(df_temp[criteria], errors='coerce')
            df_temp = df_temp.dropna(subset=[criteria])

            table = PrettyTable()
            table.field_names = ["Player", "Pos", "Team", criteria]

            # Top 3
            output.write(f"Top 3 players with the criteria '{criteria}':\n")
            top_3 = df_temp.nlargest(3, criteria)
            for _, row in top_3.iterrows():
                table.add_row(list(row[["Player", "Pos", "Team", criteria]]))
            output.write(str(table) + "\n")

            # Bottom 3
            output.write(f"Bottom 3 players with the criteria '{criteria}':\n")
            table.clear_rows()
            bottom_3 = df_temp.nsmallest(3, criteria)
            for _, row in bottom_3.iterrows():
                table.add_row(list(row[["Player", "Pos", "Team", criteria]]))
            output.write(str(table) + "\n\n")

    print("All data have been written to top_3.txt")
