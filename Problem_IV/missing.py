import pandas as pd

# Sample DataFrames with player names
df1 = pd.read_csv("player_transfer_values.csv")
df2 = pd.read_csv("Transfer_values.csv")

# Find players in df1 missing in df2
missing_in_df2 = set(df1['Player']) - set(df2['Player'])
print("Players in df1 missing in df2:")
print(missing_in_df2)

# Optionally, find players in df2 missing in df1
missing_in_df1 = set(df2['Player']) - set(df1['Player'])
print("Players in df2 missing in df1:")
print(missing_in_df1)