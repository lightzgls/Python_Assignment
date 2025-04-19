import requests
import pandas as pd
from utils import *
from unidecode import unidecode


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
df_from_fbref = pd.read_csv("result.csv", encoding="utf-8")

result_df = pd.merge(
    df_from_fbref[['Player',"Team",'Standard_Min']],
    df[['Player', 'Estimated Value']],
    on="Player",
    how='left'
)
result_df = result_df.rename(columns={"Standard_Min": "Played Time"})
result_df = result_df[result_df["Played Time"] > 900]

# Find players in result_df missing the Estimated Value
missing_values_df = result_df[result_df["Estimated Value"].isna()]

# Iterate through missing players and find the best match in df
for index, row in missing_values_df.iterrows():
    player_name = row["Player"]
    player_team = row["Team"]
    # Normalize player name to remove special characters
    normalized_name = unidecode(player_name)
    print(f"Tranfer value of player {player_name} in {player_team} is missing, starts to find on website")
    # Perform external lookup to get the estimated value using the normalized name
    estimated_value = external_lookup(normalized_name, player_team)
    
    # Update the result_df with the retrieved value
    if estimated_value:
        print("Found!")
        result_df.loc[index, "Estimated Value"] = estimated_value
    else:
        print("Not found!")

# Save the updated DataFrame
result_df = result_df[["Player","Team","Estimated Value"]]
result_df.to_csv("Transfer_values.csv", index=False, encoding="utf-8-sig")

print(result_df)