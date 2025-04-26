import pandas as pd

#generate all the header need for the DataFrame
def make_header(criterias):
    res = [""]
    for criteria in criterias:
        res.extend([f"Median of {criteria}",f"Mean of {criteria}",f"Std of {criteria}"])
    return res


df = pd.read_csv("results.csv")
criterias = df.columns[4:]

    
#initialize DataFrame
header = make_header(criterias)
result_df = pd.DataFrame(columns=header)


#process the first row
row0 = ["all"]
for criteria in criterias:
    # Change all the "N/a" to NaN
    df[criteria] = pd.to_numeric(df[criteria], errors='coerce')


    #calculate all the required value
    median = round(df[criteria].median(),2)
    mean = round(df[criteria].mean(),2)
    std = round(df[criteria].std(),2)
    
    row0.extend([median,mean,std])

#add the first row to DataFrame
result_df.loc[len(result_df)] = row0

# Group rows by 'Standard_Squad' and assign them to the corresponding team's DataFrame
grouped = df.groupby("Team")
for team, group in grouped:
    row = [team]
    for criteria in criterias:
        #reformat all data to number, and skip NaN
        numeric_column = pd.to_numeric(group[criteria], errors="coerce")

        row.extend([round(numeric_column.median(),2), round(numeric_column.mean(),2), round(numeric_column.std(),2)])
    result_df.loc[len(result_df)] = row

#fill missing value with "N/a"
result_df = result_df.replace("","N/a").fillna("N/a")

#convert Dataframe to csv file
result_df.to_csv("results2.csv",index=True)
