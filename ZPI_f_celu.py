import numpy as np


def f_celu(kategorie, prod_koszyk, popularnosc, cena, ahp_kryteria):
    lista_wartosci_f_celu = []
    for i in range(len(prod_koszyk)):

        funkcja = kategorie[i] * ahp_kryteria[0] + popularnosc[i] * ahp_kryteria[1] + cena[i] * ahp_kryteria[2]

        lista_wartosci_f_celu.append((prod_koszyk[i], round(funkcja, 3)))

    return lista_wartosci_f_celu


def sortowanie(lista):

    lista.sort(key=lambda x: x[1], reverse=True)
    return lista
