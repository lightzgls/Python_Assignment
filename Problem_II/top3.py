import pandas as pd

# Read CSV file
df = pd.read_csv("result.csv")

# Check if the dataframe is empty
if df.empty:
    print("Result.csv file not found")
else:
    # Get all the headers
    criterias = df.columns[4:]
    # Open the output file in append mode with UTF-8 encoding
    with open("top_3.txt", mode="w", encoding="utf-8") as output:
        for criteria in criterias:
            # Sort the dataframe by the given criteria
            sorted_df = df.sort_values(by=criteria, ascending=True, kind="mergesort")

            # Write the top 3 players for the given criteria
            output.write(f"Top 3 players with the criteria {criteria}:\n")
            output.write(" , ".join(df.columns) + "\n")
            top_3 = sorted_df.head(3)
            for index, row in top_3.iterrows():
                output.write(" | ".join(str(value) for value in row) + "\n")

            # Write the bottom 3 players for the given criteria
            output.write(f"Bottom 3 players with the criteria {criteria}:\n")
            output.write(" , ".join(df.columns) + "\n")
            bottom_3 = sorted_df.tail(3)
            for index, row in bottom_3.iterrows():
                output.write(" | ".join(str(value) for value in row) + "\n")