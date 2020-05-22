import csv
import wyszukiwanie as wysz

# wczytanie wszystkich produktow
with open('baza_wszystkich_produktow.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    baza_produktow = list(reader)

# wczytanie wszystkich tagow
with open('tagi.csv', newline='', encoding='utf-8-sig') as g:
    reader2 = csv.reader(g)
    baza_tagi = list(reader2)

# bierzemy tylko tag, bez nazwy podkategorii i tworzymy jedną listę a nie listę list
baza_tagi2 = []
for para in baza_tagi:
    baza_tagi2.append(para[0])
flat_tagi = baza_tagi2

command = ''
pasujace_prod = []
obecne_tagi = []
obecne_wyszukiwanie = []
iter1 = 0

while command != 'q':

    command = str(input("Wyszukaj: "))

    if command != 'q' and command != 'clear' and iter1 == 0:
        obecne_wyszukiwanie = wysz.znajdowanie_tagow_first(baza_produktow, command, pasujace_prod, obecne_tagi, flat_tagi)
        print(obecne_wyszukiwanie[1])
        for i in obecne_wyszukiwanie[0]:
            print(i[3])
        iter1 = 1

    elif command != 'q' and command != 'clear':
        obecne_wyszukiwanie = wysz.znajdowanie_tagow(command, obecne_wyszukiwanie[0], obecne_wyszukiwanie[1], flat_tagi)
        print(obecne_wyszukiwanie[1])
        for i in obecne_wyszukiwanie[0]:
            print(i[3])

    elif command != 'q' and command == 'clear':
        obecne_wyszukiwanie = wysz.znajdowanie_tagow(command, obecne_wyszukiwanie[0], obecne_wyszukiwanie[1], flat_tagi)
        print('Wyczyszczono.')
        iter1 = 0
