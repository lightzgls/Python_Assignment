import requests
import pandas as pd
from utils import *



url = 'https://www.footballtransfers.com/us/values/actions/most-valuable-football-players/overview'

headers = {
    "authority": "www.footballtransfers.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Referer": "https://www.footballtransfers.com/us/values/players/most-valuable-soccer-players/playing-in-uk-premier-league",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

payload = {
    "orderBy": "estimated_value",
    "orderByDescending": 1,
    "page": 1,
    "pages": 0,
    "pageItems": 25,
    "positionGroupId": "all",
    "mainPositionId": "all",
    "playerRoleId": "all",
    "age": "all",
    "countryId": "all",
    "tournamentId": 31
}

all_transfers = []

# Fetch data from all pages
for page in range(1, 23):
    print(f"Start reading page {page}.")
    payload['page'] = page
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    records = data["records"]
    df_page = pd.DataFrame(records)
    df_page = df_page[["player_name", "age", "team_name", "estimated_value"]]
    df_page["player_name"] = df_page["player_name"].str.replace("\u00a0", "")
    all_transfers.append(df_page)
    print(f"Done reading page {page}!")

# Concatenate all transfer data into a single DataFrame
df = pd.concat(all_transfers)
df.columns = ["Player", "Age", "Team", "Estimated Value"]

# Read minute data CSV
df1 = pd.read_csv("result.csv", encoding="utf-8")


df["Canonical_Player"] = df["Player"].apply(canonical_name)
df1["Canonical_Player"] = df1["Player"].apply(canonical_name)


# For df1, create a list of canonical names
df1_players = df1["Canonical_Player"].tolist()

filtered_df = df[df.apply(lambda row: fuzzy_filter(row, df1_players), axis=1)]

# Use .loc to avoid SettingWithCopyWarning and ensure proper assignment
filtered_df = filtered_df.copy()  # Create a copy to avoid chained assignment issues
filtered_df["Best_Match"] = filtered_df["Canonical_Player"].apply(lambda n: get_best_match(n, df1_players))

# Ensure 'Match' column exists in df1 before merging
df1 = df1.rename(columns={'Canonical_Player': 'Match'})

# Merge DataFrames on 'Best_Match' (without using Team as a key)
result_df = pd.merge(
    df1[['Player',"Team" ,'Standard_Min', 'Match']],
    filtered_df[['Player', 'Best_Match', 'Estimated Value']],
    left_on=["Match"],
    right_on=["Best_Match"],
    how='left'
)

# Choose the desired columns:
result_df = result_df[["Player_x", "Standard_Min", "Team", "Estimated Value"]]
result_df = result_df.rename(columns={"Player_x": "Player", "Standard_Min": "Played Time"})
result_df = result_df[result_df["Played Time"] > 900]
# Find players in result_df missing the Estimated Value
missing_values_df = result_df[result_df["Estimated Value"].isna()]

# Iterate through missing players and find the best match in df
for index, row in missing_values_df.iterrows():
    player_name = row["Player"]
    player_team = row["Team"]
    print(f"Tranfer value of player {player_name} in {player_team} is missing, starts to find on website")
    # Perform external lookup to get the estimated value
    estimated_value = external_lookup(player_name, player_team)
    
    # Update the result_df with the retrieved value
    if estimated_value:
        print("Found!")
        result_df.loc[index, "Estimated Value"] = estimated_value
    else:
        print("Not found!")

# Save the updated DataFrame
result_df.to_csv("Transfer_values.csv", index=False, encoding="utf-8-sig")

print(result_df)