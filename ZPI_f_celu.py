import numpy as np
import itertools

def f_celu(kategorie, prod_koszyk, popularnosc, cena, ahp_kryteria):
    lista_wartosci_f_celu = []
    for i in range(len(prod_koszyk)):

        funkcja = kategorie[i] * ahp_kryteria[0] + popularnosc[i] * ahp_kryteria[1] + cena[i] * ahp_kryteria[2]

        lista_wartosci_f_celu.append([prod_koszyk[i], round(funkcja, 3), cena[i]])

    return lista_wartosci_f_celu


def sortowanie(lista):

    lista.sort(key=lambda x: x[1], reverse=True)
    return lista


def optymalizacja(wagi_osob_dict, lista_dopasowan, budzet):

    same_wagi = list(wagi_osob_dict.values())
    for i in range(len(same_wagi)):
        for produkt in lista_dopasowan[i]:
            produkt[1] = produkt[1] * same_wagi[i]

    all_kombinacje = list(itertools.product(*lista_dopasowan))

    sumy = []
    for i in range(len(all_kombinacje)):
        suma_wartosci = 0
        suma_ceny = 0
        for j in range(len(all_kombinacje[i])):
            suma_ceny += all_kombinacje[i][j][2]
        if suma_ceny <= budzet:
            for j in range(len(all_kombinacje[i])):
                suma_wartosci += all_kombinacje[i][j][1]
            sumy.append([suma_wartosci, all_kombinacje[i]])

    sumy.sort(key=lambda x: x[0], reverse=True)

    return sumy[0:5]
