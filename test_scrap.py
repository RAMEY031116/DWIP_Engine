import requests
from bs4 import BeautifulSoup
import csv

url = "https://scrapeme.live/shop/"

response = requests.get(url)

soup = BeautifulSoup(response.content,"html.parser" )

ul_elements = soup.find("ul", class_= "products columns-4")
li_elements = ul_elements.find_all("li")

print(li_elements)

results = []

for li in li_elements:
    title = li.find("h2", class_="woocommerce-loop-product__title").text
    price = li.find("span", class_="price").text
    title = li.find("h2", class_="woocommerce-loop-product__title").text

    # Filter: Only keep items with price £73 or £130
    if "£73" in price or "£130" in price:
        pokemon = {
            "title" : title,
            "price" : price,
            "title" : title
        }

        results.append(pokemon)
        print(pokemon)

# Write to CSV
with open("pokemon_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "price"])
    writer.writeheader()
    writer.writerows(results)
