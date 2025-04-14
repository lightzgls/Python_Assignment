import requests
import pandas as pd

url = 'https://www.footballtransfers.com/en/transfers/actions/confirmed/overview'

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.footballtransfers.com/en/transfers/confirmed/2024-2025/uk-premier-league",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

payload = {
    "orderBy": "date_transfer",
    "orderByDescending": 1,
    "page": 1,
    "pages": 14,
    "pageItems": 25,
    "countryId": "",      
    "season": 5845,
    "tournamentId": 31,
    "clubFromId": "",
    "clubToId": "",
}

all_transfers = []

# Fetch data from all pages
for page in range(1, 15):
    payload['page'] = page
    response = requests.post(url, headers=headers, data=payload)
    data = response.json()
    records = data["records"]
    df = pd.DataFrame(records)
    df = df[["player_name", "club_from_name", "club_to_name", "amount"]]
    all_transfers.append(df)

# Concatenate all transfer data into a single DataFrame
df = pd.concat(all_transfers)
df.columns = ["Player", "From", "To", "Price"]

# Read minute data CSV
df1 = pd.read_csv("result.csv")

# Filter players with more than 900 minutes
df1_filtered = df1[df1['Standard_Min'] > 900]

# Filter transfer list to keep only those players
df1_players = df1_filtered['Player'].tolist()
filtered_df = df[df['Player'].isin(df1_players)]

# Merge transfer data with minute data
result_df = pd.merge(filtered_df, df1_filtered[['Player', 'Standard_Min']], on='Player', how='left')
result_df = result_df[["Player", "From", "To", "Price","Standard_Min"]]

# Display result
print(result_df)
