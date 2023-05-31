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
output_file = "10k.csv"
request_delay = 2  # Delay between requests in seconds
requests_per_interval = 30  # Number of requests per interval
interval = 60  # Interval duration in seconds
max_attempts = 3  # Maximum number of retry attempts

dataframes = {}
total_time_waited = 0
requests_made = 0
start_time = time.time()

def fetch_data(url):
    attempts = 0
    while attempts < max_attempts:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                dfs = pd.read_html(response.content)
                if dfs:
                    return dfs[0]
            except ValueError as e:
                print(f"Error parsing HTML for URL: {url}")
        print(f"Retrying... Attempt {attempts + 1}")
        time.sleep(15)
        attempts += 1
    return None

for stat, url in urls.items():
    dataframes[stat] = pd.DataFrame()

for page in range(1, pages + 1):
    print(f"Collecting data from page {page}/{pages}...")

    for stat, url in urls.items():
        print(f" - Collecting data for {stat}...")
        table = None

        while table is None:
            if requests_made < requests_per_interval:
                table = fetch_data(f"{url}?country={country}&page={page}")

                if table is not None:
                    table = table.replace('-', '')
                    table = table.replace([np.inf, -np.inf], np.nan)

                    if page == 1:
                        dataframes[stat] = table
                    else:
                        duplicates = table[table.duplicated(subset='Player')]
                        if len(duplicates) > 0:
                            print(f"Skipping {len(duplicates)} duplicates on page {page} for {stat}.")
                        table = table.drop_duplicates(subset='Player')
                        dataframes[stat] = pd.concat([dataframes[stat], table], ignore_index=True)
                else:
                    print(f"Error retrieving data for {stat} on page {page}.")
                    break

            else:
                current_time = time.time()
                elapsed_time = current_time - start_time

                if elapsed_time < interval:
                    sleep_time = interval - elapsed_time
                    print(f"Waiting for {sleep_time:.2f} seconds to comply with rate limit...")
                    time.sleep(sleep_time)
                    start_time = time.time()  # Reset the start time after waiting
                    requests_made = 0  # Reset the requests made counter
                else:
                    start_time = current_time  # Start a new interval
                    requests_made = 0  # Reset the requests made counter

        requests_made += 1
        time.sleep(request_delay)  # Delay between requests

    # Merge all dataframes based on matching player name
    merged_df = dataframes["RankScore"]

    for stat in dataframes.keys():
        if stat != "RankScore" and "Player" in dataframes[stat].columns:
            temp_df = dataframes[stat][['Player', stat]]
            temp_df = temp_df.rename(columns={stat: f"{stat}_temp"})
            merged_df = merged_df.merge(temp_df, on='Player', how='left')

    # Drop the "Unnamed: 2" column if it exists
    merged_df = merged_df.drop("Unnamed: 2", axis=1, errors="ignore")

    # Convert float columns to nullable integers
    for stat in dataframes.keys():
        if stat != "RankScore":
            if stat == "Kills":
                merged_df[stat] = merged_df[f"{stat}_temp"].replace(np.nan, pd.NA).astype("Int64")
            else:
                merged_df[stat] = merged_df[f"{stat}_temp"].fillna(pd.NA).astype("Int64")
            merged_df = merged_df.drop(f"{stat}_temp", axis=1)

    merged_df.to_csv(output_file, index=False)
    current_time = time.time()
    page_time = current_time - start_time
    total_time_waited += page_time
    print(f"Completed page {page}/{pages} - Data saved to {output_file}")
    print(f"Page time: {page_time:.2f} seconds")
    print(f"Total time elapsed: {total_time_waited:.2f} seconds\n")

print(f"Total time taken: {total_time_waited:.2f} seconds")
