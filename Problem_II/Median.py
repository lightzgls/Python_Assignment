import pandas as pd

df = pd.read_csv("result.csv")
criterias = df.columns[4:]

def make_header(criterias):
    res = [""]
    for criteria in criterias:
        res.extend([f"Median of {criteria}",f"Mean of {criteria}",f"Std of {criteria}"])
    return res



teams_name = set(df["Standard_Squad"])
teams_df = {}
for team in teams_name:
    new_df = pd.DataFrame(columns=df.columns)
    for index,row in df.iterrows():
        if row["Standard_Squad"] == team:
            new_df.loc[len(new_df)] = row
    teams_df[team] = new_df


header = make_header(criterias)
result_df = pd.DataFrame(columns=header)
row0 = ["all"]
for criteria in criterias:
    # Chuyển các giá trị "N/a" thành NaN, rồi tính median
    df[criteria] = pd.to_numeric(df[criteria], errors='coerce')

    median = df[criteria].median()
    mean = df[criteria].mean()
    std = df[criteria].std()
    row0.extend([median,mean,std])

result_df.loc[len(result_df)] = row0

for key, value in teams_df.items():
    row = [f"{key}"]
    for criteria in criterias:
        # Chuyển các giá trị "N/a" thành NaN, rồi tính median
        df[criteria] = pd.to_numeric(df[criteria], errors='coerce')

        
        median = df[criteria].median()
        mean = df[criteria].mean()
        std = df[criteria].std()
        row.extend([median,mean,std])
    result_df.loc[len(result_df)] = row

result_df.to_csv("result2.csv",index=True)
