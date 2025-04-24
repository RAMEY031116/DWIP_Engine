
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
from datetime import datetime
import re
import csv

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL to scrape (replace with the actual URL)
url = "https://www.racingpost.com/profile/horse/4350647/lisnamult-lad/form"  # Replace with actual URL

# Load the page
driver.get(url)

# Wait for the page to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hp-details")))

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Prepare to write to a CSV file
csv_filename = "horse_form.csv"
fieldnames = ["Age", "Breeder", "Trainer", "Owner", "Sire", "Dam", "Dam's Sire", "Race Type", "Runs", "Wins", "2nds", "3rds", "Winnings", "Prize", "Earnings", "Best TS", "Best RPR", "Best MR"]

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    # Extract horse details
    try:
        # Extract Horse's Age (which is in the form of birthdate)
        age_section = soup.find("dt", text="8yo:")  # You might want to adjust this if the text changes
        age = age_section.find_next("dd").get_text(strip=True) if age_section else "Age not found"

        # Extract the birthdate (e.g., "01Jun17") from the age text
        birthdate_match = re.search(r"\((\d{2}[A-Za-z]{3}\d{2})", age)
        if birthdate_match:
            birthdate_str = birthdate_match.group(1)  # e.g., "01Jun17"
            
            # Convert the birthdate string into a datetime object
            birthdate = datetime.strptime(birthdate_str, "%d%b%y")

            # Calculate the horse's age by subtracting birthdate from today's date
            today = datetime.today()
            age_years = today.year - birthdate.year
            if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
                age_years -= 1  # If the horse hasn't had its birthday yet this year
            
            print(f"Birthdate: {birthdate.strftime('%d-%b-%Y')}")
            print(f"Age: {age_years} years")
        else:
            print("Birthdate not found in the age section.")

        # Extract other details as before (Breeder, Trainer, etc.)
        breeder_section = soup.find("dt", text="Breeder:")
        breeder = breeder_section.find_next("dd").get_text(strip=True) if breeder_section else "Breeder not found"
        
        trainer_section = soup.find("dt", text="Trainer:")
        trainer = trainer_section.find_next("dd").get_text(strip=True) if trainer_section else "Trainer not found"
        
        owner_section = soup.find("dt", text="Owner:")
        owner = owner_section.find_next("dd").get_text(strip=True) if owner_section else "Owner not found"
        
        sire_section = soup.find("dt", text="Sire:")
        sire = sire_section.find_next("dd").get_text(strip=True) if sire_section else "Sire not found"
        
        dam_section = soup.find("dt", text="Dam:")
        dam = dam_section.find_next("dd").get_text(strip=True) if dam_section else "Dam not found"
        
        dams_sire_section = soup.find("dt", text="Dam's Sire:")
        dams_sire = dams_sire_section.find_next("dd").get_text(strip=True) if dams_sire_section else "Dam's Sire not found"

        # Find the race record table
        table = soup.find("table", class_="ui-table hp-raceRecords ui-table_type2")
        if table:
            rows = table.find_all("tr", class_="ui-table__row")
            
            for row in rows:
                cells = row.find_all("td", class_="ui-table__cell")
                if cells:
                    race_type = cells[0].get_text(strip=True)
                    runs = cells[1].get_text(strip=True)
                    wins = cells[2].get_text(strip=True)
                    seconds = cells[3].get_text(strip=True)
                    thirds = cells[4].get_text(strip=True)
                    winnings = cells[5].get_text(strip=True)
                    prize = cells[6].get_text(strip=True)
                    earnings = cells[7].get_text(strip=True)
                    best_ts = cells[9].get_text(strip=True)
                    best_rpr = cells[10].get_text(strip=True)
                    best_mr = cells[11].get_text(strip=True)

                    # Write the extracted data to the CSV file
                    writer.writerow({
                        "Age": age_years,
                        "Breeder": breeder,
                        "Trainer": trainer,
                        "Owner": owner,
                        "Sire": sire,
                        "Dam": dam,
                        "Dam's Sire": dams_sire,
                        "Race Type": race_type,
                        "Runs": runs,
                        "Wins": wins,
                        "2nds": seconds,
                        "3rds": thirds,
                        "Winnings": winnings,
                        "Prize": prize,
                        "Earnings": earnings,
                        "Best TS": best_ts,
                        "Best RPR": best_rpr,
                        "Best MR": best_mr
                    })

    except AttributeError as e:
        print(f"Error extracting data: {e}")

# Close the driver after scraping
driver.quit()

print("Data has been written to horse_form.csv")
