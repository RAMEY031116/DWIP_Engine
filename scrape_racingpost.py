import requests
from bs4 import BeautifulSoup
import csv
import datetime

base_url = 'https://gg.com/racing/'

def get_dates_interval(start, finish, fmt):
    start = datetime.datetime.strptime(start, fmt)
    finish = datetime.datetime.strptime(finish, fmt)
    while start <= finish:
        yield start.strftime("%d-%b-%Y").lower()
        start += datetime.timedelta(days=1)

def get_races(date):
    url = base_url + date
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    races = []

    for result_span in soup.select("span.result"):
        a_tag = result_span.find_parent().find_next_sibling("td").find("a")
        if a_tag and a_tag.get("href"):
            races.append(a_tag["href"])
    return races

def get_results(url):
    print("Fetching:", url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    race = []

    try:
        date, coursetime = url.split("/")[-2:]
        course, time = coursetime.rsplit("-", 1)
    except:
        return race  # Malformed URL or data

    condition_tag = soup.select_one("h1.winning-post .going")
    condition = condition_tag.text.strip() if condition_tag else ""

    nonrunners_tag = soup.select_one(".footnote")
    nonrunners = nonrunners_tag.text.split(", ") if nonrunners_tag and nonrunners_tag.text else []
    num_nonrunners = len(nonrunners)

    rows = soup.select("#race-card tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 4:
            continue  # skip malformed rows

        horse = {}
        try:
            # Col 1: place, number, draw
            place = cols[0].text.strip()
            number_draw = cols[0].find_all("span")[1].text.strip().replace("(", "").replace(")", "").split()
            number = number_draw[0] if len(number_draw) > 0 else ""
            draw = number_draw[1] if len(number_draw) > 1 else ""

            # Col 2: form and additional info
            form = cols[1].find_all("span")[1].text.strip() if len(cols[1].find_all("span")) > 1 else ""
            additional = cols[1].find("a").text.strip() if cols[1].find("a") else ""

            # Col 3: horse, jockey, trainer, owner
            tds = cols[2].find_all("a")
            horse_name = tds[0].text.strip() if len(tds) > 0 else ""
            jockey = tds[1].text.strip() if len(tds) > 1 else ""
            trainer = tds[2].text.strip() if len(tds) > 2 else ""
            owner = cols[2].find_all("td")[-1].text.strip() if cols[2].find_all("td") else ""

            # Col 4: odds and explanation
            odds = cols[3].text.strip()
            explain = ""
            if place == "-" and len(cols[3].find_all("span")) > 1:
                explain = cols[3].find_all("span")[1].text.strip()

            horse['place'] = place
            horse['no'] = number
            horse['draw'] = draw
            horse['form'] = form
            horse['additional'] = additional
            horse['horse'] = horse_name
            horse['jockey'] = jockey
            horse['trainer'] = trainer
            horse['owner'] = owner
            horse['odds'] = odds
            horse['explain'] = explain
            horse['date'] = date
            horse['course'] = course
            horse['time'] = time
            horse['condition'] = condition
            horse['nonrunners'] = num_nonrunners
            horse['winner'] = "YES" if place == "1st" else "NO"

            race.append(horse)
        except Exception as e:
            print("Skipping row due to error:", e)
            continue
    return race

def dic_to_csv(d, path):
    if not d:
        print("No data to write.")
        return
    keys = d[0].keys()
    with open(path, 'w', newline='', encoding='utf-8') as f:
        dt = csv.DictWriter(f, keys)
        dt.writeheader()
        dt.writerows(d)

def main(dates):
    table = []
    for date in dates:
        for race_url in get_races(date):
            table.extend(get_results(race_url))
    dic_to_csv(table, "race.csv")

# Example usage:
# main(get_dates_interval("2011-08-03", "2011-08-03", "%Y-%m-%d"))
main(["03-oct-2011"])
