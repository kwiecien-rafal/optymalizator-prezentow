import requests
from bs4 import BeautifulSoup
import time
import numpy as np
start_time = time.time()

page = requests.get("https://allegro.pl/")
soup = BeautifulSoup(page.content, 'html.parser')
parent_kategorie = soup.find_all("div", {"class": "_1h7wt _1bo4a _irxvs _882d6_2vUHQ"})
elektronika = parent_kategorie[0]
moda = parent_kategorie[1]
dom_i_ogrod = parent_kategorie[2]
supermarket = parent_kategorie[3]
dziecko = parent_kategorie[4]
uroda = parent_kategorie[5]
zdrowie = parent_kategorie[6]
kultura_i_rozrywka = parent_kategorie[7]
sport_i_turystyka = parent_kategorie[8]
motoryzacja = parent_kategorie[9]
nieruchomosci = parent_kategorie[10]
kolekcje_i_sztuka = parent_kategorie[11]
firma_i_uslugi = parent_kategorie[12]

lista_parent_kategorii = [elektronika, moda, dom_i_ogrod, supermarket, dziecko, uroda, zdrowie, kultura_i_rozrywka,
                          sport_i_turystyka, motoryzacja, nieruchomosci, kolekcje_i_sztuka, firma_i_uslugi]
ile_podkategorii = {
    'elektronika': 8,
    'moda': 5,
    'dom_i_ogrod': 6,
    'supermarket': 4,
    'dziecko': 6,
    'uroda': 5,
    'zdrowie': 7,
    'kultura_i_rozrywka': 7,
    "sport_i_turystyka": 6,
    "motoryzacja": 7,
    "nieruchomosci": 2,
    "kolekcje_i_sztuka": 5,
    "firma_i_uslugi": 2
}


def normalizacja(lista):

    znormalizowana_lista = []
    for i in range(len(lista)):
        znormalizowana_wartosc = (lista[i] - min(lista)) / (max(lista) - min(lista))
        znormalizowana_lista.append(round(znormalizowana_wartosc, 1)*10)

    return znormalizowana_lista


def tworzenie_bazy_kategorii(kategoria, ilosc_podkategorii_do_stworzenia):

    kategoria_ul = list(kategoria.children)[1].find_all('ul')
    podkategoria_dict = dict()

    for i in range(0, ilosc_podkategorii_do_stworzenia*2, 2):
        wartosci = []
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            wartosci.append(kategoria_ul[i].find_all('a')[j].get_text())
        podkategoria_dict[kategoria_ul[i].find_all('a')[0].get_text()] = wartosci

    return podkategoria_dict


