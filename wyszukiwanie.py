import csv
import difflib


def znajdowanie_tagow_first(baza, command, pasujace_prod, obecne_tagi, baza_tagi):

    command = command.lower()
    obecne_tagi = []
    pasujace_prod = []

    if command != 'q' and command != 'clear' and len(obecne_tagi) == 0:
        pierwsze_tagi = []
        for i in range(len(baza_tagi)):
            if command in baza_tagi[i]:
                pierwsze_tagi.extend([baza_tagi[i]])
        pierwsze_tagi = list(dict.fromkeys(pierwsze_tagi))  # usuwanie duplikatów
        obecne_tagi.append(pierwsze_tagi)

        for tag in pierwsze_tagi:
            for produkt in baza:
                if tag in produkt[3].lower():
                    pasujace_prod.append(produkt)

    return pasujace_prod, obecne_tagi


def znajdowanie_tagow(command, pasujace_prod, obecne_tagi, baza_tagi):

    # zmiana komendy na małe litery
    command = command.lower()

    if command != 'q' and command != 'clear':
        kolejne_tagi = []
        for i in range(len(baza_tagi)):
            if command in baza_tagi[i]:
                kolejne_tagi.extend([baza_tagi[i]])
        kolejne_tagi = list(dict.fromkeys(kolejne_tagi))  # usuwanie duplikatów
        obecne_tagi.append(kolejne_tagi)

        pasujace_prod2 = []
        for tag in kolejne_tagi:
            for produkt in pasujace_prod:
                if tag in produkt[3].lower():
                    pasujace_prod2.append(produkt)

        pasujace_prod = pasujace_prod2

    # czyszczenie
    elif command != 'q' and command == 'clear':
        obecne_tagi = []
        pasujace_prod = []

    # po wprowadzeniu wielu tagów, pokazują się te tagi które pasują do produktu
    obecne_tagi_temp = []
    for grupa_tagow in obecne_tagi:
        obecna_grupa = []
        for produkt in pasujace_prod:
            for tag in grupa_tagow:
                if tag in produkt[3].lower() and tag not in obecna_grupa:
                    obecna_grupa.append(tag)
        obecne_tagi_temp.extend([obecna_grupa])
    obecne_tagi = obecne_tagi_temp

    # usuwanie duplikatów produktów w liście pasujących produktów (na wszelki wypadek)
    pasujace_prod_temp = []
    for produkt in pasujace_prod:
        if produkt not in pasujace_prod_temp:
            pasujace_prod_temp.append(produkt)
    pasujace_prod = pasujace_prod_temp

    return pasujace_prod, obecne_tagi
