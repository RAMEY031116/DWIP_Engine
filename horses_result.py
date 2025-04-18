# Import necessary libraries
import requests  # To send requests to the webpage
from bs4 import BeautifulSoup  # To parse the HTML content
import csv  # To save the data into a CSV file

# Step 1: Set the URL of the webpage from which we want to scrape data
url = 'https://www.racingpost.com/fast-results/'

# Step 2: Send a request to the URL and get the webpage content
# We also add a 'User-Agent' header to make the request look like it's from a browser
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Step 3: Check if the request was successful
# If the status code is 200, it means the webpage was fetched correctly
if response.status_code == 200:

    # Step 4: Parse the webpage content (HTML) using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 5: Create a list to store the data we will scrape
    data = []

    # Step 6: Find all sections that contain race information
    # In this case, each section has a specific class name that we use to find it
    race_sections = soup.find_all('div', class_='data-test-selector="results-items-container"')

    # Step 7: Loop through each race section to extract the relevant information
    for race in race_sections:

        # Step 8: Extract the race date from the section (it’s stored in a custom attribute)
        race_date = race.get('rp-timeView__list', 'Unknown Date')

        # Step 9: Find all the links (horse names) in this section
        horse_links = race.find_all('a')

        # Step 10: Set variables to store the current race time and meeting (track)
        # Initially, these values will be None until we find them
        current_time = None
        current_meeting = None

        # Step 11: Loop through each link (horse name) and process the data
        for link in horse_links:
            # Get the text from the link (the horse's name)
            text = link.get_text(strip=True)

            # Step 12: Check if the text contains a race time and meeting (e.g., "3:15 HAP")
            # We split the text into two parts: time and meeting
            if ':' in text and len(text.split()) == 2:
                time, meeting = text.split()
                current_time = time  # Store the race time
                current_meeting = meeting  # Store the meeting (track) code
            elif current_time and current_meeting:
                # Step 13: If we already have the race time and meeting, the text is a horse name
                data.append({
                    'Race Date': race_date,
                    'Race Time': current_time,
                    'Meeting': current_meeting,
                    'Horse Name': text
                })

    # Step 14: After scraping all the data, we save it into a CSV file
    # The CSV file will have columns for 'Race Date', 'Race Time', 'Meeting', and 'Horse Name'
    with open('horse_races_today.csv', 'w', newline='', encoding='utf-8') as csvfile:
        # Define the column names for the CSV file
        fieldnames = ['Race Date', 'Race Time', 'Meeting', 'Horse Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header (column names) to the CSV file
        writer.writeheader()

        # Step 15: Write each row of data to the CSV file
        for row in data:
            writer.writerow(row)

    # Step 16: Print a success message to indicate that the data has been saved
    print("✅ Data scraped and saved to horse_races_today.csv")

else:
    # If the request failed (status code other than 200), print an error message
    print(f"❌ Failed to retrieve webpage. Status code: {response.status_code}")
