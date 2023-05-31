#!/usr/bin/env python3
import pandas as pd
import requests
import time
import asyncio
import aiohttp
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
output_file = "1000.csv"
request_delay = 2

dataframes = {}

for stat, url in urls.items():
    dataframes[stat] = pd.DataFrame()

total_time_waited = 0
start_time = time.time()

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def process_page(session, page):
    print(f"Collecting data from page {page}/{pages}...")

    tasks = []
    for stat, url in urls.items():
        print(f" - Collecting data for {stat}...")
        task = asyncio.create_task(fetch(session, f"{url}?country={country}&page={page}"))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    for response, (stat, url) in zip(responses, urls.items()):
        try:
            dfs = pd.read_html(response)
            if dfs:
                table = dfs[0]
                table = table.replace('-', '')
                table = table.replace([np.inf, -np.inf], np.nan)

                if page == 1:
                    dataframes[stat] = table
                else:
                    dataframes[stat] = pd.concat([dataframes[stat], table], ignore_index=True)
            else:
                print(f"No tables found for {stat} on page {page}")
        except ValueError:
            print(f"No tables found for {stat} on page {page}")

    end_time = time.time()
    time_taken = end_time - start_time
    global total_time_waited
    total_time_waited += time_taken
    print(f"Completed page {page}/{pages} - Data collected (Time taken: {time_taken:.2f} seconds)\n")

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[process_page(session, page) for page in range(1, pages+1)])

# Run the event loop
asyncio.run(main())

# Merge all dataframes based on matching player name
merged_df = dataframes["RankScore"]
for stat in dataframes.keys():
    if stat != "RankScore" and "Player" in dataframes[stat].columns:
        if stat in merged_df.columns:
            merged_df = merged_df.merge(dataframes[stat][['Player', stat]], on='Player', how='left')

# Drop the "Unnamed: 2" column if it exists
merged_df = merged_df.drop("Unnamed: 2", axis=1, errors="ignore")

# Convert float columns to integers
for stat in dataframes.keys():
    if stat != "RankScore":
        if stat in merged_df.columns:
            if stat == "Kills":
                merged_df[stat] = merged_df[stat].replace(np.nan, -1).astype(int)
            else:
                merged_df[stat] = merged_df[stat].fillna(-1).astype(int)

# Save the merged dataframe to the output file
merged_df.to_csv(output_file, index=False)

total_time = time.time() - start_time
print(f"Data saved to {output_file}")
print(f"Total time taken: {total_time:.2f} seconds")
print(f"Total time waited due to delay: {total_time_waited:.2f} seconds")
