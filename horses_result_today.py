# import requests
# from bs4 import BeautifulSoup

# # Step 1: Define the URL
# url = "https://www.racingpost.com/results/2025-04-20/time-order/"

# # Step 2: Send a request
# response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# # Step 3: If successful
# if response.status_code == 200:
#     print("Page fetched successfully!")

#     # Step 4: Parse the HTML
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Step 5: Find race sections (lighter class name)
#     race_sections = soup.find_all('div', class_="rp-timeView__list")

#     # Step 6: Write results to text file
#     with open("result_today.csv", "w", encoding="utf-8") as f:
#         for section in race_sections:
#             # Write cleaner plain text with line breaks
#             text = section.get_text(separator="\n", strip=True)
#             f.write(text)  # Add spacing between sections
                
# else:
#     print("Failed to fetch page.")


# import requests
# from bs4 import BeautifulSoup

# # 1. Set the date and URL
# date = "2025-04-20"
# url = f"https://www.racingpost.com/results/{date}/time-order/"

# # 2. Get the page
# response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# # 3. Check if the page loaded
# if response.status_code == 200:
#     print("✅ Page fetched successfully!")

#     soup = BeautifulSoup(response.text, "html.parser")

#     # 4. Find all race sections
#     all_races = soup.find_all('div', class_="rp-timeView__listItem")

#     # 5. Prepare list to store selected race info
#     selected_races = []

#     # 6. Loop through each race and filter
#     for race in all_races:
#         text = race.get_text(" ", strip=True)

#         # Include only Class 1, 2, or 3, and exclude (Class 1) style
#         if ("Class 1" in text and "(Class 1)" not in text) or \
#            ("Class 2" in text and "(Class 2)" not in text) or \
#            ("Class 3" in text and "(Class 3)" not in text):
#             selected_races.append(text)

#     # 7. Save to CSV file manually
#     if selected_races:
#         file_name = f"class_1_to_3_races_{date}.csv"
#         with open(file_name, "w", encoding="utf-8") as f:
#             f.write("Race Info\n")  # CSV header
#             for race_info in selected_races:
#                 f.write(f"\"{race_info}\"\n")  # Write each race in quotes

#         print(f"✅ Saved {len(selected_races)} races to {file_name}")
#     else:
#         print("⚠️ No Class 1, 2 or 3 races found.")

# else:
#     print("❌ Failed to fetch the page.")


import requests
from bs4 import BeautifulSoup
import csv

# Set the date and build the URL
date = "2025-04-20"
url = f"https://www.racingpost.com/results/{date}/time-order/"

# Get the webpage
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

if response.status_code == 200:
    print("✅ Page fetched!")

    soup = BeautifulSoup(response.text, "html.parser")

    all_races = soup.find_all('div', class_="rp-timeView__listItem")

    # Prepare CSV
    file_name = f"races_clean_{date}.csv"
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Horse Name", "Race Meeting", "Class", "Position"])  # Header

        # Loop through each race block
        for race in all_races:
            text = race.get_text(" ", strip=True)

            # Only include Class 1–3 and not (Class X)
            if ("Class 1" in text and "(Class 1)" not in text) or \
               ("Class 2" in text and "(Class 2)" not in text) or \
               ("Class 3" in text and "(Class 3)" not in text):

                # Extract class
                if "Class 1" in text:
                    race_class = "Class 1"
                elif "Class 2" in text:
                    race_class = "Class 2"
                else:
                    race_class = "Class 3"

                # Extract meeting (e.g., "Plumpton", "Bath")
                try:
                    meeting = text.split(" ")[1]
                except:
                    meeting = "Unknown"

                # Get each line (each horse starts on a new line usually)
                lines = text.split(".")  # We'll use '.' to find end of each horse line

                for line in lines:
                    line = line.strip()
                    parts = line.split()

                    if len(parts) >= 2:
                        last_part = parts[-1]
                        if last_part.isdigit():
                            position = last_part
                            horse_name = " ".join(parts[:-1])
                            writer.writerow([horse_name, meeting, race_class, position])

    print(f"✅ Results saved to {file_name}")

else:
    print("❌ Failed to load the page")


