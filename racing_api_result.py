# import requests
# from requests.auth import HTTPBasicAuth

# # 1. API endpoint
# url = "https://api.theracingapi.com/v1/courses"

# # 2. Parameters (optional: filter by region)
# # Example: Fetch courses in Great Britain and Ireland
# params = {
#     "region_codes": ["gb", "ire"]
# }

# # 3. Authentication (replace with your actual credentials)
# username = "oRglCxQSvw3HNbIfFJJShSsV"
# password = "HZ0mCM9WCHfOeWcXnI3pi1xv"

# # 4. Send the GET request
# response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)

# # 5. Handle the response
# if response.status_code == 200:
#     # Successful request
#     courses = response.json()
#     for course in courses:
#         print(f"Course ID: {course['id']}, Name: {course['name']}, Region: {course['region_code']}")
# else:
#     print(f"Error {response.status_code}: {response.text}")









import requests
from requests.auth import HTTPBasicAuth

def get_race_time(race):
    for key in ["race_time", "time", "scheduled_time"]:
        time = race.get(key)
        if time:
            return time
    return "N/A"

username = "oRglCxQSvw3HNbIfFJJShSsV"
password = "HZ0mCM9WCHfOeWcXnI3pi1xv"
url = "https://api.theracingapi.com/v1/racecards/free"

# Add region_codes param to filter by GB horses/races
params = {
    "day": "today",
    "region_codes": ["gb"]
}

response = requests.get(url, auth=HTTPBasicAuth(username, password), params=params)

if response.status_code == 200:
    data = response.json()
    racecards = data.get("racecards", [])

    for race in racecards:
        race_class = race.get("race_class", "").lower()
        if race_class not in ["class 1", "class 2", "class 3"]:
            continue

        course_name = race.get("course_name") or race.get("course") or "N/A"
        race_name = race.get("race_name", "N/A")
        race_time = get_race_time(race)

        print(f"Course: {course_name}")
        print(f"Race: {race_name}")
        print(f"Time: {race_time}")
        print(f"Class: {race_class.title()}")

        runners = race.get("runners", [])
        print("Runners:")
        if runners:
            for runner in runners:
                horse_name = runner.get("horse", "N/A")
                horse_id = runner.get("horse_id", "N/A")
                print(f"  - {horse_name} (ID: {horse_id})")
        else:
            print("  No runner info available.")
        print("-" * 30)
else:
    print(f"Error: {response.status_code} - {response.text}")
