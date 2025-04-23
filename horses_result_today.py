import requests
from bs4 import BeautifulSoup
import csv

# 1. Set the date and URL
url = f"https://www.racingpost.com/results/2025-04-20/time-order/"

# 2. Get the page
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# 3. Check if the page loaded
if response.status_code == 200:
    print("✅ Page fetched successfully!")

    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Find all race sections
    listItem_races = soup.find_all("div", class_="rp-timeView_listItem")

    # 5. Filter for Class 5
    for race in listItem_races:
        try:
            race_description = race.find("div", class_="rp-timeView__raceDescription").text
            if "Class 5" in race_description:
                print("✅ Found Class 5 Race")
                print(race_description)
        except AttributeError:
            continue
