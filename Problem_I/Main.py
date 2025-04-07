import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from ultils import rename_duplicates
import csv
# Set up Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without GUI
options.add_argument("--disable-gpu")  # Required for some systems
options.add_argument("--no-sandbox")  # Helps avoid permission errors in Linux
options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues

# Create the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Links and id to scrape
links = {
    "https://fbref.com/en/comps/9/stats/Premier-League-Stats#all_stats_standard": "stats_standard",
    "https://fbref.com/en/comps/9/keepers/Premier-League-Stats#all_stats_keeper": "stats_keeper",
    "https://fbref.com/en/comps/9/shooting/Premier-League-Stats#all_stats_shooting": "stats_shooting",
    "https://fbref.com/en/comps/9/passing/Premier-League-Stats#all_stats_passing": "stats_passing",
    "https://fbref.com/en/comps/9/gca/Premier-League-Stats#all_stats_gca": "stats_gca",
    "https://fbref.com/en/comps/9/defense/Premier-League-Stats#all_stats_defense": "stats_defense",
    "https://fbref.com/en/comps/9/possession/Premier-League-Stats#all_stats_possession": "stats_possession",
    "https://fbref.com/en/comps/9/misc/Premier-League-Stats#all_stats_misc": "stats_misc"
}

# Scrape tables
tables = {}
for link, id in links.items():
    driver.get(link)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    table = soup.find("table", id=id)
    if table is None:
        print(f"Table with id '{id}' not found.")
        continue

    table_data = [] #initialize an array to store each table

    rows = table.find_all("tr") #extract all the row in the table 
    for row_idx, row in enumerate(rows):
        cells = row.find_all(["th", "td"]) #extract all the cells in the table
        row_data = [cell.get_text(strip=True) for cell in cells] #Format all the data in each cell to string and strip excess space
        if row_idx == 0 or row_data[1] == "Rk": #skip the duplicate header and the first header
            continue
        else:
            if row_data:
                table_data.append(row_data[1:]) #add the row to the current 2d array, skip the ranking

    tables[id] = table_data
    print(f"Fetched table {id}")



stats_standard = pd.DataFrame(columns=tables["stats_standard"][0])


min_index = tables["stats_standard"][0].index("Min")
age_index = tables['stats_standard'][0].index("Age")



tables["stats_standard"].sort(key = lambda row: (row[0].split()[0]))



for row in tables["stats_standard"]:
    min_played = row[min_index].replace(",", "")
    str_age = row[age_index]
    def calc_age(str_age):
        year = int(str_age.split("-")[0])
        day = int(str_age.split("-")[1])
        return round(year+(day/365),2)
    if min_played.isdigit() and int(min_played) > 90:
        row[min_index] = int(min_played)
        row[age_index] = calc_age(str_age)
        stats_standard.loc[len(stats_standard)] = row


# Read dataframes directly from the scraped tables
standard_df = stats_standard
goalkeep_df = pd.DataFrame(tables["stats_keeper"][1:], columns=tables["stats_keeper"][0])
shooting_df = pd.DataFrame(tables["stats_shooting"][1:], columns=tables["stats_shooting"][0])
passing_df = pd.DataFrame(tables["stats_passing"][1:], columns=tables["stats_passing"][0])
GCA_df = pd.DataFrame(tables["stats_gca"][1:], columns=tables["stats_gca"][0])
defense_df = pd.DataFrame(tables["stats_defense"][1:], columns=tables["stats_defense"][0])
possession_df = pd.DataFrame(tables["stats_possession"][1:], columns=tables["stats_possession"][0])
misc_df = pd.DataFrame(tables["stats_misc"][1:], columns=tables["stats_misc"][0])


DFs = [standard_df, goalkeep_df, shooting_df, passing_df, GCA_df, defense_df, possession_df, misc_df]





standard_df.columns = [f"Standard_{col}" if col != "Player" else col for col in standard_df.columns]
goalkeep_df.columns = [f"Goalkeeping_{col}" if col != "Player" else col for col in goalkeep_df.columns]
shooting_df.columns = [f"Shooting_{col}" if col != "Player" else col for col in shooting_df.columns]
passing_df.columns = [f"Passing_{col}" if col != "Player" else col for col in passing_df.columns]
GCA_df.columns = [f"GCA_{col}" if col != "Player" else col for col in GCA_df.columns]
defense_df.columns = [f"Defense_{col}" if col != "Player" else col for col in defense_df.columns]
possession_df.columns = [f"Possession_{col}" if col != "Player" else col for col in possession_df.columns]
misc_df.columns = [f"Misc_{col}" if col != "Player" else col for col in misc_df.columns]


#go through every df and rename the columns
for df in DFs:
    df.columns = rename_duplicates(df.columns)

