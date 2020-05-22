import csv
import numpy as np

# wczytanie wszystkich produktow
with open('baza_wszystkich_produktow.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    baza_produktow = list(reader)

tagi = []

for i in range(len(baza_produktow)):

    # nazwa produktu jako lista wszystkich wyrazow z jego nazwy
    nazwa_danego_produktu = baza_produktow[i][3].split()

    for j in range(len(nazwa_danego_produktu)):

        obecna_para = []
        tag = nazwa_danego_produktu[j].lower()
        nazwa_podkategorii = baza_produktow[i][1].lower()
        obecna_para.extend([tag, nazwa_podkategorii])
        tagi.append(obecna_para)

np.savetxt('tagi.csv', [
    x for i in zip(tagi)
        for x in i
], delimiter=',', fmt='%s', encoding='utf-8-sig')