def tworzenie_bazy_produktow(kategoria, ilosc_podkategorii):

    kategoria_glowna = 'elektronika'
    kategoria_ul = list(kategoria.children)[1].find_all('ul')
    linki_do_kategorii = []
    produkty_kategorii = []
    popularnosc = []  # lista do obliczenia popularności

    # tworzenie listy z linkami do podpodkategorii
    for i in range(0, ilosc_podkategorii*2, 2):
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            obecna_para = []
            nazwa_kategorii = kategoria_ul[i].find_all('a')[j].get_text()
            obecny_link = kategoria_ul[i].find_all('a')[j].get('href')
            obecna_para.extend([nazwa_kategorii, obecny_link])
            linki_do_kategorii.append(obecna_para)

    # tworzenie listy z nazwami podkategorii i podpodkategorii
    kategoria_nazwy_dzieci = []
    for i in range(0, ilosc_podkategorii*2, 2):
        podpodkategorie_nazwy = []
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            podpodkategoria = kategoria_ul[i].find_all('a')[j].get_text()
            podpodkategoria = podpodkategoria.replace(",", "")
            podpodkategorie_nazwy.append(podpodkategoria)

        podkategoria_lista = [kategoria_ul[i].find_all('a')[0].get_text(), podpodkategorie_nazwy]
        kategoria_nazwy_dzieci.append(podkategoria_lista)

    #
    iter1 = 0
    iter2 = 0
    for i in range(len(linki_do_kategorii)):
        produkt_page = requests.get("https://allegro.pl"+linki_do_kategorii[i][1])
        produkt_soup = BeautifulSoup(produkt_page.content, 'html.parser')
        nazwa_podkategorii = kategoria_nazwy_dzieci[iter1][0]
        nazwa_podpodkategorii = kategoria_nazwy_dzieci[iter1][1][iter2]
        produkty_podkategorii = []
        podkategoria_ile_osob_kupilo = []

        for j in range(2, 7):
            dany_produkt = []
            parent_produkt = produkt_soup.find_all("article", {"data-analytics-view-custom-index0": str(j)})
            nazwa_produktu = list(parent_produkt[0].find_all('a'))[1].get_text()
            nazwa_produktu = nazwa_produktu.replace(',', ' ')

            ten_link = list(parent_produkt[0].find_all('a'))[1].get('href')

            # cena danego produktu
            cena = parent_produkt[0].find_all("span", {"class": "_9c44d_1zemI"})[0].get_text()
            cena = cena[0:len(cena) - 3]  # usuwanie dopisku o złotych
            cena = cena.replace(" ", "")
            cena = cena.replace(",", "")
            cena = cena[0:len(cena) - 2]  # usuwanie dwóch zer z końca

            # liczba, ile osób kupiło dany produkt
            ile_osob_kupilo = parent_produkt[0].find_all("span", {"class": "_9c44d_2o04k"})[0].get_text()
            ile_osob_kupilo = ile_osob_kupilo[0:len(ile_osob_kupilo) - 12]
            ile_osob_kupilo = ile_osob_kupilo.replace(" ", "")
            ile_osob_kupilo = ile_osob_kupilo.replace("o", "")
            if ile_osob_kupilo == '': ile_osob_kupilo = '0'
            if ile_osob_kupilo == "niktn": ile_osob_kupilo = '0'
            # dodanie do listy, żeby potem obliczyć popularność:
            podkategoria_ile_osob_kupilo.append(int(ile_osob_kupilo))

            dany_produkt.extend([kategoria_glowna, nazwa_podkategorii, nazwa_podpodkategorii, nazwa_produktu, ten_link, cena, ile_osob_kupilo])
            produkty_podkategorii.append(dany_produkt)

        iter2 += 1
        if iter2 == len(kategoria_nazwy_dzieci[iter1][1]):
            iter2 = 0
            iter1 += 1

        if max(podkategoria_ile_osob_kupilo) == 0 and min(podkategoria_ile_osob_kupilo) == 0:
            podkategoria_popularnosc = [0, 0, 0, 0, 0]
        else:
            podkategoria_popularnosc = normalizacja(podkategoria_ile_osob_kupilo)
        popularnosc.extend(podkategoria_popularnosc)

        produkty_kategorii.append(produkty_podkategorii)

    return produkty_kategorii, popularnosc


elektronika_produkty = tworzenie_bazy_produktow(elektronika, 8)[0]
elektronika_popularnosc = tworzenie_bazy_produktow(elektronika, 8)[1]
#print(elektronika_popularnosc)

#print('-'*25)
#print('A',elektronika_produkty)
#print('B',elektronika_produkty[0])
#print('C',elektronika_produkty[0][0])

iter3 = 0
for i in range(len(elektronika_produkty)):
    for j in range(len(elektronika_produkty[i])):
        elektronika_produkty[i][j].append(elektronika_popularnosc[iter3])
        iter3 += 1


np.savetxt('elektronika.csv', [
    x for p in zip(elektronika_produkty)
        for z in p
            for x in z
], delimiter=',', fmt='%s')



'''
print(elektronika_produkty)
print(elektronika_produkty[0])
print(elektronika_produkty[0][0][2],elektronika_produkty[0][0][3])
print(elektronika_produkty[0][1][2],elektronika_produkty[0][1][3])
print(elektronika_produkty[0][2][2],elektronika_produkty[0][2][3])
print(elektronika_produkty[0][3][2],elektronika_produkty[0][3][3])
for i in range(len(elektronika_produkty)):
    for j in range(len(elektronika_produkty[0])):
        print(elektronika_produkty[i][j][3],elektronika_produkty[i][j][1],elektronika_produkty[i][j][0])'''

