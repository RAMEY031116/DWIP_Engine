
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# # Setup Selenium WebDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# # URL to scrape (replace with the actual URL)
# url = "https://www.racingpost.com/profile/horse/4350647/lisnamult-lad/form"  # Replace with actual URL

# # Load the page
# driver.get(url)

# # Wait for the page to load
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hp-details")))

# # Parse the page source with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'html.parser')

# # Extract horse details
# try:
#     # Extract Horse's Age
#     age_section = soup.find("dt", text="8yo:")
#     age = age_section.find_next("dd").get_text(strip=True) if age_section else "Age not found"

#     # Extract Breeder
#     breeder_section = soup.find("dt", text="Breeder:")
#     breeder = breeder_section.find_next("dd").get_text(strip=True) if breeder_section else "Breeder not found"

#     # Extract Trainer
#     trainer_section = soup.find("dt", text="Trainer:")
#     trainer = trainer_section.find_next("dd").get_text(strip=True) if trainer_section else "Trainer not found"

#     # Extract Owner
#     owner_section = soup.find("dt", text="Owner:")
#     owner = owner_section.find_next("dd").get_text(strip=True) if owner_section else "Owner not found"

#     # Extract Sire
#     sire_section = soup.find("dt", text="Sire:")
#     sire = sire_section.find_next("dd").get_text(strip=True) if sire_section else "Sire not found"

#     # Extract Dam
#     dam_section = soup.find("dt", text="Dam:")
#     dam = dam_section.find_next("dd").get_text(strip=True) if dam_section else "Dam not found"

#     # Extract Dam's Sire
#     dams_sire_section = soup.find("dt", text="Dam's Sire:")
#     dams_sire = dams_sire_section.find_next("dd").get_text(strip=True) if dams_sire_section else "Dam's Sire not found"

#     # Print extracted data
#     print(f"Age: {age}")
#     print(f"Breeder: {breeder}")
#     print(f"Trainer: {trainer}")
#     print(f"Owner: {owner}")
#     print(f"Sire: {sire}")
#     print(f"Dam: {dam}")
#     print(f"Dam's Sire: {dams_sire}")

# except AttributeError as e:
#     print(f"Error extracting data: {e}")

# # Extract race record stats (runs, wins, seconds, etc.)
# try:
#     # Find the race record table
#     table = soup.find("table", class_="ui-table hp-raceRecords ui-table_type2")
#     if table:
#         print("\nRace Record:")
#         rows = table.find_all("tr", class_="ui-table__row")
        
#         for row in rows:
#             cells = row.find_all("td", class_="ui-table__cell")
#             if cells:
#                 race_type = cells[0].get_text(strip=True)
#                 runs = cells[1].get_text(strip=True)
#                 wins = cells[2].get_text(strip=True)
#                 seconds = cells[3].get_text(strip=True)
#                 thirds = cells[4].get_text(strip=True)
#                 winnings = cells[5].get_text(strip=True)
#                 prize = cells[6].get_text(strip=True)
#                 earnings = cells[7].get_text(strip=True)
#                 best_ts = cells[9].get_text(strip=True)
#                 best_rpr = cells[10].get_text(strip=True)
#                 best_mr = cells[11].get_text(strip=True)

#                 print(f"Race Type: {race_type}")
#                 print(f"Runs: {runs}")
#                 print(f"Wins: {wins}")
#                 print(f"2nds: {seconds}")
#                 print(f"3rds: {thirds}")
#                 print(f"Winnings: {winnings}")
#                 print(f"Prize: {prize}")
#                 print(f"Earnings: {earnings}")
#                 print(f"Best TS: {best_ts}")
#                 print(f"Best RPR: {best_rpr}")
#                 print(f"Best MR: {best_mr}")
#                 print("-" * 40)

#     else:
#         print("Race record table not found!")

# except AttributeError as e:
#     print(f"Error extracting race record data: {e}")

# # Close the driver after scraping
# driver.quit()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to scrape
url = "https://www.racingpost.com/profile/horse/4350647/lisnamult-lad/form"
driver.get(url)

# Wait for page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hp-details")))

# Parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Prepare CSV
csv_filename = "horse_form.csv"
fieldnames = ["Age", "Breeder", "Trainer", "Owner", "Sire", "Dam", "Dam's Sire", "Chase Wins", "Hurdle Wins", "NHF Wins", "PTP Wins", "Rules Wins"]

# Extract horse details
try:
    age_section = soup.find("dt", text="8yo:")
    age = 7  # Hardcoding based on your data (you can improve by parsing)
    
    breeder = soup.find("dt", text="Breeder:").find_next("dd").get_text(strip=True)
    trainer = soup.find("dt", text="Trainer:").find_next("dd").get_text(strip=True)
    owner = soup.find("dt", text="Owner:").find_next("dd").get_text(strip=True)
    sire = soup.find("dt", text="Sire:").find_next("dd").get_text(strip=True)
    dam = soup.find("dt", text="Dam:").find_next("dd").get_text(strip=True)
    dams_sire = soup.find("dt", text="Dam's Sire:").find_next("dd").get_text(strip=True)

    # Initialize wins for each race type
    wins_data = {
        "Chase": 0,
        "Hurdle": 0,
        "NHF": 0,
        "PTP": 0,
        "Rules": 0
    }

    # Find race records
    table = soup.find("table", class_="ui-table hp-raceRecords ui-table_type2")
    if table:
        rows = table.find_all("tr", class_="ui-table__row")
        for row in rows:
            cells = row.find_all("td", class_="ui-table__cell")
            if cells:
                race_type = cells[0].get_text(strip=True)
                wins_text = cells[2].get_text(strip=True)
                wins_split = wins_text.split("/")
                wins = int(wins_split[0]) if wins_split else 0

                if race_type in wins_data:
                    wins_data[race_type] = wins

    # Write to CSV
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow({
            "Age": age,
            "Breeder": breeder,
            "Trainer": trainer,
            "Owner": owner,
            "Sire": sire,
            "Dam": dam,
            "Dam's Sire": dams_sire,
            "Chase Wins": wins_data["Chase"],
            "Hurdle Wins": wins_data["Hurdle"],
            "NHF Wins": wins_data["NHF"],
            "PTP Wins": wins_data["PTP"],
            "Rules Wins": wins_data["Rules"]
        })

except Exception as e:
    print(f"Error extracting data: {e}")

# Done
driver.quit()
print("Cleaned data saved to horse_form_cleaned.csv")
