import csv
import ograniczenia as ogr
import AHP as aha
import ZPI_f_celu as fcl

def normalizacja(lista):

    znormalizowana_lista = []
    for i in range(len(lista)):
        znormalizowana_wartosc = (lista[i] - min(lista)) / (max(lista) - min(lista))
        znormalizowana_lista.append(round(znormalizowana_wartosc, 1)*10)

    return znormalizowana_lista


# wczytanie wszystkich produktow
with open('baza_wszystkich_produktow.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    baza_produktow = list(reader)

il_osob = int(input('Podaj ilość osób, którym będziesz wybierał/wybierała prezenty: '))
budzet = int(input('Podaj swój łączny budżet na wszystkie prezenty: '))
print('Zaczynamy!')

# lista z osobami
lista_osob = []
lista_przedmiotow_osob = []

# main loop
while len(lista_osob) < il_osob:

    obecna_baza = baza_produktow

    imie = str(input('Jak ma na imię ta osoba? >>>'))
    plec = str(input('Jakiej płci jest ' + imie + ' [K/M] >>>'))
    plec = plec.lower()
    wiek = int(input('Ile lat ma ' + imie + ' >>>'))

    obecna_os = [imie, plec, wiek]
    lista_osob.append(obecna_os)

    obecna_baza = ogr.ograniczenia_plec(obecna_baza, plec)
    obecna_baza = ogr.ograniczenia_wiek(obecna_baza, wiek)
    obecna_baza = ogr.ograniczenie_budzet(obecna_baza, 0, budzet)

    print('Lp | Nazwa produtu | cena | popularność')
    for produkt in obecna_baza:
        print(obecna_baza.index(produkt)+1, ' | ', produkt[3], ' | ', produkt[5], ' | ', produkt[7])

    print('-'*50)
    print('Wpisz liczby porządkowe produktów, które cię interesują (jedna na raz, potem enter)')
    print('Gdy wpiszesz wszystkie produkty, wpisz: "end"')
    wybrane_prod = []
    wybor = ''
    while wybor != 'end':
        wybor = str(input('>>>'))
        if wybor != 'end':
            wybor = int(wybor) - 1
            wybrane_prod.append(obecna_baza[wybor])

    print('Lp | Nazwa produtu | cena | popularność')
    for produkt in wybrane_prod:
        print(obecna_baza.index(produkt) + 1, ' | ', produkt[3], ' | ', produkt[5], ' | ', produkt[7])

    wybrane_pkat = []
    for produkt in wybrane_prod:
        if produkt[1].lower() not in wybrane_pkat:
            wybrane_pkat.append(produkt[1].lower())
    print(wybrane_pkat)

    ahp_1 = aha.ahp(wybrane_pkat)
    print(ahp_1)

    ahp_2 = aha.ahp(['kategorie', 'popularnosc', 'cena'])
    print(ahp_2)
    ahp_2_lista_wartosci = []
    for key in ahp_2:
        ahp_2_lista_wartosci.append(ahp_2[key])

    wskaznik_ceny = []
    cena = []
    for produkt in wybrane_prod:
        cena.append(int(produkt[5]))
    wskaznik_ceny = normalizacja(cena)

    nazwa_produktu = []
    wsk_podkategorii = []
    wsk_popularnosc_prod = []
    wsk_cena_prod = []
    for i in range(len(wybrane_prod)):
        nazwa_produktu.append(wybrane_prod[i][3])
        wsk_podkategorii.append(float(ahp_1[wybrane_prod[i][1].lower()]))
        wsk_popularnosc_prod.append(float(wybrane_prod[i][7]))
        wsk_cena_prod.append(wskaznik_ceny[i])

    wynik = fcl.f_celu(wsk_podkategorii, nazwa_produktu, wsk_popularnosc_prod, wskaznik_ceny, ahp_2_lista_wartosci)
    wynik = fcl.sortowanie(wynik)

    for i in wynik:
        print(i)

    lista_przedmiotow_osob.append(wynik)

imiona = []
for osoba in lista_osob:
    imiona.append(osoba[0])

ahp_3 = aha.ahp(imiona)

zz = fcl.optymalizacja(ahp_3, lista_przedmiotow_osob, budzet)
print(zz)
