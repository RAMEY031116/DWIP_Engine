# # Import necessary libraries
# import requests  # To send requests to the webpage
# from bs4 import BeautifulSoup  # To parse the HTML content
# import csv  # To save the data into a CSV file

# # Step 1: Set the URL of the webpage from which we want to scrape data
# url = 'https://www.racingpost.com/racecards/runners-index'

# # Step 2: Send a request to the URL and get the webpage content
# # We also add a 'User-Agent' header to make the request look like it's from a browser
# response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# # Step 3: Check if the request was successful
# # If the status code is 200, it means the webpage was fetched correctly
# if response.status_code == 200:

#     # Step 4: Parse the webpage content (HTML) using BeautifulSoup
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Step 5: Create a list to store the data we will scrape
#     data = []

#     # Step 6: Find all sections that contain race information
#     # In this case, each section has a specific class name that we use to find it
#     race_sections = soup.find_all('div', class_='RC-alphabetIndexPanes js-diffusionTopicSettingsRace')

#     # Step 7: Loop through each race section to extract the relevant information
#     for race in race_sections:

#         # Step 8: Extract the race date from the section (it’s stored in a custom attribute)
#         race_date = race.get('data-diffusion-racedate', 'Unknown Date')

#         # Step 9: Find all the links (horse names) in this section
#         horse_links = race.find_all('a')

#         # Step 10: Set variables to store the current race time and meeting (track)
#         # Initially, these values will be None until we find them
#         current_time = None
#         current_meeting = None

#         # Step 11: Loop through each link (horse name) and process the data
#         for link in horse_links:
#             # Get the text from the link (the horse's name)
#             text = link.get_text(strip=True)

#             # Step 12: Check if the text contains a race time and meeting (e.g., "3:15 HAP")
#             # We split the text into two parts: time and meeting
#             if ':' in text and len(text.split()) == 2:
#                 time, meeting = text.split()
#                 current_time = time  # Store the race time
#                 current_meeting = meeting  # Store the meeting (track) code
#             elif current_time and current_meeting:
#                 # Step 13: If we already have the race time and meeting, the text is a horse name
#                 data.append({
#                     'Race Date': race_date,
#                     'Race Time': current_time,
#                     'Meeting': current_meeting,
#                     'Horse Name': text
#                 })

#     # Step 14: After scraping all the data, we save it into a CSV file
#     # The CSV file will have columns for 'Race Date', 'Race Time', 'Meeting', and 'Horse Name'
#     with open('horse_races_today.csv', 'w', newline='', encoding='utf-8') as csvfile:
#         # Define the column names for the CSV file
#         fieldnames = ['Race Date', 'Race Time', 'Meeting', 'Horse Name']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         # Write the header (column names) to the CSV file
#         writer.writeheader()

#         # Step 15: Write each row of data to the CSV file
#         for row in data:
#             writer.writerow(row)

#     # Step 16: Print a success message to indicate that the data has been saved
#     print("✅ Data scraped and saved to horse_races_today.csv")

# else:
#     # If the request failed (status code other than 200), print an error message
#     print(f"❌ Failed to retrieve webpage. Status code: {response.status_code}")



import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Define the URL where we want to get the race data from
url = "https://www.racingpost.com/results/time-order/"

# Step 2: Make a request to fetch the webpage content
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Step 3: Check if the webpage was fetched successfully (HTTP status code 200 means OK)
if response.status_code == 200:
    print("Page fetched successfully!")

    # Step 4: Use BeautifulSoup to parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, "html.parser")

    # Step 5: Find all sections that contain race results
    race_sections = soup.find_all('div', class_="rp-timeView__list")

    # Step 6: Open a CSV file to save the extracted data
    with open("race_results.csv", "w", newline='', encoding="utf-8") as file:
        # Create a CSV writer to write data into the CSV file
        writer = csv.writer(file)

        # Write the header row (column names) into the CSV
        writer.writerow(["Race Time", "Location", "Race Name", "Distance", "Class", "Prize Money", "Position", "Horse Name", "Odds"])

        # Step 7: Loop through each race section and extract relevant information
        for section in race_sections:
            # Extract race time, location, and race name
            race_time = section.find_previous('time').get_text(strip=True) if section.find_previous('time') else "Unknown Time"
            meeting_info = section.find_previous('h3').get_text(strip=True).split("\n")
            location = meeting_info[0] if len(meeting_info) > 0 else "Unknown Location"
            race_name = meeting_info[1] if len(meeting_info) > 1 else "Unknown Race Name"

            # Extract race distance, class, and prize money
            distance_and_prize = section.find_all('span', class_="rp-timeView__distance-prize")
            distance = distance_and_prize[0].get_text(strip=True) if len(distance_and_prize) > 0 else "Unknown Distance"
            prize = distance_and_prize[1].get_text(strip=True) if len(distance_and_prize) > 1 else "Unknown Prize"

            # Extract race class
            race_class = section.find('span', class_="rp-timeView__class")
            race_class = race_class.get_text(strip=True) if race_class else "Unknown Class"

            # Step 8: Find all the horses' results (names, positions, odds)
            results = section.find_all('div', class_="rp-timeView__horseDetails")
            for result in results:
                # Extract the horse's name, finishing position, and odds
                horse_name = result.find('a').get_text(strip=True) if result.find('a') else "Unknown Horse"
                position = result.find('span', class_="rp-timeView__position")
                position = position.get_text(strip=True) if position else "Unknown Position"
                odds = result.find('span', class_="rp-timeView__odds")
                odds = odds.get_text(strip=True) if odds else "Unknown Odds"

                # Write each result as a new row in the CSV file
                writer.writerow([race_time, location, race_name, distance, race_class, prize, position, horse_name, odds])

    # Success message once data is written
    print("Data has been written to race_results.csv successfully.")
else:
    # If the page was not fetched successfully, print an error message
    print("Failed to fetch page. HTTP Status Code:", response.status_code)
