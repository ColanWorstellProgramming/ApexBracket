#!/usr/bin/env python3
import pandas as pd
import requests

url = "https://liquipedia.net/apexlegends/Apex_Legends_Global_Series/2023/Split_1/Playoffs/Statistics"
response = requests.get(url)

dfs = pd.read_html(response.content)

table = dfs[6]
table = table.replace('-', '')

table.to_csv('apex.csv', index=False)

# Table Scanner
#for i, table in enumerate(dfs):
#    print(f"Table {i + 1}:")
#    print(table)
#    print()
