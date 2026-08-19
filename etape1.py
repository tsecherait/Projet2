import requests
from bs4 import BeautifulSoup
import re
import csv
import argparse

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


rating_mapping = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
tds=soup.findAll('td')
url = str(url)
upc = tds[0].string
title=soup.h1.text
price_inc = tds[3].string
price_exc = tds[2].string
number = int(re.search(r'\d+', tds[5].string).group())
product_description = soup.find("meta", {"name": "description"}).get("content").strip()
category = soup.find("ul", class_="breadcrumb").find_all("li")[-2].find("a").text
#review_rating = soup.select_one('p.star-rating')['class'][1]
review_class = soup.find('p', class_='star-rating')['class'][1]
review_rating = rating_mapping.get(review_class, None)
image_url=soup.find('article', class_='product_page').find("div").find("img").get("src")
image_url = url.rsplit('/', 2)[0] + '/' + image_url
        
"""# Retourner les données sous forme de dictionnaire
product_data = {
'product_page_url': product_page_url,
'universal_product_code': universal_product_code,
'title': title,
'price_including_tax': price_including_tax,
'price_excluding_tax': price_excluding_tax,
'number_available': number_available,
'product_description': product_description,
'category': category,
'review_rating': review_rating,
'image_url': image_url
}

print(product_data)

with open('book_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = product_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Ecrire les en-têtes de colonnes
            writer.writeheader()

            # Ecrire les données du produit
            writer.writerow(product_data)
"""
with open("un_seul_livre.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"])  # en-têtes
    writer.writerow([url, upc, title, price_inc, price_exc, number, product_description, category, review_rating, image_url])  # les valeurs