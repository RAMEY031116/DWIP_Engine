import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

# File name to store the race results
csv_file = "Horse_results.csv"

# Get previous results from the file to avoid duplicates
existing_entries = set()

try:
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            existing_entries.add(tuple(row))
except FileNotFoundError:
    pass  # File doesn't exist yet, will be created later

# Loop through the last 20 days
for days_ago in range(20):
    date_str = (datetime.today() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    url = f"https://www.racingpost.com/results/{date_str}/time-order"

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        race_container = soup.find("div", class_="rp-timeView__list")

        if race_container:
            race_sections = race_container.find_all("div", class_="rp-timeView__listItem")
            race_data_list = []

            for race in race_sections:
                meeting_name = race.find("div", class_="rp-timeView__raceName")
                race_description = race.find("p", class_="rp-timeView__raceDescription")
                horses = race.find_all("li", class_="rp-raceResult__horse")

                if meeting_name and race_description and horses:
                    description_text = race_description.get_text(strip=True)
                    distance = description_text.split(",")[0]  # First part contains distance
                    class_type = next((cls for cls in ["Class 1", "Class 2", "Class 3"] if cls in description_text), None)

                    if class_type:
                        # Get top 3 horses from each race
                        for horse in horses[:3]:
                            horse_name = horse.find("span", class_="rp-raceResult__horseName")
                            position = horse.get("data-outcome-desc")
                            odds = horse.find("span", class_="rp-raceResult__horsePrice")

                            if horse_name and position:
                                race_entry = (
                                    date_str,
                                    meeting_name.get_text(strip=True),
                                    class_type,
                                    distance,
                                    horse_name.get_text(strip=True),
                                    position.strip(),
                                    odds.get_text(strip=True) if odds else "N/A"
                                )

                                # Add only new entries
                                if race_entry not in existing_entries:
                                    race_data_list.append(race_entry)
                                    existing_entries.add(race_entry)

            # Save new race data to CSV
            if race_data_list:
                with open(csv_file, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)

                    # Write headers only if the file is empty
                    if file.tell() == 0:
                        writer.writerow(["Date", "Meeting Name", "Class", "Distance", "Horse Name", "Position", "Odds"])

                    writer.writerows(race_data_list)

                print(f"✅ Added data for {date_str}!")
            else:
                print(f"⚠️ No Class 1, 2, or 3 races found for {date_str}.")
    else:
        print(f"❌ Couldn't get data for {date_str}. Status code: {response.status_code}")

print("✅ Done fetching race results for the past 20 days!")