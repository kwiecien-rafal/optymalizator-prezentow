import numpy as np

prod_koszyk = ['banan', 'koparka', 'rower', 'suszarka']
kategorie = [0.03, 0.21, 0.40, 0.36]
popularnosc = [0.30, 0.24, 0.21, 0.25]
cena = [0.60, 0.14, 0.06, 0.20]
ahp_kryteria = [.7, 0.12, 0.18]


def f_celu(kategorie, prod_koszyk, popularnosc, cena, ahp_kryteria):
    lista_wartosci_f_celu = []
    for i in range(len(prod_koszyk)):

        funkcja = kategorie[i] * ahp_kryteria[0] + popularnosc[i] * ahp_kryteria[1] + cena[i] * ahp_kryteria[2]

        lista_wartosci_f_celu.append((prod_koszyk[i], round(funkcja, 3)))

    return lista_wartosci_f_celu


def sortowanie(lista):

    lista.sort(key=lambda x: x[1], reverse=True)
    return lista


print(f_celu(kategorie, prod_koszyk, popularnosc, cena, ahp_kryteria))
print(sortowanie(f_celu(kategorie, prod_koszyk, popularnosc, cena, ahp_kryteria)))
