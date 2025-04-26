# # Import necessary libraries
# import requests  # To send requests to the webpage
# from bs4 import BeautifulSoup  # To parse the HTML content
# import csv  # To save the data into a CSV file

# # Step 1: Set the date and URL
# url = f"https://www.racingpost.com/fast-results/"

# # Step 2: Send a request to fetch the webpage content
# headers = {'User-Agent': 'Mozilla/5.0'}
# response = requests.get(url, headers=headers)

# # Step 3: Check if the request was successful
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Step 4: Locate the race container
#     race_container = soup.find("div", class_="rp-timeView__list")

#     # Step 5: Prepare list to store race details
#     race_data_list = []

#     if race_container:
#         race_sections = race_container.find_all("div", class_="rp-timeView__listItem")

#         for race in race_sections:
#             meeting_name = race.find("div", class_="rp-timeView__raceName")
#             race_description = race.find("p", class_="rp-timeView__raceDescription")
#             horses = race.find_all("li", class_="rp-raceResult__horse")

#             if meeting_name and race_description and horses:
#                 # Extract class type & distance
#                 description_text = race_description.get_text(strip=True)
#                 distance = description_text.split(",")[0]  # Extract distance (first part)
#                 class_type = None

#                 # Check for Class 1, 2, or 3 in description
#                 for cls in ["Class 1", "Class 2", "Class 3"]:
#                     if cls in description_text:
#                         class_type = cls
#                         break  # Stop checking once we find a matching class

#                 if class_type:
#                     # Extract horse results (only top 3)
#                     for horse in horses[:3]:  # Limit to 1st, 2nd, 3rd places
#                         horse_name = horse.find("span", class_="rp-raceResult__horseName")
#                         position = horse.get("data-outcome-desc")  # Extract race position
#                         odds = horse.find("span", class_="rp-raceResult__horsePrice")

#                         if horse_name and position:
#                             race_data_list.append({
#                                 "Meeting Name": meeting_name.get_text(strip=True),
#                                 "Class": class_type,
#                                 "Distance": distance,
#                                 "Horse Name": horse_name.get_text(strip=True),
#                                 "Position": position.strip(),
#                                 "Odds": odds.get_text(strip=True) if odds else "N/A"  # Handle missing odds
#                             })

#     # Step 6: Save to CSV if race data was found
#     if race_data_list:
#         with open("Horse_today_result.csv", "w", newline="", encoding="utf-8") as file:
#             fieldnames = ["Meeting Name", "Class", "Distance", "Horse Name", "Position", "Odds"]
#             writer = csv.DictWriter(file, fieldnames=fieldnames)

#             writer.writeheader()
#             writer.writerows(race_data_list)

#         print("✅ Data successfully scraped and saved to Horse_today_result.csv")
#     else:
#         print("❌ No Class 1, 2, or 3 races found.")

# else:
#     print(f"❌ Failed to retrieve webpage. Status code: {response.status_code}")


# Import necessary libraries
import requests  # To send requests to the webpage
from bs4 import BeautifulSoup  # To parse the HTML content
import csv  # To save the data into a CSV file


def todays_results():
    # Step 1: Set the date and URL
    url = f"https://www.racingpost.com/fast-results/"

    # Step 2: Send a request to fetch the webpage content
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    # Step 3: Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 4: Locate the race container
        race_container = soup.find("div", class_="rp-timeView__list")

        # Step 5: Prepare list to store race details
        race_data_list = []

        if race_container:
            race_sections = race_container.find_all("div", class_="rp-timeView__listItem")

            for race in race_sections:
                meeting_name = race.find("div", class_="rp-timeView__raceName")
                race_description = race.find("p", class_="rp-timeView__raceDescription")
                horses = race.find_all("li", class_="rp-raceResult__horse")

                if meeting_name and race_description and horses:
                    # Extract class type & distance
                    description_text = race_description.get_text(strip=True)
                    distance = description_text.split(",")[0]  # Extract distance (first part)
                    class_type = None

                    # Check for Class 1, 2, or 3 in description
                    for cls in ["Class 1", "Class 2", "Class 3"]:
                        if cls in description_text:
                            class_type = cls
                            break  # Stop checking once we find a matching class

                    if class_type:
                        # Extract horse results (only top 3)
                        for horse in horses[:3]:  # Limit to 1st, 2nd, 3rd places
                            horse_name = horse.find("span", class_="rp-raceResult__horseName")
                            position = horse.get("data-outcome-desc")  # Extract race position
                            odds = horse.find("span", class_="rp-raceResult__horsePrice")

                            if horse_name and position:
                                race_data_list.append({
                                    "Meeting Name": meeting_name.get_text(strip=True),
                                    "Class": class_type,
                                    "Distance": distance,
                                    "Horse Name": horse_name.get_text(strip=True),
                                    "Position": position.strip(),
                                    "Odds": odds.get_text(strip=True) if odds else "N/A"  # Handle missing odds
                                })

        # Step 6: Save to CSV if race data was found
        if race_data_list:
            with open("Horse_today_result.csv", "w", newline="", encoding="utf-8") as file:
                fieldnames = ["Meeting Name", "Class", "Distance", "Horse Name", "Position", "Odds"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(race_data_list)

            print("✅ Data successfully scraped and saved to Horse_today_result.csv")
        else:
            print("❌ No Class 1, 2, or 3 races found.")

    else:
        print(f"❌ Failed to retrieve webpage. Status code: {response.status_code}")

todays_results()