#list all the stat need to find
header = ['Player', 'Standard_Nation', 'Standard_Pos', 'Standard_Squad',
'Standard_Age','Standard_MP', 'Standard_Starts','Standard_Min',
'Standard_Gls', 'Standard_Ast','Standard_CrdY', 'Standard_CrdR',
'Standard_xG','Standard_xAG','Standard_PrgC', 'Standard_PrgP',
'Standard_PrgR','Standard_Gls_1', 'Standard_Ast_1','Standard_xG_1', 'Standard_xAG_1',
'Goalkeeping_GA90','Goalkeeping_Save%','Goalkeeping_CS%','Goalkeeping_Save%_1',
'Shooting_SoT%','Shooting_SoT/90','Shooting_G/Sh','Shooting_Dist',
'Passing_Cmp','Passing_Cmp%','Passing_TotDist','Passing_Cmp%_1','Passing_Cmp%_2',
'Passing_Cmp%_3','Passing_KP', 'Passing_1/3', 'Passing_PPA',
'Passing_CrsPA', 'Passing_PrgP','GCA_SCA', 'GCA_SCA90','GCA_GCA', 'GCA_GCA90',
'Defense_Tkl','Defense_TklW','Defense_Att','Defense_Lost',
'Defense_Blocks', 'Defense_Sh', 'Defense_Pass', 'Defense_Int',
'Possession_Touches', 'Possession_Def Pen', 'Possession_Def 3rd',
'Possession_Mid 3rd', 'Possession_Att 3rd', 'Possession_Att Pen',
'Possession_Att','Possession_Succ%','Possession_Tkld%',
'Possession_Carries', 'Possession_TotDist', 'Possession_PrgDist',
'Possession_PrgC', 'Possession_1/3', 'Possession_CPA', 'Possession_Mis',
'Possession_Dis','Possession_Rec', 'Possession_PrgR',
'Misc_Fls', 'Misc_Fld', 'Misc_Off', 'Misc_Crs','Misc_Recov',
'Misc_Won','Misc_Lost', 'Misc_Won%']

# Initialize the resulting DataFrame
result_df = pd.DataFrame(columns=header)

# Create a dictionary for quick lookup of DataFrames by player
player_data_dict = {}
for file in DFs:
    if "Player" in file.columns:
        for _, row in file.iterrows():
            player = row["Player"]
            if player not in player_data_dict:
                player_data_dict[player] = {}
            for col in file.columns:
                if pd.notna(row[col]) and str(row[col]).strip() != "":
                    player_data_dict[player][col] = row[col]

# Iterate through each player in Player_df and populate result_df
for _, row in standard_df.iterrows():
    player = row["Player"]
    player_data = {col: "N/a" for col in header}
    
    # Add data from Player_df itself
    for col in standard_df.columns:
        if col in header and pd.notna(row[col]) and str(row[col]).strip() != "":
            player_data[col] = row[col]
    
    # Add data from other DataFrames using the dictionary
    if player in player_data_dict:
        for col in header:
            if col in player_data_dict[player]:
                player_data[col] = player_data_dict[player][col]
    
    # Append the player's data to result_df
    result_df.loc[len(result_df)] = player_data

newheader = ['Player', 'Standard_Nation', 'Standard_Pos', 'Standard_Squad',
'Standard_Age','Standard_MP', 'Standard_Starts','Standard_Min',
'Standard_Gls', 'Standard_Ast','Standard_CrdY', 'Standard_CrdR',
'Standard_xG','Standard_xAG','Standard_PrgC', 'Standard_PrgP',
'Standard_PrgR','Standard_Gls/90', 'Standard_Ast/90','Standard_xG/90', 'Standard_xAG/90',
'Goalkeeping_GA90','Goalkeeping_Save%','Goalkeeping_CS%','Goalkeeping_Penalty_Save%',
'Shooting_SoT%','Shooting_SoT/90','Shooting_G/Sh','Shooting_Dist',
'Passing_Cmp','Passing_Total_Cmp%','Passing_TotDist','Passing_Short_Cmp%','Passing_Medium_Cmp%',
'Passing_Long_Cmp%','Passing_KP', 'Passing_1/3', 'Passing_PPA',
'Passing_CrsPA', 'Passing_PrgP','GCA_SCA', 'GCA_SCA90','GCA_GCA', 'GCA_GCA90',
'Defense_Tkl','Defense_TklW','Defense_Att','Defense_Lost',
'Defense_Blocks', 'Defense_Sh', 'Defense_Pass', 'Defense_Int',
'Possession_Touches', 'Possession_Def Pen', 'Possession_Def 3rd',
'Possession_Mid 3rd', 'Possession_Att 3rd', 'Possession_Att Pen',
'Possession_Att','Possession_Succ%','Possession_Tkld%',
'Possession_Carries', 'Possession_TotDist', 'Possession_PrgDist',
'Possession_PrgC', 'Possession_1/3', 'Possession_CPA', 'Possession_Mis',
'Possession_Dis','Possession_Rec', 'Possession_PrgR',
'Misc_Fls', 'Misc_Fld', 'Misc_Off', 'Misc_Crs','Misc_Recov',
'Misc_Won','Misc_Lost', 'Misc_Won%']

# Read and modify the CSV file
result_df.columns = newheader[:len(result_df.columns)] 

# Save the resulting DataFrame to a CSV file
result_df.to_csv("result.csv", index=False)




# Close the WebDriver
driver.quit()
