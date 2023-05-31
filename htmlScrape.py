#!/usr/bin/env python3
import pandas as pd
import requests
import time
import numpy as np

urls = {
    "RankScore": "https://apex.tracker.gg/apex/leaderboards/stats/all/RankScore",
    "Kills": "https://apex.tracker.gg/apex/leaderboards/stats/all/Kills",
    "Season 17 Wins": "https://apex.tracker.gg/apex/leaderboards/stats/all/SeasonWins",
    "Winning Kills": "https://apex.tracker.gg/apex/leaderboards/stats/all/WinningKills",
    "Kills As Kill Leader": "https://apex.tracker.gg/apex/leaderboards/stats/all/KillsAsKillLeader",
    "Damage": "https://apex.tracker.gg/apex/leaderboards/stats/all/Damage",
    "Headshots": "https://apex.tracker.gg/apex/leaderboards/stats/all/Headshots",
    "Matches Played": "https://apex.tracker.gg/apex/leaderboards/stats/all/MatchesPlayed",
    "Times Top 3": "https://apex.tracker.gg/apex/leaderboards/stats/all/TimesPlacedtop3"
}

country = "us"
pages = 100
output_file = "html.csv"

dataframes = {}

for stat, url in urls.items():
    dataframes[stat] = pd.DataFrame()

for page in range(1, pages+1):
    start_time = time.time()
    print(f"Collecting data from page {page}/{pages}...")

    for stat, url in urls.items():
        print(f" - Collecting data for {stat}...")
        response = requests.get(f"{url}?country={country}&page={page}")

        if response.status_code == 200:
            dfs = pd.read_html(response.content)

            if dfs:
                table = dfs[0]
                table = table.replace('-', '')
                table = table.replace([np.inf, -np.inf], np.nan)

                if page == 1:
                    dataframes[stat] = table
                else:
                    dataframes[stat] = pd.concat([dataframes[stat], table], ignore_index=True)
        else:
            print(f"Error on page {page}: {stat} - {response.status_code}")
            break

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Completed page {page}/{pages} - Data collected (Time taken: {time_taken:.2f} seconds)\n")

# Merge all dataframes based on matching player name
merged_df = dataframes["RankScore"]

for stat in dataframes.keys():
    if stat != "RankScore" and "Player" in dataframes[stat].columns:
        merged_df = merged_df.merge(dataframes[stat][['Player', stat]], on='Player', how='left')

# Update the columns in merged_df
for stat in dataframes.keys():
    if stat != "RankScore":
        if stat == "Kills":
            merged_df[stat] = merged_df[stat].replace(np.nan, -1).astype(int)
        else:
            merged_df[stat] = merged_df[stat].fillna(-1)

# Save the merged dataframe to the output file
merged_df.to_csv(output_file, index=False)

print(f"Data saved to {output_file}")
