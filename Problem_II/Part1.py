import pandas as pd
from prettytable import PrettyTable

# Read CSV file
df = pd.read_csv("result.csv")

# Check if the dataframe is empty
if df.empty:
    print("Result.csv file not found")
else:
    # Get all the headers
    print("Result.csv read!")
    criterias = df.columns[4:]  # get all the criteria start from the 5th column

    # Open the output file in write mode with UTF-8 encoding
    with open("top_3.txt", mode="w", encoding="utf-8") as output:
        for criteria in criterias:
            # Sort the dataframe by the given criteria
            sorted_df = df.sort_values(by=criteria, ascending=False, kind="mergesort")

            # Write the top 3 players for the given criteria
            output.write(f"Top 3 players with the criteria '{criteria}':\n")
            table = PrettyTable()
            table.field_names = df.columns  # Set the table headers
            top_3 = sorted_df.head(3)
            for _, row in top_3.iterrows():
                table.add_row(row)  # Add each row to the table
            output.write(str(table) + "\n")  # Write the table to the file

            # Write the bottom 3 players for the given criteria
            output.write(f"Bottom 3 players with the criteria '{criteria}':\n")
            table.clear_rows()  # Clear the table rows for reuse
            bottom_3 = sorted_df.tail(3)
            for _, row in bottom_3.iterrows():
                table.add_row(row)  # Add each row to the table
            output.write(str(table) + "\n")  # Write the table to the file
            output.write("\n")
        print("All data have been written to top_3.txt")