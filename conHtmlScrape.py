#!/usr/bin/env python3
import pandas as pd
import requests
import time
import numpy as np
import concurrent.futures

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
pages = 10
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
    print(f"Failed to retrieve data for {url}. Skipping all pages for this URL.")
    return None

for stat, url in urls.items():
    dataframes[stat] = pd.DataFrame()

def process_page(page):
    global requests_made
    print(f"Collecting data from page {page}/{pages}...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for stat, url in urls.items():
            if url in dataframes[stat].columns:
                continue  # Skip the URL if already fetched

            print(f" - Collecting data for {stat}...")
            table = None
            url_failed = False

            while table is None:
                if requests_made < requests_per_interval:
                    requests_made += 1
                    futures.append(executor.submit(fetch_data, f"{url}?page={page}&country={country}"))
                else:
                    print("Reached request limit for current interval. Waiting...")
                    time.sleep(interval)
                    requests_made = 0
                    total_time_waited += interval

                if total_time_waited >= interval:
                    total_time_waited = 0
                    break

        for future in concurrent.futures.as_completed(futures):
            table = future.result()
            if table is not None:
                stat = table.columns[0]
                table.columns = table.columns.droplevel(0)
                table = table.replace([-np.inf, np.inf], np.nan)
                dataframes[stat] = pd.concat([dataframes[stat], table])

    time.sleep(request_delay)

for page in range(1, pages + 1):
    process_page(page)

print("Merging dataframes...")
merged_df = dataframes["RankScore"]
for stat in dataframes.keys():
    if stat != "RankScore":
        if 'Player' in merged_df.columns and 'Player' in dataframes[stat].columns:
            merged_df = merged_df.merge(dataframes[stat], on="Player", how="left")

# Convert float columns to nullable integers
for stat in dataframes.keys():
    if stat != "RankScore" and stat in merged_df.columns:
        if stat == "Kills":
            merged_df[stat] = merged_df[stat].replace(np.nan, pd.NA).astype("Int64")
        else:
            merged_df[stat] = merged_df[stat].fillna(pd.NA).astype("Int64")

print("Writing merged dataframe to file...")
merged_df.to_csv(output_file, index=False)

end_time = time.time()
execution_time = end_time - start_time
print(f"Data collection and merging completed in {execution_time:.2f} seconds.")
