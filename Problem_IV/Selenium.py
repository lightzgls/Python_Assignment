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

for i in range(1, 15):
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
        # Extract row data
        for cell in cells:
            cell_classes = cell.get("class") or []
            if "td-player" in cell_classes:
                span = cell.find("span")
                if span:
                    row_data.append(span.get_text(strip=True))
                else:
                    row_data.append("")  # fallback in case <span> doesn't exist
            else:
                a_tags = cell.find_all("a")
                if len(a_tags) == 2:
                    title_lst = [a["title"] for a in a_tags if a.has_attr("title")]
                    from_squad, to_squad = title_lst if len(title_lst) == 2 else ("", "")
                    row_data.append(from_squad + "/" + to_squad)
                else:
                    row_data.append(cell.get_text(strip=True))
                # Ensure row_data matches the number of headers
        table_data.append(row_data)

# Convert table data to a DataFrame
df = pd.DataFrame(table_data[1:],columns=table_data[0])
# Read the player CSV
player_df = pd.read_csv("result.csv")

df.to_csv("900Min.csv")

# Filter players with more than 900 minutes
player_df_filtered = player_df[player_df['Standard_Min'] > 900]

# Filter transfer list to keep only those players
players = player_df_filtered['Player'].tolist()
filtered_df = df[df['Player'].isin(players)]

# Merge transfer data with minute data
result_df = pd.merge(filtered_df, player_df_filtered[['Player', 'Standard_Min']], on='Player', how='left')
# Print the resulting dataframe
print(result_df)
result_df.to_csv("Prob4.csv")