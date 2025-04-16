#!/home/lightzgls/code/Python-Assignment/venv/bin/python
import requests
import pandas as pd

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
    df = pd.DataFrame(records)
    df = df[["player_name", "age", "team_name", "estimated_value"]]
    all_transfers.append(df)
    print(f"Done reading page {page}!")

# Concatenate all transfer data into a single DataFrame
df = pd.concat(all_transfers)
df.columns = ["Player", "Age", "Team","Estimated Value"]

# Read minute data CSV
df1 = pd.read_csv("result.csv")

# Filter players with more than 900 minutes
df1_filtered = df1[df1['Standard_Min'] > 900]
print("Done filtering playing with play time > 900 minutes!")
# Filter transfer list to keep only those players
df1_players = df1_filtered['Player'].tolist()
filtered_df = df[df['Player'].isin(df1_players)]

# Merge transfer data with minute data
result_df = pd.merge(filtered_df, df1_filtered[['Player', 'Standard_Min']], on='Player', how='left')
result_df = result_df[["Player", "Age", "Team","Standard_Min","Estimated Value"]]

# Display result
print(result_df)

result_df.to_csv("Transfer_values.csv")
print("Data saved to Trandfer_values.csv")