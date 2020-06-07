import csv
import numpy as np
import plec_wiek_kategorie as pwk

kobiece_podkategorie = pwk.kobiece_podkategorie
meskie_podkategorie = pwk.meskie_podkategorie
kobiece_kategorie_szczegolowe = pwk.kobiece_kategorie_szczegolowe
meskie_kategorie_szczegolowe = pwk.meskie_kategorie_szczegolowe

dziecko_podkategorie = pwk.dziecko_podkategorie
mlodziez_podkategorie = pwk.mlodziez_podkategorie
dorosly_podkategorie = pwk.dorosly_podkategorie
starsza_podkategorie = pwk.starsza_podkategorie


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