'''
def tworzenie_bazy_kategorii(kategoria, ilosc_podkategorii):

    kategoria_ul = list(kategoria.children)[1].find_all('ul')
    kategoria_nazwy_dzieci = []

    for i in range(0, ilosc_podkategorii*2, 2):
        podpodkategorie_nazwy = []
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            podpodkategorie_nazwy.append(kategoria_ul[i].find_all('a')[j].get_text())

        podkategoria_lista = [kategoria_ul[i].find_all('a')[0].get_text(), podpodkategorie_nazwy]
        kategoria_nazwy_dzieci.append(podkategoria_lista)

    return kategoria_nazwy_dzieci


lista = tworzenie_bazy_kategorii(elektronika, ile_podkategorii['elektronika'])
print(lista[0][1][0])
'''










'''
wszystkie_kategorie = dict()
wszystkie_kategorie['elektronika'] = tworzenie_bazy_kategorii(elektronika, ile_podkategorii['elektronika'])
wszystkie_kategorie['moda'] = tworzenie_bazy_kategorii(moda, ile_podkategorii['moda'])
wszystkie_kategorie['dom_i_ogrod'] = tworzenie_bazy_kategorii(dom_i_ogrod, ile_podkategorii['dom_i_ogrod'])
wszystkie_kategorie['supermarket'] = tworzenie_bazy_kategorii(supermarket, ile_podkategorii['supermarket'])
wszystkie_kategorie['dziecko'] = tworzenie_bazy_kategorii(dziecko, ile_podkategorii['dziecko'])
wszystkie_kategorie['uroda'] = tworzenie_bazy_kategorii(uroda, ile_podkategorii['uroda'])
wszystkie_kategorie['zdrowie'] = tworzenie_bazy_kategorii(zdrowie, ile_podkategorii['zdrowie'])
wszystkie_kategorie['kultura_i_rozrywka'] = tworzenie_bazy_kategorii(kultura_i_rozrywka, ile_podkategorii['kultura_i_rozrywka'])
wszystkie_kategorie['sport_i_turystyka'] = tworzenie_bazy_kategorii(sport_i_turystyka, ile_podkategorii['sport_i_turystyka'])
wszystkie_kategorie['motoryzacja'] = tworzenie_bazy_kategorii(motoryzacja, ile_podkategorii['motoryzacja'])
wszystkie_kategorie['nieruchomosci'] = tworzenie_bazy_kategorii(nieruchomosci, ile_podkategorii['nieruchomosci'])
wszystkie_kategorie['kolekcje_i_sztuka'] = tworzenie_bazy_kategorii(kolekcje_i_sztuka, ile_podkategorii['kolekcje_i_sztuka'])
wszystkie_kategorie['firma_i_uslugi'] = tworzenie_bazy_kategorii(firma_i_uslugi, ile_podkategorii['firma_i_uslugi'])
'''

#elektronika_produkty = tworzenie_bazy_produktow(elektronika, 8)
#print(elektronika_produkty)
#print(elektronika_produkty[0])

#moda_produkty = tworzenie_bazy_produktow(moda, 5)
#dom_i_ogrod_produkty = tworzenie_bazy_produktow(dom_i_ogrod, 6)
#supermarket_produkty = tworzenie_bazy_produktow(supermarket, 4)
#dziecko_produkty = tworzenie_bazy_produktow(dziecko, 6)
#uroda_produkty = tworzenie_bazy_produktow(uroda, 5)
#zdrowie_produkty = tworzenie_bazy_produktow(zdrowie, 7)
#kultura_i_rozrywka_produkty = tworzenie_bazy_produktow(kultura_i_rozrywka, 7)
#sport_i_turystyka_produkty = tworzenie_bazy_produktow(sport_i_turystyka, 6)
#motoryzacja_produkty = tworzenie_bazy_produktow(motoryzacja, 7)
#nieruchomosci_produkty = tworzenie_bazy_produktow(nieruchomosci, 2)
#kolekcje_i_sztuka_produkty = tworzenie_bazy_produktow(kolekcje_i_sztuka, 5)
#firma_i_uslugi_produkty = tworzenie_bazy_produktow(firma_i_uslugi, 2)

