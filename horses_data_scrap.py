import requests
from bs4 import BeautifulSoup

# URL of the page where the horse race data is located
url = 'https://www.racingpost.com/racecards/runners-index'

# Send a GET request to fetch the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all divs with the specified class 'RC-alphabetIndexPanes js-diffusionTopicSettingsRace'
    race_info = soup.find_all('div', class_='RC-alphabetIndexPanes js-diffusionTopicSettingsRace')
    
    # Now, we will also get the divs with class 'RC-alphabetIndexPanes__column'
    race_columns = soup.find_all('div', class_='RC-alphabetIndexPanes__column')

    # Print the race date and all horse names
    for race in race_info:
        # Extract race date from the data-diffusion-racedate attribute
        race_date = race.get('data-diffusion-racedate')
        
        if race_date:
            print(f"Race Date: {race_date}")
        else:
            print("Race Date not found")
        
        # Extract all horse names within the div (adjust based on actual structure)
        horse_names = race.find_all('a', class_='horse-name')  # Assuming horse names are under this class
        if horse_names:
            for horse in horse_names:
                print(f"Horse Name: {horse.text.strip()}")
        else:
            print("No horses found in this race.")
    
    # Extract content from columns with class 'RC-alphabetIndexPanes__column'
    for column in race_columns:
        # You can extract the content you need from each column here
        # For example, print the text content
        column_text = column.get_text(strip=True)
        if column_text:
            print(f"Column Content: {column_text}")
        else:
            print("No content found in this column.")
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")
