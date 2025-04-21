import requests
from bs4 import BeautifulSoup
import csv

# 1. Set the date and URL
date = "2025-04-20"
url = f"https://www.racingpost.com/results/{date}/time-order/"

# 2. Get the page
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# 3. Check if the page loaded
if response.status_code == 200:
    print("✅ Page fetched successfully!")

    soup = BeautifulSoup(response.text, "html.parser")

    # 4. Find all race sections
    listItem_races = soup.find_all("div", class_="rp-timeView_listItem")

    # 5. Prepare list to store selected race info
    selected_races = []

    # 6. Loop through each race and extract data
    for race in listItem_races:
        meeting = race.find("div", class_="timeView__raceName")
        race_class = race.find("span", class_="rp-timeView__raceDescription__distance")
        horse = race.find("span", class_="price")
        position = race.find("li", class_="rp-raceResult__horse")

        if meeting and race_class and horse and position:
            meeting_name = meeting.text.strip()
            horse_class_name = race_class.text.strip()
            horse_name = horse.text.strip()
            pos = position.text.strip()

            # ✅ Filtering inside the loop
            if (("Class 1" in horse_class_name and "(Class 1)" not in horse_class_name) or 
                ("Class 2" in horse_class_name and "(Class 2)" not in horse_class_name) or 
                ("Class 3" in horse_class_name and "(Class 3)" not in horse_class_name)):
                
                selected_races.append({
                    "Meeting Name": meeting_name,
                    "Class name": horse_class_name,
                    "Horse name": horse_name,
                    "Position": pos
                })

# 7. Write results to CSV
if selected_races:
    with open("Horse_today_result.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Meeting Name", "Class name", "Horse name", "Position"])
        writer.writeheader()
        writer.writerows(selected_races)
    print("✅ Results saved to Horse_today_result.csv")
else:
    print("❌ No races found that match the criteria.")
