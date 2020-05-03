import requests
from bs4 import BeautifulSoup
import time
import numpy as np

start_time = time.time()

page = requests.get('https://allegro.pl/')
soup = BeautifulSoup(page.content, 'html.parser')
parent_kategorie = soup.find_all('div', {'class': '_1h7wt _1bo4a _irxvs _882d6_2vUHQ'})
elektronika = parent_kategorie[0]
dom_i_ogrod = parent_kategorie[2]
supermarket = parent_kategorie[3]
dziecko = parent_kategorie[4]
uroda = parent_kategorie[5]
zdrowie = parent_kategorie[6]
kultura_i_rozrywka = parent_kategorie[7]
sport_i_turystyka = parent_kategorie[8]
motoryzacja = parent_kategorie[9]

lista_parent_kategorii = [elektronika, dom_i_ogrod, supermarket, dziecko, uroda, zdrowie, kultura_i_rozrywka,
                          sport_i_turystyka, motoryzacja]

lista_nazw_parent_kategorii = ['elektronika', 'dom_i_ogrod', 'supermarket', 'dziecko', 'uroda', 'zdrowie',
                               'kultura_i_rozrywka', 'sport_i_turystyka', 'motoryzacja']

ile_podkategorii = {
    'elektronika': 8,
    'dom_i_ogrod': 6,
    'supermarket': 4,
    'dziecko': 6,
    'uroda': 4,
    'zdrowie': 7,
    'kultura_i_rozrywka': 7,
    'sport_i_turystyka': 6,
    'motoryzacja': 7,
}

ile_podkategorii_lista = [ile_podkategorii['elektronika'], ile_podkategorii['dom_i_ogrod'],
                          ile_podkategorii['supermarket'], ile_podkategorii['dziecko'], ile_podkategorii['uroda'],
                          ile_podkategorii['zdrowie'], ile_podkategorii['kultura_i_rozrywka'],
                          ile_podkategorii['sport_i_turystyka'], ile_podkategorii['motoryzacja']]

ilosc_kategorii = len(lista_parent_kategorii)


def normalizacja(lista):
    znormalizowana_lista = []
    for i in range(len(lista)):
        znormalizowana_wartosc = (lista[i] - min(lista)) / (max(lista) - min(lista))
        znormalizowana_lista.append(round(znormalizowana_wartosc, 1) * 10)

    return znormalizowana_lista


def normalizacja_cen(lista):
    znormalizowana_lista = []
    for i in range(len(lista)):
        znormalizowana_wartosc = (lista[i] - min(lista)) / (max(lista) - min(lista))
        znormalizowana_lista.append(10-(round(znormalizowana_wartosc, 1) * 10))

    return znormalizowana_lista


def tworzenie_bazy_kategorii(kategoria, ilosc_podkategorii_do_stworzenia):
    kategoria_ul = list(kategoria.children)[1].find_all('ul')
    podkategoria_dict = dict()

    for i in range(0, ilosc_podkategorii_do_stworzenia * 2, 2):
        wartosci = []
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            wartosci.append(kategoria_ul[i].find_all('a')[j].get_text())
        podkategoria_dict[kategoria_ul[i].find_all('a')[0].get_text()] = wartosci

    return podkategoria_dict


