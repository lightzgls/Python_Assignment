import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
from ultils import rename_duplicates

# # Set up Chrome options for headless mode
# options = webdriver.ChromeOptions()
# # options.add_argument("--headless")  # Run without GUI
# options.add_argument("--disable-gpu")  # Required for some systems
# options.add_argument("--no-sandbox")  # Helps avoid permission errors in Linux
# options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
# options.add_argument("--ignore-certificate-errors")  # Ignore SSL certificate errors
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--disable-webgl")  # Disable WebGL to avoid warnings
# options.add_argument("--log-level=3")  # Suppress all logs except fatal errors
# # options.add_argument("user-data-dir=/path/to/your/chrome/profile")

# # Create the WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=options)



# Setup undetected Chrome
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")  # Suppress all logs except fatal errors
# options.add_argument("--headless")  # Optional, but not recommended if CAPTCHA needs to be solved manually

driver = uc.Chrome(options=options)

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
    time.sleep(20)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    #find the table by the tag name
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

# Close the WebDriver
driver.quit()

# Read dataframes directly from the scraped tables
standard_df = pd.DataFrame(tables["stats_standard"][1:], columns=tables["stats_standard"][0])
goalkeep_df = pd.DataFrame(tables["stats_keeper"][1:], columns=tables["stats_keeper"][0])
shooting_df = pd.DataFrame(tables["stats_shooting"][1:], columns=tables["stats_shooting"][0])
passing_df = pd.DataFrame(tables["stats_passing"][1:], columns=tables["stats_passing"][0])
GCA_df = pd.DataFrame(tables["stats_gca"][1:], columns=tables["stats_gca"][0])
defense_df = pd.DataFrame(tables["stats_defense"][1:], columns=tables["stats_defense"][0])
possession_df = pd.DataFrame(tables["stats_possession"][1:], columns=tables["stats_possession"][0])
misc_df = pd.DataFrame(tables["stats_misc"][1:], columns=tables["stats_misc"][0])


#reformat Min and Age to int and float
standard_df["Min"] = pd.to_numeric(standard_df["Min"].str.replace(",",""), errors= "coerce")
standard_df['Age'] = standard_df['Age'].apply(lambda x: round((int(x.split('-')[0]) + int(x.split('-')[1]) / 365),2) if isinstance(x, str) and '-' in x else pd.NA)
standard_df = standard_df[standard_df["Min"] > 90] 



DFs = [standard_df, goalkeep_df, shooting_df, passing_df, GCA_df, defense_df, possession_df, misc_df]

#rename header of dataframes by adding prefix tableid
standard_df.columns = list(standard_df.columns[:4]) + [f"Standard_{col}" for col in standard_df.columns[4:]]
goalkeep_df.columns = list(goalkeep_df.columns[:4]) + [f"Goalkeeping_{col}" for col in goalkeep_df.columns[4:]]
shooting_df.columns = list(shooting_df.columns[:4]) + [f"Shooting_{col}" for col in shooting_df.columns[4:]]
passing_df.columns = list(passing_df.columns[:4]) + [f"Passing_{col}" for col in passing_df.columns[4:]]
GCA_df.columns = list(GCA_df.columns[:4]) + [f"GCA_{col}" for col in GCA_df.columns[4:]]
defense_df.columns = list(defense_df.columns[:4]) + [f"Defense_{col}" for col in defense_df.columns[4:]]
possession_df.columns = list(possession_df.columns[:4]) + [f"Possession_{col}" for col in possession_df.columns[4:]]
misc_df.columns = list(misc_df.columns[:4]) + [f"Misc_{col}" for col in misc_df.columns[4:]]


#go through every df and rename the columns
for df in DFs:
    df.columns = rename_duplicates(df.columns)

#list all the stat need to find
result_header = ['Player', 'Nation', 'Pos', 'Squad',
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
'Possession_Carries', 'Possession_PrgDist',
'Possession_PrgC', 'Possession_1/3', 'Possession_CPA', 'Possession_Mis',
'Possession_Dis','Possession_Rec', 'Possession_PrgR',
'Misc_Fls', 'Misc_Fld', 'Misc_Off', 'Misc_Crs','Misc_Recov',
'Misc_Won','Misc_Lost', 'Misc_Won%']


# Initialize the resulting DataFrame
result_df = standard_df
for df in DFs[1:]:
    result_df = pd.merge(result_df, df, how="left", on=["Player", "Nation", "Pos", "Squad"])
# result_df.to_csv("Unfiltered_stats.csv")
#keep the columns listed in result_header
result_df = result_df[result_header]


#list all the header to rename
newheader = ['Player', 'Nation', 'Pos', 'Team','Age',
             
'Standard_MP', 'Standard_Starts','Standard_Min',

'Standard_Gls', 'Standard_Ast','Standard_CrdY', 'Standard_CrdR',

'Standard_xG','Standard_xAG','Standard_PrgC', 'Standard_PrgP',
'Standard_PrgR',

'Standard_Gls/90', 'Standard_Ast/90','Standard_xG/90', 'Standard_xAG/90',

'Goalkeeping_GA90','Goalkeeping_Save%','Goalkeeping_CS%','Goalkeeping_Penalty_Save%',

'Shooting_SoT%','Shooting_SoT/90','Shooting_G/Sh','Shooting_Dist',

'Passing_Cmp','Passing_Total_Cmp%','Passing_TotDist','Passing_Short_Cmp%','Passing_Medium_Cmp%',
'Passing_Long_Cmp%','Passing_KP', 'Passing_1/3', 'Passing_PPA',
'Passing_CrsPA', 'Passing_PrgP',

'GCA_SCA', 'GCA_SCA90','GCA_GCA', 'GCA_GCA90',

'Defense_Tkl','Defense_TklW','Defense_Att','Defense_Lost',
'Defense_Blocks', 'Defense_Sh', 'Defense_Pass', 'Defense_Int',

'Possession_Touches', 'Possession_Def Pen', 'Possession_Def 3rd',
'Possession_Mid 3rd', 'Possession_Att 3rd', 'Possession_Att Pen',
'Possession_Att','Possession_Succ%','Possession_Tkld%',
'Possession_Carries', 'Possession_PrgDist',
'Possession_PrgC', 'Possession_1/3', 'Possession_CPA', 'Possession_Mis',
'Possession_Dis','Possession_Rec', 'Possession_PrgR',

'Misc_Fls', 'Misc_Fld', 'Misc_Off', 'Misc_Crs','Misc_Recov',
'Misc_Won','Misc_Lost', 'Misc_Won%']


#fill missing value with "N/a"
pd.set_option('future.no_silent_downcasting', True)
result_df = result_df.replace("","N/a").fillna("N/a")
#sort player base on their first name

result_df = result_df.sort_values(by="Player")
result_df["Nation"] = result_df["Nation"].apply(lambda nation: ''.join([c for c in nation if c.isupper()]))

#rename the header
result_df.columns = newheader[:len(newheader)]

# Save the resulting DataFrame to a CSV file
result_df.to_csv("source code\\results.csv", index=False)
