import numpy as np

kategorie = ['książki', 'telefony', 'drukarki', 'konsole', 'AGD małe']

def ahp(kategorie):
    k_macierz = np.zeros((len(kategorie), len(kategorie)))
    for i in range(k_macierz.shape[0]):
        for j in range(k_macierz.shape[0]):
            if i == j :
                k_macierz[i][j] = 1
            if i < j:
                inp = input(kategorie[i]+' do '+kategorie[j]+': ')
                if inp == '>':
                    inp = 10
                elif inp == '<':
                    inp = 0.1
                else:
                    inp = 1
                k_macierz[i][j] = inp
                k_macierz[j][i] = k_macierz[i][j]**(-1)

    k_macierz = np.true_divide(k_macierz, np.sum(k_macierz, axis = 0)) #podziel każdy element kolumny przez sumę kolumny
    k_macierz = np.sum(k_macierz, axis = 1) / k_macierz.shape[0]       #zsumuj rzędy i podziel każdy przez liczbę kategorii
                   
    kategorie_dict = {}
    for i in range(k_macierz.shape[0]):
        kategorie_dict[kategorie[i]] = ("%.2f" % k_macierz[i])

    return kategorie_dict


print('- określ preferencje jednej kategorii względem drugiej (>, =, <) - ')
wynik = ahp(kategorie)
print('-'*100+'\n',wynik,'\n'+'-'*100)