def tworzenie_bazy_produktow(kategoria_nazwa, kategoria, ilosc_podkategorii):
    kategoria_glowna = kategoria_nazwa
    kategoria_ul = list(kategoria.children)[1].find_all('ul')
    linki_do_kategorii = []
    produkty_kategorii = []
    popularnosc = []  # lista do obliczenia popularności
    cena_normalizacja = []

    # tworzenie listy z linkami do podpodkategorii
    for i in range(0, ilosc_podkategorii * 2, 2):
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            obecna_para = []
            nazwa_kategorii = kategoria_ul[i].find_all('a')[j].get_text()
            obecny_link = kategoria_ul[i].find_all('a')[j].get('href')
            obecna_para.extend([nazwa_kategorii, obecny_link])
            linki_do_kategorii.append(obecna_para)

    # tworzenie listy z nazwami podkategorii i podpodkategorii
    kategoria_nazwy_dzieci = []
    for i in range(0, ilosc_podkategorii * 2, 2):
        podpodkategorie_nazwy = []
        for j in range(1, len(kategoria_ul[i].find_all('a'))):
            podpodkategoria = kategoria_ul[i].find_all('a')[j].get_text()
            podpodkategoria = podpodkategoria.replace(',', '')
            podpodkategorie_nazwy.append(podpodkategoria)

        podkategoria_lista = [kategoria_ul[i].find_all('a')[0].get_text(), podpodkategorie_nazwy]
        kategoria_nazwy_dzieci.append(podkategoria_lista)

    #
    iter1 = 0
    iter2 = 0
    for i in range(len(linki_do_kategorii)):
        produkt_page = requests.get('https://allegro.pl' + linki_do_kategorii[i][1])
        produkt_soup = BeautifulSoup(produkt_page.content, 'html.parser')
        nazwa_podkategorii = kategoria_nazwy_dzieci[iter1][0]
        nazwa_podpodkategorii = kategoria_nazwy_dzieci[iter1][1][iter2]
        produkty_podkategorii = []
        podkategoria_ile_osob_kupilo = []
        podkategoria_cena = []

        for j in range(2, 7):
            dany_produkt = []
            parent_produkt = produkt_soup.find_all('article', {'data-analytics-view-custom-index0': str(j)})
            nazwa_produktu = list(parent_produkt[0].find_all('a'))[1].get_text()
            nazwa_produktu = nazwa_produktu.replace(',', ' ')

            ten_link = list(parent_produkt[0].find_all('a'))[1].get('href')

            # cena danego produktu
            cena = parent_produkt[0].find_all('span', {'class': '_9c44d_1zemI'})[0].get_text()
            cena = cena[0:len(cena) - 3]  # usuwanie dopisku o złotych
            cena = cena.replace(' ', '')
            cena = cena.replace(',', '')
            cena = cena[0:len(cena) - 2]  # usuwanie dwóch zer z końca
            podkategoria_cena.append(int(cena))

            # liczba, ile osób kupiło dany produkt
            ile_osob_kupilo = parent_produkt[0].find_all('span', {'class': '_9c44d_2o04k'})[0].get_text()
            ile_osob_kupilo = ile_osob_kupilo[0:len(ile_osob_kupilo) - 12]
            ile_osob_kupilo = ile_osob_kupilo.replace(' ', '')
            ile_osob_kupilo = ile_osob_kupilo.replace('o', '')
            # usuwanie wszystkiego, co nie jest numerem
            ile_osob_kupilo = ''.join(i for i in ile_osob_kupilo if i.isdigit())
            if ile_osob_kupilo == '': ile_osob_kupilo = '0'
            if ile_osob_kupilo == 'niktn': ile_osob_kupilo = '0'
            # dodanie do listy, żeby potem obliczyć popularność:
            podkategoria_ile_osob_kupilo.append(int(ile_osob_kupilo))

            dany_produkt.extend(
                [kategoria_glowna, nazwa_podkategorii, nazwa_podpodkategorii, nazwa_produktu, ten_link, cena,
                 ile_osob_kupilo])
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

        if max(podkategoria_cena) == 0 and min(podkategoria_cena) == 0:
            podkategoria_normalizacja_cen = [0, 0, 0, 0, 0]
        else:
            podkategoria_normalizacja_cen = normalizacja_cen(podkategoria_cena)
        cena_normalizacja.extend(podkategoria_normalizacja_cen)

    return produkty_kategorii, popularnosc, cena_normalizacja


lista_produkty = []
lista_popularnosci = []
lista_cen_normalizacja = []

# kod do zrobienia jednej kategorii (do zmiennej konkretna_kategoria przypisz nazwę kategorii)
konkretna_kategoria = 'motoryzacja'
indeks_kategorii = lista_nazw_parent_kategorii.index(konkretna_kategoria)
lista_produkty.append(tworzenie_bazy_produktow(konkretna_kategoria, lista_parent_kategorii[indeks_kategorii],
                                               ile_podkategorii[konkretna_kategoria])[0])
lista_popularnosci.append(tworzenie_bazy_produktow(konkretna_kategoria, lista_parent_kategorii[indeks_kategorii],
                                                   ile_podkategorii[konkretna_kategoria])[1])
lista_cen_normalizacja.append(tworzenie_bazy_produktow(konkretna_kategoria, lista_parent_kategorii[indeks_kategorii],
                                                       ile_podkategorii[konkretna_kategoria])[2])

iter3 = 0
for i in range(len(lista_produkty[0])):
    for j in range(len(lista_produkty[0][i])):
        lista_produkty[0][i][j].append(lista_popularnosci[0][iter3])
        lista_produkty[0][i][j].append(lista_cen_normalizacja[0][iter3])
        iter3 += 1

np.savetxt(konkretna_kategoria + '.csv', [
    x for p in zip(lista_produkty[0])
        for z in p
            for x in z
], delimiter=',', fmt='%s', encoding='utf-8-sig')

# kod do zrobienia wszystkich kategorii na raz
'''
for i in range(ilosc_kategorii):
    lista_produkty.append(tworzenie_bazy_produktow(lista_nazw_parent_kategorii[i], lista_parent_kategorii[i],
                                                   ile_podkategorii_lista[i])[0])
for i in range(ilosc_kategorii):
    lista_popularnosci.append(tworzenie_bazy_produktow(lista_nazw_parent_kategorii[i], lista_parent_kategorii[i],
                                                       ile_podkategorii_lista[i])[1])
for i in range(ilosc_kategorii):
    lista_cen_normalizacja.append(tworzenie_bazy_produktow(lista_nazw_parent_kategorii[i], lista_parent_kategorii[i],
                                                           ile_podkategorii_lista[i])[2])
iter3 = 0
for k in range(ilosc_kategorii):
    iter3 = 0
    for i in range(len(lista_produkty[k])):
        for j in range(len(lista_produkty[k][i])):
            lista_produkty[k][i][j].append(lista_popularnosci[k][iter3])
            lista_produkty[k][i][j].append(lista_cen_normalizacja[k][iter3])
            iter3 += 1

for i in range(ilosc_kategorii):
    np.savetxt(lista_nazw_parent_kategorii[i] + '.csv', [
        x for p in zip(lista_produkty[i])
            for z in p
                for x in z
    ], delimiter=',', fmt='%s', encoding='utf-8-sig')'''

print("--- %s seconds ---" % (time.time() - start_time))
