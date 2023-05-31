ML Model To Predict Future Apex Legends Brackets.

We start by grabbing X amount of datapoints from the Base Data Source via web-scraping html
using requests. Then we processes it with various models.

Our webscraping file sorts through wanted variables and attributes for each player seperately
then combines it all into html.csv, -1 being a non-found value. The greater the datapoint
search the more information each datapoint will have increasing the value of the actual data.

We are testing / validating 80%/20% to predict the rank of each player / team of players based
on test data grabbed from Apex Legends live servers

Base Data Source : https://apex.tracker.gg/apex/leaderboards/stats/all/RankScore?country=us&page=1


Dev Stuff:

Required Installations

pip install pandas
pip install requests
pip install tensorflow
pip install keras
pip install aiohttp

To Scrape |$ ./htmlScrape.py
