import requests
from bs4 import BeautifulSoup
import csv

# wczytanie wszystkich produktow
baza_prod_path = 'TUTAJ TWÓJ PATH DO BAZA_WSZYSTKICH_PRODUKTÓW.CSV'
with open(baza_prod_path, newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    baza_produktow = list(reader)

for i in range(len(baza_produktow)):

    page = requests.get(baza_produktow[i][4])
    soup = BeautifulSoup(page.content, 'html.parser')

    link_do_zdjecia = soup.find("img", {"class": "_b8e15_1nMOJ"}).get('src')

    img_data = requests.get(link_do_zdjecia).content
    with open('produkt_' + str(i) + '.jpg', 'wb') as handler:
        handler.write(img_data)

