import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Ensure unique column names
def rename_duplicates(columns):
    seen = {}
    new_columns = []
    
    for col in columns:
        if col in seen:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_columns.append(col)
    
    return new_columns

#function to find all the needed table ids
def find_ids(links):
    # Set up Chrome options for headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without GUI
    options.add_argument("--disable-gpu")  # Required for some systems
    options.add_argument("--no-sandbox")  # Helps avoid permission errors in Linux
    options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues

# Create the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)


    tables_id = []
    for link in links:
        driver.get(link)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        tables = soup.find("table") #find all the table tag
        
        if tables is None:
            print("Found no table")
        else:
            for table in tables:
                id = table.get('id')
                if "squad" not in id:
                    tables_id.append(id)
    return tables_id