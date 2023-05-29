#!/usr/bin/env python3
import pandas as pd
import requests

url = "https://liquipedia.net/apexlegends/Apex_Legends_Global_Series/2023/Split_1/Playoffs/Statistics"
url2 = "https://apex.tracker.gg/apex/leaderboards/stats/all/RankScore?country=us&page=1"
response = requests.get(url2)

dfs = pd.read_html(response.content)

# table = dfs[6]
# table = table.replace('-', '')

# table.to_csv('nb.csv', index=False)

# Table Scanner
for i, table in enumerate(dfs):
    print(f"Table {i + 1}:")
    print(table)
    print()
