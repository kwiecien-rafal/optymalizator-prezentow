import csv
import numpy as np
import plec_wiek_kategorie as pwk
import okazje as okz

# wczytanie wszystkich produktow
with open('baza_wszystkich_produktow.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    baza_produktow = list(reader)

kobiece_podkategorie = pwk.kobiece_podkategorie
meskie_podkategorie = pwk.meskie_podkategorie
kobiece_kategorie_szczegolowe = pwk.kobiece_kategorie_szczegolowe
meskie_kategorie_szczegolowe = pwk.meskie_kategorie_szczegolowe

dziecko_podkategorie = pwk.dziecko_podkategorie
mlodziez_podkategorie = pwk.mlodziez_podkategorie
dorosly_podkategorie = pwk.dorosly_podkategorie
starsza_podkategorie = pwk.starsza_podkategorie

urodziny_gwiazdka = okz.urodziny_gwiazdka
walentynki = okz.walentynki
dzien_kobiet_chlopaka = okz.dzien_kobiet_chlopaka
dzien_dziadka_babci_mamy_taty = okz.dzien_dziadka_babci_mamy_taty
dzien_dziecka = okz.dzien_dziecka
slub = okz.slub
komunia = okz.komunia


def ograniczenia_plec(poczatkowa_baza, plec):

    global kobiece_podkategorie
    global meskie_podkategorie
    global kobiece_kategorie_szczegolowe
    global meskie_kategorie_szczegolowe

    # baza ktora bedziemy zmieniac ze wzgledu na parametry
    obecna_baza = []

    if plec == 'k':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][2].lower() not in meskie_kategorie_szczegolowe and poczatkowa_baza[i][1].lower() not in meskie_podkategorie:
                obecna_baza.append(poczatkowa_baza[i])
    elif plec == 'm':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() not in kobiece_podkategorie and poczatkowa_baza[i][2].lower() not in kobiece_kategorie_szczegolowe:
                obecna_baza.append(poczatkowa_baza[i])

    return obecna_baza


def ograniczenia_wiek(poczatkowa_baza, wiek):

    global dziecko_podkategorie
    global mlodziez_podkategorie
    global dorosly_podkategorie
    global starsza_podkategorie

    if wiek <= 12:
        wiek_przedzial = 'dziecko'
    elif wiek <= 18:
        wiek_przedzial = 'mlodziez'
    elif wiek <= 49:
        wiek_przedzial = 'dorosly'
    else:
        wiek_przedzial = 'starsza'

    # baza ktora bedziemy zmieniac ze wzgledu na parametry
    obecna_baza = []

    if wiek_przedzial == 'dziecko':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dziecko_podkategorie:
                obecna_baza.append(poczatkowa_baza[i])
    elif wiek_przedzial == 'mlodziez':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in mlodziez_podkategorie:
                obecna_baza.append(poczatkowa_baza[i])
    elif wiek_przedzial == 'dorosly':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dorosly_podkategorie:
                obecna_baza.append(poczatkowa_baza[i])
    elif wiek_przedzial == 'starsza':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in starsza_podkategorie:
                obecna_baza.append(poczatkowa_baza[i])

    return obecna_baza


def ograniczenie_budzet(poczatkowa_baza, budzet):

    obecna_baza = []

    for i in range(len(poczatkowa_baza)):
        if int(poczatkowa_baza[i][5]) <= budzet:
            obecna_baza.append(poczatkowa_baza[i])

    return obecna_baza


def ograniczenia_okazja(poczatkowa_baza, okazja):
    
    global urodziny_gwiazdka 
    global walentynki 
    global dzien_kobiet_chlopaka 
    global dzien_dziadka_babci_mamy_taty
    global dzien_dziecka 
    global slub 
    global komunia

    # baza ktora bedziemy zmieniac ze wzgledu na parametry
    obecna_baza = []

    if okazja == 'urodziny':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in urodziny_gwiazdka:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'gwiazdka':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in urodziny_gwiazdka:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'walentynki':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in walentynki:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien kobiet':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_kobiet_chlopaka:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien chlopaka':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_kobiet_chlopaka:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien dziadka':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_dziadka_babci_mamy_taty:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien babci':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_dziadka_babci_mamy_taty:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien mamy':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_dziadka_babci_mamy_taty:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien taty':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_dziadka_babci_mamy_taty:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'dzien dziecka':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in dzien_dziecka:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'slub':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in slub:
                obecna_baza.append(poczatkowa_baza[i])
    elif okazja == 'komunia':
        for i in range(len(poczatkowa_baza)):
            if poczatkowa_baza[i][1].lower() in komunia:
                obecna_baza.append(poczatkowa_baza[i])

    return obecna_baza
