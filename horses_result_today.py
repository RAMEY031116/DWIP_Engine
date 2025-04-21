import requests
from bs4 import BeautifulSoup

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
    all_races = soup.find_all('div', class_="rp-timeView__listItem")

    # 5. Prepare list to store selected race info
    selected_races = []

    # 6. Loop through each race and filter
    for race in all_races:
        text = race.get_text(" ", strip=True)

        # Include only Class 1, 2, or 3, and exclude (Class 1) style
        if ("Class 1" in text and "(Class 1)" not in text) or \
           ("Class 2" in text and "(Class 2)" not in text) or \
           ("Class 3" in text and "(Class 3)" not in text):
            selected_races.append(text)

    # 7. Save to CSV file manually
    if selected_races:
        file_name = f"class_1_to_3_races_{date}.csv"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("Race Info\n")  # CSV header
            for race_info in selected_races:
                f.write(f"\"{race_info}\"\n")  # Write each race in quotes

        print(f"✅ Saved {len(selected_races)} races to {file_name}")
    else:
        print("⚠️ No Class 1, 2 or 3 races found.")

else:
    print("❌ Failed to fetch the page.")




