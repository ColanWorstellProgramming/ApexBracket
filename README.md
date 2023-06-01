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
pip install scikit-learn


To Scrape |$ ./htmlScrape.py



Results:

Neural Network:
    Test Loss: -8155.3427734375
    Test Accuracy: 0.0

Data Tree Model:
    Test Accuracy: 0.06428571428571428

Random Forest Model:
    Test Accuracy: 0.014285714285714285

Support Vector Machines Model:
    Test Accuracy: 0.0

Naive Bayes Model:
    Test Accuracy: 0.0

K-nearest Neighbors Model:
    Test Accuracy: 0.0


Conclusion | The 2100.csv Dataset has too many missing values. We need to re-evaluate our datapoints.