import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Set up Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without GUI
options.add_argument("--disable-gpu")  # Required for some systems
options.add_argument("--no-sandbox")  # Helps avoid permission errors in Linux
options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-webgl")  # Disable WebGL to avoid warnings
options.add_argument("--log-level=3")  # Suppress all logs except fatal errors

# Create the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# The first page URL
base_url = "https://www.footballtransfers.com/us/transfers/confirmed/2024-2025/uk-premier-league"

# This table has 14 pages
lastpage = 14

# Initialize list for storing table data
table_data = []

for i in range(1, lastpage + 1):
    if i == 1:
        url = base_url
    else:
        url = f"{base_url}/{i}"

    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    table = soup.find("table")
    print(f"Read table from page {i}")
    if not table:
        print(f"[!] No table found on page {i}")
        continue

    # Extract rows from the table
    rows = table.find_all("tr") 
    for row_idx, row in enumerate(rows):
        cells = row.find_all(["th", "td"])
        row_data = []

        # Extract headers only once
        if i == 1 and row_idx == 0:
            headers = [cell.get_text(strip=True) for cell in cells]
            table_data.append(headers)
            continue

        # Extract row data
        for cell in cells:
            a_tags = cell.find_all("a")
            if len(a_tags) == 2:
                title_lst = [a["title"] for a in a_tags if a.has_attr("title")]
                from_squad, to_squad = title_lst
                row_data.append(from_squad + "/" + to_squad)
            elif len(a_tags) == 1:
                row_data.append(a_tags[0]["title"] if a_tags[0].has_attr("title") else cell.get_text(strip=True))
            else:
                row_data.append(cell.get_text(strip=True))

        # Ensure row_data matches the number of headers
        if len(row_data) == len(table_data[0]):
            table_data.append(row_data)

# Convert table data to a DataFrame
df = pd.DataFrame(columns=table_data[0])

# Read the player CSV
player_df = pd.read_csv("result.csv")

# Filter table data by checking if the player is in the CSV file
for row in table_data[1:]:
    if len(row) == len(df.columns):
        player_name = row[0]
        if player_name in player_df["Player"].values:
            filtered = player_df.loc[player_df["Player"] == player_name, "Standard_Min"]
            if not filtered.empty and len(filtered) == 1:
                played_time = filtered.values[0]
                if int(played_time) > 900:
                    df.loc[len(df)] = row

# Print the resulting dataframe
print(df)
