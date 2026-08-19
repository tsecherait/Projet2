import requests
from bs4 import BeautifulSoup
import re
import csv
import argparse

"""
Description : Ce script visite une page d'un bouquin spécifiée sur le site "http://books.toscrape.com",
               extrait les informations essentielles, puis les écrit dans un fichier CSV avec des
               en-têtes de colonnes appropriées.

Version : 1.0.0

Auteur : Kenza BAZI-KABBAJ

Date : 07/09/2023


    Input:
        URL(string): URL de la page du bouquin

    Output:
        product_data.csv : fichier CSV contenant les informations du bouquin: product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url
"""

def extract_product_info(url: str) -> dict:
    """_summary_ : Fonction pour extraire les informations d'une page d'un bouquin

    Args:
        url (string): URL de la page du bouquin

    Returns:
        _dict_: Retourne les données du bouquin sous forme de dictionnaire
    """

    # Utiliser requests pour obtenir le contenu HTML de la page
    response = requests.get(url)
    page = response.content

    # Mapping des valeurs textuelles aux chiffres
    rating_mapping = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    # Vérifier si la requête s'est correctement déroulée
    if response.status_code == 200:
        # Créez un objet BeautifulSoup à partir du contenu HTML
        soup = BeautifulSoup(page, 'html.parser')

        # Extraire les informations requises
        tds=soup.findAll('td')
        product_page_url = str(url)
        universal_product_code = tds[0].string
        title=soup.h1.text
        price_including_tax = tds[3].string
        price_excluding_tax = tds[2].string
        number_available = int(re.search(r'\d+', tds[5].string).group())
        product_description = soup.find("meta", {"name": "description"}).get("content").strip()
        category = soup.find("ul", class_="breadcrumb").find_all("li")[-2].find("a").text
        #review_rating = soup.select_one('p.star-rating')['class'][1]
        review_class = soup.find('p', class_='star-rating')['class'][1]
        review_rating = rating_mapping.get(review_class, None)
        image_url=soup.find('article', class_='product_page').find("div").find("img").get("src")
        image_url = url.rsplit('/', 2)[0] + '/' + image_url
        
        # Retourner les données sous forme de dictionnaire
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
        return product_data
    
    else:
        print("La requête a échoué avec le code :", response.status_code)
        return None


def main():

    # Configuration de argparse
    parser = argparse.ArgumentParser(description='Ce script visite une page produit spécifiée sur le site "http://books.toscrape.com", extrait les informations essentielles, puis les écrit dans un fichier CSV avec des en-têtes de colonnes appropriées.')
    parser.add_argument("url", help="URL de la page produit")
    args = parser.parse_args()

    # URL de la page du produit
    url = args.url

    # Extraire les informations du produit
    product_data=extract_product_info(url)

    # Vérifier si les données ont été extraites avec succès
    if product_data:
        # Ecrire les données dans un fichier CSV
        with open('book_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = product_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Ecrire les en-têtes de colonnes
            writer.writeheader()

            # Ecrire les données du produit
            writer.writerow(product_data)
        print("Les données du livre ont été écrites dans book_data_p1.csv.")
    else:
        print("Impossible d'extraire les données du livre.")

if __name__ == "__main__":
    main()