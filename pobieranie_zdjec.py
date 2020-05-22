import requests
from bs4 import BeautifulSoup
import csv

# UWAGA: zdjęcia zaczną się tworzyć w folderze, gdzie znajduje się ten plik
# jak baza w tym samym folderze co plik to po prostu path = 'baza_wszystkich_produktow.csv'
baza_prod_path = 'TUTAJ TWÓJ PATH DO BAZA_WSZYSTKICH_PRODUKTÓW.CSV'
with open(baza_prod_path, newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    baza_produktow = list(reader)

'''
# na później: jak dostać numer z nazwy pliku:
nazwa = 'produkt_0176'
nazwa = nazwa[-3:]
str(int('nazwa'))
>>'176'
'''

for i in range(len(baza_produktow)):

    page = requests.get(baza_produktow[i][4])
    soup = BeautifulSoup(page.content, 'html.parser')

    link_do_zdjecia = soup.find("img", {"class": "_b8e15_1nMOJ"}).get('src')

    img_data = requests.get(link_do_zdjecia).content
    if i < 10:
        with open('produkt_000' + str(i) + '.jpg', 'wb') as handler:
            handler.write(img_data)
    elif i < 100:
        with open('produkt_00' + str(i) + '.jpg', 'wb') as handler:
            handler.write(img_data)
    elif i < 1000:
        with open('produkt_0' + str(i) + '.jpg', 'wb') as handler:
            handler.write(img_data)
    elif i >= 1000:
        with open('produkt_' + str(i) + '.jpg', 'wb') as handler:
            handler.write(img_data)

