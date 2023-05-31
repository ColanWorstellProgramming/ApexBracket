#!/usr/bin/env python3
import requests

base_url = "https://public-api.tracker.gg/v2/apex/"
endpoint = "leaderboards/legend/{platform}/{legend}?limit=10000"
platform = "steam"
legend = "pathfinder"
api_key = "ed26b035-5bb8-4d15-9733-7e607c3848df"

url = base_url + endpoint.format(platform=platform, legend=legend)
headers = {"TRN-Api-Key": api_key}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    with open('api.txt', 'w') as file:
        file.write(str("Status Code: {}\n\n".format(response.status_code)))
        file.write(str(data))

    print("Response content saved to 'api.txt' file.")
else:
    print("Error:", response.status_code)