#print(dom_i_ogrod_produkty)
#print(supermarket_produkty)
#print(dziecko_produkty)
#print(uroda_produkty)
#print(zdrowie_produkty)
#print(kultura_i_rozrywka_produkty)
#print(sport_i_turystyka_produkty)
#print(motoryzacja_produkty)
#print(nieruchomosci_produkty)
#print(kolekcje_i_sztuka_produkty)
#print(firma_i_uslugi_produkty)



#print(wszystkie_kategorie)

'''
print(tworzenie_podkategorii(elektronika, ile_podkategorii['elektronika']))
print(tworzenie_podkategorii(moda, ile_podkategorii['moda']))
print(tworzenie_podkategorii(dom_i_ogrod, ile_podkategorii['dom_i_ogrod']))
print(tworzenie_podkategorii(supermarket, ile_podkategorii['supermarket']))
print(tworzenie_podkategorii(dziecko, ile_podkategorii['dziecko']))
print(tworzenie_podkategorii(uroda, ile_podkategorii['uroda']))
print(tworzenie_podkategorii(zdrowie, ile_podkategorii['zdrowie']))
print(tworzenie_podkategorii(kultura_i_rozrywka, ile_podkategorii['kultura_i_rozrywka']))
print(tworzenie_podkategorii(sport_i_turystyka, ile_podkategorii['sport_i_turystyka']))
print(tworzenie_podkategorii(motoryzacja, ile_podkategorii['motoryzacja']))
print(tworzenie_podkategorii(nieruchomosci, ile_podkategorii['nieruchomosci']))
print(tworzenie_podkategorii(kolekcje_i_sztuka, ile_podkategorii['kolekcje_i_sztuka']))
print(tworzenie_podkategorii(firma_i_uslugi, ile_podkategorii['firma_i_uslugi']))
'''




#print(elektronika_dict)
#print(linki_dict)
#_9c44d_3pyzl

'''for i in range(2, 7):
    #parent_produkt = produkt_soup.find_all("div", {"class": '_9c44d_3pyzl'})
    parent_produkt = produkt_soup.find_all("article", {"data-analytics-view-custom-index0": str(i)})
    wszystkie_a = parent_produkt.find_all('a')
    print(wszystkie_a)
    print('-----------')'''



'''
ele_ul = list(sport_i_turystyka.children)[1].find_all('ul')

elektronika_podkategorie = []
for i in range(len(ele_ul[0].find_all('a'))):
    elektronika_podkategorie.append(ele_ul[0].find_all('a')[i].get_text())

linki_dict = dict()
#lista_linkow = []
elektronika_dict = dict()
for i in range(0, 16, 2):
    values = []
    for j in range(1,len(ele_ul[i].find_all('a'))):
        values.append(ele_ul[i].find_all('a')[j].get_text())
        obecny_link = ele_ul[i].find_all('a')[j].get('href')
        #print(obecny_link)
        #lista_linkow.append(obecny_link)
        linki_dict[ele_ul[i].find_all('a')[j].get_text()] = obecny_link
    elektronika_dict[ele_ul[i].find_all('a')[0].get_text()] = values

produkt_page = requests.get("https://allegro.pl"+linki_dict['Siłownia'])
produkt_soup = BeautifulSoup(produkt_page.content, 'html.parser')
produkty_podkategorii = []
for i in range(2, 7):
    dany_produkt = []
    parent_produkt = produkt_soup.find_all("article", {"data-analytics-view-custom-index0": str(i)})
    wszystkie_a = list(parent_produkt[0].find_all('a'))[1].get_text()
    ten_link = list(parent_produkt[0].find_all('a'))[1].get('href')
    dany_produkt.extend([wszystkie_a, ten_link])
    produkty_podkategorii.append(dany_produkt)

print(produkty_podkategorii)
print(produkty_podkategorii[0])'''

print("--- %s seconds ---" % (time.time() - start_time))